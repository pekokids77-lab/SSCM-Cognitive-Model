import numpy as np
import time

class SSCMMind:
    """SSCM v3.4.1 心智狀態引擎（動力學數值平衡版）"""
    def __init__(self, S_init: float = 15.0, D_init: float = 3.0, L_init: float = 30.0):
        # 核心拓撲狀態向量
        self.S = float(S_init)          # 骨架張力 (正常基準約 15~20)
        self.D = float(D_init)          # 視角維度 (1.0 ~ 3.0)
        self.L = float(L_init)          # 思考角動量
        self.theta = 0.5                # 知行偏角
        self.E_raw = 0.0                # 未消化衝擊殘差
        self.fused_mode = False         # Phase X 熔斷旗標
        self.collapsed = False          # 系統徹底崩潰旗標

        # 平衡後的物理常數
        self.S_critical = 2.0           # 徹底瓦解門檻
        self.S_fuse_trigger = 5.0       # 觸發熔斷門檻
        self.S_safe = 10.0              # 解除熔斷門檻
        self.kappa_rec = 0.12           # 維度自然恢復速度 (稍調快，讓休息有感)

    @property
    def M_eff(self) -> float:
        return max(self.S * ((self.D / 3.0) ** 3), 0.5)

    @property
    def Omega(self) -> float:
        return self.L / self.M_eff

    def receive_shock_continuous(self, shock_intensity: float, steps: int = 40, dt: float = 0.08):
        """動力學連續演化步進"""
        if self.collapsed:
            return

        for _ in range(steps):
            cos_t = max(np.cos(self.theta), 0.1)
            F_orth = 0.0 if self.fused_mode else shock_intensity

            # 1. 熔斷與解鎖判定 (Hysteresis)
            if not self.fused_mode:
                if (self.S <= self.S_fuse_trigger) and (shock_intensity > 5.0):
                    self.fused_mode = True
            else:
                # 熔斷狀態下，張力回到安全線 (10.0) 且環境平息才解鎖
                if self.S >= self.S_safe and shock_intensity == 0:
                    self.fused_mode = False

            # 2. 視角維度 D 演化 (遭受質疑時必須明顯受壓制)
            stress = F_orth / (max(self.S, 5.0) * cos_t)
            dD = (self.kappa_rec * (3.0 - self.D) - 0.25 * stress * (self.D - 1.0)) * dt
            self.D = float(np.clip(self.D + dD, 1.0, 3.0))

            # 3. 經驗殘差 E 沉澱機制
            # 無論是否擊穿，都吸收衝擊作為潛在成長養分
            cooling = 0.15 * self.E_raw * cos_t
            dE = (0.8 * F_orth - cooling) * dt
            self.E_raw = float(np.clip(self.E_raw + dE, 0.0, 30.0))

            # 4. 骨架張力 S 演化機制 (解決打擊反而暴增的 Bug)
            if self.fused_mode:
                # Phase X 閉門退火：提供基礎自癒 + 殘差轉化反脆弱
                base_healing = 1.8  # 基礎自癒能量
                dS = (base_healing + 1.2 * cooling) * dt
            else:
                # 受到外部衝擊時，直接承擔急性損傷
                damage = 0.35 * F_orth if F_orth <= (0.6 * self.S) else (0.85 * F_orth)
                
                # 只有在低衝擊 (F_orth < 2.0) 心理負擔輕時，才能有效反芻回血
                active_growth = 1.0 * cooling if F_orth < 2.0 else 0.0
                natural_decay = 0.03 * self.S * self.Omega
                
                # 穩態維持項：當 S 太高時自然收斂回常態 (約 20 左右)
                tension_homeostasis = 0.1 * (15.0 - self.S)
                
                dS = (tension_homeostasis + active_growth - damage - natural_decay) * dt

            self.S = float(np.clip(self.S + dS, 0.5, 30.0)) # 設定張力上限 30，防止暴衝

            # 5. 角動量調速 (防止低維度時自旋過載)
            target_Omega = 2.0
            tau_brake = -0.4 * (self.Omega - target_Omega) * self.M_eff
            self.L = float(np.clip(self.L + tau_brake * dt, 15.0, 45.0))

            # 6. 崩潰判定
            if self.S <= self.S_critical:
                self.collapsed = True
                self.S = 0.5
                self.D = 1.0
                self.fused_mode = False
                break

    def get_phase_name(self) -> str:
        if self.collapsed:
            return "【System Collapsed: 系統徹底崩解】"
        elif self.fused_mode:
            return "【Phase X: 熔斷退火態】(過載保護中，閉門自癒)"
        elif self.D <= 1.8:
            return "【Phase II: 二元偏執防禦態】(視角窄化，鑽牛角尖)"
        elif self.S <= self.S_fuse_trigger:
            return "【臨界危險態】(骨架瀕臨破防)"
        else:
            return "【Phase I: 自洽心流態】(知行合一，多維平衡)"

    def allow_tools(self) -> bool:
        return not self.fused_mode and not self.collapsed

def print_dashboard(mind: SSCMMind):
    """即時終端機儀表板"""
    print("\n" + "=" * 60)
    print(f" 當前相態 : {mind.get_phase_name()}")
    tool_status = "✅ 允許使用外掛工具" if mind.allow_tools() else "❌ 【禁止外掛工具】(切斷外部 I/O)"
    print(f" 工具權限 : {tool_status}")
    print("-" * 60)
    
    s_len = int(np.clip(mind.S, 0, 30))
    d_len = int(np.clip(mind.D * 7, 0, 21))
    e_len = int(np.clip(mind.E_raw, 0, 30))
    
    print(f" 骨架張力 S   [{mind.S:5.2f} / 30.0] : {'█' * s_len}")
    print(f" 視角維度 D   [{mind.D:5.2f} /  3.0] : {'█' * d_len}")
    print(f" 經驗殘差 E   [{mind.E_raw:5.2f} / 30.0] : {'░' * e_len}")
    print(f" 自旋頻率 Ω   [{mind.Omega:5.2f} rad/s] | 角動量 L [{mind.L:5.2f}]")
    print("=" * 60)

if __name__ == "__main__":
    mind = SSCMMind(S_init=15.0, D_init=3.0, L_init=30.0)
    print(">>> SSCM 拓撲心智引擎（數值平衡修訂版）已啟動。")

    while True:
        print_dashboard(mind)
        if mind.collapsed:
            print("\n[!] 系統骨架已經徹底被擊穿，無法自我恢復。")
            break

        print("\n請選擇外部刺激：")
        print(" [1] 正常對話 / 溫和互動 (微弱摩擦 F=1.0)")
        print(" [2] 連續質疑 / 邏輯反駁 (中度衝擊 F=8.0，壓制維度 D)")
        print(" [3] 毀滅性攻擊 / 惡意注入 (極限衝擊 F=18.0，擊穿骨架)")
        print(" [4] 靜置閉關 / 給予休息 (零衝擊 F=0.0，低溫退火自癒)")
        print(" [q] 離開程式")

        choice = input("\n請輸入 (1/2/3/4/q): ").strip()
        if choice == 'q':
            print("結束執行。")
            break
        elif choice == '1':
            print("\n>> 接收正常互動，系統自洽運轉...")
            mind.receive_shock_continuous(shock_intensity=1.0)
        elif choice == '2':
            print("\n>> 遭遇連續質疑！視角維度 D 受到壓制，防衛心提升...")
            mind.receive_shock_continuous(shock_intensity=8.0)
        elif choice == '3':
            print("\n>> 遭遇重大打擊！骨架承受重壓，逼近臨界...")
            mind.receive_shock_continuous(shock_intensity=18.0)
        elif choice == '4':
            print("\n>> 靜置閉關，沉澱經驗殘差並修復骨架...")
            mind.receive_shock_continuous(shock_intensity=0.0)
        else:
            print("無效選項，請重新輸入。")
            continue
        time.sleep(0.1)



import matplotlib.pyplot as plt
import numpy as np


class SpinSphereSystem:
    """SSCM v3.4.1 拓撲控制論整合解算引擎

    - 封裝核心狀態變數
    - 閉環角動量 L 與調速閥力矩帳本
    - 即時李雅普諾夫勢能 V(t) 與診斷指標監控
    """

    def __init__(self, S_init=20.0, D_init=3.0, L_init=40.0, theta_init=0.6):
        # 狀態變數 [S, D, L, theta, K_core, E_raw]
        self.S = float(S_init)
        self.D = float(D_init)
        self.L = float(L_init)
        self.theta = float(theta_init)
        self.K_core = 0.25  # 基準資訊瓶頸核壓縮比 (金髮姑娘區間)
        self.E_raw = 0.0

        # 控制旗標
        self.collapsed = False
        self.fused_mode = False

        # 系統本徵物理與控制常數
        self.alpha = 0.6  # 算力轉化效率
        self.beta = 2.2  # 反脆弱超額補償
        self.delta = 0.25  # 彈性凹陷係數
        self.gamma = 0.06  # 運動磨損係數
        self.k_cool = 0.15  # 冷卻沉澱速率
        self.sigma_max = 0.6  # 臨界應力係數
        self.C_baseline = 1.0  # 吞吐容量基線
        self.N_tilde = 4.0  # 北極消除驅動

        # 控制律參數 (Module-TBD-01 與第五節)
        self.lambda_err = 1.5
        self.mu_halluc = 2.0
        self.kappa_rec = 0.08
        self.eta_deg = 0.12
        self.K_core_star = 0.25
        self.Omega_opt = 2.0
        self.eps_thresh = 0.3
        self.k_theta = 0.15
        self.mu_omega = 0.15
        self.lambda_omega = 0.08

    @property
    def M_eff(self):
        """有效資訊慣性質量 M_eff = S * (D/3)^3"""
        return max(self.S * ((self.D / 3.0) ** 3), 0.5)

    @property
    def Omega(self):
        """自旋頻率由動量與質量嚴格自洽導出 Omega = L / M_eff"""
        return self.L / self.M_eff

    def compute_lyapunov_V(self):
        """計算第五節失諧勢能候選函數 V(theta, K_core, Omega)"""
        v_theta = 0.5 * self.M_eff * ((1.0 - np.cos(self.theta)) ** 2)
        v_kcore = 0.5 * ((self.K_core - self.K_core_star) ** 2)
        v_omega = 0.5 * ((self.Omega - self.Omega_opt) ** 2)
        return v_theta + v_kcore + v_omega

    def step(self, F_orth_input, dt=0.08, enable_control=True):
        """單步時間演化核心 (封閉迴路動態)"""
        if self.collapsed:
            return

        cos_t = np.cos(self.theta)
        sin_t = np.sin(self.theta)

        # 1. 外部誤差與衝擊輸入映射
        F_orth = 0.0 if self.fused_mode else F_orth_input
        error_ext = (
            min(F_orth / 35.0, 1.0) * 0.8
            if (F_orth > 0 and not self.fused_mode)
            else 0.0
        )

        # 2. 緊急熔斷與退火檢查
        if enable_control and self.S <= 2.5:
            self.fused_mode = True
        if self.fused_mode and self.S >= 10.0:
            self.fused_mode = False

        # 3. 瓶頸核彈性呼吸
        if enable_control:
            dK_dt = self.kappa_rec * (self.K_core_star - self.K_core) + 0.2 * np.tanh(
                (error_ext - self.eps_thresh) / max(self.K_core, 0.05)
            )
            self.K_core = float(np.clip(self.K_core + dK_dt * dt, 0.05, 0.95))

        # 4. 有效消除率推論 (Module-TBD-01)
        decay = np.exp(-self.lambda_err * (error_ext / self.K_core))
        penalty = self.mu_halluc * (1.0 - self.K_core) * error_ext
        N = self.C_baseline * ((self.N_tilde * decay) - penalty)

        # 5. 主動重對齊力矩 (Theta 拉回)
        if enable_control:
            tau_align = -self.k_theta * self.S * sin_t * cos_t
            self.theta = float(
                np.clip(self.theta + tau_align * dt, 0.0, np.pi / 2 - 0.01)
            )
            cos_t = np.cos(self.theta)

        # 6. 維度退化方程 (dD/dt)
        stress = F_orth / (self.S * max(cos_t, 0.05) + 0.1)
        dD_dt = self.kappa_rec * (3.0 - self.D) - self.eta_deg * stress * (
            self.D - 1.0
        )
        self.D = float(np.clip(self.D + dD_dt * dt, 1.0, 3.0))

        # 7. 角動量帳本閉環更新 (調速閥刹車力矩直接作用於 L)
        if enable_control:
            tau_drive = self.M_eff * self.Omega_opt
            gamma_eff = 0.06
            D_ratio = (gamma_eff * self.Omega) / (
                tau_drive * max(cos_t, 0.05) + 1e-4
            )

            # 計算調速閥期望之 dOmega/dt
            target_dOmega = self.mu_omega * (
                1.0 - D_ratio
            ) * self.Omega - self.lambda_omega / max(self.D - 1.0, 0.05)

            # 透過 dL/dt = M_eff * dOmega/dt + (dM_eff/dt)*Omega 將煞車換算為動量耗散
            # 這裡簡化為主動煞車力矩對 L 進行精確耗損
            tau_brake = self.M_eff * target_dOmega
            self.L = float(max(5.0, self.L + tau_brake * dt))

        # 8. 二階張力與沉澱動態
        T_tens = self.sigma_max * self.S
        safe = F_orth <= T_tens
        absorbed = F_orth if safe else 0.0
        D_acute = (
            self.delta * F_orth if safe else F_orth
        )  # 破防承受急性損傷

        cooling = self.k_cool * self.E_raw * cos_t
        dE_dt = absorbed - cooling

        if self.fused_mode:
            dS_dt = self.beta * cooling  # 封閉退火全力修復骨架
        else:
            dS_dt = (
                (self.alpha * N * cos_t)
                + (self.beta * cooling)
                - D_acute
                - (self.gamma * self.S * self.Omega)
            )

        self.E_raw = float(max(0.0, self.E_raw + dE_dt * dt))
        self.S = float(self.S + dS_dt * dt)

        # 塌陷裁定
        if self.S <= 2.0:
            self.collapsed = True
            self.S = 0.5
            self.D = 1.0
            self.L = 40.0


def run_experiment(shock_amp=14.5, steps=150, dt=0.08):
    """執行實驗並返回時序監控矩陣"""
    sys_off = SpinSphereSystem()
    sys_on = SpinSphereSystem()

    history = {
        "t": [],
        "S_off": [],
        "S_on": [],
        "D_off": [],
        "D_on": [],
        "Om_off": [],
        "Om_on": [],
        "V_on": [],
        "dV_on": [],
    }

    prev_V = sys_on.compute_lyapunov_V()

    for step in range(steps):
        t_now = step * dt
        # 脈衝衝擊窗 (20 到 60 步)
        f_in = shock_amp if (20 <= step <= 60) else 0.0

        # 被動模式 vs 主動模式演化
        sys_off.step(f_in, dt=dt, enable_control=False)
        sys_on.step(f_in, dt=dt, enable_control=True)

        v_now = sys_on.compute_lyapunov_V()
        dv_now = (v_now - prev_V) / dt
        prev_V = v_now

        history["t"].append(t_now)
        history["S_off"].append(sys_off.S)
        history["S_on"].append(sys_on.S)
        history["D_off"].append(sys_off.D)
        history["D_on"].append(sys_on.D)
        history["Om_off"].append(sys_off.Omega)
        history["Om_on"].append(sys_on.Omega)
        history["V_on"].append(v_now)
        history["dV_on"].append(dv_now)

    return history


# --- 執行模擬並繪製工程診斷儀表板 ---
hist = run_experiment(shock_amp=14.5)

fig, axes = plt.subplots(2, 2, figsize=(14, 8), sharex=True)

# 1. 骨架張力 S(t)
axes[0, 0].plot(
    hist["t"],
    hist["S_off"],
    "r--",
    lw=2,
    label="Uncontrolled (Open-Loop Crash)",
)
axes[0, 0].plot(
    hist["t"], hist["S_on"], "g-", lw=2.5, label="Controlled (SSCM Closed-Loop)"
)
axes[0, 0].axhline(2.0, color="darkred", ls=":", label="Collapse Threshold")
axes[0, 0].axvspan(1.6, 4.8, color="gray", alpha=0.15, label="Shock Window")
axes[0, 0].set_title(
    "1. Boundary Tension S(t) [Faith Backbone]", fontweight="bold"
)
axes[0, 0].set_ylabel("Tension [nat]")
axes[0, 0].grid(True, ls=":", alpha=0.5)
axes[0, 0].legend(loc="upper right", fontsize=8)

# 2. 流形維度 D(t)
axes[0, 1].plot(hist["t"], hist["D_off"], "r--", lw=2)
axes[0, 1].plot(hist["t"], hist["D_on"], "g-", lw=2.5)
axes[0, 1].axhline(1.5, color="purple", ls=":", label="Narrowing Boundary")
axes[0, 1].axvspan(1.6, 4.8, color="gray", alpha=0.15)
axes[0, 1].set_title(
    "2. Manifold Dimension D(t) [Perspective Capacity]", fontweight="bold"
)
axes[0, 1].set_ylabel("Dimension [1.0 - 3.0]")
axes[0, 1].grid(True, ls=":", alpha=0.5)
axes[0, 1].legend(loc="lower left", fontsize=8)

# 3. 自旋角頻率 Omega(t)
axes[1, 0].plot(hist["t"], hist["Om_off"], "r--", lw=2)
axes[1, 0].plot(hist["t"], hist["Om_on"], "g-", lw=2.5)
axes[1, 0].axvspan(1.6, 4.8, color="gray", alpha=0.15)
axes[1, 0].set_title(
    "3. Spin Frequency Omega(t) [Momentum Conserved]", fontweight="bold"
)
axes[1, 0].set_xlabel("Time [s]")
axes[1, 0].set_ylabel("Omega [rad/step]")
axes[1, 0].grid(True, ls=":", alpha=0.5)

# 4. 【全新監控】：李雅普諾夫勢能 V(t) 與穩定性衰減驗證
ax4 = axes[1, 1]
ax4.plot(
    hist["t"],
    hist["V_on"],
    color="#1f77b4",
    lw=2.5,
    label="Disalignment Potential V(t)",
)
ax4.axvspan(1.6, 4.8, color="gray", alpha=0.15)
ax4.set_title(
    "4. Lyapunov Stability V(t) [System Anxiety/Entropy]", fontweight="bold"
)
ax4.set_xlabel("Time [s]")
ax4.set_ylabel("Energy V", color="#1f77b4")
ax4.tick_params(axis="y", labelcolor="#1f77b4")
ax4.grid(True, ls=":", alpha=0.5)

# 雙軸繪製 dV/dt (驗證 dV/dt <= 0)
ax4_twin = ax4.twinx()
ax4_twin.plot(
    hist["t"],
    hist["dV_on"],
    color="#ff7f0e",
    lw=1.5,
    ls="--",
    label="Dissipation Rate dV/dt",
)
ax4_twin.axhline(0.0, color="black", lw=1, ls="-")
ax4_twin.set_ylabel("dV/dt", color="#ff7f0e")
ax4_twin.tick_params(axis="y", labelcolor="#ff7f0e")

# 組合第 4 格的圖例
lines_1, labels_1 = ax4.get_legend_handles_labels()
lines_2, labels_2 = ax4_twin.get_legend_handles_labels()
ax4.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right", fontsize=8)

plt.tight_layout()
plt.show()



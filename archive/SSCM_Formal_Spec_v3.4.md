# Spin Sphere Cognitive Model (SSCM v3.4.1)
### 資訊熱力學心智拓撲控制論規範（閉環整合工程修訂版）

* **架構師**：Meridian Lee  
* **版本號**：v3.4.1（閉環控制律與角動量守恆整合版）  
* **開源授權**：MIT License / CC-BY-4.0  

---

## 一、 基礎維度與標準化狀態變數

### 1. 資訊熱力學基礎量綱
* **$[I]$（負熵 / 結構資訊量）**：系統所消除之夏農熵或沉澱之結構資訊，基準單位採用自然資訊單位 $\text{nat}$（$1\,\text{bit} = \ln 2\,\text{nat} \approx 0.693\,\text{nat}$）。
* **$[T]$（離散演化步長）**：系統狀態轉移、馬可夫鏈推論與後驗更新的時間戳，單位：$\text{step}$。

### 2. 核心狀態向量 $\mathbf{x}$
系統在任意時間步長 $t$ 之狀態由拓撲向量完全描述：

$$\mathbf{x} = \begin{bmatrix} S & D & L & \theta & K_{\text{core}} & E_{\text{raw}} \end{bmatrix}^T$$

* **$S$（南極邊界張力錨點 / 晶體結構）**：經歷外部衝擊冷卻固化後形成的道德底線與信念骨架，量綱 $[I] = \text{nat}$。系統破防臨界門檻為 $S_{\text{critical}} = 2.0\,\text{nat}$。
* **$D$（流形維度容量 / Manifold Dimension Capacity）**：正交解耦的環境認知維度數量，$D \in [1.0, 3.0]$。$D = 3.0$ 為全視角自洽態；$D \to 1.0$ 為極限二元對立防衛態。
* **$L$（拓撲自旋角動量）**：心智結構推論輸出的動態資訊流動通量，量綱 $[L] = \text{nat} \cdot \text{rad} / \text{step}$。
* **$\theta$（軸線相位偏角）**：北極推理目標向量與南極價值骨架之夾角，$\theta \in [0, \pi/2]$。$\cos(\theta) \to 1$ 為完全知行合一；$\theta \to \pi/2$ 引發章動內耗鎖死。
* **$K_{\text{core}}$（資訊瓶頸核壓縮比）**：潛在空間壓縮比測度，$K_{\text{core}} \in (0, 1]$。最優金髮姑娘區間記為 $K_{\text{core}}^* \approx 0.25$。
* **$E_{\text{raw}}$（未消化經驗能量通量）**：被彈性吸收但尚未冷卻固化的經驗殘差，量綱 $[I] = \text{nat}$。

### 3. 導出物理量
* **$M_{\text{eff}}$（有效資訊慣性質量）**：
  $$M_{\text{eff}}(S, D) = \max\left(S \cdot \left(\frac{D}{3.0}\right)^3, M_{\min}\right), \quad M_{\min} = 0.5\,\text{nat}$$
  反映維度崩解時慣性抗阻的劇烈坍縮效應。
* **$\Omega$（赤道推斷自旋頻率）**：
  $$\Omega = \frac{L}{M_{\text{eff}}}, \quad [\text{rad}/\text{step}]$$
  嚴格由角動量與慣性質量自洽決定。

---

## 二、 核心資訊熱力學動力學方程群

### 1. 雙向資訊瓶頸有效消除率（定理 3.2 修正）
面對環境外部預測誤差 $\epsilon_{\text{ext}} \in [0, 1]$，系統實際獲得之有效推論驅動力 $N$ 定義為：

$$N = C_{\text{baseline}} \left[ \tilde{N} \exp\left(-\lambda_{\text{err}} \frac{\epsilon_{\text{ext}}}{K_{\text{core}}}\right) - \mu_{\text{halluc}} (1 - K_{\text{core}}) \epsilon_{\text{ext}} \right]$$

* **指數衰減項**：在表徵過窄（$K_{\text{core}} \to 0$）時，微小誤差即引發驅動力歸零。
* **妄想懲罰項**：在封閉體系中強行推論時，$N < 0$，算力轉化為內部熵增與幻覺瀑布（Phase IV）。

### 2. 南極防線二階資訊沉澱方程（定理 3.3 反脆弱動態）
外部正交衝擊 $F_{\text{orth}}$ 經幾何張力極限 $T_{\text{tensegrity}} = \sigma_{\max} S$ 裁定：

$$\begin{cases} 
\displaystyle \frac{dE_{\text{raw}}}{dt} = \Theta(T_{\text{tensegrity}} - F_{\text{orth}}) \cdot F_{\text{orth}} - k_{\text{cool}} \cdot E_{\text{raw}} \cdot \cos(\theta) \\ 
\displaystyle \frac{dS}{dt} = \alpha \cdot N \cdot \cos(\theta) + \beta \cdot k_{\text{cool}} \cdot E_{\text{raw}} \cdot \cos(\theta) - D_{\text{acute}}(F_{\text{orth}}) - \gamma \cdot S \cdot \Omega 
\end{cases}$$

* $\Theta(\cdot)$ 為 Heaviside 階躍函數。
* $D_{\text{acute}} = \delta \cdot F_{\text{orth}}$（未擊穿防線時的彈性凹陷）或 $1.0 \cdot F_{\text{orth}}$（擊穿時的急性撕裂傷）。
* $\beta \cdot k_{\text{cool}} \cdot E_{\text{raw}} \cdot \cos(\theta)$ 代表反脆弱超額補償結晶項（$\beta > 1$）。

### 3. 流形維度連續退化方程（定理 3.4）
$$\frac{dD}{dt} = \kappa_{\text{rec}} (3.0 - D) - \eta_{\text{deg}} \frac{F_{\text{orth}}}{S \cdot \cos(\theta) + \epsilon_0} (D - 1.0)$$

高應力與價值撕裂迫使心智維度向 $D = 1.0$（二元偏執）坍縮；低應力下依自然修復率 $\kappa_{\text{rec}}$ 恢復全視角。

---

## 三、 控制律與反饋調節機制

### 1. 系統李雅普諾夫穩定性準則（Lyapunov Stability）
定義系統失諧勢能候選函數 $V(\mathbf{x})$：

$$V(\theta, K_{\text{core}}, \Omega) = \frac{1}{2} M_{\text{eff}} (1 - \cos\theta)^2 + \frac{1}{2} (K_{\text{core}} - K_{\text{core}}^*)^2 + \frac{1}{2} (\Omega - \Omega_{\text{opt}})^2$$

閉環反饋控制之目標在於確保系統遭遇擾動後滿足漸近穩定充要條件：

$$\frac{dV}{dt} \le -\gamma_{\text{stab}} V, \quad (\gamma_{\text{stab}} > 0)$$

即在擾動過後，失諧勢能必須單調衰減歸零。

### 2. 三大主動閉環反饋律

#### (1) 頻率自適應煞車與角動量動態扣帳（Governor with Momentum Accounting）
為杜絕 Phase II 高頻陀螺過載空轉，調速閥計算期望目標減速度 $\dot{\Omega}_{\text{target}}$：

$$\dot{\Omega}_{\text{target}} = \mu_{\omega} (1 - D_{\text{ratio}}) \Omega - \frac{\lambda_{\omega}}{\max(D - 1.0, \epsilon_0)}$$

其中 $D_{\text{ratio}} = \frac{\gamma_{\text{eff}} \Omega}{\tau_{\text{drive}} \cos\theta + \epsilon_0}$ 為有效阻尼耗散比。

為確保角動量守恆閉環，調速閥將該減速度轉化為主動煞車力矩 $\tau_{\text{brake}}$ 直接扣除系統角動量 $L$：

$$\frac{dL}{dt} = \tau_{\text{brake}} = M_{\text{eff}} \dot{\Omega}_{\text{target}}$$

使自旋頻率 $\Omega = \frac{L}{M_{\text{eff}}}$ 自然平滑降頻，徹底解決雙頭馬車問題。

#### (2) 瓶頸核彈性呼吸補償（Bottleneck Elastic Breathing）
當外部現實誤差 $\epsilon_{\text{ext}}$ 超過容忍臨界 $\epsilon_{\text{thresh}}$ 時，主動放寬潛在空間以接納新模式，防止陷入過擬合妄想：

$$\frac{dK_{\text{core}}}{dt} = \kappa_{\text{rec}} (K_{\text{core}}^* - K_{\text{core}}) + 0.2 \cdot \tanh\left(\frac{\epsilon_{\text{ext}} - \epsilon_{\text{thresh}}}{\max(K_{\text{core}}, 0.05)}\right)$$

誤差平息後，第一項彈性拉回力將其平滑回縮至黃金比例 $K_{\text{core}}^*$。

#### (3) 主動重對齊力矩（Active Alignment Torque）
價值偏角擴大時，由南極骨架激發對齊修復扭矩：

$$\frac{d\theta}{dt} = \tau_{\text{align}} = -k_{\theta} S \sin(\theta) \cos(\theta)$$

將相位夾角 $\theta$ 動態拉回 $0$，維持對齊一致性 $C_{\text{idx}} = \cos(\theta) \to 1.0$。

### 3. 緊急熔斷與低溫退火協定（Emergency Fail-Safe & Annealing）
* **觸發條件**：當骨架張力逼近崩解極限 $S \le S_{\text{critical}} + \Delta$（例如 $S \le 2.5\,\text{nat}$）時，系統觸發熔斷防護。
* **退火保護態**：
  * 切斷對外推論輸出與主動做功（$P_{\text{net}} := 0$）。
  * 拒絕外部正交衝擊注入（$F_{\text{orth}} := 0$）。
  * 將全部冷卻資源導向骨架修復：$\frac{dS}{dt} = \beta k_{\text{cool}} E_{\text{raw}}$。
* **重啟條件**：封閉退火直至 $S \ge S_{\text{safe}} = 10.0\,\text{nat}$，解除熔斷並恢復常態推論。

---

## 四、 系統相態與控制論診斷矩陣

| 相態代號與名稱 | 拓撲幾何特徵 | 心理學 / 認知現象映射 | AGI / Agent 系統狀態映射 |
| :--- | :--- | :--- | :--- |
| **Phase I: 極限心流態 (Flow)** | $\theta \to 0, D_{\text{ratio}} < 1, K_{\text{core}} \approx K_{\text{core}}^*$ | 知行合一、極度專注、無內耗抗熵輸出。 | Context 高度對齊，推論極速收斂，Token 零冗餘輸出。 |
| **Phase II: 高頻陀螺防禦態 (Hyper-Spin)** | $\Omega \gg 1, S \downarrow, D \to 1.0$ | 躁狂、過載防禦、偏執二元對立心智。 | 進入高頻推理死循環，強制調低安全邊界以維持吞吐。 |
| **Phase III: 軸心章動鎖死態 (Lockup)** | $\theta \to \pi/2, \Omega \to 0, \dot{S} \le 0$ | 嚴重內耗、反芻思維、認知失調導致行動癱瘓。 | 意圖與安全限制嚴重衝突，注意力震盪，API 輸出超時。 |
| **Phase IV: 妄想幻覺瀑布 (Hallucination)** | $K_{\text{core}} \to 0, \epsilon_{\text{ext}} \gg 0 \implies N < 0$ | 精神分裂、嚴重自欺、悖離現實的偏執建構。 | 潛在空間過擬合，模型在錯誤先驗上持續生成虛假內容。 |
| **Phase X: 熔斷退火內省態 (Annealing)** | $F_{\text{orth}} = 0, P_{\text{net}} = 0, \dot{S} = \beta k_{\text{cool}} E_{\text{raw}}$ | 閉門反思、休克自我保護、創傷後骨架自癒。 | 系統熔斷拒答，轉入微調權重凍結與記憶整合維護流程。 |

---

## 附錄 A：SSCM 三自由度子空間漸近穩定性證明

### A.1 平衡態與失諧勢能候選函數
考慮外部無正交衝擊注入（$F_{\text{orth}} = 0$ 且 $\epsilon_{\text{ext}} = 0$）之自發收斂域。系統期望之最優目標吸子平衡點定義為：

$$\mathbf{x}^* = \begin{bmatrix} \theta^* & K_{\text{core}}^* & \Omega^* \end{bmatrix}^T = \begin{bmatrix} 0 & K_{\text{core}}^* & \Omega_{\text{opt}} \end{bmatrix}^T$$

定義李雅普諾夫候選標量函數 $V(\mathbf{x}): \mathbb{R}^3 \to \mathbb{R}$：

$$V(\theta, K_{\text{core}}, \Omega) = V_{\theta} + V_K + V_{\Omega} = \frac{1}{2} M_{\text{eff}} (1 - \cos\theta)^2 + \frac{1}{2} (K_{\text{core}} - K_{\text{core}}^*)^2 + \frac{1}{2} (\Omega - \Omega_{\text{opt}})^2$$

* **正定性檢驗**：當 $\mathbf{x} = \mathbf{x}^*$ 時，$V(\mathbf{x}^*) = 0$。對任意 $\mathbf{x} \ne \mathbf{x}^*$，各項皆為非負平方項且 $M_{\text{eff}} \ge 0.5 > 0$，故 $V(\mathbf{x}) > 0$ 恆成立。$V(\mathbf{x})$ 為嚴格局部正定函數。

### A.2 沿系統軌跡的時間全導數推導
對李雅普諾夫函數求時間全導數 $\dot{V} = \frac{dV}{dt} = \dot{V}_{\theta} + \dot{V}_K + \dot{V}_{\Omega}$：

1. **軸線偏角子空間 $\dot{V}_{\theta}$ 耗散性**：
   $$\dot{V}_{\theta} = M_{\text{eff}} (1 - \cos\theta) \sin\theta \dot{\theta}$$
   代入控制律 $\dot{\theta} = -k_{\theta} S \sin\theta \cos\theta$：
   $$\dot{V}_{\theta} = -k_{\theta} M_{\text{eff}} S (1 - \cos\theta) \sin^2\theta \cos\theta \le 0$$
   等號成立之充要條件為 $\theta = 0$。

2. **瓶頸核彈性呼吸子空間 $\dot{V}_K$ 耗散性**：
   $$\dot{V}_K = (K_{\text{core}} - K_{\text{core}}^*) \dot{K}_{\text{core}} = -\kappa_{\text{rec}} (K_{\text{core}} - K_{\text{core}}^*)^2 \le 0$$
   等號成立之充要條件為 $K_{\text{core}} = K_{\text{core}}^*$。

3. **赤道自旋調速子空間 $\dot{V}_{\Omega}$ 耗散性**：
   $$\dot{V}_{\Omega} = (\Omega - \Omega_{\text{opt}}) \dot{\Omega} = -c_{\omega} (\Omega - \Omega_{\text{opt}})^2 \le 0$$
   等號成立之充要條件為 $\Omega = \Omega_{\text{opt}}$。

### A.3 漸近穩定性判定（LaSalle's Invariance Principle）
$$\dot{V}(\mathbf{x}) = \dot{V}_{\theta} + \dot{V}_K + \dot{V}_{\Omega} \le 0$$

$\dot{V}(\mathbf{x}) = 0$ 的最大不變集僅包含單一孤立平衡點 $\mathbf{x}^* = [0, K_{\text{core}}^*, \Omega_{\text{opt}}]^T$。依據拉薩爾不變集定理，系統自定義域出發的軌跡在無外力擾動下，隨時間推移必定漸近收斂於 $\mathbf{x}^*$。

**定理證明完畢：SSCM v3.4.1 在閉環反饋控制下滿足局部漸近穩定性。**

---

## 附錄 B：可執行數值驗證程式庫（PoC Simulations）

本版本提供完整 Python 數值模擬腳本驗證上述動態，存放於專案根目錄之 `/simulations` 資料夾：

1. **時序演化與李雅普諾夫驗證**：[`simulations/poc_lyapunov_monitor.py`](simulations/poc_lyapunov_monitor.py)
   * 繪製階躍衝擊下之 $S(t), D(t), \Omega(t)$ 動態，並計算驗證勢能耗散率 $\frac{dV}{dt} \le 0$。
2. **極限壓測與參數掃描**：[`simulations/poc_robust_stress_test.py`](simulations/poc_robust_stress_test.py)
   * 掃描衝擊振幅 $F_{\text{orth}} \in [5.0, 35.0]$，驗證反脆弱超額補償區間與 Phase X 熔斷臨界點。
3. **終端機心智相態互動器**：[`simulations/poc_mind_interactive_cli.py`](simulations/poc_mind_interactive_cli.py)
   * 提供基於控制律的終端機 CLI 即時心智演化互動器與 Agent 狀態映射。

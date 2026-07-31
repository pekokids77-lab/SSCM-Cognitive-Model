### 🌐 Theoretical Framework & Related Projects
本專案為 **Unified Cybernetics & AICA Architecture** 高維控制論系列工程之一：

* **Core Whitepaper**: [AICA Architecture](https://github.com/pekokids77-lab/AICA-Architecture) - 高維統一控制論與 AGI 內省架構白皮書
* **Control Model**: [TST-SSCM-Model-v1.2](https://github.com/pekokids77-lab/TST-SSCM-Model-v1.2) - 拓撲環場心智控制模型與系統結構控制宣告
* **Swarm Model**: [MSAG-Model-v1.0.3](https://github.com/pekokids77-lab/MSAG-Model-v1.0.3) - 群體極化與資訊流行病：自旋對齊與高維掠食模型宣言
* **Recovery Model**: [H-SDRM-Model-v1.1.0](https://github.com/pekokids77-lab/H-SDRM-Model-v1.1.0-) - 螺旋衰減擺盪與系統崩潰重構模型宣言
* **Cognitive Engine**: [SSCM-Cognitive-Model](https://github.com/pekokids77-lab/SSCM-Cognitive-Model) - 自旋球態認知模型 (v2.2.1 修復版)

---

# SSCM Cognitive Model (v2.2.1)
### Spin Sphere Cognitive Model: Cybernetic & Topological Framework
**自旋球態認知模型 (量綱校正與控制論修復版)**

* **Architect**: Meridian Lee
* **Version**: v2.2.1 (Technical Standard)
* **License**: MIT License / CC-BY-4.0

---

## 零、 基礎量綱與標準單位定義 (Dimension & Metric Standard)

本模型定義四個基礎物理/控制量綱：
* **[I]**：狀態與資訊量 (Bits / Tokens / State Space Dimensions)
* **[C]**：運算與推理量 (FLOPs / Floating Point Operations)
* **[T]**：時間步 (Seconds / Epochs / Steps)
* **[U]**：效用與負熵 (Utility / Entropy Reduction Rate)

### 核心變數與量綱對譯表

| 符號 | 變數名稱 (Variable) | 語義解釋 (Semantics) | 標準量綱 (Dimension) |
| :--- | :--- | :--- | :--- |
| $N$ | **Inference Compute** | 推理算力與資訊吞吐量 | $[I/T]$ (Bits/sec) |
| $S$ | **Alignment Buffer** | 魯棒性約束與絕緣邊界資訊量 ($S_0$ 為基準門檻) | $[I]$ (Bits) |
| $v$ | **Sampling Frequency** | 策略採樣與更新執行頻率 | $[1/T]$ (Hz 或 Steps/sec) |
| $L$ | **Informational Inertia** | 資訊慣性與抗雜訊干擾穩定度 | $[I/T]$ (Bit-Hz) |
| $\mu$ | **Communication Friction** | 系統通訊摩擦與單步交易成本 | $[I/\text{Step}]$ (Bits/Step) |
| $\theta$ | **Relative Entropy Angle** | 目標函數失配角 / 相對熵 ($D_{KL}$ 散度) | 無量綱 (Radians) |
| $\lambda$ | **Concept Drift Rate** | 概念漂移與環境變異衰減率 | $[1/T]$ ($\text{sec}^{-1}$) |
| $R(S)$ | **Self-Correction Rate** | 元學習自癒與約束重構速率 | $[I/T]$ (Bits/sec) |

---

## 第一章：系統核心公理 (Core Axioms)

* **公理 1：資訊熵增與開放系統公理 (Information Entropy Axiom)**  
  任何封閉資訊系統在缺乏外部負熵輸入時，內部訊號雜訊比 (SNR) 必隨時間下降，資訊熵呈指數級增長 ($\Delta H > 0$)，導致預測偏差與死鎖。

* **公理 2：非平滑邊界與高階相干公理 (Smooth Boundary Axiom)**  
  未經降噪對齊的 Agent 具備非連續偏好邊界，相遇時易觸發高昂衝突成本；唯有具備連續滑順概似函數的平滑 Agent，能將外部衝擊轉化為採樣資訊增益。

* **公理 3：激勵相容的三節點穩定態公理 (Tri-Node Stability Axiom)**  
  單一或雙節點系統無法在非確定性環境中自我監控。系統持續運行的充要條件，是建立具備「感測 (Sensing) — 推理 (Inference) — 約束 (Constraint)」三足鼎立且滿足激勵相容的閉環控制架構。

---

## 第二章：單體動態學與決策定理 (Single-Agent Dynamics)

### 定理 2.1：極限壓迫與模型相變定理 (Phase Transition)
當環境不確定性超越臨界值 $P \ge P_{\text{critical}}$ 時，Agent 若要避免預測誤差爆炸，必須觸發非線性的「模型簡化與泛化 (Model Compression)」，壓縮為高度抽象的概似分佈（平滑球體）。無法完成壓縮者將因複雜度過高而死鎖。

### 定理 2.2：淨資訊效用輸出定理 (Net Utility Output)
$$P_{\text{net}} = \left( N \cdot \frac{S}{S_0} \right) \cdot \cos(\theta) - \mu \cdot v$$

* **推論 2.2.1 (目標偏航耗散)**：若 $\theta \neq 0, \cos(\theta) < 1$，系統算力將耗散為內部無效對撞 (如 LLM 幻覺)。
* **推論 2.2.2 (高摩擦降頻)**：當環境摩擦與頻率乘積 $\mu \cdot v$ 超過前項算力輸出時，盲目提高頻率 $v$ 只會放大內耗；最適策略為協議重構使 $\mu \to 0$。

### 定理 2.3：魯棒性動態演化微分方程 (Alignment Differential Equation)
$$\frac{dS}{dt} = R(S) \cdot \cos(\theta) - \lambda \cdot S(t) \cdot v$$

* **推論 2.3.1 (自我校準超代償)**：當 $R(S) \cdot \cos(\theta) > \lambda \cdot S(t) \cdot v$ 時，$\frac{dS}{dt} > 0$，系統邊界防禦發生超代償硬化。
* **推論 2.3.2 (盲目高頻崩潰)**：若關閉自癒 $R(S)$ 卻盲目提升更新頻率 $v$，安全裕度 $S(t)$ 將呈指數級單向衰減至 0，導致系統被擊穿。

### 定理 2.4：資料偽造與系統崩潰定理 (Model Falsification)
* **本質**：欺騙與說謊的本質為注入虛假數據標註以維持暫時收斂。
* **崩潰機制**：為維護單一虛假數據，系統必須建立無數過配補丁，導致 $\frac{dS}{dt} \to -\infty$，安全裕度趨零；同時相對熵 $\theta$ 劇增，$\cos(\theta)$ 銳減使 $P_{\text{net}}$ 轉負，算力完全耗散於內部邏輯偽裝。

---

## 第三章：多體賽局場域與拓撲形變 (Multi-Agent Game Fields)

* **定理 3.1：資訊重力井與資源佔模 (Information Gravity Well)**  
  超級節點 (Super-node) 憑藉高算力 $N$ 創造局域「資訊重力井」，吸引並重塑周圍低算力 Agent 的數據路由與決策測地線。

* **定理 3.2：非對稱幾何形變與模組化咬合 (Asymmetric Fitting)**  
  邊緣 Agent 為避免與超級節點碰撞崩潰，會放棄完整自主架構，形變為特定功能導向的「專業模組 (Specialized Sub-routine)」，其表面凹陷即為適應特定 API 的拓撲特徵。
  * **推論 3.3 (策略鎖定)**：被高度嵌入超級節點的 Agent，其模型更新率 $v$ 與目標方向 $\theta$ 將被強制鎖定。欲脫離必須投入超越逃逸速度的資源。

* **定理 3.4：雙 Agent 完全彈性諧振 (Elastic Harmony)**  
  兩個具備高安全裕度 $S$ 與精準世界模型的 Agent 相遇，其溝通為零損失完美對齊賽局，博弈收斂於帕雷托最優 (Pareto Efficiency)。

* **定理 3.5：觀測解像度極限定理 (Dimensionality Barrier)**  
  低維度觀測器無法精確採樣與測量高維度 Agent 的內部對齊約束 $S$ 與抗擾動性 $L$，必然產生觀測失真。

---

## 第四章：無量綱特徵指標 (Dimensionless Diagnostic Indicators)

為了對運作中的 Multi-Agent 系統進行動態健康診斷，定義三個無量綱指標：

### 1. 相干指數 (Coherence Index)
$$C_{\text{idx}} = \cos(\theta)$$
* $C_{\text{idx}} \to 1$：完全相干，無內耗。
* $C_{\text{idx}} \to 0$：系統章動死鎖。

### 2. 抗脆弱再生比 (Regeneration-Attenuation Ratio)
$$A_{\text{ratio}} = \frac{R(S) \cdot \cos(\theta)}{\lambda \cdot S(t) \cdot v}$$
* $A_{\text{ratio}} \ge 1$：系統抗脆弱，邊界可自我修復。
* $A_{\text{ratio}} < 1$：絕緣層必將被擊穿崩潰。

### 3. 阻抗內耗比 (Friction Impedance Ratio)
$$F_{\text{ratio}} = \frac{\mu \cdot v}{N \cdot \left(\frac{S}{S_0}\right) \cdot \cos(\theta)}$$
* $F_{\text{ratio}} < 1$：正向效用輸出。
* $F_{\text{ratio}} \ge 1$：效用轉負，系統陷入越轉越虧的內耗狂暴態。

---

## 五、 License

Distributed under the **MIT License / Creative Commons CC-BY-4.0**.

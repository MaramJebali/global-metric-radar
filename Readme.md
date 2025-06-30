# Global Metric Radar

A Python module to compute a composite **Global Score** from multiple metrics using radar chart geometry, with threshold-based penalties and weighted importance. Provides both numeric scores and human-readable interpretations.

## Features

✅ Radar polygon area calculation to combine multiple metrics into a single geometric score.  
✅ Customizable per-metric thresholds to flag metrics below minimum acceptable levels.  
✅ Weighted penalties that reduce the global score based on the importance of failing metrics.  
✅ Interpretation layer that classifies overall quality (`excellent`, `acceptable`, `poor`) with meaningful feedback.  
✅ Interactive radar visualization with Streamlit.

## 📐 How It Works: Step-by-Step Calculation

The **Global Metric Radar** computes an overall quality score by representing multiple normalized metrics as points on a radar chart and calculating the polygon area they form. This geometric approach allows capturing combined performance in a single scalar value.

### 1️⃣ Represent Metrics as Points on a Radar Chart

- For *n* metrics normalized to [0, 1], denoted:

  r = [r₀, r₁, ..., rₙ₋₁]

- Metrics are placed on evenly spaced axes around a radar chart.

- The angle between consecutive axes is:

  θ = 2π / n

---

### 2️⃣ Compute the Polygon Area Formed by Metrics

The area of the polygon formed by connecting metrics in order is calculated by:

Area = (1/2) × | Σᵢ₌₀ⁿ⁻¹  rᵢ × r_{(i+1) mod n} × sin(θ) |

where:

- rᵢ is the metric on axis i,
- r_{(i+1) mod n} wraps around to form a closed shape,
- sin(θ) accounts for the fixed angle between consecutive axes.

---

### 3️⃣ Normalize the Polygon Area

The maximum possible area, achieved when all metrics equal 1, is:

Max Area = (1/2) × n × sin(θ)

The **normalized area** is given by:

Normalized Area = Area / Max Area

which ensures the result lies in [0, 1].

---

### 4️⃣ Identify Metrics Below Thresholds

Each metric is compared against its threshold. Metrics with:

rᵢ < thresholdᵢ

are recorded as failing.

---

### 5️⃣ Compute Weighted Penalty

Metrics have importance weights wᵢ. The penalty is calculated as:

- Total weight:

  W_total = Σᵢ₌₀ⁿ⁻¹ wᵢ

- Weight of failing metrics:

  W_bad = Σ_{i ∈ bad} wᵢ

- Penalty factor:

  Penalty = 1 - (W_bad / W_total)

---

### 6️⃣ Calculate Final Global Score

Combining geometry and penalty:

Global Score = Normalized Area × Penalty

This single score reflects both overall performance and the severity of failing metrics.

---

### 7️⃣ Generate Human-Readable Interpretation

The `interpret_score()` function provides insights like:

- The number of metrics below thresholds.
- Penalty impact as percentage reduction from normalized area.
- Overall quality category:

  - ✅ Excellent  
  - ⚠️ Acceptable with moderate issues  
  - ❌ Poor, critical improvements needed.

---

## 🔧 Installation

This package requires:

- `numpy`  
- `streamlit`  
- `plotly`

Install via pip:

```bash
pip install numpy streamlit plotly

```

# API Reference

### `global_score(metrics, threshold=0.5, weights=None) -> (score, normalized_area, bad_metrics_indices)`

Calculate a weighted global quality score from a list of metrics.

#### Parameters:

- `metrics` (`list[float]` or `np.ndarray`): Metric values in the range [0, 1].
- `threshold` (`float` or `list[float]`, optional): Threshold(s) below which metrics are penalized. Default is `0.5`.
- `weights` (`list[float]` or `np.ndarray`, optional): Importance weights for each metric. Default is equal weights.

#### Returns:

- `score` (`float`): Final global score in [0, 1].
- `normalized_area` (`float`): Normalized radar polygon area representing combined metric performance.
- `bad_metrics_indices` (`list[int]`): Indices of metrics below their respective thresholds.

---

### `interpret_score(score, normalized_area, bad_metrics_indices, thresholds, metrics) -> str`

Generate a human-readable interpretation of the global score.

#### Parameters:

- `score` (`float`): Global score computed from `global_score`.
- `normalized_area` (`float`): Normalized radar area computed from `global_score`.
- `bad_metrics_indices` (`list[int]`): Indices of metrics below their thresholds.
- `thresholds` (`list[float]`): Threshold values per metric.
- `metrics` (`list[float]`): Original metric values.

#### Returns:

- `interpretation` (`str`): Text summary indicating quality level (`excellent`, `acceptable`, or `poor`), penalty impact, and metrics below threshold.

---

# 🚀 Live Demo with Streamlit
The included if __name__ == "__main__" block demonstrates usage with Streamlit and Plotly for an interactive dashboard showing your metrics, thresholds, and radar chart in real time.


## 📄 License

This project is licensed under the MIT License 
import numpy as np
import streamlit as st
import plotly.graph_objects as go


def global_score(metrics, threshold=0.5, weights=None):
    metrics = np.array(metrics)
    n = len(metrics)

    if n < 3:
        raise ValueError("You need at least 3 metrics to have a global metric.")

    # Handle weights
    if weights is None:
        weights = np.ones(n)  # Equal weights
    else:
        weights = np.array(weights)
        if len(weights) != n:
            raise ValueError("Length of weights must match number of metrics.")

    # Step 1: Calculate radar area
    angle = 2 * np.pi / n
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += metrics[i] * metrics[j] * np.sin(angle)
    area = 0.5 * abs(area)

    max_area = 0.5 * n * np.sin(angle)
    normalized_area = area / max_area

    # Step 2: Identify metrics below thresholds
    if isinstance(threshold, (list, np.ndarray)):
        if len(threshold) != n:
            raise ValueError("Threshold list must match number of metrics.")
        bad_metrics_indices = [i for i, val in enumerate(metrics) if val < threshold[i]]
    else:
        bad_metrics_indices = [i for i, val in enumerate(metrics) if val < threshold]

    # Step 3: Apply weighted penalty
    weight_sum = np.sum(weights)
    bad_weights = np.sum([weights[i] for i in bad_metrics_indices])
    penalty = 1 - bad_weights / weight_sum

    # Step 4: Compute global score with area + penalty
    score = normalized_area * penalty

    return score, normalized_area, bad_metrics_indices
def interpret_score(score, normalized_area, bad_metrics_indices, thresholds, metrics):
    interpretation = ""

    if bad_metrics_indices:
        interpretation += f"❌ {len(bad_metrics_indices)} metric(s) below threshold. "
    else:
        interpretation += "✅ All metrics meet thresholds. "

    drop_ratio = (normalized_area - score) / normalized_area if normalized_area > 0 else 0
    interpretation += f"\n📉 Penalty impact: {drop_ratio*100:.1f}% reduction in quality."

    # Check if all metrics exceed threshold by 15%
    all_excellent = all(
        metrics[i] >= 1.15 * thresholds[i] for i in range(len(metrics))
    )

    if all_excellent:
        interpretation += " Quality is excellent ✅ (all metrics exceed thresholds by 15%+)."
    elif score >= 0.75 and drop_ratio < 0.1:
        interpretation += " Quality is excellent ✅."
    elif score >= 0.5 and drop_ratio < 0.3:
        interpretation += " Quality is acceptable ⚠️ with moderate issues."
    else:
        interpretation += " Quality is poor ❌. Critical improvements needed."

    return interpretation


if __name__ == "__main__":
    import streamlit as st
    import plotly.graph_objects as go

    st.title("📊 Global Metric Radar Visualization")

    # Example inputs 
    example_metrics = [0.99, 0.99, 0.99, 0.1]
    thresholds = [0.5, 0.3, 0.5, 0.5]
    weights = [1, 1, 2, 1]  # Example: third metric twice as important

    # Assume you have a global_score function defined that returns (score, normalized_area, bad_metrics_indices)
    score, area, bad = global_score(example_metrics, thresholds, weights)

    
    interpretation = interpret_score(
        score,
        area,
        bad,
        thresholds,
        example_metrics
    )

    st.write(f"### Global Score: {score:.3f} → {interpretation}")
    st.write(f"Radar Area (normalized): {area:.3f}")

    if bad:
        st.warning(f"Metrics below threshold (indices): {bad}")
    else:
        st.success("All metrics meet the thresholds!")

    # Radar chart
    categories = [f"Metric {i+1}" for i in range(len(example_metrics))]
    metrics_extended = example_metrics + [example_metrics[0]]  # Close the loop for radar
    thresholds_extended = thresholds + [thresholds[0]]

    fig = go.Figure()

    # User metrics line
    fig.add_trace(go.Scatterpolar(
        r=metrics_extended,
        theta=categories + [categories[0]],
        fill='toself',
        name='Metrics',
        line=dict(color='blue')
    ))

    # Threshold line (red zone border)
    fig.add_trace(go.Scatterpolar(
        r=thresholds_extended,
        theta=categories + [categories[0]],
        fill='toself',
        name='Thresholds',
        line=dict(color='red', dash='dot')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

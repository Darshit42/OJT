# Electricity Load Diagrams (2011–2014) — Chart Visualization Analysis

This document describes each chart/visualization produced in the `data_preprocessing.ipynb` notebook, explaining **what data it shows**, **how to read it**, and **what insights it provides**.

---

## 1. Distribution of Zero-Value Percentage Across Meters (Histogram)

**Section:** 4.3 — Zero-Consumption Meters Check

**What it shows:**
A histogram where the X-axis is the *percentage of zero values* for each meter (0–100%), and the Y-axis is *how many meters* fall into that percentage bin. Each bar represents a group of meters that share a similar proportion of zero readings.

**How to read it:**
- A bar at the far left (near 0%) means those meters were almost always active — they reported non-zero consumption most of the time.
- A bar at the far right (near 100%) means those meters were almost always inactive — they recorded zero consumption throughout the dataset.

**What analysis it provides:**
- **Identifies inactive or partially active meters.** Meters with very high zero-percentages (e.g. >90%) may have been installed late in the study period, decommissioned early, or faulty.
- **Guides data cleaning decisions.** Fully inactive meters (100% zeros) can be dropped, and heavily zero-dominated meters may need special handling in downstream models.
- **Quantifies data sparsity.** Understanding how many meters are "mostly silent" helps gauge the overall density and quality of the dataset.

---

## 2. Daily Average Total Electricity Consumption (2011–2014) (Line Chart)

**Section:** 7.1 — Total Consumption Over Time

**What it shows:**
A time-series line chart spanning the full 4-year period. The X-axis is *date* and the Y-axis is *daily mean of total consumption* across all meters (kWh). The `total_consumption` feature (sum of all meter columns per 15-minute interval) is resampled to daily averages.

**How to read it:**
- The overall shape shows macro trends — is electricity usage growing, flat, or declining over the years?
- Periodic dips and peaks reveal **seasonal patterns** (e.g., lower consumption in summer vs. winter, or vice versa depending on climate).

**What analysis it provides:**
- **Long-term trend detection.** Reveals whether total consumption has increased year over year (more customers, economic growth) or decreased (energy efficiency, customer churn).
- **Seasonality identification.** Clear annual "waves" indicate strong seasonal dependency — critical knowledge for any forecasting model.
- **Anomaly spotting.** Isolated large spikes or dips may correspond to extreme weather events, public holidays, or data collection issues.

---

## 3. Average Total Consumption by Hour of Day (Bar Chart)

**Section:** 7.2 — Hourly Consumption Pattern

**What it shows:**
A bar chart with the X-axis showing the *hour of the day* (0–23) and the Y-axis showing *average total consumption (kWh)*. Each bar represents the mean of `total_consumption` at that hour, averaged across all days in the dataset.

**How to read it:**
- Low bars in the early morning hours (e.g. 0–5) indicate minimal overnight demand.
- Rising bars during morning hours reflect people waking up, businesses opening, etc.
- Peak bars (typically late morning to early evening) show the highest sustained demand period.
- Declining bars in the evening signify reduced commercial/industrial activity.

**What analysis it provides:**
- **Identifies daily load profile.** This is one of the most fundamental patterns in electricity demand — it separates "base load" from "peak load."
- **Peak hour detection.** Knowing when demand peaks is essential for grid planning, demand-response programs, and pricing strategies.
- **Consumer-type inference.** A strong midday peak suggests a heavy commercial/industrial component in the customer mix; a double peak (morning + evening) leans more residential.

---

## 4. Average Hourly Consumption: Weekday vs Weekend (Line Chart)

**Section:** 7.3 — Weekday vs Weekend Comparison

**What it shows:**
Two overlaid line charts on the same axes. The X-axis is *hour of day (0–23)*, and the Y-axis is *average total consumption (kWh)*. One line represents **weekdays** (Monday–Friday) and the other represents **weekends** (Saturday–Sunday).

**How to read it:**
- Where the weekday line sits above the weekend line, demand is higher on working days at that hour (typically during business hours).
- Where the two lines converge or the weekend line rises above, residential usage dominates.

**What analysis it provides:**
- **Behavioral segmentation.** Clearly separates commercial/industrial patterns (weekday-dominant) from residential patterns (more uniform across week).
- **Weekend base-load estimation.** The weekend curve approximates the "residential baseline" because commercial/industrial activity drops.
- **Demand-response planning.** Utilities can use the weekday–weekend gap to design programs that shift load from weekday peaks.

---

## 5. Average Total Consumption by Month (Bar Chart)

**Section:** 7.4 — Monthly Consumption Pattern

**What it shows:**
A bar chart where the X-axis is *month* (January–December) and the Y-axis is *average total consumption (kWh)*. Each bar represents the mean of `total_consumption` for that calendar month, averaged across all years.

**How to read it:**
- Higher bars indicate months with greater average demand.
- The overall shape reveals **seasonal patterns** — e.g. higher demand in winter months (heating) or summer months (cooling), depending on climate.

**What analysis it provides:**
- **Seasonal demand profiling.** Identifies whether the service area has a winter-peaking or summer-peaking load (or both).
- **Capacity planning input.** Utilities use monthly demand profiles to schedule maintenance outages during low-demand months and ensure adequate capacity during high-demand months.
- **Forecasting features.** Month-of-year is a strong seasonal predictor; this chart validates its importance.

---

## 6. Individual Meter Daily Average Profiles (Multi-panel Line Chart)

**Section:** 7.5 — Sample Individual Meter Profiles

**What it shows:**
A stacked set of line charts (one per meter) for the top 5 active meters. Each sub-plot has *date* on the X-axis and *daily average consumption (kWh)* on the Y-axis. The data is resampled to daily averages.

**How to read it:**
- Each panel shows one meter's 4-year consumption trajectory.
- Smooth seasonal oscillations indicate regular usage patterns.
- Abrupt step-changes may indicate meter installation/removal, customer changes, or data issues.

**What analysis it provides:**
- **Meter-level trend analysis.** Reveals whether individual customers have stable, growing, or declining consumption.
- **Customer characterization.** Different shapes (flat vs. seasonal, high vs. low amplitude) hint at different customer types (industrial with flat load, commercial with weekday peaks, residential with seasonal heating/cooling).
- **Data quality verification.** Sudden drops to zero or unrealistic spikes at the meter level are easier to spot in individual plots than in aggregated views.

---

## 7. Correlation Heatmap (Top 20 Meters by Total Consumption)

**Section:** 7.6 — Correlation Heatmap

**What it shows:**
A 20×20 matrix heatmap where both axes list the *top 20 highest-consumption meters*. Each cell shows the **Pearson correlation coefficient** between two meters' consumption time series. Colors range from blue (strong negative correlation, –1) through white (no correlation, 0) to red (strong positive correlation, +1).

**How to read it:**
- **Diagonal cells** are always +1 (each meter perfectly correlates with itself).
- **Red/warm clusters** of cells indicate groups of meters whose consumption patterns move together — they rise and fall at the same times.
- **Blue/cool cells** indicate meters with opposite patterns — when one goes up, the other tends to go down.
- **White/neutral cells** indicate meters whose patterns are independent.

**What analysis it provides:**
- **Customer segmentation / clustering.** Highly correlated meters likely serve similar customer types (e.g. all commercial, all residential) or are geographically co-located. These "natural clusters" are the starting point for unsupervised-learning-based customer segmentation.
- **Dimensionality reduction guidance.** If many meters are highly correlated (r > 0.8), they carry overlapping information. Techniques like PCA or autoencoders can compress them into fewer features without significant information loss — important for scalable forecasting pipelines.
- **Anomaly detection.** A meter that shows very low correlation with all others is an outlier — it may have faulty readings, represent a unique customer type, or have experienced a usage regime change.
- **Synchronized demand risk.** Meters that are strongly positively correlated imply their demand peaks simultaneously. This is critical for grid operators — synchronized peaks stress the network and must be managed proactively (e.g. via demand-response or energy storage).
- **Cross-meter forecasting.** Knowing which meters co-move allows "transfer learning" — a model trained on one meter can be adapted for a correlated meter with less retraining data.

---

## Summary

| # | Chart | Type | Key Insight |
|---|-------|------|-------------|
| 1 | Zero-Value Distribution | Histogram | Identifies inactive/partially active meters for data cleaning |
| 2 | Daily Avg Total Consumption (2011–2014) | Time-series line | Reveals long-term trends and seasonality |
| 3 | Avg Consumption by Hour of Day | Bar chart | Identifies daily peak/off-peak load profile |
| 4 | Weekday vs Weekend Consumption | Dual line chart | Separates commercial/industrial vs. residential patterns |
| 5 | Avg Consumption by Month | Bar chart | Reveals seasonal demand variation |
| 6 | Individual Meter Profiles | Multi-panel line | Shows meter-level trends, anomalies, and customer diversity |
| 7 | Top 20 Meters Correlation Heatmap | Heatmap matrix | Enables clustering, dimensionality reduction, and anomaly detection |

# ------------------- CONFIGURE THE PAGE -------------------
import streamlit as st
import pandas as pd
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

st.set_page_config(page_title='Citi Bike 2022 Dashboard', layout='wide')

st.title("Citi Bike 2022 Dashboard")
st.markdown("This dashboard explores 2022 Citi Bike usage patterns, visualising the most popular start stations, seasonal ride trends, and temperature effects on ridership in New York City.")


# ######################### IMPORT DATA #########################

# Load Top 20 stations csv
top20 = pd.read_csv("top20_stations.csv")
# Load trips and temperature csv
daily = pd.read_csv("daily_trips_vs_temp_2022.csv")

# Ensure the date column is parsed
if "date" in daily.columns:
    daily["date"] = pd.to_datetime(daily["date"])

# ######################### DEFINE THE CHARTS #########################

## Bar chart (Top 20)
st.subheader("Top 20 Start Stations by Trips (2022)")

# ensure sorted Top 20
top20 = top20.sort_values("trip_count", ascending=False).head(20)

fig_bar = go.Figure(
    go.Bar(
        x=top20["station"],
        y=top20["trip_count"],
        marker={"color": top20["trip_count"], "colorscale": "Viridis"},
    )
)
fig_bar.update_layout(
    title="Top 20 Start Stations by Trips (2022)",
    xaxis_title="station",
    yaxis_title="trip_count",
    height=600,
)
st.plotly_chart(fig_bar, use_container_width=True)

## Line chart (Dual axis: Trips vs Temp)
st.subheader("Daily Trips vs Average Temperature (Dual Axis)")

fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# trips on left axis
fig_2.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["trip_count"],
        name="Daily bike rides",
        mode="lines",
        line=dict(width=2),
    ),
    secondary_y=False,
)

# temperature on right axis
fig_2.add_trace(
    go.Scatter(
        x=daily["date"],
        y=daily["avg_temp"],
        name="Daily temperature (°C)",
        mode="lines",
        line=dict(width=2, dash="dot"),
    ),
    secondary_y=True,
)
fig_2.update_layout(
    title="Daily Trips vs Avg Temperature in 2022",
    height=800,
)
fig_2.update_xaxes(title_text="Date")
fig_2.update_yaxes(title_text="Sum of trips", secondary_y=False)
fig_2.update_yaxes(title_text="Avg Temp (°C)", secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)

# ######################### ADD THE MAP #########################
st.subheader("Citi Bike Flow Map (Kepler.gl)")

map_path = Path("kepler.gl.html")

if map_path.exists():
    st.caption(f"✅ Loading map: {map_path.name} ({os.path.getsize(map_path)/1e6:.1f} MB)")
    with open(map_path, "r", encoding="utf-8") as f:
        html_data = f.read()
    components.html(html_data, height=1000, scrolling=True)
else:
    st.error("Map file not found — place kepler.gl.html next to st_dashboard.py")
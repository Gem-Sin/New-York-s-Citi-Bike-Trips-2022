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
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)
    
# Load Top 20 stations csv
top20 = load_csv("top20_stations.csv")
# Load trips and temperature csv
daily = load_csv("daily_trips_vs_temp_2022.csv")

# Ensure the date column is parsed
if "date" in daily.columns:
    daily["date"] = pd.to_datetime(daily["date"])

# =============== SIDEBAR FILTERS ===============
with st.sidebar:
    st.header("Filters")
    # Top-N slider 
    top_n = st.slider("Show top start stations", 5, 20, 20)

    # Filter within the Top 20
    station_choices = sorted(top20["station"].unique())
    picked_stations = st.multiselect("Filter specific station(s)", station_choices)

    # Date range filter for the daily chart
    min_date = pd.to_datetime(daily["date"]).min().date()
    max_date = pd.to_datetime(daily["date"]).max().date()
    date_range = st.slider(
        "Date range (daily chart)",
        min_value=min_date, max_value=max_date,
        value=(min_date, max_date)
    )

st.caption("Use the filters in the sidebar to adjust the number of top start stations and the time range for analysis.")


# ######################### DEFINE THE CHARTS #########################

## Bar chart (Top 20)
st.subheader("Top 20 Start Stations by Trips (2022)")

# Create a filtered Top-N dataframe for plotting
df_top = top20.sort_values("trip_count", ascending=False)
if picked_stations:
    df_top = df_top[df_top["station"].isin(picked_stations)]
df_top = df_top.head(top_n)

if df_top.empty:
    st.warning("No stations match the current filter(s). Try clearing the station filter or increasing Top-N.")
else:
    fig_bar = go.Figure(data=[
        go.Bar(
            x=df_top["station"],
            y=df_top["trip_count"],
            text=df_top["trip_count"],
            textposition="auto",
            hovertemplate="<b>%{x}</b><br>Trips: %{y:,}<extra></extra>",
            marker=dict(color=df_top["trip_count"], colorscale="Viridis"),
        )
    ])
    
fig_bar.update_layout(
        xaxis_title="Station",
        yaxis_title="Trips",
        height=600,
        margin=dict(l=40, r=20, t=60, b=100),
       
        xaxis=dict(
            categoryorder="array",
            categoryarray=df_top["station"],
            tickangle=-35,
            tickfont=dict(size=10),
        ),
    )

st.plotly_chart(fig_bar, use_container_width=True)

# Insight
top_row = df_top.iloc[0]
st.markdown(
    f"**Insight:** Showing top **{len(df_top)}** start stations. "
    f"Peak station: **{top_row['station']}** with **{int(top_row['trip_count']):,}** trips."
)


# ######################### Line Chart: Trips vs Temperature ###########################
st.subheader("Daily Trips vs Average Temperature (Dual Axis)")

# Filter the daily df by date range
mask = (
    (daily["date"].dt.date >= date_range[0])
    & (daily["date"].dt.date <= date_range[1])
)
daily_f = daily.loc[mask].copy()

# Make the dual-axis chart
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
fig_2.add_trace(
    go.Scatter(
        x=daily_f["date"],
        y=daily_f["trip_count"],
        name="Daily bike rides",
        mode="lines",
        line=dict(width=2),
    ),
    secondary_y=False,
)

fig_2.add_trace(
    go.Scatter(
        x=daily_f["date"],
        y=daily_f["avg_temp"],
        name="Average temperature (°C)",
        mode="lines",
        line=dict(width=2, dash="dot"),
    ),
    secondary_y=True,
)

fig_2.update_layout(
    height=800,
    margin=dict(l=40, r=20, t=40, b=60),
    legend=dict(orientation="h", y=-0.2),
)
fig_2.update_xaxes(title_text="Date")
fig_2.update_yaxes(title_text="Number of Trips", secondary_y=False)
fig_2.update_yaxes(title_text="Temperature (°C)", secondary_y=True)

st.plotly_chart(fig_2, use_container_width=True)

# Insight
if len(daily_f) > 2:
    corr = daily_f["trip_count"].corr(daily_f["avg_temp"])
    st.markdown(
        f"**Insight:** Between {date_range[0]} and {date_range[1]}, the correlation between temperature and rides is **{corr:.2f}**. "
        f"This suggests that warmer days generally see more rides."
    )
else:
    st.caption("Select a wider date range to view trip and temperature trends.")

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
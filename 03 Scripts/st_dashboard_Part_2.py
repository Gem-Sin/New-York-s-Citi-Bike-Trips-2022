# ------------------- CONFIGURE THE PAGE -------------------
import streamlit as st
import pandas as pd
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]  # repo root
DATA_DIR = BASE_DIR / "02 Data"
MAP_DIR = BASE_DIR / "04 Analysis & Visualisations"
KEPLER_PATH = MAP_DIR / "kepler.gl.html"



st.set_page_config(page_title='Citi Bike 2022 Dashboard', layout='wide')


# ######################### IMPORT DATA #########################
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

# Sample for stations + seasons
trips = load_csv(DATA_DIR / "citibike_sample.csv")

# Daily trips vs temperature for dual-axis chart
daily = load_csv(DATA_DIR / "daily_trips_vs_temp_2022.csv")

# Top 20 stations for bar chart
top20 = load_csv(DATA_DIR / "top20_stations.csv")


# Ensure date column is parsed in trips sample
if "date" in trips.columns:
    trips["date"] = pd.to_datetime(trips["date"])
    trips["month"] = trips["date"].dt.month.astype(int)

    trips["season"] = trips["month"].apply(
        lambda m: (
            "winter" if (m == 12 or 1 <= m <= 4)
            else "spring" if (4 < m <= 5)
            else "summer" if (6 <= m <= 9)
            else "fall"
        )
    )

# Ensure the date column is parsed
if "date" in daily.columns:
    daily["date"] = pd.to_datetime(daily["date"])

# =============== SIDEBAR FILTERS ===============
with st.sidebar:

     # Page selection
    page = st.selectbox(
        "Select page",
        (
            "Intro",
            "Trips vs Temperature",
            "Most Popular Stations",
            "Kepler Map",
            "Recommendations",
        )
    )
    st.header("Filters")

    # Top-N slider
    top_n = st.slider("Show top start stations", 5, 20, 20)

    # Season filter (based on trips sample)
    season_filter = st.multiselect(
        "Select season(s)",
        options=sorted(trips["season"].unique()),
        default=sorted(trips["season"].unique())
    )

    # Optional: filter by specific start stations
    station_choices = sorted(trips["start_station_name"].dropna().unique())
    picked_stations = st.multiselect("Filter specific station(s)", station_choices)

    # Date range filter for the daily chart (unchanged)
    min_date = pd.to_datetime(daily["date"]).min().date()
    max_date = pd.to_datetime(daily["date"]).max().date()
    date_range = st.slider(
        "Date range (daily chart)",
        min_value=min_date, max_value=max_date,
        value=(min_date, max_date)
    )


# Apply season and station filters to the trips sample
filtered_trips = trips[trips["season"].isin(season_filter)]

if picked_stations:
    filtered_trips = filtered_trips[
        filtered_trips["start_station_name"].isin(picked_stations)
    ]

# ######################### INTRODUCTION PAGE #########################
if page == "Intro":
    st.title("Citi Bike 2022 Strategy Dashboard")

    st.markdown(
        """
        ### Objective  
        As the lead analyst for New York City's Citi Bike program, my role is to help the  
        business strategy and operations teams understand user behaviour, diagnose  
        distribution issues, and identify opportunities to improve bike availability across  
        the network.

        This dashboard provides a descriptive analysis of 2022 ride data to uncover:  
        - Where demand is highest  
        - How seasonality affects ridership  
        - How weather influences daily trips  
        - How bikes move across the city  
        - Which operational improvements would have the greatest impact  

        The aim is to deliver actionable insights that support Citi Bike’s position as a  
        leader in accessible, eco-friendly transportation.
        """
    )

    st.markdown("---")

    # Insert image
    try:
        st.image(
            "images/citibike_intro.jpg",
            use_column_width=True,
        )
    except:
        pass

    st.markdown(
        """
        ### Context  
        Citi Bike ridership has grown rapidly since 2013, with even higher demand following  
        the Covid-19 pandemic as more residents turned to cycling as a dependable,  
        sustainable transport option.

        This growing demand has exposed key distribution challenges, including:
        - popular stations running out of available bikes  
        - other stations filling up with docked bikes  
        - customers unable to return or find a bike at peak times  

        My task as analyst is to diagnose these issues using data, and provide  
        clear recommendations that the strategy team and operations managers  
        can act on.
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ### Dashboard Structure  
        This dashboard is organised into four main sections:

        1. **Most Popular Stations**  
           Identify the busiest start stations and uncover high-demand clusters.

        2. **Trips vs Temperature**  
           Analyse how weather patterns correlate with daily ridership.

        3. **Trip Flow Map (Kepler.gl)**  
           Explore ride movement across New York City.

        4. **Recommendations**  
           Actionable strategies to reduce shortages, balance the fleet,  
           and improve service reliability.

        Use the sidebar to switch between analysis pages and apply filters  
        such as season, station, and date range.
        """
    )

# ######################### DEFINE THE CHARTS #########################

# ############################## BAR CHART ##################################
if page == "Most Popular Stations":
    st.subheader("Top Start Stations by Trips (sampled 2022 data)")

    if filtered_trips.empty:
        st.warning("No trips for these filters. Try selecting more seasons or stations.")
    else:
        # Group by start_station_name and count trips
        station_counts = (
            filtered_trips
            .groupby("start_station_name")
            .size()
            .reset_index(name="trip_count")
            .sort_values("trip_count", ascending=False)
        )

        # Top N based on the slider
        df_top = station_counts.head(top_n)

        fig = px.bar(
            df_top,
            x="start_station_name",
            y="trip_count",
            labels={
                "start_station_name": "Start Station",
                "trip_count": "Number of Trips"
            },
            title=f"Top {top_n} Start Stations by Trips",
            color="trip_count",
            color_continuous_scale="Viridis"
        )

        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Insight (Top Stations)
        top_row = df_top.iloc[0]

        st.markdown(f"""
        **Insight:** Demand is highly concentrated around a small group of core stations.
        The busiest location—**{top_row['start_station_name']} ({int(top_row['trip_count'])} trips)**—
        consistently outperforms all others, indicating a persistent supply–demand imbalance at this site.

        High-demand stations (e.g., **{top_row['start_station_name']}**, Broadway & W 25 St,
        and West St & Chambers St) likely require:

        - More frequent bike rebalancing  
        - Increased docking capacity  
        - Priority placement of e-bikes or larger bike fleets  

        These stations represent critical “pressure points” where availability issues are most likely to occur.
        """)

# ######################### Line Chart: Trips vs Temperature ###########################
if page == "Trips vs Temperature":
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

    # Insight (Trips vs Temperature)
    if len(daily_f) > 2:
        corr = daily_f["trip_count"].corr(daily_f["avg_temp"])
        st.markdown(
            f"**Insight:** Warmer weather strongly increases bike usage.  \n"
            f"Between **{date_range[0]} and {date_range[1]}**, the correlation between "
            f"daily temperature and trip volume is **{corr:.2f}**, which is a very strong "
            f"positive relationship.  \n\n"
            f"This pattern shows that warmer days drive significantly more rides, especially "
            f"in spring and summer, and should guide **staffing, bike distribution, and "
            f"seasonal promotions**."
        )
    else:
        st.caption("Select a wider date range to view trip and temperature trends.")

# ######################### ADD THE MAP #########################
if page == "Kepler Map":
    st.subheader("Citi Bike Flow Map (Kepler.gl)")

    # Use the map stored in 04 Analysis & Visualisations
    map_path = KEPLER_PATH

    if map_path.exists():
        st.caption(
            f"✅ Loading map: {map_path.name} "
            f"({os.path.getsize(map_path)/1e6:.1f} MB)"
        )
        with open(map_path, "r", encoding="utf-8") as f:
            html_data = f.read()
        components.html(html_data, height=1000, scrolling=True)
    else:
        st.error(
            f"Map file not found — expected at: {map_path}"
        )

# ############### RECOMMENDATIONS PAGE ####################
if page == "Recommendations":
    st.subheader("Recommendations")

    st.markdown(
        """
        Based on the analysis in this dashboard, the following actions are recommended
        for Citi Bike in New York City:

        1. **Prioritise bike availability at the busiest start stations.**
           Stations such as W 21 St & 6 Ave show consistently high demand. Ensure
           regular rebalancing and enough docking capacity at these locations,
           especially during peak seasons.

        2. **Plan operations around seasonal demand.**
           Trip volume increases in warmer months (spring and summer). Increase
           staffing, maintenance capacity, and bike availability ahead of these
           seasons to minimise shortages.

        3. **Leverage weather patterns for forecasting and promotions.**
           The dual-axis chart shows a positive relationship between temperature
           and trips. Use temperature-based forecasts to anticipate demand and
           run targeted promotions on days with warmer weather.

        4. **Target casual riders during peak tourist periods.**
           Casual usage is likely higher in summer and on warm weekends. Consider
           short-term passes, discounts, or partnerships to convert casual riders
           into repeat customers.

        These recommendations should help improve service reliability, customer
        satisfaction, and overall utilisation of the Citi Bike network.
        """
    )



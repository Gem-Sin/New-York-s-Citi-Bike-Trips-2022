# New York Citi Bike Trips – 2022 Analysis

A Python and Streamlit project analysing the New York Citi Bike system (2022) to uncover usage patterns, seasonal trends, and station-level behaviour across New York City. This project forms part of the CareerFoundry Data Analytics Course and demonstrates skills in data cleaning, visualisation, geospatial mapping, dashboard development, and storytelling with data.

---

## Project Summary

This project explores the Citi Bike trips dataset for 2022, combined with local weather data, to understand how New Yorkers use shared bicycles throughout the year.

The analysis focuses on:

- How daily ridership changes across the seasons  
- The relationship between temperature and number of trips  
- Identifying the top 20 busiest stations across the network  
- Mapping station flows using Kepler.gl  
- Building an interactive Streamlit dashboard to present the insights concisely  

The goal is to create clear, actionable insights supported by both visual and geospatial analysis.

---

## Key Questions

- **How does Citi Bike usage vary throughout the year?**  
- **What is the relationship between temperature and trip volume?**  
- **Which stations are the busiest, and how do they compare?**  
- **How do trip start–end flows appear on a geospatial map?**  
- **What patterns can be identified when visualising the data interactively?**

---

## Datasets

The project uses the 2022 Citi Bike trip data provided by Citi Bike NYC, along with 2022 NYC temperature data.

Included datasets (<25MB):

- `citibike_sample.csv` - 5% sample for development  
- `daily_trips_vs_temp_2022.csv` - merged daily trips + temperature  
- `top20_stations.csv` - extracted top 20 busiest stations  

**Note:** Raw full trip data is excluded via `.gitignore` due to GitHub file limits.

---

## Tools & Libraries

### **Python (Exploratory Analysis, Wrangling & Visualisation)**

- **pandas** - cleaning, wrangling, merging  
- **NumPy** - numerical operations  
- **matplotlib / seaborn** - statistical and temporal visualisations  
- **plotly.express & graph_objects** - interactive charts  
- **keplergl** - advanced geospatial mapping  
- **geopandas/json** - spatial integrations  
- **Streamlit** - interactive dashboard development  

### **Other Tools**
- **GitHub** - project organisation  
- **Jupyter Notebook** - EDA and preprocessing  
- **Kepler.gl (web)** - station flow and arc visualisations  

---

## Folder Structure

- 01 Project Management/ - Project brief
- 02 Data/ - Cleaned & sample datasets (<25MB)
- 03 Scripts/ - Jupyter notebooks, Streamlit scripts
- 04 Analysis & Visualisations/ - Charts, maps, HTML exports, PNG versions of visuals

---

## Deliverables

- **Streamlit Dashboard:** 
- **Kepler.gl Geospatial Map:** Included in `/04 Analysis & Visualisations/`  
- **PNG Visualisations:** Located in `/visualisations/`  

---

## How to Use This Repository

1. Open the **02 Data** folder for small datasets used in the notebooks.  
2. Explore the **03 Scripts** folder for each analysis step:  
   - data cleaning  
   - wrangling  
   - visualisation  
   - mapping  
   - dashboard development  
3. View exported charts and maps in **04 Analysis & Visualisations**.  
4. Run the Streamlit dashboard  


---

## Disclaimer

This dataset is used for educational purposes as part of the **CareerFoundry Data Analytics Course**.  

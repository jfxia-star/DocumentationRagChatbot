## **Data Center Analytics Dashboard — Technical Documentation**

### 1. Project Objectives

- Create a dashboard report for U.S. data centers and evaluate how their geospatial layouts align with power grid capacities and environmental risks.
- Demonstrate integration of AI elements for enhanced interactivity, narrative generation, and maintenance.
- Showcase capabilities in data flow design, modeling logic, Python ingestion, and applied AI.
- Serve as a job‑hunting demo; analytical depth is secondary to demonstrating architecture and workflow.

### 2. Project Overview

- A three‑page Power BI dashboard designed to present modern, AI‑augmented analytics practices.
- Integrates Python‑driven narrative generation, multi‑source data ingestion, and a future‑ready architecture supporting automated refresh and AI agents.
- Demonstrates how AI can be embedded into BI workflows and how narrative intelligence can be generated dynamically.
- Currently powered by static snapshots of curated datasets retrieved via Python API calls; architecture is ready for dynamic ingestion once server refresh is available.

### 3. Data Sources

##### 3.1 IM3 — Data Centers & Spatial Infrastructure

- Source: IM3 Open Source Data Center Atlas
- Provides: Coordinates, building footprints, state/county metadata
- Dashboard Value: Establishes map POIs and supports density cluster analysis

##### 3.2 EIA — Electricity Grids & Power Load

- Source: EIA Open Data API & Electricity Data Browser
- Provides: Balancing authority data, net generation, retail prices, grid capacity
- Dashboard Value: Enables overlay of data centers onto grid regions to assess reliability and clean‑energy availability

##### 3.3 NOAA — Ambient Temperature & Cooling Demands

- Source: NOAA Climate Data Online & Climate at a Glance
- Provides: Daily max/min temperatures, air temperature maps, cooling degree days
- Dashboard Value: Supports creation of a Cooling Stress Index affecting PUE

##### 3.4 USDM — Water Availability & Drought Risk

- Source: U.S. Drought Monitor GIS shapefiles
- Provides: Weekly drought classifications (D0–D4)
- Dashboard Value: Flags data centers operating in water‑stressed regions

### 4. Data Connections & Ingestions

Python scripts perform the following standardized ingestion workflow:

##### 4.1 API Retrieval

- Send authenticated API requests
- Retrieve raw JSON responses
- Save raw responses to /data_raw

##### 4.2 Data Processing

- Load JSON/CSV into Pandas DataFrames
- Clean column names
- Enforce numeric and categorical data types
- Drop invalid entries
- Add ingestion timestamps

##### 4.3 Export

- Reduce dataset size for Power BI efficiency
- Save processed CSVs to /data_processed with timestamped filenames

This workflow ensures curated, analytics‑ready data.

### 5. Data Dictionary

##### EIA — Hourly (eia_hourly_YYYYMMDD_HHMM.csv)

- period
- respondent
- respondent-name
- type
- type-name
- value
- value-units

##### EIA — Daily (eia_daily_YYYYMMDD_HHMM.csv)

- Date
- Daily_Demand_MWh
- Daily_Generation_MWh

##### IM3 — Data Centers (im3_datacenters_YYYYMMDD_HHMM.csv)

- id
- state
- state_abb
- state_id
- county
- county_id
- operator
- ref
- name
- sqft
- lon
- lat
- type
- ingested_at

##### NOAA — Daily (noaa_daily_YYYYMMDD_HHMM.csv)

- date
- datatype
- station
- attributes
- value

##### USDM — Drought (usdm_YYYYMMDD_HHMM.geojson)

- GEOJSON polygon features with drought classifications

### 6. Relationship Modeling

##### Dimension Tables

- states_to_grids — Grid_Operator, State
- grid_lookup — Grid_Operator

##### Relationships

- grid_lookup → 1:M → IM3 datacenters
- grid_lookup → 1:M → EIA daily
- grid_lookup → 1:1 → states_to_grids
- states_to_grids → 1:M → IM3 datacenters

##### Additional columns added for modeling:

- EIA & NOAA: state
- IM3: date

### 7. DAX Measures

##### Summary & KPI Measures

- Active_Facilities_Over_Time — cumulative facility count by date
- Total Facilities — total facility count
- High_Risk_Facility_Count — distinct count of high‑risk facilities
- Data_Freshness — latest ingestion timestamp

##### Energy & Capacity Measures

- Estimated_Power_Capacity_MW — sqft × 125 W/sqft → MW
- Peak_Load_MWh — max daily demand
- Lowest_Margin_Operator — selected grid operator or default “PJM”

##### Climate Measures

- Max_Summer_Heat — max daily TMAX

##### Risk & Narrative Measures

- Highest_Risk_State — TOPN(1) by high‑risk facility count
- Indicators_Index — multi‑line indicator legend
- Executive_Summary — dynamic narrative combining multiple measures

### 8. Report Page 1 — Spatial & Facility Overview

##### Purpose: Geographic and operational overview of U.S. data centers.

##### Key Visuals:

- Map — IM3 lat/lon, operator, facility type
- KPI Cards — Active Facilities, Total Footprint, Estimated Power Capacity, Data Ingestion Time
- Bar Charts — facilities by state and operator
- Matrix — grid → state → facility drilldown
- Image — data center exterior

##### Conceptual Layout:

- Top: KPI summary
- Middle Left: Map
- Middle Right: Bar chart + matrix
- Bottom Left: Chart + image

### 9. Report Page 2 — Operational Volatility: Climate & Grid Strain

##### Purpose: Show climate‑driven and grid‑driven operational risk.

##### Key Visuals:

- Charts — Avg TMAX + active facilities (2026)
- Treemap — power capacity by grid operator
- Donut Chart — state by risk level
- KPI Cards — Total Asset Capacity, Avg Max Temperature
- Matrix — daily max temperature by state

##### Conceptual Layout:

- Left: Title → chart → summary
- Middle: Treemap → donut chart
- Right: KPI cards → matrix

### 10. Report Page 3 — Summary, AI, and Maintenance Scores

##### Purpose: Provide AI‑generated narrative, recommendations, and maintenance scoring.

##### Key Visuals:

- Python Visuals — AI narrative + AI recommendations
- Slicer — state‑based dynamic narrative
- KPI Card + Bar Chart — maintenance health scores
- Textbox — explanation of maintenance scoring logic

##### Conceptual Layout:

- Top Left: AI narrative
- Top Right: AI recommendation + slicer
- Bottom Left/Middle: Maintenance KPIs + charts
- Bottom Right: Maintenance scoring explanation
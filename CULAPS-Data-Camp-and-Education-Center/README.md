# 🌿 CULAP Data Camp and Education Center

Welcome to the CULAP Data Camp and Education Center application! This web application helps track and document environmental conditions, wildlife, and natural phenomena across Cook County, Illinois, with a focus on Project Based Learning (PBL) and the BIOS 399 Sodium Trap Project.

## 🚀 Key Research Projects

### 1. 🐿️ The Sodium Trap Project (BIOS 399)
Modeling the "Behavioral Trap" created by urban road salt (NaCl) at Schiller Woods.
- **Giving-Up Density (GUD)**: Measures the point where a squirrel's drive for sodium overrides its fear of predation.
- **River Bend Picnic Area**: Primary experimental site with specific urban stressors (O'Hare noise, Pace bus stops, and traffic).
- **Custom Variables**:
  - `site_type`: Robinson Homestead (Control) vs. River Bend (Experimental).
  - `mask_a` (Acoustic Masking): 1–5 scale accounting for O'Hare flight paths and truck traffic.
  - `vis_score` (Visibility): 1–5 scale based on "Squirrel Eye Level."
  - `dist_to_road`: Proxy for salt concentration.
  - `transit_active`: Boolean for idling Pace buses during observations.

### 2. 🤖 Squirrel AI Model
A dedicated AI behavioral model powered by OpenAI.
- **Prompt Integration**: Uses custom prompt ID `pmpt_697e4...` (Version 6) to model squirrel behavior.
- **Real-time Generation**: Generates behavioral predictions based on site parameters.

### 3. 🗺️ Project Based Learning Maps
Interactive spatial analysis tools for environmental research.
- **Cook County Interactive Map**: Visualizes observation density.
- **Site Coordinates**: River Bend is located at `[41.9515, -87.8430]`.
- **Thematic Layers**: Forest Preserve districts, hydrological mapping, and wildlife corridors.

## 📊 Data Integration & Analysis

### Google Colab Connection
Researchers can pull live data from this app directly into Google Colab for advanced statistical analysis.
- **Endpoint**: `/api/squirrel-data`
- **CORS Support**: Enabled for secure cross-origin data fetching.
- **Analysis Example**:
  ```python
  import pandas as pd
  import requests
  app_url = "YOUR_REPLIT_APP_URL"
  df = pd.DataFrame(requests.get(f"{app_url}/api/squirrel-data").json())
  ```

## 🛠️ Technical Implementation
- **Backend**: Python 3.11 with `http.server`
- **AI Integration**: Replit AI Integrations (OpenAI API)
- **Database**: SQLite tracking multiple environmental categories
- **Assistant**: **Professor CULAPSED** (Google Dialogflow) available on every page for real-time assistance.

---
*Happy exploring and researching! 🌳🐿️📊*

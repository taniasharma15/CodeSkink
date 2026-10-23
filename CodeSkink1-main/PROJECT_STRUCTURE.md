# LifeLine Navigator - Clean Project Structure

## 📁 Root Directory Files

### Core Application Files
- `app.py` - Main Streamlit application entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules

### Configuration Files
- `.streamlit/config.toml` - Streamlit configuration
- `src/config.py` - Application configuration

## 📁 Source Code (`src/`)

### API Layer (`src/api/`)
- `__init__.py` - API module initialization
- `alerts.py` - Alert management API
- `routing.py` - Route calculation API
- `schemas.py` - Data schemas and models
- `services.py` - Core business logic services
- `utils.py` - Utility functions

### UI Layer (`src/ui/`)
- `__init__.py` - UI module initialization
- `styles.py` - CSS styles and themes
- `components.py` - Reusable UI components

#### Pages (`src/ui/pages/`)
- `__init__.py` - Pages module initialization
- `home.py` - Home/dashboard page
- `map_page.py` - Emergency map page
- `family_page.py` - Family tracker page
- `alerts_page.py` - Alerts & accessibility page
- `settings_page.py` - Settings page

### Data Layer (`src/data/`)
- `__init__.py` - Data module initialization
- `loader.py` - Data loading and management

## 📁 Deployment (`deploy/`)
- `Dockerfile` - Container deployment configuration
- `streamlit_config.toml` - Deployment-specific config

## 🚀 How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## ✨ Features Working

- ✅ Navigation between all pages
- ✅ Emergency contact buttons (📞112, 🔥101, 🚑102/108, 👮100)
- ✅ Interactive map (requires folium libraries)
- ✅ Family tracker forms
- ✅ Alert simulation buttons
- ✅ Settings page

## 🔧 Dependencies

- **Streamlit** - Web framework
- **Folium & streamlit-folium** - Interactive maps
- **Pandas & NumPy** - Data manipulation
- **Requests** - HTTP requests
- **Pydantic** - Data validation
- **Geopy** - Geographic calculations
- **NetworkX** - Graph algorithms
- **Haversine** - Distance calculations
- **Pillow** - Image processing
- **Plotly** - Data visualization
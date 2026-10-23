# LifeLine Navigator 🚨

A comprehensive emergency navigation system providing real-time hazard awareness, safe routing, and family coordination during emergencies.

## 🎯 Overview

LifeLine Navigator is an offline-first emergency navigation web application designed to help users navigate safely through hazardous areas, find emergency shelters, and coordinate with family members during crisis situations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-green.svg)
![Framework](https://img.shields.io/badge/framework-Streamlit-red.svg)

## ✨ Key Features

- 🗺️ **Interactive Emergency Map** - Real-time hazard visualization with safe routing
- 🏠 **Smart Shelter Locator** - Find nearby shelters with capacity tracking
- 👨‍👩‍👧‍👦 **Family Tracker** - Coordinate with family during emergencies
- 🚨 **Emergency Alerts** - Broadcast and receive emergency notifications
- 📞 **Quick Actions** - One-tap access to emergency services

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lifeline-navigator.git
cd lifeline-navigator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

## 📁 Project Structure

```
lifeline-navigator/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .streamlit/config.toml      # Streamlit configuration
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contributing guidelines
├── deploy/                     # Deployment files
│   └── docker-compose.yml      # Docker configuration
├── src/                        # Source code
│   ├── api/                    # API layer and business logic
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic data models
│   │   ├── routing.py          # Custom A* routing engine
│   │   ├── services.py         # Service orchestration
│   │   ├── alerts.py           # Alert management
│   │   └── utils.py            # Utility functions
│   ├── data/                   # Data management layer
│   │   ├── __init__.py
│   │   ├── loader.py           # Data loading and caching
│   │   └── shelters.csv        # Shelter data
│   │   └── hazards.csv         # Hazard data
│   └── ui/                     # User interface components
│       ├── __init__.py
│       ├── pages/              # Application pages
│       │   ├── __init__.py
│       │   ├── home.py          # Home page
│       │   ├── map_page.py     # Emergency map page
│       │   ├── family_page.py  # Family tracker page
│       │   ├── alerts_page.py  # Alerts page
│       │   └── settings_page.py # Settings page
│       ├── components.py       # Reusable UI components
│       ├── styles.py           # Styling and CSS
│       └── forms.py            # Form components
├── config/                     # Configuration files
│   ├── config.py              # Application configuration
│   └── __init__.py
└── docs/                       # Additional documentation
    ├── API.md                  # API documentation
    ├── DEPLOYMENT.md           # Deployment guide
    └── CONTRIBUTING.md         # Contributing guidelines
```

## 🔧 Architecture

### Frontend Stack
- **Streamlit** - Python web framework for rapid UI development
- **Folium** - Interactive map visualization
- **Plotly** - Advanced data visualization
- **Pydantic** - Data validation and type safety

### Backend Stack
- **Custom A* Routing Engine** - Multi-hazard pathfinding algorithm
- **Pandas/NumPy** - Data processing and grid creation
- **Geopy/Haversine** - Geospatial calculations
- **Offline-first design** - No external API dependencies

### Key Components

1. **Routing Engine**
   - Custom A* implementation with hazard awareness
   - 8-directional movement for optimal paths
   - Dynamic hazard weighting and penalties
   - Emergency fallback routing

2. **Data Management**
   - CSV-based data storage for shelters and hazards
   - Grid preprocessing for fast routing
   - Caching system for performance
   - Configurable hazard weights

3. **Family Coordination**
   - Real-time location sharing
   - Geometric median meetup point calculation
   - Group-based alert broadcasting
   - Member status tracking

## 🗺️ Usage

### Emergency Map
- View real-time hazards with color-coded zones
- Calculate safe routes avoiding hazards
- Update your location and mark debris
- View shelters and their capacity

### Family Tracker
- Create emergency family groups with unique codes
- Share real-time locations with family members
- Calculate optimal meetup points
- Monitor family member status

### Alerts
- Send emergency alerts to family groups
- Receive location-based notifications
- View alert history and manage alerts
- Test alert functionality

### Quick Actions
- One-tap emergency service contacts
- Emergency siren activation
- Debris reporting
- Location updates

## 🎮 Configuration

### Hazard Weights
Configure hazard avoidance priorities in `src/config.py`:

```python
HAZARD_WEIGHTS = {
    "flood": 10.0,       # Deep water - impassable
    "fire": 8.0,         # Active fire perimeter
    "debris": 5.0,       # Building collapse
    "crowd": 3.0,        # Protest, stampede risk
    "traffic": 2.0,      # Normal congestion
    "landslide": 9.0,    # Mountain areas
    "chemical": 10.0,    # Industrial hazard
    "structural": 7.0,   # Damaged buildings
}
```

### Map Configuration
Adjust city bounds and map settings:

```python
# City bounds for Amritsar
AMRITSAR_BOUNDS = {
    "min_lat": 31.55,
    "min_lon": 74.70,
    "max_lat": 31.75,
    "max_lon": 74.95,
}
```

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Docker Deployment
```bash
# Build the image
docker build -t lifeline-navigator .

# Run the container
docker run -p 8501:8501 lifeline-navigator
```

### Streamlit Cloud
1. Push your code to GitHub
2. Deploy to Streamlit Cloud
3. Connect your GitHub repository

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📋 Data Requirements

### Shelters Data Format
```csv
id,name,type,latitude,longitude,capacity,contact_person,contact_phone,address,facilities
shelter_1,Guru Nanak Dev University,college,31.6340,74.8723,5000,Dr. Singh,9876543210,GNDU Campus,"Medical,Food,Water"
```

### Hazards Data Format
```csv
id,type,latitude,longitude,radius_m,severity,reported_at,reported_by,description
hazard_1,flood,31.6300,74.8700,1000,high,2024-01-01T10:00:00,user1,Flooding in low-lying areas
```

## 🔐 Security

- All data processing happens locally
- No external API dependencies for core functionality
- Input validation using Pydantic
- Session state management for user data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit community for the amazing framework
- Folium team for interactive mapping
- OpenStreetMap contributors for map data
- Emergency response professionals for domain guidance

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in `docs/`
- Review API documentation in `docs/API.md`

---

Built with ❤️ for emergency preparedness and response.
# 🇮🇳 SkyCast India — AI Weather Intelligence

A **stunning, creative weather prediction web app** built with **Streamlit** & **Python**, featuring **40+ Indian cities**, real-time weather data, air quality index, city comparison, AI-powered forecasts, and beautiful interactive charts — all wrapped in a mesmerizing glassmorphism UI.

![SkyCast India](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Open-Meteo](https://img.shields.io/badge/Open--Meteo-API-blue?style=for-the-badge)

---

## ✨ What's New (v2.0)

| Feature | Description |
|---------|-------------|
| 🇮🇳 **40+ Indian Cities** | Pre-loaded database with Delhi, Mumbai, Bangalore, Chennai, Kolkata, and 35+ more |
| 🏙️ **Quick City Chips** | One-click city selector with emoji icons |
| 🔀 **City Comparison Mode** | Compare weather between any two Indian cities side-by-side |
| 🌬️ **Air Quality Index (AQI)** | Real-time AQI with PM2.5, PM10, NO₂, CO, O₃ breakdown |
| ☀️ **UV Index & Advice** | UV levels with safety recommendations |
| ⏰ **24-Hour Temperature Chart** | Hourly forecast with gradient fill |
| 🗺️ **All Cities Overview** | Horizontal bar chart comparing temps across all major cities |
| 🔮 **Enhanced AI Predictions** | Trend analysis with confidence bars for next 3 days |
| 🎨 **Upgraded UI** | Floating animations, shimmer effects, rotating sun, glassmorphism 2.0 |

---

## 🚀 Quick Deploy

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "🇮🇳 SkyCast India v2.0"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/skycast-india.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select: `YOUR_USERNAME/skycast-india`
5. Set **Main file path**: `app.py`
6. Click **Deploy!** 🚀

Your app will be live at: `https://skycast-india-xxx.streamlit.app`

---

## 📁 Project Structure

```
skycast-india/
├── app.py                  # Main Streamlit app (631 lines)
├── requirements.txt        # Dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── deploy.sh              # Linux/Mac deploy script
├── deploy.bat             # Windows deploy script
└── .streamlit/
    └── config.toml        # Dark theme config
```

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit + Custom CSS (Glassmorphism 2.0)
- **Charts**: Plotly Express & Graph Objects
- **Data**: Pandas
- **APIs**: Open-Meteo (Weather + Air Quality) — Free, no key needed
- **Fonts**: Outfit + Space Grotesk (Google Fonts)
- **Animations**: CSS Keyframes (float, shimmer, rotate, pulse, slide-in)

---

## 🎨 UI Features

- **Deep space gradient** background with particle feel
- **Glassmorphism cards** with `backdrop-filter: blur(30px)`
- **Shimmering temperature** display with animated gradient
- **Floating cards** with gentle hover lift effects
- **Rotating India flag** emoji in header
- **Smooth slide-in & scale-in** animations
- **Dark-themed Plotly charts** with custom color scales
- **Responsive grid** adapting to all screen sizes

---

## 🏙️ Included Indian Cities

**North**: Delhi, Jaipur, Lucknow, Kanpur, Agra, Varanasi, Allahabad, Meerut, Ghaziabad, Faridabad, Chandigarh, Amritsar, Ludhiana, Shimla, Dehradun, Srinagar

**West**: Mumbai, Pune, Ahmedabad, Vadodara, Rajkot, Nashik, Nagpur, Indore, Bhopal, Jodhpur, Goa

**South**: Bangalore, Chennai, Hyderabad, Kochi, Coimbatore, Madurai, Mangalore, Mysore, Thiruvananthapuram, Visakhapatnam

**East**: Kolkata, Patna, Ranchi, Bhubaneswar, Guwahati

---

## 🔮 How AI Predictions Work

The prediction engine analyzes:
1. **Temperature trend slope** from 7-day forecast
2. **Precipitation probability trends**
3. **Extrapolates** next 3 days with confidence scoring
4. Shows **warming ↗️ / cooling ↘️ / stable ➡️** indicators

> **Note**: Simplified trend-based model. For production ML, integrate TensorFlow with historical data.

---

## 📝 Customization Ideas

| Upgrade | How |
|---------|-----|
| Add more cities | Extend `INDIAN_CITIES` dictionary |
| Weather alerts | Integrate IMD API for India-specific warnings |
| Rain radar | Add `folium` with precipitation layers |
| Historical data | Cache data in SQLite for trend analysis |
| Push notifications | Use Streamlit's `st.toast()` for alerts |
| Dark/Light mode | Toggle theme with session state |
| Voice search | Integrate `speech_recognition` |
| Weather maps | Add `pydeck` for 3D weather visualization |

---

## 📄 License

MIT License — free to use, modify, and deploy!

---

## 🙌 Credits

- Weather & AQI data: [Open-Meteo API](https://open-meteo.com/)
- Built with: [Streamlit](https://streamlit.io/)
- Fonts: [Google Fonts](https://fonts.google.com/)

---

<div align="center">
  <h3>⭐ Star this repo if you found it helpful!</h3>
  <p>Made with 🇮🇳 and Python</p>
</div>

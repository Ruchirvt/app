import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SkyCast India | AI Weather Intelligence",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== INDIAN CITIES DATABASE ====================
INDIAN_CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi", "icon": "🏛️"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "state": "Maharashtra", "icon": "🌊"},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946, "state": "Karnataka", "icon": "🌳"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "state": "Tamil Nadu", "icon": "🏖️"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "state": "West Bengal", "icon": "🎭"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "state": "Telangana", "icon": "🏰"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "state": "Maharashtra", "icon": "📚"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "state": "Gujarat", "icon": "🦁"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "state": "Rajasthan", "icon": "🏰"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "state": "Uttar Pradesh", "icon": "🍢"},
    "Kanpur": {"lat": 26.4499, "lon": 80.3319, "state": "Uttar Pradesh", "icon": "🏭"},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882, "state": "Maharashtra", "icon": "🍊"},
    "Indore": {"lat": 22.7196, "lon": 75.8577, "state": "Madhya Pradesh", "icon": "🍽️"},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126, "state": "Madhya Pradesh", "icon": "🏞️"},
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185, "state": "Andhra Pradesh", "icon": "⚓"},
    "Patna": {"lat": 25.5941, "lon": 85.1376, "state": "Bihar", "icon": "📜"},
    "Vadodara": {"lat": 22.3072, "lon": 73.1812, "state": "Gujarat", "icon": "🎨"},
    "Agra": {"lat": 27.1767, "lon": 78.0081, "state": "Uttar Pradesh", "icon": "🕌"},
    "Nashik": {"lat": 19.9975, "lon": 73.7898, "state": "Maharashtra", "icon": "🍇"},
    "Rajkot": {"lat": 22.3039, "lon": 70.8022, "state": "Gujarat", "icon": "🥭"},
    "Varanasi": {"lat": 25.3176, "lon": 82.9739, "state": "Uttar Pradesh", "icon": "🕉️"},
    "Srinagar": {"lat": 34.0837, "lon": 74.7973, "state": "Jammu & Kashmir", "icon": "🏔️"},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "state": "Punjab", "icon": "🙏"},
    "Jodhpur": {"lat": 26.2389, "lon": 73.0243, "state": "Rajasthan", "icon": "🔵"},
    "Madurai": {"lat": 9.9252, "lon": 78.1198, "state": "Tamil Nadu", "icon": "🛕"},
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "state": "Tamil Nadu", "icon": "🧵"},
    "Kochi": {"lat": 9.9312, "lon": 76.2673, "state": "Kerala", "icon": "🚢"},
    "Guwahati": {"lat": 26.1445, "lon": 91.7362, "state": "Assam", "icon": "🦏"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "state": "Chandigarh", "icon": "🏛️"},
    "Mysore": {"lat": 12.2958, "lon": 76.6394, "state": "Karnataka", "icon": "👑"},
    "Shimla": {"lat": 31.1048, "lon": 77.1734, "state": "Himachal Pradesh", "icon": "🌲"},
    "Dehradun": {"lat": 30.3165, "lon": 78.0322, "state": "Uttarakhand", "icon": "🏔️"},
    "Ranchi": {"lat": 23.3441, "lon": 85.3096, "state": "Jharkhand", "icon": "🏏"},
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245, "state": "Odisha", "icon": "🏛️"},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366, "state": "Kerala", "icon": "🌴"},
    "Goa": {"lat": 15.2993, "lon": 74.1240, "state": "Goa", "icon": "🏖️"},
}

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    * { font-family: 'Outfit', 'Space Grotesk', sans-serif; }
    .main { background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 30%, #16213e 60%, #0f3460 100%); min-height: 100vh; }

    @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
    @keyframes float2 { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
    @keyframes shimmer { 0%{background-position:-200% center} 100%{background-position:200% center} }
    @keyframes slideIn { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
    @keyframes scaleIn { from{opacity:0;transform:scale(0.9)} to{opacity:1;transform:scale(1)} }
    @keyframes rotateSun { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
    @keyframes pulseGlow { 0%,100%{box-shadow:0 0 20px rgba(102,126,234,0.3)} 50%{box-shadow:0 0 50px rgba(102,126,234,0.6)} }

    .floating { animation: float 6s ease-in-out infinite }
    .floating2 { animation: float2 7s ease-in-out infinite 1s }
    .sun-spin { animation: rotateSun 25s linear infinite; display:inline-block }
    .slide-in { animation: slideIn 0.6s ease-out forwards }
    .scale-in { animation: scaleIn 0.5s ease-out forwards }

    .glass {
        background: rgba(255,255,255,0.03);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
    }
    .glass:hover { transform: translateY(-8px) scale(1.01); box-shadow: 0 25px 60px rgba(0,0,0,0.4), 0 0 40px rgba(102,126,234,0.15); border-color: rgba(255,255,255,0.15); }

    .glass-strong {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .temp-hero {
        font-size: 7rem; font-weight: 900;
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 25%, #a8edea 50%, #fed6e3 75%, #d299c2 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        line-height: 1; animation: shimmer 4s ease-in-out infinite;
    }
    .city-hero { font-size: 3rem; font-weight: 700; color: white; letter-spacing: -1px; }
    .state-badge { display:inline-block; background: linear-gradient(135deg, rgba(255,154,158,0.2), rgba(250,208,196,0.2)); border: 1px solid rgba(255,255,255,0.15); color: rgba(255,255,255,0.9); padding: 0.4rem 1.2rem; border-radius: 50px; font-size: 0.9rem; font-weight: 500; margin-top: 0.5rem; }
    .weather-status { font-size: 1.4rem; color: rgba(255,255,255,0.7); font-weight: 400; margin-top: 0.5rem; }

    .metric-box { background: rgba(255,255,255,0.02); border-radius: 20px; padding: 1.5rem 1rem; text-align: center; border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease; }
    .metric-box:hover { background: rgba(255,255,255,0.06); transform: scale(1.05); }
    .metric-icon { font-size: 2.5rem; margin-bottom: 0.8rem; display: block; }
    .metric-val { font-size: 1.6rem; font-weight: 700; color: white; font-family: 'Space Grotesk', sans-serif; }
    .metric-label { font-size: 0.8rem; color: rgba(255,255,255,0.45); margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 1px; }

    .forecast-box { background: rgba(255,255,255,0.02); border-radius: 24px; padding: 1.5rem 1rem; text-align: center; border: 1px solid rgba(255,255,255,0.05); transition: all 0.4s cubic-bezier(0.4,0,0.2,1); cursor: pointer; }
    .forecast-box:hover { background: rgba(255,255,255,0.08); transform: translateY(-5px) scale(1.03); box-shadow: 0 15px 40px rgba(0,0,0,0.3); border-color: rgba(255,255,255,0.15); }
    .forecast-day { font-size: 1rem; font-weight: 600; color: rgba(255,255,255,0.85); }
    .forecast-date { font-size: 0.75rem; color: rgba(255,255,255,0.4); margin-bottom: 0.5rem; }
    .forecast-emoji { font-size: 3rem; margin: 0.5rem 0; display: block; }
    .forecast-high { font-size: 1.4rem; font-weight: 700; color: white; }
    .forecast-low { font-size: 0.95rem; color: rgba(255,255,255,0.5); }
    .forecast-rain { font-size: 0.8rem; color: #6dd5ed; margin-top: 0.3rem; font-weight: 500; }

    .aqi-good { background: rgba(56,239,125,0.15); color: #38ef7d; border: 1px solid rgba(56,239,125,0.3); }
    .aqi-mod { background: rgba(255,217,155,0.15); color: #ffd89b; border: 1px solid rgba(255,217,155,0.3); }
    .aqi-sensitive { background: rgba(255,154,100,0.15); color: #ff9a64; border: 1px solid rgba(255,154,100,0.3); }
    .aqi-bad { background: rgba(245,87,108,0.15); color: #f5576c; border: 1px solid rgba(245,87,108,0.3); }
    .aqi-very { background: rgba(180,100,200,0.15); color: #b464c8; border: 1px solid rgba(180,100,200,0.3); }
    .aqi-haz { background: rgba(139,0,0,0.2); color: #ff6b6b; border: 1px solid rgba(139,0,0,0.4); }
    .aqi-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1.2rem; border-radius: 50px; font-weight: 600; font-size: 0.9rem; }

    .section-title { font-size: 1.6rem; font-weight: 700; color: white; margin: 2.5rem 0 1.2rem 0; display: flex; align-items: center; gap: 0.6rem; letter-spacing: -0.5px; }
    .section-sub { font-size: 0.9rem; color: rgba(255,255,255,0.45); margin-bottom: 1.5rem; margin-top: -0.5rem; }
    .divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin: 2rem 0; }

    .pred-card { background: rgba(255,255,255,0.02); border-radius: 20px; padding: 1.2rem; border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease; }
    .pred-card:hover { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.12); }

    .chart-box { background: rgba(255,255,255,0.02); border-radius: 28px; padding: 1.5rem; border: 1px solid rgba(255,255,255,0.05); }

    .city-chip { display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 50px; padding: 0.5rem 1rem; color: rgba(255,255,255,0.7); font-size: 0.9rem; cursor: pointer; transition: all 0.3s ease; margin: 0.25rem; }
    .city-chip:hover { background: rgba(102,126,234,0.2); border-color: rgba(102,126,234,0.4); color: white; transform: translateY(-2px); }

    .stTextInput > div > div > input { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 20px !important; color: white !important; font-size: 1.1rem !important; padding: 1rem 1.5rem !important; font-family: 'Outfit', sans-serif !important; }
    .stTextInput > div > div > input:focus { border-color: rgba(102,126,234,0.5) !important; box-shadow: 0 0 20px rgba(102,126,234,0.2) !important; }
    .stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.35) !important; }

    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important; background-size: 200% 200% !important; border: none !important; border-radius: 20px !important; color: white !important; font-weight: 600 !important; padding: 0.9rem 2.5rem !important; font-size: 1.1rem !important; transition: all 0.4s ease !important; font-family: 'Outfit', sans-serif !important; letter-spacing: 0.5px; }
    .stButton > button:hover { background-position: 100% 0 !important; transform: translateY(-3px) !important; box-shadow: 0 15px 40px rgba(102,126,234,0.4) !important; }

    .stSelectbox > div > div { background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 16px !important; color: white !important; }

    .footer { text-align: center; padding: 3rem 0 1rem 0; color: rgba(255,255,255,0.25); font-size: 0.85rem; }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
</style>
""", unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================
def get_emoji(code, is_day=1):
    day = {0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',51:'🌦️',53:'🌦️',55:'🌧️',56:'🌧️',57:'🌧️',
           61:'🌧️',63:'🌧️',65:'🌧️',66:'🌧️',67:'🌧️',71:'🌨️',73:'🌨️',75:'❄️',77:'❄️',
           80:'🌧️',81:'🌧️',82:'⛈️',85:'🌨️',86:'❄️',95:'⛈️',96:'⛈️',99:'🌪️'}
    night = {0:'🌙',1:'🌙',2:'☁️',3:'☁️',45:'🌫️',48:'🌫️',51:'🌧️',53:'🌧️',55:'🌧️',56:'🌧️',57:'🌧️',
             61:'🌧️',63:'🌧️',65:'🌧️',66:'🌧️',67:'🌧️',71:'🌨️',73:'🌨️',75:'❄️',77:'❄️',
             80:'🌧️',81:'🌧️',82:'⛈️',85:'🌨️',86:'❄️',95:'⛈️',96:'⛈️',99:'🌪️'}
    return day.get(code, '☀️') if is_day else night.get(code, '🌙')

def get_desc(code):
    d = {0:'Clear Sky',1:'Mainly Clear',2:'Partly Cloudy',3:'Overcast',45:'Foggy',48:'Rime Fog',
         51:'Light Drizzle',53:'Moderate Drizzle',55:'Dense Drizzle',56:'Freezing Drizzle',57:'Freezing Drizzle',
         61:'Slight Rain',63:'Moderate Rain',65:'Heavy Rain',66:'Freezing Rain',67:'Heavy Freezing Rain',
         71:'Slight Snow',73:'Moderate Snow',75:'Heavy Snow',77:'Snow Grains',
         80:'Slight Showers',81:'Moderate Showers',82:'Violent Showers',
         85:'Slight Snow Showers',86:'Heavy Snow Showers',
         95:'Thunderstorm',96:'Thunderstorm with Hail',99:'Thunderstorm with Heavy Hail'}
    return d.get(code, 'Clear Sky')

def get_aqi_info(val):
    if val <= 50: return "Good", "aqi-good", "😊"
    elif val <= 100: return "Moderate", "aqi-mod", "😐"
    elif val <= 150: return "Unhealthy for Sensitive", "aqi-sensitive", "😷"
    elif val <= 200: return "Unhealthy", "aqi-bad", "🤢"
    elif val <= 300: return "Very Unhealthy", "aqi-very", "😵"
    else: return "Hazardous", "aqi-haz", "☠️"

def get_uv_advice(uv):
    if uv <= 2: return "Low", "#38ef7d", "Safe"
    elif uv <= 5: return "Moderate", "#ffd89b", "Use Sunscreen"
    elif uv <= 7: return "High", "#ff9a64", "Seek Shade"
    elif uv <= 10: return "Very High", "#f5576c", "Avoid Sun"
    else: return "Extreme", "#b464c8", "Stay Inside"

@st.cache_data(ttl=600)
def get_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,wind_speed_10m,surface_pressure,visibility,uv_index&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max,precipitation_sum&hourly=temperature_2m,weather_code,precipitation_probability&timezone=auto&forecast_days=8"
        r = requests.get(url, timeout=15)
        return r.json(), None
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=600)
def get_aqi(lat, lon):
    try:
        url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone&timezone=auto"
        r = requests.get(url, timeout=15)
        return r.json(), None
    except Exception as e:
        return None, str(e)

def predict(daily):
    mx, mn = daily['temperature_2m_max'], daily['temperature_2m_min']
    pr = daily.get('precipitation_probability_max', [0]*8)
    tm = (mx[-1]-mx[0])/len(mx) if len(mx)>=3 else 0
    tn = (mn[-1]-mn[0])/len(mn) if len(mn)>=3 else 0
    tp = (pr[-1]-pr[0])/len(pr) if pr else 0
    preds = []
    for i in range(1,4):
        preds.append({
            'day': (datetime.now()+timedelta(days=7+i)).strftime('%a'),
            'date': (datetime.now()+timedelta(days=7+i)).strftime('%b %d'),
            'max': round(mx[-1]+tm*i, 1), 'min': round(mn[-1]+tn*i, 1),
            'rain': max(0, min(100, round(pr[-1]+tp*i))) if pr else 0,
            'trend': 'warming' if tm>0.5 else 'cooling' if tm<-0.5 else 'stable',
            'conf': max(50, 95-abs(tm)*10)
        })
    return preds

# ==================== SESSION STATE ====================
if 'city' not in st.session_state:
    st.session_state.city = "Delhi"
if 'compare' not in st.session_state:
    st.session_state.compare = False
if 'comp_city' not in st.session_state:
    st.session_state.comp_city = "Mumbai"

# ==================== HEADER ====================
st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 0.5rem 0;">
        <div style="font-size:4rem; margin-bottom:0.3rem;" class="sun-spin">🇮🇳</div>
        <h1 style="font-size:3.2rem; font-weight:900; color:white; margin-bottom:0.3rem; letter-spacing:-2px;">
            SkyCast <span style="background:linear-gradient(135deg,#ff9a9e,#fecfef,#a8edea); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">India</span>
        </h1>
        <p style="font-size:1.1rem; color:rgba(255,255,255,0.5); font-weight:300; letter-spacing:2px; text-transform:uppercase;">
            AI-Powered Weather Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)

# ==================== CITY SELECTION ====================
c1, c2, c3 = st.columns([2, 3, 2])
with c2:
    sel = st.selectbox("", options=list(INDIAN_CITIES.keys()),
                       index=list(INDIAN_CITIES.keys()).index(st.session_state.city),
                       key="sel_city", placeholder="🔍 Search Indian cities...")
    if sel != st.session_state.city:
        st.session_state.city = sel
        st.rerun()

# Quick chips
st.markdown("<div style='text-align:center; margin:0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)
chips = ["Delhi","Mumbai","Bangalore","Chennai","Kolkata","Hyderabad","Pune","Jaipur"]
chip_cols = st.columns(8)
for i, cn in enumerate(chips):
    with chip_cols[i]:
        if st.button(f"{INDIAN_CITIES[cn]['icon']} {cn}", key=f"chip_{cn}", use_container_width=True):
            st.session_state.city = cn
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Compare toggle
c_comp1, c_comp2, c_comp3 = st.columns([3, 2, 3])
with c_comp2:
    comp_tog = st.toggle("🔀 Compare Cities", value=st.session_state.compare)
    if comp_tog != st.session_state.compare:
        st.session_state.compare = comp_tog
        st.rerun()

# ==================== FETCH DATA ====================
info = INDIAN_CITIES[st.session_state.city]
wd, we = get_weather(info['lat'], info['lon'])
ad, ae = get_aqi(info['lat'], info['lon'])

if we or not wd:
    st.error(f"❌ Error: {we or 'No data'}")
    st.stop()

cur = wd['current']
daily = wd['daily']
hourly = wd['hourly']

code = cur.get('weather_code', 0)
is_day = cur.get('is_day', 1)
emoji = get_emoji(code, is_day)
desc = get_desc(code)

# ==================== MAIN WEATHER ====================
st.markdown("<div class='slide-in'>", unsafe_allow_html=True)
cm1, cm2 = st.columns([1.2, 1])

with cm1:
    aqi_val = 0
    aqi_lbl, aqi_cls, aqi_emo = "Unknown", "aqi-good", "😐"
    if ad and 'current' in ad:
        aqi_val = ad['current'].get('us_aqi', 0)
        aqi_lbl, aqi_cls, aqi_emo = get_aqi_info(aqi_val)

    uv_idx = cur.get('uv_index', 0)
    uv_lbl, uv_col, uv_adv = get_uv_advice(uv_idx)

    st.markdown(f"""
        <div class="glass-strong floating">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem;">
                <div>
                    <div class="city-hero">{st.session_state.city}</div>
                    <div class="state-badge">{info['icon']} {info['state']}, India</div>
                </div>
                <div class="aqi-badge {aqi_cls}">{aqi_emo} AQI {aqi_val} — {aqi_lbl}</div>
            </div>
            <div style="display:flex; align-items:center; gap:1.5rem; margin:1.5rem 0;">
                <div style="font-size:5.5rem; line-height:1;">{emoji}</div>
                <div>
                    <div class="temp-hero">{round(cur['temperature_2m'])}°</div>
                    <div class="weather-status">{desc}</div>
                </div>
            </div>
            <div style="display:flex; gap:1rem; flex-wrap:wrap;">
                <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:0.6rem 1rem; border:1px solid rgba(255,255,255,0.06);">
                    <span style="color:rgba(255,255,255,0.5); font-size:0.8rem;">Feels Like</span>
                    <div style="color:white; font-weight:600; font-size:1.1rem;">{round(cur['apparent_temperature'])}°C</div>
                </div>
                <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:0.6rem 1rem; border:1px solid rgba(255,255,255,0.06);">
                    <span style="color:rgba(255,255,255,0.5); font-size:0.8rem;">UV Index</span>
                    <div style="color:{uv_col}; font-weight:600; font-size:1.1rem;">{uv_idx} — {uv_lbl}</div>
                </div>
                <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:0.6rem 1rem; border:1px solid rgba(255,255,255,0.06);">
                    <span style="color:rgba(255,255,255,0.5); font-size:0.8rem;">Visibility</span>
                    <div style="color:white; font-weight:600; font-size:1.1rem;">{cur.get('visibility',0)/1000:.1f} km</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with cm2:
    st.markdown("<div class='glass-strong'>", unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)

    sr = daily['sunrise'][0].split('T')[1] if daily['sunrise'] else "06:00"
    ss = daily['sunset'][0].split('T')[1] if daily['sunset'] else "18:00"
    dn = "☀️ Daytime" if is_day else "🌙 Nighttime"

    with mc1:
        st.markdown(f'<div class="metric-box"><span class="metric-icon">💧</span><div class="metric-val">{cur["relative_humidity_2m"]}%</div><div class="metric-label">Humidity</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box" style="margin-top:0.8rem;"><span class="metric-icon">💨</span><div class="metric-val">{cur["wind_speed_10m"]} <span style="font-size:0.9rem;color:rgba(255,255,255,0.5)">km/h</span></div><div class="metric-label">Wind</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box" style="margin-top:0.8rem;"><span class="metric-icon">📊</span><div class="metric-val">{cur["surface_pressure"]} <span style="font-size:0.9rem;color:rgba(255,255,255,0.5)">hPa</span></div><div class="metric-label">Pressure</div></div>', unsafe_allow_html=True)

    with mc2:
        st.markdown(f'<div class="metric-box"><span class="metric-icon">🌅</span><div class="metric-val">{sr}</div><div class="metric-label">Sunrise</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box" style="margin-top:0.8rem;"><span class="metric-icon">🌇</span><div class="metric-val">{ss}</div><div class="metric-label">Sunset</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box" style="margin-top:0.8rem;"><span class="metric-icon">{"☀️" if is_day else "🌙"}</span><div class="metric-val">{dn}</div><div class="metric-label">Phase</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================== COMPARE MODE ====================
if st.session_state.compare:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔀 City Comparison</div>", unsafe_allow_html=True)

    ccs, _ = st.columns([2, 3])
    with ccs:
        comp_city = st.selectbox("Compare with:", options=[c for c in INDIAN_CITIES if c != st.session_state.city],
                                 index=0, key="comp_sel")

    ci = INDIAN_CITIES[comp_city]
    cwd, _ = get_weather(ci['lat'], ci['lon'])

    if cwd:
        cc = cwd['current']
        cd = cwd['daily']
        cc1, cc2 = st.columns(2)

        with cc1:
            st.markdown(f"""
                <div class="glass" style="border-left:4px solid #667eea;">
                    <h3 style="color:white;margin-bottom:1rem;">{info['icon']} {st.session_state.city}</h3>
                    <div style="font-size:3rem;font-weight:800;color:white;">{round(cur['temperature_2m'])}°C</div>
                    <div style="color:rgba(255,255,255,0.6);margin:0.5rem 0;">{desc}</div>
                    <div style="display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap;">
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">💧 {cur['relative_humidity_2m']}%</span>
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">💨 {cur['wind_speed_10m']} km/h</span>
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">🌡️ {round(cur['apparent_temperature'])}°</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with cc2:
            cdesc = get_desc(cc.get('weather_code',0))
            st.markdown(f"""
                <div class="glass" style="border-left:4px solid #f5576c;">
                    <h3 style="color:white;margin-bottom:1rem;">{ci['icon']} {comp_city}</h3>
                    <div style="font-size:3rem;font-weight:800;color:white;">{round(cc['temperature_2m'])}°C</div>
                    <div style="color:rgba(255,255,255,0.6);margin:0.5rem 0;">{cdesc}</div>
                    <div style="display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap;">
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">💧 {cc['relative_humidity_2m']}%</span>
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">💨 {cc['wind_speed_10m']} km/h</span>
                        <span style="background:rgba(255,255,255,0.05);padding:0.3rem 0.8rem;border-radius:10px;font-size:0.85rem;color:rgba(255,255,255,0.7);">🌡️ {round(cc['apparent_temperature'])}°</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Comparison chart
        cdf = pd.DataFrame({
            'Day': [datetime.strptime(d,'%Y-%m-%d').strftime('%a') for d in daily['time'][:7]],
            st.session_state.city: daily['temperature_2m_max'][:7],
            comp_city: cd['temperature_2m_max'][:7]
        })
        fcomp = go.Figure()
        fcomp.add_trace(go.Scatter(x=cdf['Day'], y=cdf[st.session_state.city], mode='lines+markers', name=st.session_state.city, line=dict(color='#667eea', width=3), marker=dict(size=8)))
        fcomp.add_trace(go.Scatter(x=cdf['Day'], y=cdf[comp_city], mode='lines+markers', name=comp_city, line=dict(color='#f5576c', width=3), marker=dict(size=8)))
        fcomp.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Outfit'), height=350,
                           legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), margin=dict(l=20,r=20,t=60,b=20),
                           xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='°C'))
        st.plotly_chart(fcomp, use_container_width=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ==================== 7-DAY FORECAST ====================
st.markdown("<div class='section-title'>📅 7-Day Forecast</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Daily weather outlook with precipitation probability</div>", unsafe_allow_html=True)

fc = st.columns(7)
for i in range(7):
    dd = daily['time'][i]
    dn = datetime.strptime(dd, '%Y-%m-%d').strftime('%a')
    ds = datetime.strptime(dd, '%Y-%m-%d').strftime('%b %d')
    mx = daily['temperature_2m_max'][i]
    mn = daily['temperature_2m_min'][i]
    wc = daily['weather_code'][i]
    ic = get_emoji(wc, 1)
    pp = daily['precipitation_probability_max'][i]
    ps = daily.get('precipitation_sum', [0]*8)[i]

    with fc[i]:
        extra = f'<div style="font-size:0.7rem;color:rgba(109,213,237,0.6);margin-top:0.2rem;">{ps}mm</div>' if ps > 0 else ''
        st.markdown(f"""
            <div class="forecast-box scale-in" style="animation-delay:{i*0.1}s;">
                <div class="forecast-day">{dn}</div>
                <div class="forecast-date">{ds}</div>
                <span class="forecast-emoji">{ic}</span>
                <div class="forecast-high">{round(mx)}°</div>
                <div class="forecast-low">{round(mn)}°</div>
                <div class="forecast-rain">💧 {pp}%</div>
                {extra}
            </div>
        """, unsafe_allow_html=True)

# ==================== HOURLY CHART ====================
st.markdown("<div class='section-title'>⏰ 24-Hour Temperature</div>", unsafe_allow_html=True)
ht = hourly['time'][:24]
h_temp = hourly['temperature_2m'][:24]
hr = [datetime.strptime(t, '%Y-%m-%dT%H:%M').strftime('%H:%M') for t in ht]

fh = go.Figure()
fh.add_trace(go.Scatter(x=hr, y=h_temp, mode='lines+markers', line=dict(color='#a8edea', width=3),
                         marker=dict(size=6, color=h_temp, colorscale='RdYlBu_r', showscale=False),
                         fill='tozeroy', fillcolor='rgba(168,237,234,0.1)', name='Temp'))
fh.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Outfit'), height=300,
                margin=dict(l=20,r=20,t=20,b=20), showlegend=False,
                xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)', tickangle=-45),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='°C'))
st.plotly_chart(fh, use_container_width=True)

# ==================== TEMP TRENDS + PREDICTIONS ====================
st.markdown("<div class='section-title'>📈 Temperature Trends & AI Predictions</div>", unsafe_allow_html=True)

tc1, tc2 = st.columns([2, 1])

with tc1:
    dft = pd.DataFrame({
        'Day': [datetime.strptime(d,'%Y-%m-%d').strftime('%a %d') for d in daily['time']],
        'High': daily['temperature_2m_max'],
        'Low': daily['temperature_2m_min'],
        'Avg': [(h+l)/2 for h,l in zip(daily['temperature_2m_max'], daily['temperature_2m_min'])]
    })
    ft = go.Figure()
    ft.add_trace(go.Scatter(x=dft['Day'], y=dft['High'], mode='lines+markers', name='High', line=dict(color='#ff9a9e', width=3), marker=dict(size=8), fill='tonexty', fillcolor='rgba(255,154,158,0.08)'))
    ft.add_trace(go.Scatter(x=dft['Day'], y=dft['Low'], mode='lines+markers', name='Low', line=dict(color='#a8edea', width=3), marker=dict(size=8), fill='tonexty', fillcolor='rgba(168,237,234,0.08)'))
    ft.add_trace(go.Scatter(x=dft['Day'], y=dft['Avg'], mode='lines', name='Average', line=dict(color='#ffd89b', width=2, dash='dash')))
    ft.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Outfit'), height=420,
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), margin=dict(l=20,r=20,t=60,b=20),
                    xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='°C'))
    st.plotly_chart(ft, use_container_width=True)

with tc2:
    preds = predict(daily)
    st.markdown("""
        <div class="glass-strong" style="height:420px; overflow-y:auto;">
            <h3 style="color:white;margin-bottom:0.3rem;">🔮 AI Forecast</h3>
            <p style="color:rgba(255,255,255,0.4);font-size:0.85rem;margin-bottom:1.2rem;">Next 3 days prediction</p>
    """, unsafe_allow_html=True)

    for pred in preds:
        ti = '📈' if pred['trend']=='warming' else '📉' if pred['trend']=='cooling' else '➡️'
        tc = '#38ef7d' if pred['trend']=='warming' else '#f5576c' if pred['trend']=='cooling' else '#ffd89b'
        st.markdown(f"""
            <div class="pred-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <div style="color:white;font-weight:700;font-size:1.1rem;">{pred['day']}, {pred['date']}</div>
                    <div style="color:{tc};font-size:1.3rem;">{ti}</div>
                </div>
                <div style="display:flex;gap:1rem;margin-bottom:0.5rem;">
                    <div><div style="color:rgba(255,255,255,0.4);font-size:0.75rem;">HIGH</div><div style="color:white;font-weight:700;font-size:1.2rem;">{pred['max']}°</div></div>
                    <div><div style="color:rgba(255,255,255,0.4);font-size:0.75rem;">LOW</div><div style="color:rgba(255,255,255,0.7);font-weight:600;font-size:1.1rem;">{pred['min']}°</div></div>
                    <div><div style="color:rgba(255,255,255,0.4);font-size:0.75rem;">RAIN</div><div style="color:#6dd5ed;font-weight:600;font-size:1.1rem;">{pred['rain']}%</div></div>
                </div>
                <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.4rem 0.8rem;margin-top:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Confidence</span>
                        <span style="color:#38ef7d;font-weight:600;font-size:0.85rem;">{pred['conf']:.0f}%</span>
                    </div>
                    <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:4px;margin-top:0.3rem;overflow:hidden;">
                        <div style="background:linear-gradient(90deg,#38ef7d,#667eea);height:100%;width:{pred['conf']}%;border-radius:4px;"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== PRECIPITATION CHART ====================
st.markdown("<div class='section-title'>🌧️ Precipitation Probability</div>", unsafe_allow_html=True)

pdf = pd.DataFrame({
    'Day': [datetime.strptime(d,'%Y-%m-%d').strftime('%a') for d in daily['time']],
    'Probability': daily['precipitation_probability_max'],
    'Amount': daily.get('precipitation_sum', [0]*8)
})

fp = go.Figure()
fp.add_trace(go.Bar(x=pdf['Day'], y=pdf['Probability'], name='Probability %',
                     marker=dict(color=pdf['Probability'], colorscale=[[0,'#38ef7d'],[0.3,'#ffd89b'],[0.6,'#ff9a64'],[1,'#f5576c']], showscale=False),
                     text=pdf['Probability'].apply(lambda x: f'{x}%'), textposition='outside', textfont=dict(color='white', size=12)))
fp.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Outfit'), height=320,
                margin=dict(l=20,r=20,t=30,b=20), showlegend=False,
                xaxis=dict(showgrid=False, color='rgba(255,255,255,0.5)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='%', range=[0,105]))
st.plotly_chart(fp, use_container_width=True)

# ==================== AIR QUALITY ====================
if ad and 'current' in ad:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🌬️ Air Quality Details</div>", unsafe_allow_html=True)

    ac = ad['current']
    aqi_cols = st.columns(5)
    aqi_m = [
        ("🌫️", "PM2.5", ac.get('pm2_5', 0), "µg/m³"),
        ("💨", "PM10", ac.get('pm10', 0), "µg/m³"),
        ("🚗", "NO₂", ac.get('nitrogen_dioxide', 0), "µg/m³"),
        ("🏭", "CO", ac.get('carbon_monoxide', 0), "µg/m³"),
        ("☀️", "O₃", ac.get('ozone', 0), "µg/m³"),
    ]

    for i, (icon, label, value, unit) in enumerate(aqi_m):
        with aqi_cols[i]:
            st.markdown(f"""
                <div class="metric-box">
                    <span class="metric-icon">{icon}</span>
                    <div class="metric-val">{value} <span style="font-size:0.8rem;color:rgba(255,255,255,0.4)">{unit}</span></div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)

# ==================== ALL CITIES OVERVIEW ====================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🗺️ All Indian Cities Overview</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Quick temperature snapshot across major cities</div>", unsafe_allow_html=True)

ov_cities = ["Delhi","Mumbai","Bangalore","Chennai","Kolkata","Hyderabad","Pune","Jaipur","Ahmedabad","Lucknow","Srinagar","Kochi"]
city_data = []

for cn in ov_cities:
    try:
        inf = INDIAN_CITIES[cn]
        wurl = f"https://api.open-meteo.com/v1/forecast?latitude={inf['lat']}&longitude={inf['lon']}&current=temperature_2m,weather_code&timezone=auto"
        r = requests.get(wurl, timeout=8)
        d = r.json()
        if 'current' in d:
            city_data.append({
                'City': f"{inf['icon']} {cn}",
                'Temp': d['current']['temperature_2m'],
                'Weather': get_emoji(d['current'].get('weather_code',0), 1),
                'State': inf['state']
            })
    except:
        pass

if city_data:
    cdf = pd.DataFrame(city_data).sort_values('Temp', ascending=False)

    fig_ov = go.Figure()
    colors = ['#f5576c' if t > 35 else '#ff9a64' if t > 30 else '#ffd89b' if t > 25 else '#38ef7d' if t > 15 else '#a8edea' for t in cdf['Temp']]
    fig_ov.add_trace(go.Bar(
        y=cdf['City'], x=cdf['Temp'], orientation='h',
        marker=dict(color=colors, line=dict(color='rgba(255,255,255,0.1)', width=1)),
        text=cdf['Temp'].apply(lambda x: f'{x}°C'), textposition='outside',
        textfont=dict(color='white', size=13, family='Outfit')
    ))
    fig_ov.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', family='Outfit'), height=450,
                        margin=dict(l=20,r=60,t=20,b=20), showlegend=False,
                        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='rgba(255,255,255,0.5)', title='°C'),
                        yaxis=dict(showgrid=False, color='rgba(255,255,255,0.7)', categoryorder='total ascending'))
    st.plotly_chart(fig_ov, use_container_width=True)

# ==================== FOOTER ====================
st.markdown("""
    <div class="footer">
        <p>🇮🇳 SkyCast India | AI Weather Intelligence | Powered by Open-Meteo</p>
        <p style="font-size:0.75rem; color:rgba(255,255,255,0.2);">Built with Streamlit & Plotly | Data for educational purposes</p>
    </div>
""", unsafe_allow_html=True)

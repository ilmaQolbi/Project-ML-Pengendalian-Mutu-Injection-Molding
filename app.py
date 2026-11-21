import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# setting halaman utama
st.set_page_config(
    page_title="QC Injection Molding • Assya & Ilma Edition",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# css + responsif HP
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Nunito:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

h1, h2, h3, .miao-font {
    font-family: 'Fredoka', sans-serif !important;
    letter-spacing: 0.3px;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #FAF0BE !important;
    background-image:
        radial-gradient(circle at 12% 14%, rgba(232, 111, 114, 0.14) 0%, transparent 28%),
        radial-gradient(circle at 88% 85%, rgba(155, 182, 204, 0.22) 0%, transparent 32%),
        radial-gradient(#E86F72 1.5px, transparent 1.5px),
        radial-gradient(#F4CE46 2px, #FAF0BE 2px) !important;
    background-size: 100% 100%, 100% 100%, 48px 48px, 48px 48px !important;
    background-position: 0 0, 0 0, 0 0, 24px 24px !important;
    color: #231F20 !important;
}

[data-testid="stMain"],
.main,
.main .block-container {
    background: transparent !important;
}

[data-testid="stMainBlockContainer"] h1,
[data-testid="stMainBlockContainer"] h2,
[data-testid="stMainBlockContainer"] h3,
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] span,
[data-testid="stMainBlockContainer"] label {
    color: #231F20;
}

code {
    background-color: #FDE2DC !important;
    color: #C94A4E !important;
    border: 1.5px solid #E86F72;
    border-radius: 8px;
    padding: 2px 7px;
    font-weight: 700;
}

[data-testid="stHeader"] {
    background: rgba(250, 240, 190, 0.75) !important;
    backdrop-filter: blur(8px);
}

/* styling sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FDE6DC 0%, #FAF0BE 52%, #DCE9F5 100%) !important;
    border-right: 3px solid #231F20;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

div.sidebar-header-card {
    background: linear-gradient(135deg, #E86F72 0%, #F08A8C 100%);
    border: 2.5px solid #231F20;
    border-radius: 22px;
    padding: 16px 18px;
    margin-bottom: 14px;
    box-shadow: 4px 4px 0px #231F20;
    position: relative;
    overflow: hidden;
}

div.sidebar-header-card::after {
    content: "✦";
    position: absolute;
    top: 12px;
    right: 16px;
    font-size: 1.2rem;
    color: #F7D44C;
}

.sidebar-clasp {
    display: inline-block;
    background: #FCD5C8;
    color: #231F20 !important;
    border: 2px solid #231F20;
    border-radius: 999px;
    padding: 2px 11px;
    font-size: 0.74rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.sidebar-title {
    font-family: 'Fredoka', sans-serif !important;
    margin: 0 0 5px 0 !important;
    font-size: 1.38rem !important;
    font-weight: 400 !important;
    color: #FFFDF7 !important;
    text-shadow: 1.5px 1.5px 0px #231F20;
    line-height: 1.25;
}

div.sidebar-header-card p {
    margin: 0 !important;
    font-size: 0.82rem !important;
    color: #FFF6E9 !important;
    font-weight: 600;
    line-height: 1.35;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] {
    background: #FFFDF7;
    border: 2px solid #231F20;
    border-radius: 16px;
    padding: 10px 14px 12px 14px;
    margin-bottom: 4px;
    box-shadow: 3.5px 3.5px 0px #F7D44C;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"]:hover {
    transform: translate(-1px, -2px);
    box-shadow: 4.5px 5px 0px #E86F72;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] label p {
    color: #231F20 !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FCD5C8 !important;
    border: 1.5px solid #231F20 !important;
    border-radius: 10px !important;
    color: #231F20 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    color: #231F20 !important;
    fill: #231F20 !important;
}

[data-testid="stSidebar"] [data-testid="stSlider"] {
    background: #FFFDF7;
    border: 2px solid #231F20;
    border-radius: 16px;
    padding: 12px 14px 10px 14px;
    margin-bottom: 4px;
    box-shadow: 3.5px 3.5px 0px #9BB6CC;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

[data-testid="stSidebar"] [data-testid="stSlider"]:hover {
    transform: translate(-1px, -2px);
    box-shadow: 4.5px 5px 0px #E86F72;
}

[data-testid="stSidebar"] [data-testid="stSlider"] label p {
    color: #231F20 !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
}

[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    background: #FCD5C8 !important;
    color: #231F20 !important;
    border: 1.5px solid #231F20 !important;
    border-radius: 8px !important;
    padding: 1px 7px !important;
    font-weight: 800 !important;
    font-size: 0.8rem !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] > div > div {
    background-color: #FCD5C8 !important;
    height: 6px !important;
    border-radius: 999px !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] > div > div > div:first-child {
    background: linear-gradient(90deg, #7FA3C2 0%, #E86F72 100%) !important;
    height: 6px !important;
    border-radius: 999px !important;
}

[data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
    background-color: #F7D44C !important;
    border: 2.5px solid #231F20 !important;
    width: 18px !important;
    height: 18px !important;
    box-shadow: 0 2px 0 #231F20 !important;
}

/* kontainer utama & banner */
.main .block-container {
    max-width: 1400px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

[data-testid="stMainBlockContainer"] {
    background: rgba(255, 253, 245, 0.94) !important;
    border: 3px solid #231F20;
    border-radius: 28px;
    box-shadow: 6px 6px 0px #9BB6CC;
}

div.miao-hero {
    background:
        radial-gradient(circle at 82% 20%, rgba(247, 212, 76, 0.25) 0%, transparent 32%),
        radial-gradient(circle at 18% 85%, rgba(252, 213, 200, 0.22) 0%, transparent 35%),
        linear-gradient(125deg, #E86F72 0%, #EF8789 55%, #E36468 100%);
    border: 3px solid #231F20;
    border-radius: 26px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 6px 6px 0px #231F20;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    position: relative;
}

.miao-badge {
    display: inline-block;
    background: #FCD5C8;
    color: #231F20 !important;
    border: 2px solid #231F20;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 10px;
    box-shadow: 2px 2px 0px #231F20;
}

.hero-title {
    font-family: 'Fredoka', sans-serif !important;
    font-size: 2.15rem !important;
    font-weight: 600 !important;
    line-height: 1.2 !important;
    letter-spacing: 0.6px !important;
    color: #FFFDF7 !important;
    -webkit-text-stroke: 1.4px #231F20;
    paint-order: stroke fill;
    text-shadow: 3px 3px 0px #231F20;
    margin: 2px 0 8px 0 !important;
}

.hero-title span.highlight-word {
    color: #FAF0BE !important;
}

.hero-subtitle {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    color: #FFFDF7 !important;
    text-shadow: 1px 1px 0px rgba(35, 31, 32, 0.55);
    margin: 0 0 14px 0 !important;
    letter-spacing: 0.2px;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.hero-pill {
    font-size: 0.78rem;
    font-weight: 800;
    color: #231F20 !important;
    padding: 4px 12px;
    border-radius: 999px;
    border: 2px solid #231F20;
    box-shadow: 2px 2px 0px #231F20;
}

.mascot-group {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(255, 253, 247, 0.22);
    border: 2px dashed #FFFDF7;
    border-radius: 22px;
    padding: 12px 18px;
    flex-shrink: 0;
}

.mascot-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #FFFDF7;
    border: 2.5px solid #231F20;
    border-radius: 18px;
    padding: 8px 12px 10px 12px;
    box-shadow: 3.5px 3.5px 0px #231F20;
    transition: transform 0.22s ease;
}

.mascot-card:hover {
    transform: translateY(-4px) rotate(-2deg);
}

.mascot-card:last-child:hover {
    transform: translateY(-4px) rotate(2deg);
}

.mascot-name {
    margin-top: 4px;
    padding: 2px 14px;
    border-radius: 999px;
    border: 2px solid #231F20;
    font-family: 'Fredoka', sans-serif;
    font-size: 0.92rem;
    font-weight: 500;
    color: #231F20 !important;
    letter-spacing: 0.4px;
}

.sticker-card {
    background: #FFF9DF;
    border: 2.5px solid #231F20;
    border-radius: 20px;
    padding: 16px 20px;
    box-shadow: 4px 4px 0px #E86F72;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.sticker-card:hover {
    transform: translate(-2px, -3px);
    box-shadow: 6px 7px 0px #231F20;
}

.sticker-label {
    font-size: 0.86rem;
    font-weight: 800;
    color: #C94A4E !important;
    margin-bottom: 4px;
}

.sticker-value {
    font-family: 'Fredoka', sans-serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: #231F20 !important;
}

.miao-status-ok {
    background: #E6F8EC;
    border: 2.5px solid #231F20;
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 4px 4px 0px #4CAF7D;
    margin-bottom: 10px;
}

.miao-status-ng {
    background: #FDE4E4;
    border: 2.5px solid #231F20;
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 4px 4px 0px #E86F72;
    margin-bottom: 10px;
}

.status-caption {
    font-size: 0.92rem;
    font-weight: 700;
    color: #231F20 !important;
    margin-top: 8px;
    margin-bottom: 12px;
}

.prob-card {
    background: #FFFDF7;
    border: 2px solid #231F20;
    border-radius: 16px;
    padding: 10px 14px;
    margin-bottom: 10px;
    box-shadow: 3px 3px 0px #9BB6CC;
}

.prob-card.threshold {
    background: #FFF9DF;
    box-shadow: 3px 3px 0px #F7D44C;
}

.prob-title {
    font-size: 0.78rem;
    font-weight: 800;
    color: #57534E !important;
    margin-bottom: 2px;
}

.prob-number {
    font-family: 'Fredoka', sans-serif;
    font-size: 1.7rem;
    font-weight: 600;
    color: #231F20 !important;
    line-height: 1.15;
}

/* pembungkus tabel supaya bisa digeser ke samping saat dibuka di HP */
.table-wrap {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    background: #FFFDF7;
    border: 2.5px solid #231F20;
    border-radius: 16px;
    margin-top: 8px;
    box-shadow: 4px 4px 0px #F7D44C;
}

.miao-table {
    width: 100%;
    min-width: 460px;
    border-collapse: collapse;
    background: #FFFDF7;
    font-size: 0.85rem;
}

.miao-table th {
    background: #FCD5C8;
    color: #231F20 !important;
    padding: 9px 8px;
    text-align: center;
    font-weight: 800;
    border-bottom: 2px solid #231F20;
    white-space: nowrap;
}

.miao-table td {
    color: #231F20 !important;
    padding: 9px 8px;
    text-align: center;
    font-weight: 700;
    white-space: nowrap;
}

hr {
    border: none;
    border-top: 2px dashed #E86F72 !important;
    margin: 1.4rem 0 !important;
}

/* penyesuaian tampilan otomatis saat dibuka di layar HP */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 1rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-bottom: 2rem !important;
    }

    [data-testid="stMainBlockContainer"] {
        border-radius: 20px;
        box-shadow: 4px 4px 0px #9BB6CC;
    }

    div.miao-hero {
        flex-direction: column;
        align-items: stretch;
        padding: 18px 16px;
        gap: 14px;
        border-radius: 20px;
        box-shadow: 4px 4px 0px #231F20;
    }

    .hero-title {
        font-size: 1.55rem !important;
        -webkit-text-stroke: 1px #231F20;
        text-shadow: 2px 2px 0px #231F20;
    }

    .hero-subtitle {
        font-size: 0.86rem !important;
        margin-bottom: 10px !important;
    }

    .hero-pills {
        gap: 6px;
    }

    .hero-pill {
        font-size: 0.72rem;
        padding: 3px 10px;
    }

    .mascot-group {
        width: 100%;
        justify-content: center;
        padding: 10px 12px;
        gap: 12px;
        box-sizing: border-box;
    }

    .mascot-card {
        flex: 1;
        max-width: 130px;
        padding: 6px 10px 8px 10px;
    }

    .sticker-card {
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 16px;
    }

    .sticker-value {
        font-size: 1.45rem;
    }

    .prob-number {
        font-size: 1.45rem;
    }

    .miao-table th,
    .miao-table td {
        padding: 8px 6px;
        font-size: 0.8rem;
    }
}
</style>
""", unsafe_allow_html=True)

# banner atas + stiker Assya & Ilma
st.markdown("""
<div class="miao-hero">
<div>
<div class="miao-badge">★ Smart Factory QC • Assya &amp; Ilma Edition ★</div>
<div class="hero-title">Quality Control — <span class="highlight-word">Injection Molding</span></div>
<div class="hero-subtitle">Sistem Prediksi &amp; Monitoring Mutu Produk Berbasis Machine Learning</div>
<div class="hero-pills">
<span class="hero-pill" style="background:#FAF0BE;">🌡️ Thermal Check</span>
<span class="hero-pill" style="background:#DCE9F5;">💨 Pressure Monitor</span>
<span class="hero-pill" style="background:#FCD5C8;">🤖 ML Defect Guard</span>
</div>
</div>
<div class="mascot-group">
<div class="mascot-card">
<svg width="74" height="72" viewBox="0 0 100 96" xmlns="http://www.w3.org/2000/svg">
<rect x="6" y="28" width="14" height="34" rx="7" fill="#F7D44C" stroke="#231F20" stroke-width="3"/>
<rect x="80" y="28" width="14" height="34" rx="7" fill="#F7D44C" stroke="#231F20" stroke-width="3"/>
<path d="M22 38 Q50 8 78 38" fill="none" stroke="#F7D44C" stroke-width="7" stroke-linecap="round"/>
<polygon points="24,36 30,14 45,28" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
<polygon points="76,36 70,14 55,28" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
<ellipse cx="50" cy="54" rx="32" ry="27" fill="#9BB6CC" stroke="#231F20" stroke-width="2.5"/>
<ellipse cx="50" cy="61" rx="14" ry="10" fill="#FFF8E7"/>
<circle cx="42" cy="50" r="5.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
<circle cx="58" cy="50" r="5.5" fill="#FFFDF7" stroke="#231F20" stroke-width="1.5"/>
<circle cx="43" cy="50" r="3.2" fill="#231F20"/>
<circle cx="57" cy="50" r="3.2" fill="#231F20"/>
<polygon points="47,57 53,57 50,61" fill="#E86F72"/>
<path d="M44 65 Q50 61 50 61 Q50 61 56 65" fill="none" stroke="#231F20" stroke-width="2" stroke-linecap="round"/>
<line x1="22" y1="56" x2="36" y2="58" stroke="#231F20" stroke-width="1.8"/>
<line x1="22" y1="63" x2="36" y2="62" stroke="#231F20" stroke-width="1.8"/>
<line x1="78" y1="56" x2="64" y2="58" stroke="#231F20" stroke-width="1.8"/>
<line x1="78" y1="63" x2="64" y2="62" stroke="#231F20" stroke-width="1.8"/>
</svg>
<div class="mascot-name" style="background:#DCE9F5;">Assya</div>
</div>
<div class="mascot-card">
<svg width="74" height="72" viewBox="0 0 100 96" xmlns="http://www.w3.org/2000/svg">
<polygon points="22,38 26,13 44,28" fill="#231F20"/>
<polygon points="27,33 29,19 39,28" fill="#F5A99B"/>
<polygon points="78,38 74,13 56,28" fill="#231F20"/>
<polygon points="73,33 71,19 61,28" fill="#F5A99B"/>
<ellipse cx="50" cy="53" rx="33" ry="27" fill="#231F20"/>
<ellipse cx="43" cy="61" rx="9" ry="8" fill="#FFF8E7"/>
<ellipse cx="57" cy="61" rx="9" ry="8" fill="#FFF8E7"/>
<ellipse cx="43" cy="48" rx="6" ry="7" fill="#FFFDF7"/>
<ellipse cx="57" cy="48" rx="6" ry="7" fill="#FFFDF7"/>
<circle cx="44" cy="49" r="3.5" fill="#231F20"/>
<circle cx="56" cy="49" r="3.5" fill="#231F20"/>
<polygon points="47,56 53,56 50,59" fill="#E86F72"/>
<line x1="16" y1="54" x2="34" y2="57" stroke="#FFFDF7" stroke-width="1.8"/>
<line x1="16" y1="62" x2="34" y2="61" stroke="#FFFDF7" stroke-width="1.8"/>
<line x1="84" y1="54" x2="66" y2="57" stroke="#FFFDF7" stroke-width="1.8"/>
<line x1="84" y1="62" x2="66" y2="61" stroke="#FFFDF7" stroke-width="1.8"/>
</svg>
<div class="mascot-name" style="background:#FCD5C8;">Ilma</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# input parameter dari sidebar
st.sidebar.markdown("""
<div class="sidebar-header-card">
<div class="sidebar-clasp">🐾 Control Panel</div>
<div class="sidebar-title">⚙️ Masukkan Parameter Mesin</div>
<p>Atur mesin, shift, bahan, dan parameter proses untuk mengecek kualitas produk ★</p>
</div>
""", unsafe_allow_html=True)

mesin = st.sidebar.selectbox("🏭 Pilih Mesin", ["IM-01", "IM-02", "IM-03", "IM-04"], index=0)
shift = st.sidebar.selectbox("🕒 Pilih Shift", ["pagi", "siang", "malam"], index=1)
jenis_bahan = st.sidebar.selectbox("🧪 Jenis Bahan Plastik", ["PP", "ABS", "PC"], index=0)

melt_temp = st.sidebar.slider("🔥 Melt Temperature (°C)", 180.0, 280.0, 243.5, 0.5)
mold_temp = st.sidebar.slider("❄️ Mold Temperature (°C)", 20.0, 90.0, 71.0, 0.5)
injection_pressure = st.sidebar.slider("💨 Injection Pressure (bar)", 500.0, 1800.0, 1490.0, 10.0)
holding_pressure = st.sidebar.slider("🛡️ Holding Pressure (bar)", 300.0, 1400.0, 800.0, 10.0)
cooling_time = st.sidebar.slider("🧊 Cooling Time (detik)", 5.0, 45.0, 18.0, 0.5)
cycle_time = st.sidebar.slider("⏱️ Cycle Time (detik)", 15.0, 90.0, 35.0, 0.5)

data_input = pd.DataFrame([{
    "Mesin": mesin,
    "Shift": shift,
    "Jenis_Bahan": jenis_bahan,
    "Melt_Temp": melt_temp,
    "Mold_Temp": mold_temp,
    "Injection_Pressure": injection_pressure,
    "Holding_Pressure": holding_pressure,
    "Cooling_Time": cooling_time,
    "Cycle_Time": cycle_time
}])

# load model dan setting batas threshold 25%
file_model = "model_qc_injection.joblib"
batas_threshold = 25.0

@st.cache_resource
def ambil_model(nama_file):
    if os.path.exists(nama_file):
        return joblib.load(nama_file)
    return None

def hitung_risiko(suhu_leleh, suhu_cetakan, tek_injeksi, tek_tahan, waktu_dingin, waktu_siklus, no_mesin, jadwal_shift, bahan):
    risiko = 5.0
    if suhu_leleh < 200 or suhu_leleh > 255:
        risiko += abs(suhu_leleh - 230) * 0.75
    if suhu_cetakan < 30 or suhu_cetakan > 80:
        risiko += abs(suhu_cetakan - 55) * 0.5
    if tek_injeksi < 750 or tek_injeksi > 1620:
        risiko += abs(tek_injeksi - 1200) * 0.045
    if tek_tahan < 450 or tek_tahan > 1150:
        risiko += abs(tek_tahan - 800) * 0.03
    if waktu_dingin < 10:
        risiko += (10 - waktu_dingin) * 4.5
    if waktu_siklus < 20 or waktu_siklus > 70:
        risiko += abs(waktu_siklus - 40) * 0.45
    if jadwal_shift == "malam":
        risiko += 2.5
    if bahan in ["PC", "ABS"]:
        risiko += 1.5
    if no_mesin == "IM-03":
        risiko += 1.0
    return float(np.clip(risiko, 1.0, 98.5))

model = ambil_model(file_model)

if model is not None:
    try:
        kolom_model = getattr(model, "feature_names_in_", data_input.columns)
        fitur_uji = data_input.reindex(columns=kolom_model, fill_value=0)
        if hasattr(model, "predict_proba"):
            peluang = model.predict_proba(fitur_uji)[0]
            prob_cacat = float(peluang[-1]) * 100
        else:
            hasil_pred = model.predict(fitur_uji)[0]
            prob_cacat = 5.0 if str(hasil_pred).upper() in ["0", "OK", "NORMAL", "PASS", "GOOD"] else 68.0
    except Exception:
        prob_cacat = hitung_risiko(
            melt_temp, mold_temp, injection_pressure, holding_pressure,
            cooling_time, cycle_time, mesin, shift, jenis_bahan
        )
else:
    prob_cacat = hitung_risiko(
        melt_temp, mold_temp, injection_pressure, holding_pressure,
        cooling_time, cycle_time, mesin, shift, jenis_bahan
    )

status_lolos = prob_cacat <= batas_threshold

# 4 kartu metrik utama
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
<div class="sticker-card">
<div class="sticker-label">★ Melt Temp</div>
<div class="sticker-value">{melt_temp:.1f} °C</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
<div class="sticker-card">
<div class="sticker-label">★ Mold Temp</div>
<div class="sticker-value">{mold_temp:.1f} °C</div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
<div class="sticker-card">
<div class="sticker-label">★ Injection Pressure</div>
<div class="sticker-value">{injection_pressure:.1f} bar</div>
</div>
""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
<div class="sticker-card">
<div class="sticker-label">★ Cycle Time</div>
<div class="sticker-value">{cycle_time:.1f} dtk</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# kolom hasil prediksi & grafik parameter
kol_kiri, kol_kanan = st.columns([1.15, 1.2], gap="large")

with kol_kiri:
    st.subheader("📋 Hasil Analisis & Prediksi Model")

    kol_status, kol_angka = st.columns([1.45, 1.0], gap="medium")

    with kol_status:
        if status_lolos:
            st.markdown("""
<div class="miao-status-ok">
<div style="font-size:1.02rem; font-weight:800; color:#1B6B42;">✅ STATUS: KOMPONEN NORMAL (LOLOS QC)</div>
</div>
<div class="status-caption">Parameter proses dalam kondisi aman.</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<div class="miao-status-ng">
<div style="font-size:1.02rem; font-weight:800; color:#B83338;">⚠️ STATUS: POTENSI CACAT (NG / REJECT)</div>
</div>
<div class="status-caption">Parameter melebihi batas aman, periksa setting mesin.</div>
""", unsafe_allow_html=True)

    with kol_angka:
        st.markdown(f"""
<div class="prob-card">
<div class="prob-title">Probabilitas Cacat</div>
<div class="prob-number">{prob_cacat:.2f}%</div>
</div>
<div class="prob-card threshold">
<div class="prob-title">Batas Threshold Bisnis</div>
<div class="prob-number">{batas_threshold:.1f}%</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="table-wrap">
<table class="miao-table">
<thead>
<tr>
<th>Mesin</th>
<th>Shift</th>
<th>Bahan</th>
<th>Melt</th>
<th>Mold</th>
<th>Inj. Press</th>
<th>Cooling</th>
<th>Cycle</th>
</tr>
</thead>
<tbody>
<tr>
<td>{mesin}</td>
<td>{shift}</td>
<td>{jenis_bahan}</td>
<td>{melt_temp:.1f}°</td>
<td>{mold_temp:.1f}°</td>
<td>{injection_pressure:.0f}</td>
<td>{cooling_time:.1f}s</td>
<td>{cycle_time:.1f}s</td>
</tr>
</tbody>
</table>
</div>
""", unsafe_allow_html=True)

with kol_kanan:
    st.subheader("📊 Profil Parameter Saat Ini")

    fig, ax = plt.subplots(figsize=(7.2, 4.15))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("#FFF9DF")

    rentang_param = [
        (melt_temp, 180, 280),
        (mold_temp, 20, 90),
        (injection_pressure, 500, 1800),
        (holding_pressure, 300, 1400),
        (cooling_time, 5, 45),
        (cycle_time, 15, 90),
    ]
    persen = [(val - mn) / (mx - mn) * 100 for val, mn, mx in rentang_param]
    label_param = ["Melt Temp", "Mold Temp", "Inj. Press", "Hold Press", "Cooling", "Cycle"]
    warna_batang = ["#E86F72", "#9BB6CC", "#231F20", "#F7D44C", "#F5A99B", "#D95B60"]

    bars = ax.barh(label_param, persen, color=warna_batang, height=0.58, edgecolor="#231F20", linewidth=1.6)
    ax.bar_label(bars, fmt="%.1f%%", padding=5, color="#231F20", fontsize=9.5, fontweight="bold")

    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.grid(axis="x", linestyle="--", alpha=0.35, color="#E86F72")
    ax.set_axisbelow(True)

    ax.set_xlabel("Persentase terhadap Rentang Operasi (%)", color="#231F20", fontsize=9.5, fontweight="bold")
    ax.set_title(f"Distribusi Parameter • {mesin} ({shift.capitalize()} - {jenis_bahan}) ★", color="#231F20", fontsize=11.5, fontweight="bold", pad=12)
    ax.tick_params(colors="#231F20", labelsize=9.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#231F20")
    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["left"].set_color("#231F20")
    ax.spines["left"].set_linewidth(1.5)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

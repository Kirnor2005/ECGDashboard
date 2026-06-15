# HARTstikke Gezond - Onderzoekersdashboard (filter op wijk, leeftijd, geslacht, meting)
import streamlit as st
import pandas as pd
import base64
from pathlib import Path

st.set_page_config(layout="wide", page_title="HARTstikke Gezond Dashboard", page_icon="❤️")
BASE_DIR = Path(__file__).resolve().parent

st.markdown("<style>.stApp{background:#fbfaf7}.block-container{max-width:1180px;padding-top:2.2rem}"
            "h1,h2,h3{color:#16475b}section[data-testid='stSidebar']{background:#f2f6f4}</style>",
            unsafe_allow_html=True)

# instellingen 
KLEUREN = {
    'verhoogd': {'bar': '#e74c3c', 'txt': '#c0392b', 'pil_bg': '#f5b7b1', 'pil_txt': '#a93226', 'icon': '▲'},
    'grens':    {'bar': '#b8860b', 'txt': '#b8860b', 'pil_bg': '#fae5b8', 'pil_txt': '#9a6a00', 'icon': '!'},
    'normaal':  {'bar': '#27ae60', 'txt': '#1e8449', 'pil_bg': '#abebc6', 'pil_txt': '#1e8449', 'icon': '✓'},
    'leeg':     {'bar': '#d5d8dc', 'txt': '#95a5a6', 'pil_bg': '#eaecee', 'pil_txt': '#7f8c8d', 'icon': ''},
}
LABEL = {'verhoogd': 'Verhoogd', 'grens': 'Grenswaarde', 'normaal': 'Normaal', 'leeg': 'Geen data'}
LABEL_BMI = {**LABEL, 'grens': 'Licht Verhoogd'}
STATUS = {
    'Bloeddruk':   {'<120': 'normaal', '120-140': 'grens', '140-180': 'verhoogd', '>180': 'verhoogd'},
    'Cholesterol': {'<5': 'normaal', '5-6.5': 'grens', '6.5-8': 'verhoogd', '>8': 'verhoogd'},
    'Bloedsuiker': {'<7.8': 'normaal', '7.8-11': 'grens', '>11.1': 'verhoogd'},
    'BMI':         {'<18.5': 'grens', '18.5-25': 'normaal', '25-30': 'grens', '>30': 'verhoogd'},
    'Non-HDL':     {'<3.8': 'normaal', '>3.8': 'verhoogd'},
}
EENHEID = {'Bloeddruk': 'mmHg', 'Cholesterol': 'mmol/L', 'Bloedsuiker': 'mmol/L', 'BMI': 'kg/m²', 'Non-HDL': 'mmol/L'}
# Begin van de kolomnaam; achter komt ' 1'/' 2' (meting) en 'man/vrouw/anders' (geslacht)
KOLOMBASIS = {'Bloeddruk': 'mvc Bloeddruk (Bovendruk)', 'Cholesterol': 'mvc Cholesterol',
              'Bloedsuiker': 'mvc Bloedsuiker', 'BMI': 'mvc BMI', 'Non-HDL': 'mvc Non-HDL'}
# Hartritme/HRV voor de uitklap: (naam, kolombegin, eenheid, uitleg)
ECG_DETAILS = [
    ('SDNN', 'sdnn_', 'ms', 'HRV: variatie tussen hartslagen. Hoger = gezonder.'),
    ('RMSSD', 'rmssd_', 'ms', 'HRV: variatie tussen opeenvolgende hartslagen. Hoger = beter.'),
    ('NN50', 'nn50_', '', 'Aantal intervallen met >50 ms verschil.'),
    ('pNN50', 'pnn50_', '%', 'Percentage van NN50.'),
    ('Gem. hartslag', 'HR', 'bpm', 'Gemiddelde hartritme.'),
    ('Min. hartslag', 'MinHR', 'bpm', 'Laagste hartslag.'),
    ('Max. hartslag', 'MaxHR', 'bpm', 'Hoogste hartslag.'),
    ('SD hartslag', 'STDHR', 'bpm', 'Standaarddeviatie van de hartslag.'),
]
GESLACHT = {'Man': 'man', 'Vrouw': 'vrouw', 'Anders': 'anders'}  # knoplabel -> kolomsuffix

#  Functies 
def maak_kaart(titel, waarde, eenheid, status):
    """HTML van één kaart: gekleurde balk, waarde, icoon en statuspil."""
    k = KLEUREN[status]
    pil = (LABEL_BMI if titel == 'BMI' else LABEL)[status]
    eh = f"<span style='color:#7f8c8d;font-size:.95rem;margin-left:6px'>{eenheid}</span>" if eenheid else ""
    return (f"<div style='border:1px solid #d5d8dc;border-radius:18px;overflow:hidden;background:#fff;"
            f"box-shadow:0 1px 3px rgba(0,0,0,.04);height:205px;display:flex;flex-direction:column'>"
            f"<div style='height:6px;background:{k['bar']}'></div>"
            f"<div style='padding:20px 24px;display:flex;flex-direction:column;flex:1'>"
            f"<div style='font-weight:700;font-size:1.2rem;color:#1c2833'>{titel}</div>"
            f"<div style='margin-top:auto;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between'>"
            f"<div><span style='color:{k['txt']};font-weight:800;font-size:1.5rem'>{waarde}</span>{eh}</div>"
            f"<span style='color:{k['bar']};font-size:1.45rem;font-weight:700'>{k['icon']}</span></div>"
            f"<div><span style='display:inline-block;background:{k['pil_bg']};color:{k['pil_txt']};"
            f"padding:8px 22px;border-radius:22px;font-weight:700'>{pil}</span></div></div></div>")

def status_hartslag(hr):
    """Status op basis van de gemiddelde hartslag (bpm)."""
    if hr is None:
        return 'leeg'
    if hr < 50 or hr > 110:
        return 'verhoogd'
    if hr < 60 or hr > 100:
        return 'grens'
    return 'normaal'

def categorie(basis, metingen, geslachten, data):
    """Meest voorkomende categorie over de gekozen meting(en) en geslacht(en)."""
    waarden = [data[f"{basis} {m}_{g}"].dropna().astype(str)
               for m in metingen for g in geslachten if f"{basis} {m}_{g}" in data.columns]
    if not waarden:
        return None
    samen = pd.concat(waarden)
    return samen.mode().iloc[0] if not samen.empty else None

def gemiddelde(basis, metingen, geslachten, data):
    """Gemiddelde van een numerieke kolom over de gekozen meting(en) en geslacht(en)."""
    waarden = [pd.to_numeric(data[f"{basis}{m}_{g}"], errors='coerce')
               for m in metingen for g in geslachten if f"{basis}{m}_{g}" in data.columns]
    if not waarden:
        return None
    samen = pd.concat(waarden).dropna()
    return float(samen.mean()) if not samen.empty else None

def band_gekozen(band, onder, boven):
    """Valt een leeftijdsband (bv. '50-60') binnen de schuifbalk?"""
    start, eind = band.split('-')
    return int(start) >= onder and int(eind) <= boven

# titel met logo 
logo_pad = BASE_DIR / "hartstikke-gezondweek.png"
logo_html = (f'<img src="data:image/png;base64,{base64.b64encode(logo_pad.read_bytes()).decode()}" '
             f'style="height:62px;">') if logo_pad.exists() else ''
st.markdown("<div style='display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;margin-bottom:.6rem'>"
            "<span style='font-size:2.6rem'>❤️</span>"
            "<span style='font-size:2.6rem;font-weight:800;color:#1c2833'>HARTstikke Gezond Dashboard</span>"
            f"{logo_html}</div>", unsafe_allow_html=True)

#  data inladen (via upload en als csv bestand) 
upload = st.file_uploader('Upload een CSV-bestand met metingen', type=['csv'])
if upload is None:
    st.info('Upload een CSV-bestand om het dashboard te tonen.')
    st.stop()
data = pd.read_csv(upload)

#  filters (zijbalk) 
st.sidebar.header('Filters')
locatie = st.sidebar.selectbox('Locatie (wijk)', ['Alle locaties'] + sorted(data['Wijk'].dropna().unique().tolist()))
meting_keuze = st.sidebar.radio('Meting', ['1 (voormeting)', '2 (nameting)', 'Beide metingen'])
metingen = ['1'] if meting_keuze.startswith('1') else ['2'] if meting_keuze.startswith('2') else ['1', '2']
onder, boven = st.sidebar.slider('Leeftijd', 40, 70, (40, 70), step=10)
geslacht_keuze = st.sidebar.multiselect('Geslacht', list(GESLACHT), default=list(GESLACHT))
geslachten = [GESLACHT[g] for g in geslacht_keuze]

# filters toepassen op de rijen 
selectie = data.copy()
if locatie != 'Alle locaties':
    selectie = selectie[selectie['Wijk'] == locatie]
selectie = selectie[selectie['leeftijdscategorie'].apply(lambda b: band_gekozen(b, onder, boven))]

# ondertitel 
wijk_tekst = locatie if locatie != 'Alle locaties' else 'alle wijken'
meting_tekst = 'beide metingen' if len(metingen) == 2 else ('voormeting' if metingen == ['1'] else 'nameting')
st.markdown(f"<div style='text-align:center;color:#5d6d7e;margin:.4rem 0 1.4rem 0'>{wijk_tekst} · "
            f"{onder}–{boven} jaar · {', '.join(geslacht_keuze) or 'geen'} · {meting_tekst}</div>",
            unsafe_allow_html=True)

#  kaarten 
if selectie.empty or not geslachten:
    st.warning('Geen data voor deze selectie. Pas de filters aan.')
    st.stop()

def categorie_kaart(metric):
    cat = categorie(KOLOMBASIS[metric], metingen, geslachten, selectie)
    status = STATUS[metric].get(cat, 'leeg') if cat is not None else 'leeg'
    return maak_kaart(metric, cat if cat is not None else '—', EENHEID[metric], status)

def ecg_kaart():
    hr = gemiddelde('HR', metingen, geslachten, selectie)
    return maak_kaart('ECG (hartritme)', f"{hr:.0f}" if hr is not None else '—', 'bpm', status_hartslag(hr))

rij1 = st.columns(3)
for kol, metric in zip(rij1, ['Bloeddruk', 'Cholesterol', 'Bloedsuiker']):
    kol.markdown(categorie_kaart(metric), unsafe_allow_html=True)
st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
rij2 = st.columns(3)
rij2[0].markdown(categorie_kaart('BMI'), unsafe_allow_html=True)
rij2[1].markdown(categorie_kaart('Non-HDL'), unsafe_allow_html=True)
rij2[2].markdown(ecg_kaart(), unsafe_allow_html=True)

#  Legenda 
st.markdown("<div style='display:flex;gap:36px;justify-content:center;flex-wrap:wrap;border-top:1px solid #e5e8e8;"
            "margin-top:1.8rem;padding-top:1rem;color:#34495e'><span>🔴 Verhoogd / actie vereist</span>"
            "<span>🟠 Grenswaarde / let op</span><span>🟢 Normaal</span></div>", unsafe_allow_html=True)

# ECG / HRV-details (uitklap) 
with st.expander('🫀 ECG / HRV-details (met toelichting)'):
    rijen = []
    for naam, basis, eenheid, uitleg in ECG_DETAILS:
        v = gemiddelde(basis, metingen, geslachten, selectie)
        rijen.append({'Meetwaarde': naam,
                      'Waarde': f"{v:.1f} {eenheid}".strip() if v is not None else '—',
                      'Toelichting': uitleg})
    st.dataframe(pd.DataFrame(rijen), hide_index=True, use_container_width=True)

#  gefilterde data (uitklap, met download) 
with st.expander('📄 Gefilterde data bekijken / downloaden'):
    st.dataframe(selectie, use_container_width=True)
    st.download_button('⬇️ Download als CSV', selectie.to_csv(index=False).encode('utf-8'),
                       'gefilterde_metingen.csv', 'text/csv')
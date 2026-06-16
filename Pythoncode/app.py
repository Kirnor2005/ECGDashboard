import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import geopandas as gpd
import base64


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if 'pagina' not in st.session_state:
        st.session_state.pagina = 'kaart'
    
if 'wijken_graf' not in st.session_state:
        st.session_state.wijken_graf = []
    
if 'wijken_tab' not in st.session_state:
        st.session_state.wijken_tab = []
    
if 'variabelen' not in st.session_state:
        st.session_state.variabelen = []

if 'leeftijd' not in st.session_state:
    st.session_state.leeftijd = ['40-50', '50-60', '60-70'] # Verander naar [] als je wilt dat standaard niets geselecteerd is.
    
if 'geslacht' not in st.session_state:
    st.session_state.geslacht = ['man', 'vrouw', 'anders'] # idem
    
if 'taal' not in st.session_state:
        st.session_state.taal = 'English'
    
if 'mvc' not in st.session_state:
        st.session_state.mvc = []

if 'fontsize_scale' not in st.session_state:
    st.session_state.fontsize_scale = 1.0

#page layout

st.set_page_config(layout="wide")
if st.session_state.taal == 'العربية':
    direction = 'rtl'
    align = 'right'
else:
    direction = 'ltr'
    align = 'left'
    
st.markdown(f"""
<style>
html, body, .stApp {{
    direction: {direction};
    text-align: {align};
}}

p, div, span, label,
h1, h2, h3, h4, h5, h6 {{
    direction: {direction};
    text-align: {align};
}}

input, textarea {{
    direction: {direction};
    text-align: {align};
}}


/* EXCLUDE slider */
[data-testid="stSlider"] {{
    direction: ltr !important;
}}
[data-testid="stSlider"] * {{
    direction: ltr !important;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Afbeelding container zelf centreren */
div[data-testid="stImage"] {
    width: fit-content;
    margin-left: auto;
    margin-right: auto;
}

/* Afbeelding binnen de container centreren */
div[data-testid="stImage"] img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* Titels en tekst centreren */
h1, h2, h3, p, label {
    text-align: center !important;
}

/* Login titel exact centreren zonder Streamlit anchor/link-icoontje */
.login-title-text {
    width: 100%;
    text-align: center !important;
    display: block;
    margin: 0 auto 1rem auto;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.2;
}

/* Input labels centreren */
div[data-testid="stTextInput"] label {
    display: flex;
    justify-content: center;
}

/* E-mail input tekst exact centreren */
div[data-testid="stTextInput"] div[data-baseweb="input"] input {
    text-align: center !important;
    box-sizing: border-box !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Wachtwoordveld: compenseer het oogje rechts zodat tekst op dezelfde midden-as komt als e-mail */
div[data-testid="stTextInput"]:has(input[type="password"]) div[data-baseweb="input"] input {
    text-align: center !important;
    padding-left: 5.75rem !important;
    padding-right: 3rem !important;
    box-sizing: border-box !important;
}

/* Oogje zichtbaar houden en vaste breedte geven */
div[data-testid="stTextInput"]:has(input[type="password"]) div[data-baseweb="input"] button {
    width: 2.75rem !important;
    min-width: 2.75rem !important;
}

/* Verberg alleen de tekst "Press Enter to submit form", niet het oogje */
div[data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* Knoppen centreren */
div.stButton {
    display: flex;
    justify-content: center;
}

/* Success/error messages centreren */
div[data-testid="stAlert"] {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


BASE_DIR = Path(__file__).resolve().parent


def vind_databestand(naam):
    # Zoekt een databestand op de plekken waar het kan staan, zodat de app
    # blijft werken ongeacht of de bestanden in "Excel bestanden" staan of
    # gewoon naast dit script (bv. op een andere computer).
    kandidaten = [
        BASE_DIR / naam,
        BASE_DIR / "Excel bestanden" / naam,
        BASE_DIR.parent / "Excel bestanden" / naam,
        BASE_DIR.parent / naam,
    ]
    for pad in kandidaten:
        if pad.exists():
            return pad
    # Niets gevonden: geef het oorspronkelijke pad terug zodat de foutmelding duidelijk blijft.
    return BASE_DIR.parent / "Excel bestanden" / naam


@st.cache_data
def load_data():
    return pd.read_csv(vind_databestand("verwerkte_data_alles.csv"))

@st.cache_data
def load_talen():
    return pd.read_csv(vind_databestand("taal.csv"))

@st.cache_data
def load_data_all():
    return pd.read_csv(vind_databestand("verwerkte_data_geslacht_leeftijd_final.csv"))


df = load_data()
talen = load_talen()
df_alles = load_data_all()

#df = pd.read_csv('verwerkte_data.csv')
#talen = pd.read_csv("taal.csv", sep=';')
#df_alles = pd.read_csv(r"C:\Users\Kirno\Streamlit\verwerkte_data_geslacht_leeftijd_final.csv", sep=';')

talen.columns = talen.columns.str.strip()
talen['key'] = talen['key'].str.strip()
talen = talen.set_index('key')
    
# Voor tabel: naam die je terugkrijgt in sessionstate naar naam die gebruikt wordt in het excelbestand verwerkte_data.csv (df)
mapping = {
    'ex sdnn_1': 'sdnn_1', 
    'ex rmssd_1': 'rmssd_1', 
    'ex nn50_1': 'nn50_1', 
    'ex pnn50_1': 'pnn50_1', 
    'ex sdnn_2': 'sdnn_2', 
    'ex rmssd_2': 'rmssd_2', 
    'ex nn50_2': 'nn50_2', 
    'ex pnn50_2': 'pnn50_2', 
    'ex HR1': 'HR1', 
    'ex HR2': 'HR2', 
    'ex MinHR1': 'MinHR1', 
    'ex MinHR2': 'MinHR2', 
    'ex MaxHR1': 'MaxHR1',
    'ex MaxHR2': 'MaxHR2', 
    'ex STDHR1': 'STDHR1', 
    'ex STDHR2': 'STDHR2', 
    'ex HR Diff': 'HR Diff', 
    'ex mvc bd1': 'mvc Bloeddruk (Bovendruk) 1', 
    'ex mvc bd2': 'mvc Bloeddruk (Bovendruk) 2', 
    'ex mvc ch1': 'mvc Cholesterol 1', 
    'ex mvc ch2': 'mvc Cholesterol 2', 
    'ex mvc non1': 'mvc Non-HDL 1', 
    'ex mvc non2': 'mvc Non-HDL 2', 
    'ex mvc bs1': 'mvc Bloedsuiker 1', 
    'ex mvc bs2': 'mvc Bloedsuiker 2', 
    'ex mvc bmi1': 'mvc BMI 1', 
    'ex mvc bmi2': 'mvc BMI 2', 
    'ex bd gem 1': 'c BD 1 gem', 
    'ex bd gem 2': 'c BD 2 gem', 
    'ex ch gem 1': 'c chol1 gem', 
    'ex ch gem 2': 'c chol2 gem', 
    'ex bs gem 1': 'c bs1 gem', 
    'ex bs gem 2': 'c bs2 gem', 
    'ex bmi gem 1': 'c bmi1 gem', 
    'ex bmi gem 2': 'c bmi2 gem'
}

talen_opties = [
    'Nederlands',
    'English',
    'العربية',
    'Français',
    'Español',
    'Deutsch',
    'Português (Brasil)',
    'Русский',
    '中文',
    '日本語',
    '한국어',
    'हिंदी',
    'বাংলা', #bengali
    'Bahasa Indonesia'
]

CORRECT_EMAIL = "hartstikke@gezond.com"
CORRECT_PASSWORD = "Gezond_hartstikke@321"

#functie die ervoor zorgt dat het makkelijker is om tussen talen te switchen dan hoef je niet elke keer talen.loc['key', st.session_state.taal] te typen
def t(key):
        return talen.loc[key, st.session_state.taal]


def centered_image(image_path, width=200):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    # f"""...""" vervangen door f'...' vanwege een syntax-highlighting probleem.
    # De code werkte wel, maar alles hieronder werd blauw weergegeven.
    # -rik
    st.markdown(f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{encoded}" width="{width}"></div>',unsafe_allow_html=True)


#"hartstikke-gezondweek.png"


# ==========================================================================
#  ONDERZOEKERSDASHBOARD - instellingen en functies (pagina 'dashboard')
#  Werkt op het bestand verwerkte_data_geslacht_leeftijd_final.csv:
#  geslacht zit als kolom-suffix (_man/_vrouw/_anders) en er is een
#  kolom 'leeftijdscategorie' ('40-50', '50-60', '60-70').
# ==========================================================================
DB_KLEUREN = {
    'verhoogd': {'bar': '#e74c3c', 'txt': '#c0392b', 'pil_bg': '#f5b7b1', 'pil_txt': '#a93226', 'icon': '▲'},
    'grens':    {'bar': '#b8860b', 'txt': '#b8860b', 'pil_bg': '#fae5b8', 'pil_txt': '#9a6a00', 'icon': '!'},
    'normaal':  {'bar': '#27ae60', 'txt': '#1e8449', 'pil_bg': '#abebc6', 'pil_txt': '#1e8449', 'icon': '✓'},
    'leeg':     {'bar': '#d5d8dc', 'txt': '#95a5a6', 'pil_bg': '#eaecee', 'pil_txt': '#7f8c8d', 'icon': ''},
}
DB_LABEL = {'verhoogd': 'Verhoogd', 'grens': 'Grenswaarde', 'normaal': 'Normaal', 'leeg': 'Geen data'}
DB_LABEL_BMI = {**DB_LABEL, 'grens': 'Licht Verhoogd'}
DB_STATUS = {
    'Bloeddruk':   {'<120': 'normaal', '120-140': 'grens', '140-180': 'verhoogd', '>180': 'verhoogd'},
    'Cholesterol': {'<5': 'normaal', '5-6.5': 'grens', '6.5-8': 'verhoogd', '>8': 'verhoogd'},
    'Bloedsuiker': {'<7.8': 'normaal', '7.8-11': 'grens', '>11.1': 'verhoogd'},
    'BMI':         {'<18.5': 'grens', '18.5-25': 'normaal', '25-30': 'grens', '>30': 'verhoogd'},
    'Non-HDL':     {'<3.8': 'normaal', '>3.8': 'verhoogd'},
}
DB_EENHEID = {'Bloeddruk': 'mmHg', 'Cholesterol': 'mmol/L', 'Bloedsuiker': 'mmol/L', 'BMI': 'kg/m²', 'Non-HDL': 'mmol/L'}
DB_KOLOMBASIS = {'Bloeddruk': 'mvc Bloeddruk (Bovendruk)', 'Cholesterol': 'mvc Cholesterol',
                 'Bloedsuiker': 'mvc Bloedsuiker', 'BMI': 'mvc BMI', 'Non-HDL': 'mvc Non-HDL'}
DB_ECG_DETAILS = [
    ('SDNN', 'sdnn_', 'ms', 'HRV: variatie tussen hartslagen. Hoger = gezonder.'),
    ('RMSSD', 'rmssd_', 'ms', 'HRV: variatie tussen opeenvolgende hartslagen. Hoger = beter.'),
    ('NN50', 'nn50_', '', 'Aantal intervallen met >50 ms verschil.'),
    ('pNN50', 'pnn50_', '%', 'Percentage van NN50.'),
    ('Gem. hartslag', 'HR', 'bpm', 'Gemiddelde hartritme.'),
    ('Min. hartslag', 'MinHR', 'bpm', 'Laagste hartslag.'),
    ('Max. hartslag', 'MaxHR', 'bpm', 'Hoogste hartslag.'),
    ('SD hartslag', 'STDHR', 'bpm', 'Standaarddeviatie van de hartslag.'),
]
DB_GESLACHT = {'Man': 'man', 'Vrouw': 'vrouw', 'Anders': 'anders'}  # knoplabel -> kolomsuffix


def db_maak_kaart(titel, waarde, eenheid, status):
    """HTML van één kaart: gekleurde balk, waarde, icoon en statuspil."""
    k = DB_KLEUREN[status]
    pil = (DB_LABEL_BMI if titel == 'BMI' else DB_LABEL)[status]
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


def db_status_hartslag(hr):
    """Status op basis van de gemiddelde hartslag (bpm)."""
    if hr is None:
        return 'leeg'
    if hr < 50 or hr > 110:
        return 'verhoogd'
    if hr < 60 or hr > 100:
        return 'grens'
    return 'normaal'


def db_categorie(basis, metingen, geslachten, data):
    """Meest voorkomende categorie over de gekozen meting(en) en geslacht(en)."""
    waarden = [data[f"{basis} {m}_{g}"].dropna().astype(str)
               for m in metingen for g in geslachten if f"{basis} {m}_{g}" in data.columns]
    if not waarden:
        return None
    samen = pd.concat(waarden)
    return samen.mode().iloc[0] if not samen.empty else None


def db_gemiddelde(basis, metingen, geslachten, data):
    """Gemiddelde van een numerieke kolom over de gekozen meting(en) en geslacht(en)."""
    waarden = [pd.to_numeric(data[f"{basis}{m}_{g}"], errors='coerce')
               for m in metingen for g in geslachten if f"{basis}{m}_{g}" in data.columns]
    if not waarden:
        return None
    samen = pd.concat(waarden).dropna()
    return float(samen.mean()) if not samen.empty else None


def db_band_gekozen(band, onder, boven):
    """Valt een leeftijdsband (bv. '50-60') binnen de schuifbalk?"""
    start, eind = band.split('-')
    return int(start) >= onder and int(eind) <= boven


def db_kaart_categorie(metric, metingen, geslachten, selectie):
    cat = db_categorie(DB_KOLOMBASIS[metric], metingen, geslachten, selectie)
    status = DB_STATUS[metric].get(cat, 'leeg') if cat is not None else 'leeg'
    return db_maak_kaart(metric, cat if cat is not None else '—', DB_EENHEID[metric], status)


def db_upload_data():
    """Leest de CSV die onderaan de kaartpagina is geüpload (key='db_upload').
    Geen upload -> standaarddata (df_alles)."""
    upload = st.session_state.get('db_upload')
    if upload is not None:
        try:
            upload.seek(0)
            return pd.read_csv(upload)
        except Exception:
            return df_alles
    return df_alles


def login_screen():
    with open(BASE_DIR / "Login_achtergrond.png", "rb") as img_file:
        encoded_bg = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_bg}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    [data-testid="stForm"] {{
        max-width: 520px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # beweegt mee met resize van tab
    st.markdown(""" 
    <style> 
    /*alleen popover icon */
    [data-testid="stPopover"] button p { 
        font-size: 1.5em; 
        line-height: 1; 
    }

    /*verwijder de pijl*/
    [data-testid="stPopover"] [data-testid="stIconMaterial"] {
        display: none !important;
    }

    /*zorgt ervoor dat er geen border is*/
        [data-testid="stPopover"] button {
        border: none;
        box-shadow: none;
        background: transparent;
        padding: 0;
    }
    </style> 
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([59, 1])

    with col_right:
        with st.popover('⚙'):
            st.selectbox(t('mp taal'), options=talen_opties, key='taal')
            st.slider(label=t('mp lett'), min_value=0.2, max_value=3.5, value=st.session_state.fontsize_scale, step=0.1, key='fontsize_scale')

    scale = st.session_state.fontsize_scale

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {16 * scale}px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown("<div style='height: 8rem'></div>", unsafe_allow_html=True)
    st.markdown(
    f"<div class='login-title-text'>{t('li inloggen')}</div>",
    unsafe_allow_html=True
)

    with st.form("login_form"):
        email = st.text_input(t('li mail')) # "E-mail" veranderd naar t('li mail')
        password = st.text_input(t('li ww'), type="password") # "Wachtwoord" veranderd naar t('li ww')

        col1, col2, col3 = st.columns([4, 2, 4])

        with col2:
            login_button = st.form_submit_button(t('li inloggen'), width="stretch") # "Login" veranderd naar t('li inloggen')

        if login_button:
            if email == CORRECT_EMAIL and password == CORRECT_PASSWORD:
                st.session_state.logged_in = True
                st.success(t('li suc')) # "Succesvol ingelogd!" veranderd naar t('li suc')
                st.rerun()
            else:
                st.error(t('li fout')) # "Onjuiste e-mail of wachtwoord." veranderd naar t('li fout')


def main_app():
    
    # layout
    # Op de dashboardpagina verbergen we de filterkolom (col1) zodat het
    # dashboard de volle breedte krijgt; de dashboardfilters staan in de sidebar.

    if st.session_state.pagina == 'dashboard':
        col2 = st.container()
    else:
        col1, col2 = st.columns([1, 4], vertical_alignment="top")

        # linker kolom = filters
        with col1:

            st.markdown("<div style='height: 6rem'></div>", unsafe_allow_html=True)


            with st.expander(t('mp filter'), expanded=False): # beide de grafiek en tabel kunnen in een st.container (?)

                var_keys = pd.concat([talen.loc["ex sdnn_1":"ex HR Diff"],talen.loc["ex bd gem 1":"ex bmi gem 2"]]).index.tolist()

                geselecteerde_variabelen = st.multiselect(t('mp kies v'), #return = keys van geselecteerde waarden, dus niet de waarden die de gebruiker ziet.
                                                      options=var_keys, #lijst met opties
                                                      default=st.session_state.variabelen, #als er niks gekozen is, is het leeg
                                                      format_func=lambda x: talen.loc[x, st.session_state.taal], 
                                                      placeholder=t('menu co')
                                                     )


                # zorgt ervoor dat de keys die nu indexes zijn in een lijst worden gezet
                mvc_keys = talen.loc["ex mvc bd1":"ex mvc bmi2"].index.tolist()

                geslacht_keys = talen.loc['man':'anders'].index.tolist()



    # rechter kolom
    
    
    with col2:

        # pagina 1 = kaart
        if st.session_state.pagina == 'kaart':

            header = st.container()

            with header:
                hcol1, hcol2 = st.columns([59, 1])
                with hcol1:
                    st.markdown(
                    f"<h1 style='margin:0'>{t('mp tit kaart')}</h1>",
                    unsafe_allow_html=True
                    )

                with hcol2:
                    st.markdown(""" 
                    <style> 
                    /*alleen popover icon */
                    [data-testid="stPopover"] button p { 
                        font-size: 1.5em; 
                        line-height: 1; 
                    }

                    /*verwijder de pijl (expand_less) */
                    [data-testid="stPopover"] [data-testid="stIconMaterial"] {
                        display: none !important;
                    }

                    /*hoogte van de popover in relatie met de rest*/
                    [data-testid="stPopover"] {
                        position: relative;
                        top: 30px;
                    }

                    /*zorgt ervoor dat er geen border is*/
                    [data-testid="stPopover"] button {
                        border: none;
                        box-shadow: none;
                        background: transparent;
                        padding: 0;
                    }
                    </style> 
                    """, unsafe_allow_html=True)  
                    
                    with st.popover('⚙'):
                        selectionbox = st.selectbox(t('mp taal'),options=talen_opties,key='taal')
                        ##index=talen_opties.index(st.session_state.taal)
                        st.slider(label=t('mp lett'), min_value=0.2, max_value=3.5, value=st.session_state.fontsize_scale, step=0.1, key='fontsize_scale')

            scale = st.session_state.fontsize_scale

            st.markdown(
                f"""
                <style>
                html, body, [class*="css"] {{
                    font-size: {16 * scale}px;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

            # Databron voor de kaart: ALLEEN de onderaan geüploade CSV (key='db_upload').
            # Geen upload  -> lege kaart zonder kleur.
            # Wel upload   -> kaart inkleuren met de geüploade data.
            db_upload_kaart = st.session_state.get('db_upload')
            df_geupload_kaart = None
            if db_upload_kaart is not None:
                try:
                    db_upload_kaart.seek(0)
                    df_geupload_kaart = pd.read_csv(db_upload_kaart)
                except Exception:
                    df_geupload_kaart = None

            heeft_upload = (df_geupload_kaart is not None and 'Wijk' in df_geupload_kaart.columns)

            def kaart_waarde_per_wijk(kolom, data):
                # Eén waarde per wijk voor de kaartkleur. Werkt zowel met platte kolommen
                # (kolom) als met geslacht-gesuffixte kolommen (kolom_man/_vrouw/_anders).
                # De geslachten worden samengevoegd: categorieën -> meest voorkomende waarde,
                # getallen -> gemiddelde.
                kolommen = [kolom + s for s in ['', '_man', '_vrouw', '_anders'] if (kolom + s) in data.columns]
                if not kolommen:
                    return None
                is_numeriek = pd.to_numeric(data[kolommen[0]], errors='coerce').notna().any()
                resultaat = {}
                for wijk, groep in data.groupby('Wijk'):
                    samen = pd.concat([groep[k] for k in kolommen])
                    if is_numeriek:
                        getallen = pd.to_numeric(samen, errors='coerce').dropna()
                        resultaat[str(wijk).strip()] = round(float(getallen.mean()), 1) if not getallen.empty else None
                    else:
                        tekst = samen.dropna().astype(str)
                        resultaat[str(wijk).strip()] = tekst.mode().iloc[0] if not tekst.empty else None
                return resultaat

            try:

                buurten = gpd.read_file('https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=INDELING_GEBIED&THEMA=gebiedsindeling')

                buurten["kaart_id"] = buurten.index.astype(str)
                buurten["Gebied"] = buurten["Gebied"].astype(str).str.strip()

                st.session_state.variabelen = geselecteerde_variabelen

                if not heeft_upload:
                    # GEEN upload: lege kaart zonder kleur en zonder data.
                    # Volledig transparante vulling; alleen de gebiedsgrenzen blijven zichtbaar.
                    fig2 = go.Figure(go.Choroplethmapbox(
                        geojson=buurten.set_index("kaart_id").__geo_interface__,
                        locations=buurten["kaart_id"],
                        z=[0] * len(buurten),
                        colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,0,0,0)']],  # 100% transparant = geen kleur
                        showscale=False,
                        marker=dict(line=dict(width=1, color='#9aa0a6'), opacity=1),
                        hoverinfo='skip',  # geen data tonen
                    ))
                    fig2.update_layout(
                        mapbox_style="carto-positron",
                        mapbox_zoom=9.5,
                        mapbox_center={"lat": 52.37, "lon": 4.89},
                        margin=dict(l=0, r=0, t=0, b=0),
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                    st.info("Upload onderaan een CSV-bestand om de kaart in te kleuren.")

                else:
                    # WEL upload: welke kolom(men) kleuren we? Per variabele de kolomnaam
                    # én de weergavenaam (zoals in de gekozen taal) bewaren.
                    if len(st.session_state.variabelen) > 0:
                        kleur_items = [(mapping[k], talen.loc[k, st.session_state.taal]) for k in st.session_state.variabelen]
                    else:
                        kleur_items = [("mvc BMI 1", "BMI")]

                    for index, label in kleur_items:
                        waarden_per_wijk = kaart_waarde_per_wijk(index, df_geupload_kaart)
                        if not waarden_per_wijk:
                            st.warning(f"'{label}' staat niet in het geüploade bestand, dus deze kan niet ingekleurd worden.")
                            continue

                        # de weergavenaam als kolomnaam gebruiken, zodat de kleurenschaal
                        # en de hover de gekozen variabele tonen
                        buurten_kaart = buurten.copy()
                        buurten_kaart[label] = buurten_kaart["Gebied"].map(waarden_per_wijk)

                        fig2 = px.choropleth_mapbox(
                            buurten_kaart,
                            geojson=buurten_kaart.set_index("kaart_id").__geo_interface__,
                            locations="kaart_id",
                            color=label,
                            hover_name='Gebied',                       # wijknaam bovenaan de hover
                            hover_data={label: True, "kaart_id": False},  # variabele tonen, kaart_id verbergen
                            mapbox_style="carto-positron",
                            zoom=9.5,
                            center={"lat": 52.37, "lon": 4.89},
                            opacity=0.45,
                            color_continuous_scale="RdYlGn_r"
                        )

                        fig2.update_layout(
                            margin=dict(l=0, r=0, t=0, b=0) #verwijderd marges (l=left, r=right, t=top, b=bottom)
                        )

                        st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.image('Pythoncode/amsterdam-map.jpg')
                st.warning("Kaart kon niet geladen worden, fallback wordt gebruikt.")
                st.error(str(e))

            # ----- onderaan de kaartpagina: dashboard openen + CSV uploaden -----
            st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
            st.divider()

            onder_links, onder_rechts = st.columns([1, 2], vertical_alignment="center")
            with onder_links:
                if st.button('📊 Onderzoekersdashboard openen'):
                    st.session_state.pagina = 'dashboard'
                    st.rerun()
            with onder_rechts:
                st.file_uploader(
                    'Upload een CSV-bestand met metingen om de kaart in te kleuren en het dashboard te vullen',
                    type=['csv'],
                    key='db_upload'
                )

        #_____________________________________________________________________________________
        # pagina 2 = grafieken
    
        elif st.session_state.pagina == 'grafiek':
    
            st.title(t('gr tit g'))
    
            # terug knop
            if st.button(t('gr but terug')):
    
                st.session_state.pagina = 'kaart'
    
                st.rerun()
    
            # geselecteerde data
            filtered_df_graf = df[
                df['Wijk'].isin(st.session_state.wijken_graf)
            ]
    
            # grafieken
            if len(st.session_state.variabelen) > 0: 
    
                grafiek_cols = st.columns(len(st.session_state.variabelen)) # zorgt ervoor dat er zoveel grafieken naast elkaar komen als er gekozen zijn dus als 
                                                                            # er 4 variabelen zijn gekozen heb je 4 kolommen (4 grafieken naast elkaar
    
                for i, variabele_key in enumerate(st.session_state.variabelen): # enumerate geeft zowel de index als het element terug
                                                                                # dus: for index, element in st.session_state.variabelen
                    
                    # vertaling naar dataframe kolomnaam
                    variabele = mapping[variabele_key]
    
                    fig = px.bar(
                        filtered_df_graf,
                        x='Wijk',
                        y=variabele,
                        color='Wijk',
                        title=f"{talen.loc[variabele_key, st.session_state.taal]} {t('gr per wijk')}",
    
                        labels={variabele: talen.loc[variabele_key, st.session_state.taal]}
                    )
    
                    fig.update_layout(xaxis_title=t('ta wijk'), yaxis_title=talen.loc[variabele_key, st.session_state.taal], legend_title=t('ta wijk'))
    
                    grafiek_cols[i].plotly_chart(
                        fig,
                        use_container_width=True
                    )
    
            else:
    
                st.warning(t('gr war 1 v'))
                
    
        #_____________________________________________________________________________________
        # pagina 3 = tabellen
    
        elif st.session_state.pagina == 'tabel':
    
            st.title(t('ta tit tab')) #lol
    
            # terug knop
            if st.button(t('ta but terug')):
    
                st.session_state.pagina = 'kaart'
    
                st.rerun()
                
        
            # tabellen
            if len(st.session_state.mvc) > 0:
    
                gekozen_kolommen = [mapping[k] for k in st.session_state.mvc if k in mapping]
    
                # filter op geselecteerde wijken
                df_tabel = df[df['Wijk'].isin(st.session_state.wijken_tab)][['Wijk'] + gekozen_kolommen].copy()
    
                nieuwe_kolomnamen = ([t('ta wijk')] + [talen.loc[mvc, st.session_state.taal] for mvc in st.session_state.mvc if mvc in mapping])
    
                df_tabel.columns = nieuwe_kolomnamen
    
                st.table(df_tabel)
    
            else:
                st.warning(t('ta war 1 v'))

        #_____________________________________________________________________________________
        # pagina 'dashboard' = onderzoekersdashboard (HARTstikke Gezond)
        elif st.session_state.pagina == 'dashboard':

            # terug-knop
            if st.button('⬅ Terug naar kaart'):
                st.session_state.pagina = 'kaart'
                st.rerun()

            # titel met logo
            db_logo_pad = vind_databestand("hartstikke-gezondweek.png")
            db_logo_html = (f'<img src="data:image/png;base64,{base64.b64encode(db_logo_pad.read_bytes()).decode()}" '
                            f'style="height:56px;">') if db_logo_pad.exists() else ''
            st.markdown("<div style='display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap;margin-bottom:.4rem'>"
                        "<span style='font-size:2.3rem'>❤️</span>"
                        "<span style='font-size:2.3rem;font-weight:800;color:#1c2833'>HARTstikke Gezond Dashboard</span>"
                        f"{db_logo_html}</div>", unsafe_allow_html=True)

            # data: dezelfde upload als de kaart (onderaan de kaartpagina), anders de standaarddata
            db_data = db_upload_data()

            # filters in de zijbalk
            st.sidebar.header('Dashboard-filters')
            db_locatie = st.sidebar.selectbox('Locatie (wijk)', ['Alle locaties'] + sorted(db_data['Wijk'].dropna().unique().tolist()))
            db_meting_keuze = st.sidebar.radio('Meting', ['1 (voormeting)', '2 (nameting)', 'Beide metingen'])
            db_metingen = ['1'] if db_meting_keuze.startswith('1') else ['2'] if db_meting_keuze.startswith('2') else ['1', '2']
            db_onder, db_boven = st.sidebar.slider('Leeftijd', 40, 70, (40, 70), step=10)
            db_geslacht_keuze = st.sidebar.multiselect('Geslacht', list(DB_GESLACHT), default=list(DB_GESLACHT))
            db_geslachten = [DB_GESLACHT[g] for g in db_geslacht_keuze]

            # filters toepassen op de rijen
            db_selectie = db_data.copy()
            if db_locatie != 'Alle locaties':
                db_selectie = db_selectie[db_selectie['Wijk'] == db_locatie]
            db_selectie = db_selectie[db_selectie['leeftijdscategorie'].apply(lambda b: db_band_gekozen(b, db_onder, db_boven))]

            # ondertitel
            db_wijk_tekst = db_locatie if db_locatie != 'Alle locaties' else 'alle wijken'
            db_meting_tekst = 'beide metingen' if len(db_metingen) == 2 else ('voormeting' if db_metingen == ['1'] else 'nameting')
            st.markdown(f"<div style='text-align:center;color:#5d6d7e;margin:.4rem 0 1.4rem 0'>{db_wijk_tekst} · "
                        f"{db_onder}–{db_boven} jaar · {', '.join(db_geslacht_keuze) or 'geen'} · {db_meting_tekst}</div>",
                        unsafe_allow_html=True)

            if db_selectie.empty or not db_geslachten:
                st.warning('Geen data voor deze selectie. Pas de filters aan.')
            else:
                # kaarten (rij 1)
                db_rij1 = st.columns(3)
                for db_kol, db_metric in zip(db_rij1, ['Bloeddruk', 'Cholesterol', 'Bloedsuiker']):
                    db_kol.markdown(db_kaart_categorie(db_metric, db_metingen, db_geslachten, db_selectie), unsafe_allow_html=True)

                st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

                # kaarten (rij 2: BMI, Non-HDL, ECG)
                db_hr = db_gemiddelde('HR', db_metingen, db_geslachten, db_selectie)
                db_rij2 = st.columns(3)
                db_rij2[0].markdown(db_kaart_categorie('BMI', db_metingen, db_geslachten, db_selectie), unsafe_allow_html=True)
                db_rij2[1].markdown(db_kaart_categorie('Non-HDL', db_metingen, db_geslachten, db_selectie), unsafe_allow_html=True)
                db_rij2[2].markdown(db_maak_kaart('ECG (hartritme)', f"{db_hr:.0f}" if db_hr is not None else '—', 'bpm', db_status_hartslag(db_hr)), unsafe_allow_html=True)

                # legenda
                st.markdown("<div style='display:flex;gap:36px;justify-content:center;flex-wrap:wrap;border-top:1px solid #e5e8e8;"
                            "margin-top:1.8rem;padding-top:1rem;color:#34495e'><span>🔴 Verhoogd / actie vereist</span>"
                            "<span>🟠 Grenswaarde / let op</span><span>🟢 Normaal</span></div>", unsafe_allow_html=True)

                # ECG / HRV-details
                with st.expander('🫀 ECG / HRV-details (met toelichting)'):
                    db_rijen = []
                    for db_naam, db_basis, db_eenheid, db_uitleg in DB_ECG_DETAILS:
                        db_v = db_gemiddelde(db_basis, db_metingen, db_geslachten, db_selectie)
                        db_rijen.append({'Meetwaarde': db_naam,
                                         'Waarde': f"{db_v:.1f} {db_eenheid}".strip() if db_v is not None else '—',
                                         'Toelichting': db_uitleg})
                    st.dataframe(pd.DataFrame(db_rijen), hide_index=True, use_container_width=True)

                # gefilterde data + download
                with st.expander('📄 Gefilterde data bekijken / downloaden'):
                    st.dataframe(db_selectie, use_container_width=True)
                    st.download_button('⬇️ Download als CSV', db_selectie.to_csv(index=False).encode('utf-8'),
                                       'gefilterde_metingen.csv', 'text/csv')

    # Uitloggen helemaal onderaan links, onder de dashboard
    st.markdown("<div style='height: 3rem'></div>", unsafe_allow_html=True)

    logout_col1, logout_col2 = st.columns([1, 4], vertical_alignment="top")

    with logout_col1:
        if st.button(t('li lu')):
            st.session_state.logged_in = False
            st.rerun()


#app starten

if st.session_state.logged_in:
    main_app()
else:
    login_screen()

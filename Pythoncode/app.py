import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
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

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR.parent / "Excel bestanden" / "verwerkte_data_alles.csv")

@st.cache_data
def load_talen():
    return pd.read_csv(BASE_DIR.parent / "Excel bestanden" / "taal.csv")

@st.cache_data
def load_data_all():
    return pd.read_csv(BASE_DIR.parent / "Excel bestanden" / "verwerkte_data_geslacht_leeftijd_final.csv")


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

#CORRECT_EMAIL = "jan_pieters@gmail.com"
#CORRECT_PASSWORD = "Hartstikke_gezond123"

# in \streamlit.\secrets.toml staan de inlog gegevens.
CORRECT_EMAIL = st.secrets["inloggen"]["email"]
CORRECT_PASSWORD = st.secrets["inloggen"]["password"]

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

def login_screen():

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

    col_left, col_image, col_right = st.columns([1, 58, 1])
    
    with col_image:
        centered_image(BASE_DIR / "hartstikke-gezondweek.png", width=200)
        #centered_image("hartstikke-gezondweek.png", width=200)
        st.write("")
        st.write("") #zorgt ervoor dat er ruimte tussen het plaatje en de markdown + form is, ik hoop dat dit oke is. 
        #             Het is namelijk wel minder dan eerst (niet veel tho) 
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
    
    col1, col2 = st.columns([1, 4], vertical_alignment="top")
    
    
    # linker kolom = filters
    
    
    with col1:

        st.markdown("<div style='height: 6rem'></div>", unsafe_allow_html=True)
        
                     
        with st.expander(t('mp filter'), expanded=False): # beide de grafiek en tabel kunnen in een st.container (?)

            geselecteerde_wijken_grafiek = st.multiselect(
                t('mp wijk g'),
                options=df['Wijk'].unique(),
                default=st.session_state.wijken_graf,
                placeholder=t('menu co')
            )


            var_keys = pd.concat([talen.loc["ex sdnn_1":"ex HR Diff"],talen.loc["ex bd gem 1":"ex bmi gem 2"]]).index.tolist()

            geselecteerde_variabelen = st.multiselect(t('mp kies v'), #return = keys van geselecteerde waarden, dus niet de waarden die de gebruiker ziet.
                                                  options=var_keys, #lijst met opties
                                                  default=st.session_state.variabelen, #als er niks gekozen is, is het leeg
                                                  format_func=lambda x: talen.loc[x, st.session_state.taal], 
                                                  placeholder=t('menu co')
                                                 )

        
        
       

            # knop
            if st.button(t('mp toon g')):

                st.session_state.wijken_graf = geselecteerde_wijken_grafiek
                st.session_state.variabelen = geselecteerde_variabelen

                st.session_state.pagina = 'grafiek'

                st.rerun()
    
            geselecteerde_wijken_tabel = st.multiselect(
                t('mp wijk t'),
                options=df['Wijk'].unique(),
                default=st.session_state.wijken_tab,
                placeholder=t('menu co')
            )


            # zorgt ervoor dat de keys die nu indexes zijn in een lijst worden gezet
            mvc_keys = talen.loc["ex mvc bd1":"ex mvc bmi2"].index.tolist()


            meest_voorkomende_categorieën = st.multiselect(t('mp mvc'), # return = keys van geselecteerde waarden, dus niet de waarden die de gebruiker ziet.
                                                           options=mvc_keys, #lijst met opties
                                                           default=st.session_state.mvc, #als er niks gekozen is, is het leeg
                                                           format_func=lambda x: talen.loc[x, st.session_state.taal], #
                                                           placeholder=t('menu co')
                                                          )
        
            # knop
            if st.button(t('mp toon t')):

                st.session_state.wijken_tab = geselecteerde_wijken_tabel
                st.session_state.mvc = meest_voorkomende_categorieën

                st.session_state.pagina = 'tabel'

                st.rerun()


            leeftijds_categorie = st.multiselect(t('mp leeftijd'), 
                                                 options = ['40-50', '50-60', '60-70'],
                                                 default = st.session_state.leeftijd,
                                                 placeholder = t('mp leeftijd')
                                                )
            
            geslacht_keys = talen.loc['man':'anders'].index.tolist()
            geslacht_kiezen = st.multiselect(t('mp geslacht'),
                                             options = geslacht_keys,
                                             default = st.session_state.geslacht,
                                             format_func =lambda x: talen.loc[x, st.session_state.taal],
                                             placeholder = t('mp geslacht')
                                            )
                                                                     


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
            

        
            try:
                buurten = gpd.read_file('https://maps.amsterdam.nl/open_geodata/geojson_lnglat.php?KAARTLAAG=INDELING_GEBIED&THEMA=gebiedsindeling')
        
                fig2 = px.choropleth_mapbox(
                    buurten,
                    geojson=buurten.__geo_interface__,
                    locations=buurten.index,
                    featureidkey="id", 
                    color=buurten.index,
                    hover_name = 'Gebied',
                    mapbox_style="carto-positron",
                    zoom=9.5,
                    center={"lat": 52.37, "lon": 4.89},
                    opacity=0.45,
                )

                fig2.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0) #verwijderd marges (l=left, r=right, t=top, b=bottom), als je het weer naar het origineel wil hebben zonder dat de bovenkant weer ver van de titel af staat doe: t=0, b=140, toegevoegd omdat ik de kaart op de grafiek wou hebben met zo min mogelijk marge.
                )

                st.plotly_chart(fig2, use_container_width=True)

        
            except Exception as e:
                st.image('Pythoncode/amsterdam-map.jpg')
                st.warning("Kaart kon niet geladen worden, fallback wordt gebruikt.")
                st.error(str(e))
    
    #_____________________________________________________________________________________
        # pagina 2 = grafieken (tijdelijke visualisatie, Nina mag alles netjes gaan neerzetten :)) miss is het fijn om te kunnen wisselen tussen grafiek en tabel met 1 klik door gebruik te maken van pagina's zoals beschreven in het 2e hoorcollege op het JMH
    
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
        # pagina 3 = tabellen (tijdelijke visualisatie, Nina mag alles netjes gaan zetten :)), miss is het fijn om te kunnen wisselen tussen grafiek en tabel met 1 klik door gebruik te maken van pagina's zoals beschreven in het 2e hoorcollege op het JMH
        # af en toe zit er een waarde in het tabel die een beetje ~wonkie~ is lol, geen idee waar dit door komt, miss door de manier hoe ik de tabellen op het gezet (?)
        # Ik heb het idee dat alle waarden met > ervoor dus ~wonkie~ worden, succes!!!
    
    
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

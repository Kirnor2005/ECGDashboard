import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

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

/* Input labels centreren */
div[data-testid="stTextInput"] label {
    display: flex;
    justify-content: center;
}

/* Input tekst centreren */
div[data-testid="stTextInput"] input {
    text-align: center !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* Wachtwoord-oogje/verbergknop weghalen */
div[data-testid="stTextInput"] button {
    display: none !important;
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
    return pd.read_csv(BASE_DIR.parent / "Excel bestanden" / "verwerkte_data.csv")

@st.cache_data
def load_talen():
    return pd.read_csv(BASE_DIR.parent / "Excel bestanden" / "taal.csv", sep=';')

df = load_data()
talen = load_talen()

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

CORRECT_EMAIL = "jeemail@gmail.com"
CORRECT_PASSWORD = "Hartstikke_gezond123"

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
    
if 'taal' not in st.session_state:
        st.session_state.taal = 'English'
    
if 'mvc' not in st.session_state:
        st.session_state.mvc = []

#functie die ervoor zorgt dat het makkelijker is om tussen talen te switchen dan hoef je niet elke keer talen.loc['key', st.session_state.taal] te typen
def t(key):
        return talen.loc[key, st.session_state.taal]


#"hartstikke-gezondweek.png"

def login_screen():
    st.image('Pythoncode/hartstikke-gezondweek.png', width=200)

    st.title(t('li inloggen'))

    email = st.text_input(t('li mail'))
    password = st.text_input(t('li ww'), type="password")

    if st.button(t('li inloggen')):
        if email == CORRECT_EMAIL and password == CORRECT_PASSWORD:
            st.session_state.logged_in = True
            st.success("Succesvol ingelogd!")
            st.rerun()
        else:
            st.error("Onjuiste e-mail of wachtwoord.")


def main_app():

    st.set_page_config(layout="wide")
    
    # data
    
    #df = pd.read_csv('verwerkte_data.csv')
    
    
    #talen = pd.read_csv("taal.csv", sep=';')
    #talen.columns = talen.columns.str.strip()
    #talen['key'] = talen['key'].str.strip()
    #talen = talen.set_index('key')
    
    # Voor tabel: naam die je terugkrijgt in sessionstate naar naam die gebruikt wordt in het excelbestand verwerkte_data.csv (df)
    #mapping = {
    #    'ex sdnn_1': 'sdnn_1', 
    #    'ex rmssd_1': 'rmssd_1', 
    #    'ex nn50_1': 'nn50_1', 
    #    'ex pnn50_1': 'pnn50_1', 
    #    'ex sdnn_2': 'sdnn_2', 
    #    'ex rmssd_2': 'rmssd_2', 
    #    'ex nn50_2': 'nn50_2', 
    #    'ex pnn50_2': 'pnn50_2', 
    #    'ex HR1': 'HR1', 
    #    'ex HR2': 'HR2', 
    #    'ex MinHR1': 'MinHR1', 
    #    'ex MinHR2': 'MinHR2', 
    #    'ex MaxHR1': 'MaxHR1',
    #    'ex MaxHR2': 'MaxHR2', 
    #    'ex STDHR1': 'STDHR1', 
    #    'ex STDHR2': 'STDHR2', 
    #    'ex HR Diff': 'HR Diff', 
   #     'ex mvc bd1': 'mvc Bloeddruk (Bovendruk) 1', 
   #     'ex mvc bd2': 'mvc Bloeddruk (Bovendruk) 2', 
   #     'ex mvc ch1': 'mvc Cholesterol 1', 
   #     'ex mvc ch2': 'mvc Cholesterol 2', 
   #     'ex mvc non1': 'mvc Non-HDL 1', 
   #     'ex mvc non2': 'mvc Non-HDL 2', 
   #     'ex mvc bs1': 'mvc Bloedsuiker 1', 
   #     'ex mvc bs2': 'mvc Bloedsuiker 2', 
   #     'ex mvc bmi1': 'mvc BMI 1', 
   #     'ex mvc bmi2': 'mvc BMI 2', 
   #     'ex bd gem 1': 'c BD 1 gem', 
   #     'ex bd gem 2': 'c BD 2 gem', 
   #     'ex ch gem 1': 'c chol1 gem', 
   #     'ex ch gem 2': 'c chol2 gem', 
   #     'ex bs gem 1': 'c bs1 gem', 
   #     'ex bs gem 2': 'c bs2 gem', 
   #     'ex bmi gem 1': 'c bmi1 gem', 
   #     'ex bmi gem 2': 'c bmi2 gem'
   # }
    
    
    # session state
    
    #if 'pagina' not in st.session_state:
     #   st.session_state.pagina = 'kaart'
    
    #if 'wijken_graf' not in st.session_state:
     #   st.session_state.wijken_graf = []
    
    #if 'wijken_tab' not in st.session_state:
     #   st.session_state.wijken_tab = []
    
    #if 'variabelen' not in st.session_state:
     #   st.session_state.variabelen = []
    
    #if 'taal' not in st.session_state:
     #   st.session_state.taal = 'English'
    
    #if 'mvc' not in st.session_state:
     #   st.session_state.mvc = []
    
    
    #functie die ervoor zorgt dat het makkelijker is om tussen talen te switchen dan hoef je niet elke keer talen.loc['key', st.session_state.taal] te typen
    #def t(key):
     #   return talen.loc[key, st.session_state.taal]
    
    
    # layout
    
    col1, col2 = st.columns([1, 4], vertical_alignment="top")
    
    
    # linker kolom = filters
    
    
    with col1:

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        if st.button(t('li lu')):
            st.session_state.logged_in = False
            st.rerun()

        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    
        with st.expander(t('mp Opties'), expanded=False):
            font = st.slider(
                t('mp lett'), 
                min_value=2, 
                max_value=26, 
                value=12, 
                step=2
            )
    
            talen_opties = [
                'Nederlands',
                'English',
                'العربية',
                'Français',
                'Español',
                'Deutsch',
                'Português',
                'Русский',
                '中文',
                '日本語',
                '한국인'
            ]
    
            selectionbox = st.selectbox(
                t('mp taal'),
                options=talen_opties,
                index=talen_opties.index(st.session_state.taal),
                key='taal'
            )
            
                         
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
    
    
    # rechter kolom
    
    
    with col2:
    
        # pagina 1 = kaart
    
        if st.session_state.pagina == 'kaart':
    
            st.title(t('mp tit kaart'))
    
            st.image(
                'Pythoncode/amsterdam-map.jpg',
                use_container_width=True
            )
    
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


#app starten

if st.session_state.logged_in:
    main_app()
else:
    login_screen()

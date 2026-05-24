import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# data

df = pd.read_csv('verwerkte_data.csv')

# talen = csv met talen en alle tekst: [key Nederlands English العربية, map kaart map بطاقة, etc.]
# en dan bij tekst talen.loc["map", st.session_state.taal]

# of met functie: 
# def t(key):
#     return talen.loc[key, st.session_state.taal]
# 
# st.title(t("map"))

# session state

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


# layout

col1, col2 = st.columns([1, 4], vertical_alignment="top")


# linker kolom = filters


with col1:

    st.markdown("<div style='height: 5rem'></div>", unsafe_allow_html=True)

    with st.expander('Options', expanded=False):
        font = st.slider(
            'letter grootte', 
            min_value=2, 
            max_value=26, 
            value=12, 
            step=2
        )

        taal = st.selectbox('Taal', 
                            options=['Nederlands', 'English', 'العربية', 'Français', 'Español', 'Deutsch', 'Português', 'Русский', '中文 (Zhōngwén)', '日本語', '한국인'], 
                            index=1  # English
                           )
                     
    with st.expander('Filters', expanded=False): # beide de grafiek en tabel kunnen in een st.container (?)

        geselecteerde_wijken_grafiek = st.multiselect(
            'Kies wijken voor grafiek',
            options=df['Wijk'].unique(),
            default=st.session_state.wijken_graf
        )

        exclude = ['Wijk',
                   'mvc Bloeddruk (Bovendruk) 1', 
                   'mvc Bloeddruk (Bovendruk) 2', 
                   'mvc Cholesterol 1', 
                   'mvc Cholesterol 2', 
                   'mvc Non-HDL 1', 
                   'mvc Non-HDL 2', 
                   'mvc Bloedsuiker 1', 
                   'mvc Bloedsuiker 2',
                   'mvc BMI 1',
                   'mvc BMI 2'
                  ]

        options = [col for col in df.columns if col not in exclude]

        geselecteerde_variabelen = st.multiselect(
            'Kies variabelen',
            options=options,
            default=[v for v in st.session_state.variabelen if v in options]
        )

        # knop
        if st.button('Toon grafiek(en)'):

            st.session_state.wijken_graf = geselecteerde_wijken_grafiek
            st.session_state.variabelen = geselecteerde_variabelen

            st.session_state.pagina = 'grafiek'

            st.rerun()

        geselecteerde_wijken_tabel = st.multiselect(
            'Kies wijken voor tabel',
            options=df['Wijk'].unique(),
            default=st.session_state.wijken_tab
        )

        meest_voorkomende_categorieën = st.multiselect('Kies meest voorkomende categorie(ën)',
                                                   options=[
                                                   'Bloeddruk (Bovendruk) 1', 
                                                   'Bloeddruk (Bovendruk) 2', 
                                                   'Cholesterol 1', 
                                                   'Cholesterol 2', 
                                                   'Non-HDL 1',
                                                   'Non-HDL 2',
                                                   'Bloedsuiker 1', 
                                                   'Bloedsuiker 2', 
                                                   'BMI 1', 
                                                   'BMI 2'
                                                   ],
                                                   default=st.session_state.mvc
                                                  )
        # knop
        if st.button('Toon tabel'):

            st.session_state.wijken_tab = geselecteerde_wijken_tabel
            st.session_state.mvc = meest_voorkomende_categorieën

            st.session_state.pagina = 'tabel'

            st.rerun()


# rechter kolom


with col2:

    # pagina 1 = kaart

    if st.session_state.pagina == 'kaart':

        st.title('Kaart van Amsterdam')

        st.image(
            'amsterdam-map.jpg',
            use_container_width=True
        )

#_____________________________________________________________________________________
    # pagina 2 = grafieken (tijdelijke visualisatie, Nina mag alles netjes gaan neerzetten :)) miss is het fijn om te kunnen wisselen tussen grafiek en tabel met 1 klik door gebruik te maken van pagina's zoals beschreven in het 2e hoorcollege op het JMH

    elif st.session_state.pagina == 'grafiek':

        st.title('Grafiek(en)')

        # terug knop
        if st.button('← Terug naar kaart'):

            st.session_state.pagina = 'kaart'

            st.rerun()

        # geselecteerde data
        filtered_df_graf = df[
            df['Wijk'].isin(st.session_state.wijken_graf)
        ]

        # grafieken
        if len(st.session_state.variabelen) > 0:

            grafiek_cols = st.columns(
                len(st.session_state.variabelen)
            )

            for i, variabele in enumerate(
                st.session_state.variabelen
            ):

                fig = px.bar(
                    filtered_df_graf,
                    x='Wijk',
                    y=variabele,
                    color='Wijk',
                    title=f'{variabele.upper()} per wijk'
                )

                grafiek_cols[i].plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.warning('Selecteer minimaal één variabele.')

#_____________________________________________________________________________________
    # pagina 3 = tabellen (tijdelijke visualisatie, Nina mag alles netjes gaan zetten :)), miss is het fijn om te kunnen wisselen tussen grafiek en tabel met 1 klik door gebruik te maken van pagina's zoals beschreven in het 2e hoorcollege op het JMH
    # af en toe zit er een waarde in het tabel die een beetje ~wonkie~ is lol, geen idee waar dit door komt, miss door de manier hoe ik de tabellen op het gezet (?)
    
    elif st.session_state.pagina == 'tabel':

        st.title('tabel(len)')

        # terug knop
        if st.button('← Terug naar kaart'):

            st.session_state.pagina = 'kaart'

            st.rerun()

        # geselecteerde data
        filtered_df_tab = df[df['Wijk'].isin(st.session_state.wijken_tab)]

        # tabellen
        if len(st.session_state.mvc) > 0:

            kolommen = ['Wijk'] + [f'mvc {mvc}' for mvc in st.session_state.mvc]

            kolommen = [k for k in kolommen if k in filtered_df_tab.columns]

            st.table(filtered_df_tab[kolommen])
        
        

        else:

            st.warning('Selecteer minimaal één variabele.')

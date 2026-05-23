import streamlit as st
import pandas as pd
import plotly.express as px

# data

df = pd.read_csv('data_verwerkt_goedeversie.csv')

# session state

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'kaart'

if 'wijken' not in st.session_state:
    st.session_state.wijken = []

if 'variabelen' not in st.session_state:
    st.session_state.variabelen = []

if 'taal' not in st.session_state:
    st.session_state.taal = 'English'


# layout

col1, col2 = st.columns([1, 4])


# linker kolom = filters


with col1:

    with st.expander('Options', expanded=True):
        font = st.slider(
            'letter grootte', 
            min_value=2, 
            max_value=26, 
            value=12, 
            step=2
        )

        taal = st.multiselect(
            'Taal',
            options=['Nederlands', 'English', 'العربية', 'Français', 'Español', 'Deutsch', 'Português', 'Русский', '中文 (Zhōngwén)', '日本語', '한국인'],
            default=st.session_state.taal
        )
                     
    with st.expander('Filters', expanded=True):

        geselecteerde_wijken = st.multiselect(
            'Kies wijken',
            options=df['Wijk'].unique(),
            default=st.session_state.wijken
        )

        geselecteerde_variabelen = st.multiselect(
            'Kies variabelen',
            options=df.columns[1:],
            default=st.session_state.variabelen
        )

        # knop
        if st.button('Toon resultaten'):

            st.session_state.wijken = geselecteerde_wijken
            st.session_state.variabelen = geselecteerde_variabelen

            st.session_state.pagina = 'grafiek'

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


    # pagina 2 = grafieken

    elif st.session_state.pagina == 'grafiek':

        st.title('Grafiek(en)')

        # terug knop
        if st.button('← Terug naar kaart'):

            st.session_state.pagina = 'kaart'

            st.rerun()

        # geselecteerde data
        filtered_df = df[
            df['Wijk'].isin(st.session_state.wijken)
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
                    filtered_df,
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

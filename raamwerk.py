import streamlit as st

st.set_page_config(layout="wide")

col2, col1 = st.columns([1, 4])

with col1:
    st.image('amsterdam-map.jpg')
    
with col2: 
    st.expander('Settings', icon="⚙️")
    
    import streamlit as st

    FILTERS = {
        "Geslacht": ["Man", "Vrouw", "Anders"],
        "Leeftijd": ["40-50", "50-60", "60-70", "70+"],
        "Wijk": [
            "Sloterdijk Nieuw-West",
            "Geuzenveld, Slotermeer",
            "Osdorp",
            "De Aker, Sloten, Nieuw-Sloten",
            "Slotervaart",
            "Westerpark",
            "Bos en Lommer",
            "Oud-West, De Baarsjes",
            "Oud-Zuid",
            "Buitenveldert",
            "Amsterdamse Bos",
            "Centrum-West",
            "Centrum-Oost",
            "Oud-Oost",
            "De Pijp, Rivierenbuurt",
            "Watergraafsmeer",
            "Indische Buurt, Oostelijk Havengebied",
            "Oud-Noord",
            "Noord-West",
            "Noord-Oost",
            "IJburg, Zeeburgereiland",
            "Bijlmer-Centrum",
            "Bijlmer-West",
            "Bijlmer-Oost",
            "Gaasperdam",
            "Weesp, Driemond",
        ],
        "Waarde": [
            "Gem HR totaal",
            "HRV",
            "Bloeddruk (Bovendruk)",
            "Cholesterol",
            "Non-HDL",
            "Bloedsuiker",
            "BMI",
        ],
    }

    gekozen_filters = st.multiselect(
        "Filters",
        options=list(FILTERS.keys())
    )

    geselecteerde_waardes = {
        naam: st.multiselect(
            f"Kies {naam}",
            options=opties,
            key=f"filter_{naam}"
        )
        for naam, opties in FILTERS.items()
        if naam in gekozen_filters
    }
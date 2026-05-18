import streamlit as st

col2, col1 = st.columns([1, 4])

with col1:
    st.image('amsterdam-map.jpg')
    
with col2: 
    st.expander('Settings', icon="⚙️")
    
    gekozen_filters = st.multiselect(
        "Filters",
        ["Geslacht", "Leeftijd", "Wijk", "Waarde"]
    )

    filter_opties = {
        "Geslacht": ["Man", "Vrouw", "Anders"],
        "Leeftijd": ["40-50", "50-60", "60-70", "70+"],
        "Wijk": ["Sloterdijk Nieuw-West", "Geuzenveld, Slotermeer", "Osdorp", "De Aker, Sloten, Nieuw-Sloten", "Slotervaart", "Westerpark", "Bos en Lommer", "Oud-West, De Baarsjes", "Oud-Zuid", "Buitenveldert", "Amsterdamse Bos", "Centrum-West", "Centrum-Oost", "Oud-Oost", "De Pijp, Rivierenbuurt", "Watergraafsmeer", "Indische Buurt, Oostelijk Havengebied", "Oud-Noord", "Noord-West", "Noord-Oost", "IJburg, Zeeburgereiland", "Bijlmer-Centrum", "Bijlmer-West", "Bijlmer-Oost", "Gaasperdam", "Weesp, Driemond"],
        "Waarde": ["Gem HR totaal", "HRV", "Bloeddruk (Bovendruk)", "Cholesterol", "Non-HDL", "Bloedsuiker", "BMI"]
    }

    #geselecteerde_waardes = {}

    #for filter_naam in gekozen_filters:
     #   geselecteerde_waardes[filter_naam] = st.multiselect(
      #      f"Kies {filter_naam}",
       #     filter_opties[filter_naam]
        #)

    #st.write(geselecteerde_waardes)

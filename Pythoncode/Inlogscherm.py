import streamlit as st

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

CORRECT_EMAIL = "jan_pieters@gmail.com"
CORRECT_PASSWORD = "Hartstikke_gezond123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#"hartstikke-gezondweek.png"

def login_screen():
    st.image('hartstikke-gezondweek.png', width=200)

    st.title("Inloggen")

    email = st.text_input("E-mail")
    password = st.text_input("Wachtwoord", type="password")

    if st.button("Log in"):
        if email == CORRECT_EMAIL and password == CORRECT_PASSWORD:
            st.session_state.logged_in = True
            st.success("Succesvol ingelogd!")
            st.rerun()
        else:
            st.error("Onjuiste e-mail of wachtwoord.")


def main_app():
    st.title("Dashboard Hartstikke Gezond Week")

    st.write("Welkom! Je bent ingelogd.")

    if st.button("Uitloggen"):
        st.session_state.logged_in = False
        st.rerun()

    
    #App (dashboard) code

    st.header("Dashboard")
    st.image('4tsika.jpg')


#app starten

if st.session_state.logged_in:
    main_app()
else:
    login_screen()
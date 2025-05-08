import streamlit as st

import streamlit as st
import streamlit_authenticator as stauth

# Charger les identifiants depuis secrets
credentials = {
    "usernames": st.secrets["credentials"]["usernames"]
}

# Créer l'objet Authenticator
authenticator = stauth.Authenticate(
    credentials,
    "mon_app_cookie",  # nom du cookie
    "ma_signature_clé",  # clé de sécurité pour signer le cookie
    cookie_expiry_days=1
)

# Interface de connexion
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    authenticator.logout("Se déconnecter", "sidebar")
    st.sidebar.success(f"Connecté en tant que {name}")
    st.write(f"Bienvenue {name} 👋")
    # Ici ton app après connexion

elif authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")

elif authentication_status is None:
    st.warning("Veuillez entrer vos identifiants")


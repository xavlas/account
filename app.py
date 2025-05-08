import streamlit as st

def get_users():
    return st.secrets["users"]

def login():
    st.title("🔐 Page de connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        users = get_users()
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Bienvenue, {username} !")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

def main_app():
    st.title("🏠 Application principale")
    st.write(f"Vous êtes connecté en tant que {st.session_state['username']}.")

    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""

    if st.session_state["logged_in"]:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()

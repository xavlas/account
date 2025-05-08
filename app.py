import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

st.set_page_config(page_title="Système d'Authentification", layout="centered")

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    # Dans une application réelle, utilisez un sel unique par utilisateur
    salt = "salt_sécurisé"  # Idéalement, générez un sel unique pour chaque utilisateur
    return hashlib.sha256((password + salt).encode()).hexdigest()

def add_user(username, password, email=None):
    hashed_pwd = hash_password(password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        if email:
            c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                     (username, hashed_pwd, email))
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, hashed_pwd))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Nom d'utilisateur ou email déjà utilisé")
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result is not None:
        stored_password = result[0]
        return stored_password == hash_password(password)
    return False

def get_all_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username, email, created_at FROM users")
    users = c.fetchall()
    conn.close()
    return users


init_db()

def create_admin_if_not_exists():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    admin = c.fetchone()
    conn.close()
    
    if not admin:
        add_user("admin", "admin123")  # Dans une vraie application, utilisez un mot de passe fort

create_admin_if_not_exists()

def main():
    st.title("Système d'Authentification")
    
    # Initialiser les variables de session
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    
    # Menu latéral avec options
    menu = ["Connexion", "Inscription", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Connexion":
        st.subheader("Connexion")
        
        if st.session_state.logged_in:
            st.success(f"Vous êtes connecté en tant que {st.session_state.username}")
            if st.button("Déconnexion"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.rerun()
        else:
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            
            if st.button("Connexion"):
                if username and password:
                    if authenticate(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success(f"Connecté en tant que {username}")
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects")
                else:
                    st.warning("Veuillez entrer vos identifiants")
    
    elif choice == "Inscription":
        st.subheader("Créer un nouveau compte")
        
        new_username = st.text_input("Nom d'utilisateur")
        new_password = st.text_input("Mot de passe", type="password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password")
        email = st.text_input("Email (optionnel)")
        
        if st.button("S'inscrire"):
            if new_username and new_password:
                if new_password == confirm_password:
                    if add_user(new_username, new_password, email if email else None):
                        st.success(f"Compte créé pour {new_username}")
                        st.info("Vous pouvez maintenant vous connecter")
                else:
                    st.error("Les mots de passe ne correspondent pas")
            else:
                st.warning("Veuillez remplir les champs obligatoires")
    
    elif choice == "Admin" and st.session_state.logged_in and st.session_state.username == "admin":
        st.subheader("Panneau d'administration")
        
        st.write("Liste des utilisateurs:")
        users = get_all_users()
        
        if users:
            user_data = []
            for user in users:
                user_id, username, email, created_at = user
                user_data.append({
                    "ID": user_id,
                    "Nom d'utilisateur": username,
                    "Email": email if email else "Non renseigné",
                    "Date de création": created_at
                })
            
            st.table(user_data)
        else:
            st.info("Aucun utilisateur enregistré")
    
    elif choice == "Admin":
        st.warning("Vous devez être connecté en tant qu'administrateur pour accéder à cette page")

if __name__ == "__main__":
    main()
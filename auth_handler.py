import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

class AuthHandler:
    def __init__(self):
        self.db_path = "users.db"
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, 
                     password TEXT NOT NULL,
                     email TEXT UNIQUE NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, email, password):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            hashed_pw = self.hash_password(password)
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                     (username, email, hashed_pw))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        hashed_pw = self.hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
        result = c.fetchone()
        conn.close()
        return result is not None

    def user_exists(self, username=None, email=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if username:
            c.execute("SELECT 1 FROM users WHERE username=?", (username,))
        elif email:
            c.execute("SELECT 1 FROM users WHERE email=?", (email,))
        result = c.fetchone() is not None
        conn.close()
        return result

def show_login_page():
    st.title("Welcome to AI Chat")
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    auth = AuthHandler()

    # Tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # Login Tab
    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if auth.login_user(login_username, login_password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = login_username
                st.success(f"Welcome back, {login_username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # Sign Up Tab
    with tab2:
        st.header("Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if new_password != confirm_password:
                st.error("Passwords do not match!")
            elif auth.user_exists(username=new_username):
                st.error("Username already exists!")
            elif auth.user_exists(email=new_email):
                st.error("Email already registered!")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif not '@' in new_email:
                st.error("Please enter a valid email address!")
            else:
                if auth.register_user(new_username, new_email, new_password):
                    st.success("Registration successful! Please login.")
                    st.session_state['logged_in'] = False  # Ensure user needs to login
                else:
                    st.error("Registration failed. Please try again.") 
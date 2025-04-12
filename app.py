import streamlit as st
import hashlib
import time
from auth import authenticate_user, register_user, is_username_taken
from database import initialize_db, get_user_role
from models import User, Product, Order, Notification
from workflows import process_customer_order, process_retailer_order, process_wholesaler_order, manufacture_product
from ui_components import show_sidebar, render_dashboard, render_inventory, render_orders, render_notifications

# Set page config
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the database
initialize_db()

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'role' not in st.session_state:
    st.session_state.role = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

def login_page():
    st.title("🔐 Inventory Management System")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if username and password:
                user_authenticated, role = authenticate_user(username, password)
                if user_authenticated:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.success(f"Successfully logged in as {role}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        role_options = ["End Customer", "Retailer", "Wholesaler", "Manufacturer"]
        new_role = st.selectbox("Role", role_options)
        
        if st.button("Sign Up", key="signup_button"):
            if new_username and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif is_username_taken(new_username):
                    st.error("Username already exists. Please choose another one.")
                else:
                    success = register_user(new_username, new_password, new_role)
                    if success:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Error creating account. Please try again.")
            else:
                st.warning("Please fill all the fields")

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        # Show sidebar with navigation options
        show_sidebar()
        
        # Show page based on selection
        if st.session_state.current_page == "dashboard":
            render_dashboard(st.session_state.role, st.session_state.username)
        elif st.session_state.current_page == "inventory":
            render_inventory(st.session_state.role, st.session_state.username)
        elif st.session_state.current_page == "orders":
            render_orders(st.session_state.role, st.session_state.username)
        elif st.session_state.current_page == "notifications":
            render_notifications(st.session_state.username)
        elif st.session_state.current_page == "logout":
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.current_page = "dashboard"
            st.rerun()

if __name__ == "__main__":
    main()

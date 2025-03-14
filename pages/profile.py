import streamlit as st
import pandas as pd

# Mock function for get_user
def get_user(username):
    return ["username", "password", "email", "Full Name", "Email", "Phone"]

# Mock function for update_user
def update_user(username, full_name, email, phone):
    pass

# Mock function for get_all_users
def get_all_users():
    return [
        ["user1", "Full Name 1", "email1@example.com", "1234567890"],
        ["user2", "Full Name 2", "email2@example.com", "0987654321"]
    ]

# Mock function for delete_user
def delete_user(username):
    pass

st.set_page_config(page_title="Profile", layout="wide")

# Initialize session state variables
if "show_profile_management" not in st.session_state:
    st.session_state.show_profile_management = False
if "username" not in st.session_state:
    st.session_state.username = "guest"  # Default username

def toggle_profile_management():
    st.session_state.show_profile_management = not st.session_state.show_profile_management

# Ensure user is logged in
if st.session_state.username == "guest":
    st.warning("Please log in to access this page.")
    st.stop()

# User Profile Section
st.title("👤 User Profile")
st.button("✏️ Edit Profile", on_click=toggle_profile_management)

with st.form("user_profile_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    water_usage = st.selectbox("Primary water usage", ["Drinking", "Agriculture", "Industrial"])
    submit = st.form_submit_button("Save Profile")

if submit:
    st.success(f"✅ Profile Saved! Welcome, {name} 🎉")

# Profile Management (Only shown when Edit Profile is clicked)
if st.session_state.show_profile_management:
    st.title("👤 Profile Management")
    user = get_user(st.session_state.username)
    if user:
        full_name = st.text_input("Full Name", user[3])
        email = st.text_input("Email", user[4])
        phone = st.text_input("Phone Number", user[5])
        if st.button("Update Profile"):
            update_user(st.session_state.username, full_name, email, phone)
            st.success("Profile updated successfully!")

        if st.button("Delete Profile"):
            delete_user(st.session_state.username)
            st.success("Profile deleted successfully!")
            st.session_state.clear()
            st.rerun()

# Move logout button to the right side with a funny emoji
logout_col = st.columns([9, 1])[1]
with logout_col:
    if st.button("Logout😜"):
        st.session_state.clear()
        st.rerun()

# Smooth transitions & styling
st.markdown(
    """
    <style>
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True
)

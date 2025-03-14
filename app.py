import streamlit as st
import pandas as pd
import plotly.express as px
import time
import matplotlib.pyplot as plt
import sqlite3
import bcrypt
import chartmogul
import os  # Add this import

# Set API Key
CHARTMOGUL_API_KEY = "YOUR_API_KEY"
chartmogul.Config.api_key = CHARTMOGUL_API_KEY

st.set_page_config(page_title="Water Potability Classification", layout="wide")

# Force Streamlit to use Render's assigned port
port = int(os.environ.get("PORT", 8501))

# Database functions
def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        full_name TEXT,
                        email TEXT,
                        phone TEXT
                    )''')
    # Insert admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, full_name, email, phone) VALUES (?, ?, ?, ?, ?)",
                       ("admin", admin_password, "Administrator", "admin@example.com", "1234567890"))
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def add_user(username, password, full_name, email, phone):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, full_name, email, phone) VALUES (?, ?, ?, ?, ?)", 
                   (username, hash_password(password), full_name, email, phone))
    conn.commit()
    conn.close()
    
    # Send data to ChartMogul
    data = {
        "data_source_uuid": "YOUR_DATA_SOURCE_UUID",
        "external_id": username,
        "name": full_name,
        "email": email,
        "country": "Unknown"
    }
    try:
        customer = chartmogul.Customer.create(data)
        print("User added to ChartMogul:", customer)
    except Exception as e:
        print("ChartMogul Error:", str(e))

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(username, full_name, email, phone):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET full_name = ?, email = ?, phone = ? WHERE username = ?", 
                   (full_name, email, phone, username))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, full_name, email, phone FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Initialize DB
create_db()

# Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Login / Register")
    option = st.radio("Select an option", ["Login", "Register"])

    if option == "Register":
        with st.form(key='register_form'):
            st.subheader("Create an Account")
            new_username = st.text_input("Choose a Username")
            new_password = st.text_input("Choose a Password", type="password")
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            submit_button = st.form_submit_button(label='Register')
            if submit_button:
                try:
                    add_user(new_username, new_password, full_name, email, phone)
                    st.success("Account created successfully! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose another.")

    if option == "Login":
        with st.form(key='login_form'):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label='Login')
            if submit_button:
                user = get_user(username)
                if user and check_password(password, user[2]):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome, {user[3]}!")
                    st.session_state.current_page = "📊 Visualization"  # Redirect to third page after login
                    st.rerun()  # Rerun to apply the page change
                else:
                    st.error("Invalid credentials")
    st.stop()

# Load dataset
df = pd.read_csv("water_potability.csv")


# 🎵 Background Music with Autoplay & Loop
st.markdown(
    r"""
    <audio id="bg-music" autoplay loop>
        <source src="C:\Users\Ajmal\OneDrive\Documents\AJMAL_VR\VS.Code\project - water quality\background_music.mp3" type="audio/mp3">
    </audio>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var audio = document.getElementById("bg-music");
            audio.play();
        });
    </script>
    """,
    unsafe_allow_html=True
)

# Custom sidebar style
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-right: 2px solid rgba(255, 255, 255, 0.2);
        }
        [data-testid="stSidebarNav"] > ul {
            padding-top: 20px;
        }
        [data-testid="stSidebarNav"] a {
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            color: black;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom sidebar style
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-right: 2px solid rgba(255, 255, 255, 0.2);
        }
        [data-testid="stSidebarNav"] > ul {
            padding-top: 20px;
        }
        [data-testid="stSidebarNav"] a {
            color: white;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            color: black;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load dataset
df = pd.read_csv("water_potability.csv")

def classify_water(row):
    if row['Potability'] == 1:
        return 'Drinking - Safe for human consumption.'
    elif 6.5 <= row['ph'] <= 8.5 and row['Hardness'] <= 300:
        return 'Agriculture - Suitable for irrigation.'
    else:
        return 'Industrial - Used for cooling, cleaning, etc.'

def drinking_reason(row):
    return "✅ Yes - Safe for drinking." if row['Potability'] == 1 else "❌ No - Not potable."

def agriculture_reason(row):
    return "✅ Yes - Good for irrigation." if (6.5 <= row['ph'] <= 8.5 and row['Hardness'] <= 300) else "❌ No - Not suitable."

df['Water_Usage'] = df.apply(classify_water, axis=1)
df['Used_For_Drinking'] = df.apply(drinking_reason, axis=1)
df['Used_For_Agriculture'] = df.apply(agriculture_reason, axis=1)

# Detect which page is active
current_page = st.session_state.get("current_page", "🏠 Home")  # Default to home

# Define different styles for each page
sidebar_styles = {
    "🏠 Home": """
        <style>
            [data-testid="stSidebar"] {
                background-color: #1a1a2e; /* Dark Blue */
                border-right: 3px solid #e94560;
            }
            [data-testid="stSidebarNav"] a:hover {
                background-color: #e94560;
            }
        </style>
    """,
    "📞 Contact Us": """
        <style>
            [data-testid="stSidebar"] {
                background-color: #0a3d62; /* Deep Teal */
                border-right: 3px solid #78e08f;
            }
            [data-testid="stSidebarNav"] a:hover {
                background-color: #78e08f;
            }
        </style>
    """,
    "📊 Visualization": """
        <style>
            [data-testid="stSidebar"] {
                background-color: #222f3e; /* Dark Gray */
                border-right: 3px solid #ff9f43;
            }
            [data-testid="stSidebarNav"] a:hover {
                background-color: #ff9f43;
            }
        </style>
    """
}

# Apply the corresponding CSS
st.markdown(sidebar_styles.get(current_page, ""), unsafe_allow_html=True)

# Navigation without sidebar
page = st.radio("", ["🏠 Home", "📊 Visualization", "📞 Contact Us"], horizontal=True)
st.session_state.current_page = page  # Update the current page in session state

with st.spinner(f"⏳ Loading {page}... Please wait."):
    time.sleep(2.5)  # Loading delay for page switch

if page == "🏠 Home":
    st.title("🏠 Home - Water Potability Classification")
    st.write("This application classifies water quality based on potability, pH, and hardness levels.")
    st.dataframe(df.head(100))
    
    # Water Classification User Input
    st.write("## 🧪 Check Water Suitability")
    col1, col2, col3 = st.columns(3)
    with col1:
        ph_value = st.number_input("Enter pH value", min_value=0.0, max_value=14.0, step=0.1)
        solids_value = st.number_input("Enter Solids value (ppm)", min_value=0, max_value=50000, step=1)
    with col2:
        hardness_value = st.number_input("Enter Hardness value", min_value=0, max_value=500, step=1)
        chloramines_value = st.number_input("Enter Chloramines value (ppm)", min_value=0.0, max_value=10.0, step=0.1)
    with col3:
        sulfate_value = st.number_input("Enter Sulfate value (ppm)", min_value=0.0, max_value=500.0, step=0.1)
        conductivity_value = st.number_input("Enter Conductivity value (μS/cm)", min_value=0, max_value=10000, step=1)
    
    if st.button("🔍 Classify Water"):
        test_row = pd.Series({
            'ph': ph_value, 
            'Hardness': hardness_value, 
            'Solids': solids_value,
            'Chloramines': chloramines_value,
            'Sulfate': sulfate_value,
            'Conductivity': conductivity_value,
            'Potability': 1 if 6.5 <= ph_value <= 8.5 else 0
        })
        st.success(f"**Water Usage:** {classify_water(test_row)}")
        st.info(f"**Used for Drinking:** {drinking_reason(test_row)}")
        st.warning(f"**Used for Agriculture:** {agriculture_reason(test_row)}")

elif page == "📊 Visualization":
    st.title("📊 Water Classification Visualization")
    water_usage_counts = df['Water_Usage'].value_counts().reset_index()
    water_usage_counts.columns = ['Water Usage Category', 'Count']

    fig_bar = px.bar(water_usage_counts, x='Water Usage Category', y='Count',
                     labels={'Water Usage Category': 'Usage Type', 'Count': 'Number of Samples'},
                     color='Water Usage Category', title="Water Classification Breakdown")
    st.plotly_chart(fig_bar)
    
    st.write("### 🚰 Potability Distribution")
    potability_counts = df['Potability'].value_counts().reset_index()
    potability_counts.columns = ['Potability', 'Count']
    potability_counts['Potability'] = potability_counts['Potability'].map({1: 'Potable (Safe)', 0: 'Non-Potable (Unsafe)'})

    fig_pie = px.pie(potability_counts, names='Potability', values='Count',
                     title="Potable vs Non-Potable Water",
                     color='Potability', color_discrete_map={'Potable (Safe)': 'green', 'Non-Potable (Unsafe)': 'red'})
    st.plotly_chart(fig_pie)

elif page == "📞 Contact Us":
    st.title("📞 Contact Us")
    st.write("For inquiries, please email: MR_AJMAL@waterquality.com")
    st.write("Phone: +91 95977-54567")
    st.markdown("**Address:** <span style='font-size:20px; color:green;'>Dubai Kurukku Sandhu, Dubai City, Dubai</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Run the app on the correct port
if __name__ == "__main__":
    st.run(port=port)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Understanding Water Quality", layout="wide")

# Custom sidebar style with smooth transitions
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-right: 2px solid rgba(255, 255, 255, 0.2);
            transition: all 0.5s ease-in-out;
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
            box-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
        }
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-out {
            animation: fadeOut 0.5s ease-in-out forwards;
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    </style>
    
    <script>
        function fadeOutAndNavigate(url) {
            document.body.classList.add('fade-out');
            setTimeout(function() {
                window.location.href = url;
            }, 500); // Wait for fade-out before navigating
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Apply fade-in effect on page load
st.markdown('<div class="fade-in">', unsafe_allow_html=True)

st.title("📖 Understanding Water Quality")
st.write("🔹 Water quality is determined by multiple factors. Below, you'll find explanations of key attributes, their significance, and how they affect water usability.")

# Load dataset
df = pd.read_csv("water_potability.csv")

# Dictionary of attributes with detailed explanations
attributes = {
    'ph': {
        'desc': "Measures acidity or alkalinity. A pH level between **6.5 and 8.5** is safe for drinking. \n\n🌱 **Agriculture:** Soil pH influences plant growth. \n\n🏭 **Industrial:** Water acidity can corrode pipelines.",
        'impact': "💧 **Low pH (<6.5):** Water is acidic and can dissolve toxic metals.\n\n💧 **High pH (>8.5):** Water may have a bitter taste and cause scaling.",
        'color': 'blue'
    },
    'Hardness': {
        'desc': "Indicates the presence of **calcium and magnesium** in water. \n\n💧 **Drinking:** Hard water can cause scaling in kettles.\n\n🌾 **Agriculture:** Affects soil permeability.",
        'impact': "💧 **Low Hardness (<75 mg/L):** Soft water, but may cause pipe corrosion.\n\n💧 **High Hardness (>300 mg/L):** Leads to scale buildup in pipes.",
        'color': 'purple'
    },
    'Solids': {
        'desc': "Represents **Total Dissolved Solids (TDS)**, affecting water taste and usability. \n\n👨‍⚕️ **Drinking:** Ideal TDS is **below 500 mg/L**. \n\n🚜 **Agriculture:** High solids can affect plant absorption.",
        'impact': "💧 **Low TDS (<50 mg/L):** Water may taste flat.\n\n💧 **High TDS (>1000 mg/L):** Can cause kidney issues if consumed regularly.",
        'color': 'green'
    },
    'Chloramines': {
        'desc': "Disinfectant used in water treatment to kill bacteria. \n\n⚠️ **Too much chloramine (>4 mg/L) can cause health issues.**",
        'impact': "💧 **High Levels:** Can irritate eyes and skin.\n\n💧 **Low Levels:** Inadequate disinfection, risk of bacteria growth.",
        'color': 'orange'
    },
    'Sulfate': {
        'desc': "Occurs naturally in water. High sulfate levels can cause a bitter taste. \n\n🚰 **Safe limit:** Below **250 mg/L**.",
        'impact': "💧 **Excess sulfate (>400 mg/L):** Can cause diarrhea.\n\n💧 **Low sulfate (<100 mg/L):** No major health risks.",
        'color': 'pink'
    },
    'Conductivity': {
        'desc': "Measures water’s ability to conduct electricity, related to ion concentration. \n\n⚡ **High conductivity means more dissolved salts.**",
        'impact': "💧 **High Levels (>1000 µS/cm):** Water is too saline for drinking/agriculture.\n\n💧 **Low Levels (<100 µS/cm):** Water may be corrosive.",
        'color': 'red'
    },
    'Organic_carbon': {
        'desc': "Indicates organic matter presence in water. \n\n⚠️ **High levels can indicate contamination.**",
        'impact': "💧 **High Organic Carbon (>5 mg/L):** Could suggest industrial pollution.\n\n💧 **Low Levels (<2 mg/L):** Usually safe.",
        'color': 'brown'
    },
    'Trihalomethanes': {
        'desc': "By-products formed when chlorine reacts with organic matter. \n\n⚠️ **Excess levels (>80 µg/L) can be harmful.**",
        'impact': "💧 **High Levels (>100 µg/L):** Potential cancer risk.\n\n💧 **Low Levels (<50 µg/L):** Safe for drinking.",
        'color': 'cyan'
    },
    'Turbidity': {
        'desc': "Indicates water clarity. High turbidity means more particles in water. \n\n🌊 **Turbid water can indicate contamination.**",
        'impact': "💧 **High Turbidity (>5 NTU):** May contain bacteria.\n\n💧 **Low Turbidity (<1 NTU):** Clear and safe.",
        'color': 'gray'
    }
}

st.write("### 🔬 Key Water Quality Attributes")

# Create a tab for each attribute to make it interactive
tabs = st.tabs(list(attributes.keys()))

for idx, (attr, details) in enumerate(attributes.items()):
    with tabs[idx]:
        col1, col2 = st.columns([1, 1.5])  # Split layout for text & visualization

        with col1:
            st.subheader(f"📝 {attr}", help="Click for more details")
            st.write(f'<div class="fade-in">{details["desc"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**⚡ Impact on Water Usage:**\n{details['impact']}")
            
            # Animated progress bar to show attribute levels
            avg_value = df[attr].mean()
            min_value, max_value = df[attr].min(), df[attr].max()
            percentage = int(((avg_value - min_value) / (max_value - min_value)) * 100)
            st.progress(percentage)
            
            # Visual attribute indicator
            st.markdown(f"<div class='fade-in' style='background-color:{details['color']}; padding:5px; color:white; text-align:center; font-weight:bold;'> {attr.upper()} LEVEL </div>", unsafe_allow_html=True)

        with col2:
            fig = px.histogram(df, x=attr, title=f"{attr} Distribution",
                               color_discrete_sequence=[details['color']])
            st.plotly_chart(fig, use_container_width=True)

st.write("🔹 **Understanding these attributes ensures better water quality management.**")

# Close fade-in div
st.markdown("</div>", unsafe_allow_html=True)

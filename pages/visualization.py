import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, RobustScaler

# Load the trained model
model = joblib.load(r"C:\Users\Ajmal\OneDrive\Documents\AJMAL_VR\VS.Code\project - water quality\water_quality_model.pkl")


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

# Define expected features
expected_features = ['pH', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                     'Conductivity', 'Organic_Carbon', 'Trihalomethanes', 'Turbidity']

st.title("💧 Water Quality Classification & Visualization")

# **File Uploader**
uploaded_file = st.file_uploader("📂 Upload a CSV file for prediction", type=["csv"], label_visibility="hidden")

# **Processing Uploaded File**
if uploaded_file is not None:
    with st.spinner("⏳ Processing the uploaded file... Please wait."):
        df = pd.read_csv(uploaded_file)

        # **Check for missing columns**
        missing_features = set(expected_features) - set(df.columns)
        if missing_features:
            st.error(f"❌ Uploaded file is missing these columns: {missing_features}")
        else:
            # **Keep only expected columns**
            df = df[expected_features]

            # **Apply the same feature engineering as in training**
            poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
            poly.fit(df)  
            X_poly = poly.transform(df)  
            feature_names = poly.get_feature_names_out()  
            df_poly = pd.DataFrame(X_poly, columns=feature_names)

            # **Apply Scaling**
            scaler = RobustScaler()
            df_scaled = scaler.fit_transform(df_poly)
            df_final = pd.DataFrame(df_scaled, columns=df_poly.columns)

            # **Make Predictions**
            predictions = model.predict(df_final)
            prediction_probabilities = model.predict_proba(df_final)  # Get probability scores

            # **Add predictions to DataFrame**
            df['Potability Prediction'] = predictions
            df['Probability of Potable'] = prediction_probabilities[:, 1]  # Probability of potable water

            # **Classification for Usage**
            def classify_usage(row):
                # Drinking water criteria
                drinking_safe = (6.5 <= row['pH'] <= 8.5) and row['Potability Prediction'] == 1

                # Agriculture water criteria
                agriculture_safe = row['pH'] >= 6.0 and row['Sulfate'] <= 400 and row['Conductivity'] <= 3000

                # Industrial water criteria
                industry_safe = row['Hardness'] <= 500 and row['Conductivity'] <= 5000

                return pd.Series([drinking_safe, agriculture_safe, industry_safe], 
                                 index=['Drinking Safe', 'Agriculture Safe', 'Industry Safe'])

            df[['Drinking Safe', 'Agriculture Safe', 'Industry Safe']] = df.apply(classify_usage, axis=1)

            # **Show Full Dataset with Predictions**
            st.write("### 📊 Full Prediction Results")
            st.dataframe(df)

            # **Summarize the Results**
            potable_count = np.sum(df['Potability Prediction'] == 1)
            non_potable_count = np.sum(df['Potability Prediction'] == 0)
            drinking_safe_count = df['Drinking Safe'].sum()
            agriculture_safe_count = df['Agriculture Safe'].sum()
            industry_safe_count = df['Industry Safe'].sum()

            st.write(f"✅ **Potable Water Count:** {potable_count}")
            st.write(f"❌ **Non-Potable Water Count:** {non_potable_count}")
            st.write(f"🚰 **Safe for Drinking:** {drinking_safe_count}")
            st.write(f"🌱 **Safe for Agriculture:** {agriculture_safe_count}")
            st.write(f"🏭 **Safe for Industry:** {industry_safe_count}")

            # **Visualization - Bar Chart**
            st.write("### 📊 Classification Summary")
            st.bar_chart(pd.DataFrame({
                "Count": [drinking_safe_count, agriculture_safe_count, industry_safe_count]
            }, index=["Drinking Safe", "Agriculture Safe", "Industry Safe"]))

            # **Visualization - Pie Chart**
            st.write("### 🥧 Water Quality Distribution")
            fig, ax = plt.subplots()
            labels = ['Drinking Safe', 'Agriculture Safe', 'Industry Safe']
            sizes = [drinking_safe_count, agriculture_safe_count, industry_safe_count]
            colors = ['#66b3ff', '#99ff99', '#ffcc99']
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={"edgecolor": "black"})
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            st.pyplot(fig)

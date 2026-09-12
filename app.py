import streamlit as st
import requests


# Backend API URL
BACKEND_URL = "https://superkart-sales-backend-mpzq.onrender.com"


# Page configuration
st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)


st.title("🛒 SuperKart Sales Predictor")

st.write(
    "Enter product and store details to predict total store sales."
)


# Product details
st.header("Product Details")

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.0,
    step=0.1
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.05,
    step=0.001,
    format="%.3f"
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=150.0,
    step=1.0
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)

product_type = st.selectbox(
    "Product Type",
    [
        "Fruits and Vegetables",
        "Snack Foods",
        "Frozen Foods",
        "Dairy",
        "Household",
        "Baking Goods",
        "Canned",
        "Health and Hygiene",
        "Meat",
        "Soft Drinks",
        "Breads",
        "Hard Drinks",
        "Others",
        "Starchy Foods",
        "Breakfast",
        "Seafood"
    ]
)


# Store details
st.header("Store Details")

store_establishment_year = st.selectbox(
    "Store Establishment Year",
    [1987, 1998, 1999, 2009]
)

store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart"
    ]
)


# Prediction
if st.button("Predict Sales"):

    input_data = {
        "Product_Weight": product_weight,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Establishment_Year": store_establishment_year,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Type": product_type,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/predict",
            json=input_data,
            timeout=60
        )

        if response.status_code == 200:

            prediction = response.json()["predicted_sales"]

            st.success(
                f"Predicted Total Store Sales: {prediction:.2f}"
            )

        else:

            st.error(
                f"Prediction failed: {response.text}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Could not connect to the backend: {error}"
        )

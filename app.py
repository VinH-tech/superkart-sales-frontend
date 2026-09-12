import streamlit as st
import requests
import pandas as pd


BACKEND_URL = "https://superkart-sales-backend-mpzq.onrender.com"

REQUIRED_FEATURES = [
    "Product_Weight",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Establishment_Year",
    "Product_Sugar_Content",
    "Product_Type",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type"
]


st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)


st.title("🛒 SuperKart Sales Predictor")
st.write("Predict total store sales using product and store details.")


# ============================================================
# SINGLE PREDICTION
# ============================================================

st.header("Single Prediction")
st.write("Enter product and store details to predict sales for one record.")


st.subheader("Product Details")

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
    ["Low Sugar", "Regular", "No Sugar"]
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


st.subheader("Store Details")

store_establishment_year = st.selectbox(
    "Store Establishment Year",
    [1987, 1998, 1999, 2009]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
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


# ============================================================
# BATCH PREDICTION
# ============================================================

st.divider()

st.header("Batch Prediction")
st.write(
    "Upload a CSV file containing multiple product and store records."
)


uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


if uploaded_file is not None:

    batch_input_df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.dataframe(batch_input_df)


    missing_features = [
        feature
        for feature in REQUIRED_FEATURES
        if feature not in batch_input_df.columns
    ]


    if missing_features:

        st.error(
            "The uploaded CSV is missing these required columns: "
            + ", ".join(missing_features)
        )

    else:

        if st.button("Predict Batch Sales"):

            # Keep only the nine features required by the backend.
            # Any additional columns in the uploaded CSV are ignored.
            batch_input_df = batch_input_df[REQUIRED_FEATURES]

            batch_records = batch_input_df.to_dict(
                orient="records"
            )


            try:

                response = requests.post(
                    f"{BACKEND_URL}/batch_predict",
                    json=batch_records,
                    timeout=120
                )


                if response.status_code == 200:

                    predictions = response.json()["predictions"]

                    result_df = batch_input_df.copy()

                    result_df["Predicted_Sales"] = predictions


                    st.subheader("Batch Prediction Results")
                    st.dataframe(result_df)


                    csv_output = result_df.to_csv(
                        index=False
                    ).encode("utf-8")


                    st.download_button(
                        label="Download Prediction Results",
                        data=csv_output,
                        file_name="superkart_batch_predictions.csv",
                        mime="text/csv"
                    )

                else:

                    st.error(
                        f"Batch prediction failed: {response.text}"
                    )


            except requests.exceptions.RequestException as error:

                st.error(
                    f"Could not connect to the backend: {error}"
                )

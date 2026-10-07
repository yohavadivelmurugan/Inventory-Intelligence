import sys
import os
import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","src")))

from data_loader import load_from_db
from preprocessing import preprocess_data
from model import training_data,time_based_split,train_model
from inventory_logic import calc_inventory_status
from database import save_uploaded_data

st.set_page_config(page_title="Sales & Inventory Intelligence",page_icon="📦",layout="wide")
@st.cache_resource
def load_ml_pipeline():
    df=load_from_db()
    df=preprocess_data(df)
    model_data=training_data(df)
    train_data,test_data=time_based_split(model_data)
    numerical_features=["Previous_Day_Sales","Rolling_3D_Sales","Rolling_7D_Sales","Day_of_Week","Month","Inventory Level","Units Ordered","Price","Discount","Holiday/Promotion","Competitor Pricing"]
    categorical_features=["Store ID","Product ID","Category","Region","Weather Condition","Seasonality"]
    feature_columns=numerical_features+categorical_features
    X_train=train_data[feature_columns]
    y_train=train_data["Future Demand"]
    X_test=test_data[feature_columns]

    preprocessor=ColumnTransformer(transformers=[("categorical",OneHotEncoder(handle_unknown="ignore"),categorical_features)],remainder="passthrough")
    X_train_encoded=preprocessor.fit_transform(X_train)
    X_test_encoded=preprocessor.transform(X_test)

    model=train_model(X_train_encoded,y_train)

    y_pred=model.predict(X_test_encoded)

    test_data=test_data.copy()
    test_data["Predicted Demand"]=y_pred

    test_data=calc_inventory_status(test_data)
    return test_data

st.title("📦 Sales & Inventory Intelligence System")
uploaded_file=st.file_uploader("Upload Inventory Dataset(CSV)",type=["csv"])
if uploaded_file is not None:
    uploaded_df=pd.read_csv(uploaded_file)
    save_uploaded_data(uploaded_df)
    st.success("Dataset uploaded and saved to database successfully!")
    st.cache_resource.clear()
test_data=load_ml_pipeline()

st.write( "Predict future product demand and determine "
    "whether current inventory is sufficient.")
st.divider()
stores=sorted(test_data["Store ID"].unique())
selected_store=st.selectbox("Select Store",stores)

store_data=test_data[test_data["Store ID"]==selected_store]
products=sorted(store_data["Product ID"].unique())
selected_product=st.selectbox("Select Product",products)

product_data=store_data[store_data["Product ID"]==selected_product]

dates=sorted(product_data["Date"].unique())
selected_date=st.selectbox("Select Date",dates)

selected_data=product_data[product_data["Date"]==selected_date].iloc[0]

st.divider()
st.subheader("Inventory Intelligence")

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric("Predicted Demand",f"{selected_data['Predicted Demand']:.0f}units")
with col2:
    st.metric("Current Inventory",f"{selected_data['Inventory Level']:.0f}units")
with col3:
    st.metric("Inventory Status",selected_data['Inventory_status'])
with col4:
    st.metric("Suggested Reorder",f"{selected_data['Suggested_Reorder_Qty']:.0f}units")

st.divider()

if selected_data["Inventory_status"]=="Sufficient":
    st.success("✅ Current inventory is sufficient to meet predicted demand.")
else:
    st.warning("⚠️ Current inventory may not be sufficient. "
        "Reordering is recommended.")
    
st.subheader("Demand vs Inventory")
chart_data=product_data[["Date","Predicted Demand","Inventory Level"]].copy()
chart_data=chart_data.set_index("Date")
st.line_chart(chart_data)

st.subheader("Business Summary")
avg_demand=product_data["Predicted Demand"].mean()
avg_inventory=product_data["Inventory Level"].mean()
reorder_days=product_data["Inventory_status"].eq("Reorder Required").sum()
total_reorder=product_data["Suggested_Reorder_Qty"].sum()
col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric("Average Predicted Demand",f"{avg_demand:.0f}units")
with col2:
    st.metric("Average Inventory",f"{avg_inventory:.0f}units")
with col3:
    st.metric("Reorder Required Days",f"{reorder_days}")
with col4:
    st.metric("Total Suggested Reorder",f"{total_reorder:.0f}units")


st.write("DEBUG CHECK")
st.write(product_data[["Date","Predicted Demand","Inventory Level","Inventory_status","Suggested_Reorder_Qty"]].head(20))
    
st.subheader("Selected Record Details")

st.write (product_data[["Date", "Predicted Demand", "Inventory Level","Inventory_status", "Suggested_Reorder_Qty"]].head(20))

details=pd.DataFrame({"Field": [
        "Date",
        "Store",
        "Product",
        "Predicted Demand",
        "Current Inventory",
        "Inventory Status",
        "Suggested Reorder Quantity"
    ],
    "Value": [
        str(selected_data["Date"].date()),
        selected_data["Store ID"],
        selected_data["Product ID"],
        f"{selected_data['Predicted Demand']:.2f}",
        f"{selected_data['Inventory Level']:.0f}",
        selected_data["Inventory_status"],
        f"{selected_data['Suggested_Reorder_Qty']:.0f}"
    ]})

st.table(details)

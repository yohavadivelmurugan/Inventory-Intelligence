import pandas as pd

def calc_inventory_status(df):
    df=df.copy()
    df["Inventory_status"]=df.apply(lambda row:"Sufficient" if row["Inventory Level"]>=row["Predicted Demand"] else "Reorder Required",axis=1)
    df["Suggested_Reorder_Qty"]=(df["Predicted Demand"]-df["Inventory Level"]).clip(lower=0).round().astype(int)
    return df
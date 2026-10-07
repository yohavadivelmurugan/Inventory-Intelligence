import pandas as pd
from data_loader import load_data
from preprocessing import preprocess_data
import matplotlib.pyplot as plt

if __name__=="__main__":
    df=load_data()
    df=preprocess_data(df)
    print("EDA started!!")
    print("\nDataset Shape:")
    print(df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print(df[["Inventory Level","Units Sold","Units Ordered","Demand Forecast","Price","Discount","Competitor Pricing"]].describe())

    print("\nTotal Units Sold by Product:")
    product_sales=(df.groupby("Product ID")["Units Sold"].sum().sort_values(ascending=False))
    print(product_sales.to_string())

    print("\nTotal Units Sold by Store:")
    store_sales=(df.groupby("Store ID")["Units Sold"].sum().sort_values(ascending=False))
    print(store_sales.to_string())

    print("\nMonthly Units Sold:")
    monthly_sales=(df.groupby(df["Date"].dt.to_period("M"))["Units Sold"].sum())
    print(monthly_sales.to_string())

    print("\nMonthly Average Units Sold:")
    monthly_avg_sales=(df.groupby(df["Date"].dt.to_period("M"))["Units Sold"].mean())
    print(monthly_avg_sales)

    plt.figure(figsize=(12,5))
    plt.plot(monthly_sales.index.astype(str),monthly_sales.values,marker="o")
    plt.title("Monthly Units Sold")
    plt.xlabel("Month")
    plt.ylabel("Total Units Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print("\nInventory vs Sales:")
    inventory_sales=(df.groupby("Product ID").agg({"Inventory Level":"mean","Units Sold":"mean"}).sort_values("Units Sold",ascending=False))
    print(inventory_sales.to_string())

    inventory_sales["Inventory_to_Sales_Ratio"]=(inventory_sales["Inventory Level"]/inventory_sales["Units Sold"])
    print("\nInventory-to-Sales Ratio by Product:")
    print(inventory_sales.sort_values("Inventory_to_Sales_Ratio",ascending=False).to_string())
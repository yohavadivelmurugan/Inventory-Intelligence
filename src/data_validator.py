from data_loader import load_data
import pandas as pd
def check_missing(df):
    missing=df.isnull().sum()
    print("Missing values:",missing)
    return missing

def check_dup(df):
    dup=df.duplicated().sum()
    print("Duplicate values:",dup)

def check_datatypes(df):
    print("\nData Types:")
    print(df.dtypes)
    return df.dtypes

def check_neg_values(df,columns):
    print("\nNegative value checks:")
    for column in columns:
        count=(df[column]<0).sum()
        print(f"{column}: {count}")
    return

if __name__=="__main__":
    df=load_data()
    check_missing(df)
    check_dup(df)
    check_datatypes(df)
    numeric_columns = [
        "Inventory Level",
        "Units Sold",
        "Units Ordered",
        "Demand Forecast",
        "Price",
        "Discount",
        "Competitor Pricing"
    ]
    check_neg_values(df,numeric_columns)
    negative_demand=df[df["Demand Forecast"]<0]
    print("\nNegative Demand Forecast values:")
    print(negative_demand[["Date","Store ID","Product ID","Inventory Level","Units Sold","Demand Forecast"]].head(20).to_string(index=False))
    print("\nNumber of negative Demand Forecast values:")
    print(len(negative_demand))

    print("\nDemand Forecast statistics:")
    print(df["Demand Forecast"].describe())

    print("\nDate information:")
    df["Date"]=pd.to_datetime(df["Date"])
    print("Minimum Date:",df["Date"].min())
    print("Maximum Date:",df["Date"].max())
    print("Number of unique dates:",df["Date"].nunique())

    print("\nStore and Product information:")

    print("Number of stores",df["Store ID"].nunique())
    print("Number of products:",df["Product ID"].nunique())

    print("Number of Store-Product combination:s",df[["Store ID","Product ID"]].drop_duplicates().shape[0])
    store_prod_date_dup=df.duplicated(subset=["Store ID","Product ID","Date"]).sum()
    print("\nDuplicate Store-Product_Date combinations:",store_prod_date_dup)

    

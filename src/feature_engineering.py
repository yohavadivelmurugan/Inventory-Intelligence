import pandas as pd
from data_loader import load_data
from preprocessing import preprocess_data

def create_features(df):
    df=df.sort_values(["Store ID","Product ID","Date"]).copy()

    df["Previous_Day_Sales"]=(df.groupby(["Store ID","Product ID"])["Units Sold"].shift(1))
    df["Rolling_3D_Sales"]=(df.groupby(["Store ID","Product ID"])["Units Sold"].transform(lambda x:x.shift(1).rolling(3).mean()))
    df["Rolling_7D_Sales"]=(df.groupby(["Store ID","Product ID"])["Units Sold"].transform(lambda x:x.shift(1).rolling(7).mean()))
    df["Future Demand"]=(df.groupby(["Store ID","Product ID"])["Units Sold"].shift(-1))
    df["Day_of_Week"]=df["Date"].dt.dayofweek
    df["Month"]=df["Date"].dt.month
    df["Day_of_Month"]=df["Date"].dt.day
    return df

if __name__=="__main__":
    df=load_data()
    df=preprocess_data(df)
    df=create_features(df)
    print("Feature Engineering Completed!!")

    print(df[["Date","Store ID","Product ID","Units Sold","Previous_Day_Sales","Rolling_3D_Sales","Rolling_7D_Sales","Day_of_Week","Month","Future Demand"]].head(20).to_string(index=False))
import pandas as pd
from src.data_loader import load_data

def preprocess_data(df):
    df["Date"]=pd.to_datetime(df["Date"])
    df.loc[df["Demand Forecast"]<0,"Demand Forecast"]=0
    return df

if __name__=="__main__":
    df=load_data()
    df=preprocess_data(df)
    print("Preprocessing completed!")

    print("\nData types:")
    print(df.dtypes)
    print("\nNegative Demand Forecast values after preprocessing:")
    print((df["Demand Forecast"]<0).sum())
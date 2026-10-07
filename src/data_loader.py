import pandas as pd

def load_data():
    file_path="data/retail_store_inventory.csv"
    df=pd.read_csv(file_path)
    return df

def load_from_db():
    import sqlite3
    connection=sqlite3.connect("database/inventory.db")
    df=pd.read_sql_query(
        "SELECT*FROM sales_inventory",connection
    )
    connection.close()
    return df

if __name__=="__main__":
    df=load_data()
    print("Data loaded successfully!!")
    print("Shape:",df.shape)
    print(df.head())
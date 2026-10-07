import sqlite3
import pandas as pd
from data_loader import load_data

def create_database():
    df=load_data()
    connection=sqlite3.connect("database/inventory.db")
    df.to_sql("sales_inventory",connection,if_exists="replace",index=False)
    connection.close()
    print("Database created successfully!")

def load_from_database():
    connection=sqlite3.connect("database/inventory.db")
    query="""
    SELECT*FROM sales_inventory
    """
    df=pd.read_sql_query(query,connection)
    connection.close()
    return df

def save_uploaded_data(df):
    connection=sqlite3.connect("database/inventory.db")
    df.to_sql("sales_inventory",connection,if_exists="replace",index=False)
    connection.close()
    print("Uploaded data saved to database!")

if __name__=="__main__":
    create_database()
    df=load_from_database()
    print("Data loaded from SQLite!")
    print("Shape:",df.shape)
    print(df.head())
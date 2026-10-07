import sqlite3

def get_connection():
    return sqlite3.connect("database/inventory.db")

def tot_sales_by_store():
    connection=get_connection()
    query="""
    SELECT "Store ID",SUM("Units Sold") AS Total_sales
    FROM sales_inventory
    GROUP BY "Store ID"
    ORDER BY Total_Sales DESC;"""
    result=connection.execute(query).fetchall()
    connection.close()
    return result

def top_products():
    connection=get_connection()
    query="""
    SELECT "Product ID",SUM("Units Sold") AS Total_Sales
    FROM sales_inventory 
    GROUP BY "Product ID"
    ORDER BY Total_Sales DESC;
    """
    result=connection.execute(query).fetchall()
    connection.close()
    return result

def inventory_risk():
    connection=get_connection()
    query="""
    SELECT "Store ID","Inventory Level","Units Sold" 
    FROM sales_inventory 
    WHERE "Inventory Level" < "Units Sold"
    ORDER BY ("Units Sold"-"Inventory Level") DESC;
    """
    result=connection.execute(query).fetchall()
    connection.close()
    return result

if __name__=="__main__":
    results=tot_sales_by_store()
    print("Total Sales by Store:")
    for row in tot_sales_by_store():
        print(row)
    print("\nTop Products:")
    for row in top_products():
        print(row)
    print("\nInventory Risk Cases:")
    for row in inventory_risk()[:20]:
        print(row)
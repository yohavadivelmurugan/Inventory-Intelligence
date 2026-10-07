import pandas as pd
from src.inventory_logic import calc_inventory_status

def test_inventory_status():
    df=pd.DataFrame({"Inventory Level":[100,50],"Predicted Demand":[80,100]})
    result=calc_inventory_status(df)
    assert result.loc[0,"Inventory_status"]=="Sufficient"
    assert result.loc[1,"Inventory_status"]=="Reorder Required"

def test_reorder_qty():
    df=pd.DataFrame({"Inventory Level":[100,50],"Predicted Demand":[80,100]})
    result=calc_inventory_status(df)
    assert result.loc[0,"Suggested_Reorder_Qty"]==0
    assert result.loc[1,"Suggested_Reorder_Qty"]==50
import pandas as pd
from src.preprocessing import preprocess_data

def test_date_conversion():
    df=pd.DataFrame({"Date":["2023-01-01"],"Demand Forecast":[100]})
    result=preprocess_data(df)
    assert pd.api.types.is_datetime64_any_dtype(result["Date"])

def test_neg_demand_forecast():
    df=pd.DataFrame({"Date":["2023-01-01"],"Demand Forecast":[-10]})
    result=preprocess_data(df)
    assert result.loc[0,"Demand Forecast"]==0
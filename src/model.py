import pandas as pd
from data_loader import load_data
from preprocessing import preprocess_data
from feature_engineering import create_features
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from inventory_logic import calc_inventory_status

def training_data(df):
    df=create_features(df)
    numerical_features = ["Previous_Day_Sales","Rolling_3D_Sales","Rolling_7D_Sales","Day_of_Week","Month","Inventory Level","Units Ordered","Price","Discount","Holiday/Promotion","Competitor Pricing"]
    categorical_features = ["Store ID","Product ID","Category","Region","Weather Condition","Seasonality"]
    target_column="Future Demand"

    model_data=df[["Date"]+numerical_features+categorical_features+[target_column]].copy()
    model_data=model_data.dropna()

    return model_data

def time_based_split(df):
    unique_dates=sorted(df["Date"].unique())
    split_index=int(len(unique_dates)*0.8)

    train_data=unique_dates[:split_index]
    test_data=unique_dates[split_index:]

    train_data=df[df["Date"].isin(train_data)]
    test_data=df[df["Date"].isin(test_data)]

    return train_data,test_data

def train_model(X_train,y_train):
    model=RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=-1)
    model.fit(X_train,y_train)
    return model

def calc_baseline_pred(test_data):
    baseline_preds=test_data["Rolling_7D_Sales"]
    return baseline_preds

if __name__=="__main__":
    df=load_data()
    df=preprocess_data(df)
    model_data=training_data(df)

    train_data,test_data =time_based_split(model_data)
    numerical_features = ["Previous_Day_Sales","Rolling_3D_Sales","Rolling_7D_Sales","Day_of_Week","Month","Inventory Level","Units Ordered","Price","Discount","Holiday/Promotion","Competitor Pricing"]
    categorical_features = ["Store ID","Product ID","Category","Region","Weather Condition","Seasonality"]

    X_train=train_data[numerical_features+categorical_features]
    y_train=train_data["Future Demand"]
    X_test=test_data[numerical_features+categorical_features]
    y_test=test_data["Future Demand"]

    preprocessor=ColumnTransformer(transformers=[("categorical",OneHotEncoder(handle_unknown="ignore"),categorical_features)],remainder="passthrough")
    X_train_encoded=preprocessor.fit_transform(X_train)
    X_test_encoded=preprocessor.transform(X_test)

    print("\nTraining Random Forest model...")
    model=train_model(X_train_encoded,y_train)
    print("Model training completed!")

    print("\nMaking predictions...")
    y_pred=model.predict(X_test_encoded)
    test_data=test_data.copy()
    test_data["Predicted Demand"]=y_pred
    test_data=calc_inventory_status(test_data)
    print("\nInventory Intelligence Results:")
    print(test_data[[ "Date","Store ID","Product ID","Inventory Level","Predicted Demand","Inventory_status","Suggested_Reorder_Qty"]].head(20).to_string(index=False))

    mae=mean_absolute_error(y_test,y_pred)
    rmse=mean_squared_error(y_test,y_pred)**0.5
    r2=r2_score(y_test,y_pred)
    print("\nModel evaluation:")
    print("MAE:",mae)
    print("RMSE:",rmse)
    print("R2:",r2)

    baseline_pred=calc_baseline_pred(test_data)
    baseline_mae=mean_absolute_error(y_test,baseline_pred)
    baseline_rmse=mean_squared_error(y_test,baseline_pred)**0.5
    baseline_r2=r2_score(y_test,baseline_pred)
    print("\n7-Day Average baseline:")
    print("MAE:",baseline_mae)
    print("RMSE:",baseline_rmse)
    print("R2:",baseline_r2)

    print("Prediction completed!")
    print("\nFirst 10 actual values:")
    print(y_test.head(10).to_list())
    print("\nFirst 10 predicted values:")
    print(y_pred[:10])

    results=test_data[["Date","Store ID","Product ID","Future Demand"]].copy()
    results["Predicted Demand"]=y_pred
    results["Absolute_Error"]=(results["Future Demand"]-results["Predicted Demand"]).abs()
    print("\nLargest prediction errors:")
    print(results.sort_values("Absolute_Error",ascending=False).head(20).to_string(index=False))

    print("\nFuture Demand Stats:")
    print(y_test.describe())
    print("\nFuture Demand Percentile:")
    print(y_test.quantile([0.50,0.75,0.90,0.95,0.99]))

    high_demand=test_data[test_data["Future Demand"]>=400]
    print("\nHigh-Demand Cases(>=400):")
    print("Number of cases:",len(high_demand))
    print("\nHoliday/Promotion:")
    print(high_demand["Holiday/Promotion"].value_counts())
    print("\nSeasonality:")
    print(high_demand["Seasonality"].value_counts())
    print("\nProduct:")
    print(high_demand["Product ID"].value_counts())
    print("\nMonth:")
    print(high_demand["Date"].dt.month.value_counts().sort_index())

    print("Time based split completed!")
    print("\nTraining period:")
    print(train_data["Date"].min(),"to",train_data["Date"].max())

    print("\nTesting period:")
    print(test_data["Date"].min(),"to",test_data["Date"].max())

    print("\nTraining data:")
    print("X_train:",X_train.shape)
    print("y_train:",y_train.shape)
    print("\nTesting data:")
    print("X_test:",X_test.shape)
    print("y_test:",y_test.shape)


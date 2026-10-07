# Sales and Inventory Intelligence System

## Project Overview
The Sales & Inventory Intelligence System is a data analytics and machine learning application that uses historical sales and inventory data to predict future product demand and determine whether current inventory is sufficient to meet the predicted demand.

The system combines data preprocessing, exploratory data analysis, SQL-based analysis, feature engineering, machine learning, inventory decision logic, and an interactive Streamlit dashboard.

## Project Workflow

CSV Dataset
↓
Data Validation
↓
Preprocessing
↓
SQLite Database
↓
SQL Analysis
↓
Feature Engineering
↓
Time-Based Train/Test Split
↓
Random Forest Demand Prediction
↓
Inventory Intelligence
↓
Streamlit Dashboard

## Key Features
-Data loading and validation
-Missing-value and Duplicate checking
-Data preprocessing
-Exploratory data analysis
-SQL-based business analysis
-Historical sales feature engineering
-Time-based model evaluation
-Future demand prediction 
-Inventory sufficiency analysis
-Suggested reorder quantity
-Interactive Streamlit dashboard
-CSV dataset upload
-SQLite database integration
-Unit testing with pytest

## Machine Learning

The system uses a Random Forest Regressor to predict next-day product demand.

### Features

The model uses historical sales, rolling sales averages, calendar information, inventory information, pricing, promotions, weather, store, product, category, region, and seasonality information.

### Target

The target represents future demand based on the next day's observed sales.

## Model Evaluation

The model is evaluated using:

-MAE
-RMSE
-R²

A 7-day historical-average baseline is also used for comparison.

The current model performs slightly better than the baseline, but significant errors remain during sudden demand spikes. Further model improvement is considered future work.

## Inventory Intelligence

The predicted demand is compared with current inventory.

If:

Inventory >= Predicted Demand

the system reports:
**Sufficient**

Otherwise:
**Reorder Required**

The suggested reorder quantity is:
Predicted Demand-Current Inventory
with negative values clipped to zero.

## SQL Database

SQLite is used to store the inventory dataset.
SQL queries are used fro business analysis such as:

-Total sales by store
-Product sales ranking
-Inventory risk analysis

## Application

The application is built using Streamlit.

Users can:
1. Upload a CSV dataset.
2. Process the dataset.
3. View predicted demand.
4. Check current inventory status.
5. View suggested reorder quantity.
6. Analyze demand and inventory trends.

## Testing 

The project uses pytest for unit testing.

Current tests cover:

-Date preprocessing
-Negative demand forecast handling
-Inventory status calculation
-Reorder quantity calculation

All current tests pass successfullt.

## Technologies Used
-Python
-Pandas
-NumPy
-Scikit-learn
-SQLite
-SQL
-Streamlit
-Matplotlib
-Pytest

## Project Structure

Sales_Inventory_Intelligence/

├── app/
│   └── app.py
├── data/
│   └── retail_store_inventory.csv
├── database/
│   └── inventory.db
├── src/
│   ├── data_loader.py
│   ├── database.py
│   ├── data_validator.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── model.py
│   ├── inventory_logic.py
│   └── sql_queries.py
├── tests/
│   ├── test_inventory_logic.py
│   └── test_preprocessing.py
└── README.md

## How to Run 

Activate the virtual environment and install the required dependancies.

Then run the Streamlit application:

python -m streamlit run app/app.py

## Future Improvements
-Improve prediction accuracy during sudden demand spikes.
-Experiment with additional forecasting models.
-Improve handling of different uploaded dataset schemas.
-Add more advanced inventory
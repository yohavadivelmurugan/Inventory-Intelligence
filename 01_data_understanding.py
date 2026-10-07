import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv(r"C:\Users\ELCOT\Downloads\sales_inventory_synthetic_dataset_final.csv")
print(df.head())
print(df.shape)
print(df.columns.tolist())
df.info()
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.dtypes)
print(df['CATEGORY'].unique())
print(df["REGION"].unique())
print(df['INVENTORY_STATUS'].unique())
print(df['SUPPLIER_RELIABILITY'].unique())
print(df.describe())
print(df.select_dtypes(include="number").columns.tolist())
print(df.select_dtypes(include="str").columns.tolist())
print(df["CATEGORY"].value_counts())
print(df["PRODUCT_NAME"].value_counts())
print(df["REGION"].value_counts())
print(df["UNIT_SALES"].describe())
print(df.groupby("PROMOTION")["UNIT_SALES"].mean())


plt.hist(df["UNIT_SALES"],bins=10)
plt.xlabel("unit sales")
plt.ylabel("frequency")
plt.title("Distribution of unit sales")
plt.xticks(range(0,16001,2000))
plt.show()


plt.boxplot(df["UNIT_SALES"])
plt.ylabel("Unit sales")
plt.title("Boxplot of unit sales")
plt.show()

Q1=df["UNIT_SALES"].quantile(0.25)
Q3=df["UNIT_SALES"].quantile(0.75)
IQR=Q3-Q1
print(Q1)
print(Q3)
print(IQR)

lower_bound=Q1 - 1.5 * IQR
upper_bound=Q3 + 1.5 * IQR
print(lower_bound)
print(upper_bound)
outliers=df[(df["UNIT_SALES"]<lower_bound) | (df["UNIT_SALES"]>upper_bound)]
print(outliers[["SERIAL_NO","PRODUCT_NAME","UNIT_SALES"]])
correlation=df.select_dtypes(include="number").corr()
plt.figure(figsize=(12,8))
sns.heatmap(correlation,annot=True,fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

monthly_sales=df.groupby("DATE")["UNIT_SALES"].mean()
print(monthly_sales)

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index,monthly_sales.values,marker="o")
plt.xlabel("Date")
plt.ylabel("Average Unit Sales")
plt.title("Monthly average unit sales")
plt.xticks(rotation=45)
plt.show()


highm=monthly_sales.idxmax()
highs=monthly_sales.max()
lowm=monthly_sales.idxmin()
lows=monthly_sales.min()
print(highm,"->",highs)
print(lowm,"->",lows)



monthly_seasonality=df.groupby("MONTH")["SEASONAL_INDEX"].mean()
print(monthly_seasonality)

plt.figure(figsize=(10,5))
plt.plot(monthly_seasonality.index,monthly_seasonality.values,marker="o")
plt.xlabel("Month")
plt.ylabel("Average seasonal index")
plt.title("Monthly average seasonal index")
plt.xticks(range(1,13))
plt.show()


prod_sales=df.groupby("PRODUCT_NAME")["UNIT_SALES"].mean()
print(prod_sales)

plt.figure(figsize=(10,5))
plt.bar(prod_sales.index,prod_sales.values)
plt.xlabel("Product")
plt.ylabel("Average Unit Sales")
plt.title("Average unit sales by product")
plt.xticks(rotation=45)
plt.show()


reg_sales=df.groupby("REGION")["UNIT_SALES"].mean()
print(reg_sales)

plt.figure(figsize=(10,5))
plt.bar(reg_sales.index,reg_sales.values)
plt.xlabel("Region")
plt.ylabel("Average Unit Sales")
plt.title("Average unit sales by Region")
plt.show()

print(df["INVENTORY_STATUS"].value_counts())


cat_col=df.select_dtypes(include="str").columns
for column in cat_col:
    print(df[column].value_counts())

for column in df.columns:
    print(column,";",df[column].nunique())


dup_prod_month=df.duplicated(subset=["PRODUCT_NAME","DATE"]).sum()
print(dup_prod_month)


print(df["NEXT_MONTH_DEMAND"].describe())
print(df[["DATE","PRODUCT_NAME","UNIT_SALES","NEXT_MONTH_DEMAND"]].head(10))

print(df[["DATE","PRODUCT_NAME","UNIT_SALES","NEXT_MONTH_DEMAND"]].sort_values(["PRODUCT_NAME","DATE"]).head(20))

print(df[["DATE","PRODUCT_NAME","UNIT_SALES","NEXT_MONTH_DEMAND"]].sort_values(["PRODUCT_NAME","DATE"]).head(20).to_string(index=False))

print(df["UNIT_SALES"].corr(df["NEXT_MONTH_DEMAND"]))
berry=df[df["PRODUCT_NAME"]=="Berry Juice"]
print(berry["UNIT_SALES"].corr(berry["NEXT_MONTH_DEMAND"]))
print(df["DATE"].dtype)


df["DATE"]=pd.to_datetime(df["DATE"])
print(df['DATE'].dtype)

df["YEAR"]=df["DATE"].dt.year
df["MONTH_FEATURE"]=df["DATE"].dt.month
df["DAY_OF_WEEK"]=df["DATE"].dt.dayofweek
print(df[["DATE","YEAR","MONTH_FEATURE","DAY_OF_WEEK"]].head(10))


df=df.sort_values(["PRODUCT_NAME","DATE"])
df["PREV_MONTH_SALES"]=(df.groupby("PRODUCT_NAME")["UNIT_SALES"].shift(1))
print(df[["DATE","PRODUCT_NAME","UNIT_SALES","PREV_MONTH_SALES"]].head(15).to_string(index=False))

df["ROLLING_3M"]=(df.groupby("PRODUCT_NAME")["UNIT_SALES"].transform(lambda x: x.shift(1).rolling(3).mean()))
print(df[["DATE","PRODUCT_NAME","UNIT_SALES","PREV_MONTH_SALES","ROLLING_3M"]].head(15).to_string(index=False))

df_model=df.dropna(subset=["PREV_MONTH_SALES","ROLLING_3M"]).copy()
df["SALES_CHANGE"]=(df["UNIT_SALES"]-df["PREV_MONTH_SALES"])
print(df[["DATE","PRODUCT_NAME","UNIT_SALES","PREV_MONTH_SALES","SALES_CHANGE"]].head(15).to_string(index=False))


df["SALES_CHANGE_PCT"]=((df["UNIT_SALES"]-df["PREV_MONTH_SALES"])/df["PREV_MONTH_SALES"])*100
print(df[["DATE","PRODUCT_NAME","UNIT_SALES","PREV_MONTH_SALES","SALES_CHANGE","SALES_CHANGE_PCT"]].head(15).to_string(index=False))
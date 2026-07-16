"""
Now I am building the ETL pipeline for the TelcoInsight project. The pipeline will handle:

E - Extract : Read the 3 simulated source system CSVs
T - Transform : Clean, standardize, and join into one business-ready dataset
L - Load : Push the clean dataset into a PostgreSQL staging table
"""
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, URL

#Extract: Read the 3 simulated source system CSVs
crm_df = pd.read_csv("data/processed/crm_data.csv")
billing_df = pd.read_csv("data/processed/billing_data.csv")
usage_df = pd.read_csv("data/processed/usage_data.csv")

"""
print(f"CRM Data: {crm_df.shape[0]} rows, {crm_df.shape[1]} columns")
print(f"Billing Data: {billing_df.shape[0]} rows, {billing_df.shape[1]} columns")
print(f"Usage Data: {usage_df.shape[0]} rows, {usage_df.shape[1]} columns")

Output: 
CRM Data: 7043 rows, 13 columns
Billing Data: 7043 rows, 6 columns
Usage Data: 7043 rows, 14 columns
"""

#Transform: Clean, standardize, and join into one business-ready dataset

'''While checking the data, I noticed that the 'Total Charges' column in the billing_df has some missing values. 
#I will handle this by filling the missing values with 0 and converting the column to float type.
#Why 0? because all these are the new customers who haven't completed their first billing cycle.
#I am not dropping them, because they are valid customers'''

billing_df["Total Charges"] = billing_df["Total Charges"].replace(" ", "0")

#Converting the 'Total Charges' column to float type and making them NAN.
billing_df["Total Charges"] = pd.to_numeric(billing_df["Total Charges"], errors="coerce")

#Filling NAN values with 0.
billing_df["Total Charges"] = billing_df["Total Charges"].fillna(0)


'''Now I will standardize yes/no columns to boolean values (1 for Yes, 0 for No).'''
#creating a function

def boolean(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].map({"Yes": True, "No": False}).fillna(df[col])
    return df

crm_df = boolean(crm_df, ["Partner", "Dependents"])
billing_df = boolean(billing_df, ["Paperless Billing"])

#In usage_df, there are some columns which have more than 2 unique values, like 'Yes', 'No', 'No internet service', and 'No phone service'.
#Here I will convert 'No internet service' and 'No phone service' to 'No' for the relevant columns, and then convert them to boolean values.

def convert_to_no(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace({"No internet service": "No", "No phone service": "No"})
    return df

usage_df = convert_to_no(usage_df, ["Phone Service", "Multiple Lines", "Online Security", "Online Backup", "Device Protection", "Tech Support", "Streaming TV", "Streaming Movies"])
usage_df = boolean(usage_df, ["Phone Service", "Multiple Lines", "Online Security", "Online Backup", "Device Protection", "Tech Support", "Streaming TV", "Streaming Movies"])

'''Now here i will follow a business rule Tenure Buckets and create a new column 'Tenure Bucket' '''

#why?? beacuse it is easier to analyze the churn rate based on tenure buckets rather than individual months. This will help in identifying patterns and trends in customer behavior over time.
def tenure_buckets(months):
    if months <= 12:
        return "0-12 months"
    elif months <= 24:
        return "12-24 months"
    elif months <= 36:
        return "24-36 months"
    elif months <= 48:
        return "36-48 months"
    else:
        return "48+ months"
    
crm_df["Tenure Bucket"] = crm_df["Tenure Months"].apply(tenure_buckets)

'''Now I will merge the 3 dfs into 1 clean dataset using the common key 'CustomerID'.'''
merged_df = crm_df.merge(billing_df, on="CustomerID", how="inner")
merged_df = merged_df.merge(usage_df, on="CustomerID", how="inner")

'''
print(f"Merged Data: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
print(merged_df.head())
print(merged_df.info())
print(merged_df.describe())
print(merged_df.isnull().sum())
print(merged_df.duplicated().sum())
'''


'''Load: Push the clean dataset into a PostgreSQL staging table'''
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

connection_url = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(connection_url)

merged_df.to_sql("staging_customer_360", engine, if_exists="replace", index=False)

#print("Data loaded successfully into table: staging_customer_360")
#print("\nETL Pipeline completed successfully!")
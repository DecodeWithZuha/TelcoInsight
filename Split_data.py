""" TelcoIsight: Script to split the Kaggle Telco Customer Churn dataset into 3 separate CSVs

Purpose: Simulate a real telecom environment where customer data lives in
multiple separate source systems. This script splits the single Kaggle
dataset into 3 CSVs representing:
    1. CRM System       -> customer/account demographic data
    2. Billing System   -> financial/billing data
    3. Usage System     -> services subscribed + churn outcome
 
Each file is linked by the common key: CustomerID """

#import libraries
import pandas as pd
import os

#Defining the path of the dataset
Raw_data_path = "data/raw/Telco_customer_churn.xlsx"
Split_data_path = "data/processed"

os.makedirs(Split_data_path, exist_ok=True) #this creates the processed folder if it doesn't exist

#Loading the raw data into a pandas dataframe
df = pd.read_excel(Raw_data_path)

#checking the shape of the loaded dataset
#print(f"loaded dataset: {df.shape[0]} rows and {df.shape[1]} columns") [Output--> loaded dataset: 7043 rows and 33 columns ]

#Splitting the 1st CSV: CRM System -> customer/account demographic data
crm_cols = [
    "CustomerID", "Gender", "Senior Citizen", "Partner", "Dependents",
    "Country", "State", "City", "Zip Code", "Latitude", "Longitude",
    "Tenure Months", "Contract"
]
crm_df = df[crm_cols]
crm_df.to_csv(f"{Split_data_path}/crm_data.csv", index=False)

#Splitting the 2nd CSV: Billing System -> financial/billing data
billing_cols = [
    "CustomerID", "Monthly Charges", "Total Charges",
    "Payment Method", "Paperless Billing", "CLTV"
]
billing_df = df[billing_cols]
billing_df.to_csv(f"{Split_data_path}/billing_data.csv", index=False)

#Splitting the 3rd CSV: Usage System -> services subscribed + churn outcome
usage_cols = [
    "CustomerID", "Phone Service", "Multiple Lines", "Internet Service",
    "Online Security", "Online Backup", "Device Protection", "Tech Support",
    "Streaming TV", "Streaming Movies", "Churn Label", "Churn Value", "Churn Score", "Churn Reason"
]
usage_df = df[usage_cols]
usage_df.to_csv(f"{Split_data_path}/usage_data.csv", index=False)

print("\nSplit complete. Files created:")
print(f" - {Split_data_path}/crm_data.csv       ({crm_df.shape[0]} rows, {crm_df.shape[1]} cols)")
print(f" - {Split_data_path}/billing_data.csv   ({billing_df.shape[0]} rows, {billing_df.shape[1]} cols)")
print(f" - {Split_data_path}/usage_data.csv     ({usage_df.shape[0]} rows, {usage_df.shape[1]} cols)")
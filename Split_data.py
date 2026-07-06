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
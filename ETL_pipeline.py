"""
Now I am building the ETL pipeline for the TelcoInsight project. The pipeline will handle:

E - Extract : Read the 3 simulated source system CSVs
T - Transform : Clean, standardize, and join into one business-ready dataset
L - Load : Push the clean dataset into a PostgreSQL staging table
"""

import pandas as pd
from sqlalchemy import create_engine

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

#While checking the data, I noticed that the 'Total Charges' column in the billing_df has some missing values. 
#I will handle this by filling the missing values with 0 and converting the column to float type.
#Why 0? because all these are the new customers who haven't completed their first billing cycle.
#I am not dropping them, because they are valid customers
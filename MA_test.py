##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import csv
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

##############################################
# Loading Data
##############################################


df_flow = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dailyflow_0117_1220.csv", sep = ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\static_var.csv", sep= ";")

##############################################
# Code
##############################################

# control
#print(df_flow.head)
#print(df_staic.head)


# aggregate from daily to weekly flows
df_flow = df_flow.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Estimated Share Class Net Flow (Daily) 2017-01-01 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-02 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-03 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-31 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_flow_weekly = df_flow.groupby([i//7 for i in range(0,1456)], axis = 1).sum() # aggregate daily to weekly

name = df_static["Name"] # adding back necessary columns
Fund_Legal_Name = df_static["Fund Legal Name"]
FundId = df_static["FundId"]
SecId = df_static["SecId"]
ISIN = df_static["ISIN"]

df_flow_weekly.insert(0, "Name", name)
df_flow_weekly.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_flow_weekly.insert(2, "FundId", FundId)
df_flow_weekly.insert(3, "SecId", SecId)
df_flow_weekly.insert(4, "ISIN", ISIN)


# delete all funds with no flow data
df_flow_weekly.replace(0, np.nan, inplace=True)
df_flow_weekly = df_flow_weekly.dropna(axis="index", how= "any", thresh= 6)


# delete all weeks with no flow data
df_flow_weekly = df_flow_weekly.dropna(axis="columns", how= "all")
# nothing has changed, all weeks have at least one flow datapoint


# aggregate from share class to fund level using FundId
df_flow_weekly_fundlevel = df_flow_weekly.groupby("FundId").sum()
print(df_flow_weekly_fundlevel)


# check whether aggregating worked
n = len(pd.unique(df_flow_weekly["FundId"]))
print(n)
# aggregating worked because old dataframe has 1022 unique values which equals number of rows of new dataframe







#for line in df_flow:
#    data = line.strip().split(";")
#    data = [x.replace("Estimated Share Class Net Flow (Daily) ", "") for x in data]
#    data = [x.replace(" Base Currency", "") for x in data]
#    print(df_flow)
#with open("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv\\dailyflow012019_012021.csv") as f:








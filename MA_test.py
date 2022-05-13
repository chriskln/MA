##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd

##############################################
# Loading Data
##############################################

df_flow = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dailyflow_0117_1220.csv", sep = ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\static_var.csv", sep= ";")
df_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dailyreturn_0117_1220.csv", sep= ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_tna = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\monthlyTNA_012017_122020.csv", sep= ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})


##############################################
# Code
##############################################

# control
#print(df_flow.head)
#print(df_staic.head)
#print(df_tna.head)
#print(df_return.head)


##############################################
# Aggregate from daily to weekly flows and returns
##############################################

# aggregate from daily to weekly flows
df_flow = df_flow.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Estimated Share Class Net Flow (Daily) 2017-01-01 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-02 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-03 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-31 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_flow_weekly = df_flow.groupby([i//7 for i in range(0,1456)], axis = 1).sum()

df_flow_weekly.columns = pd.date_range(start="2017-01-04", end="2020-12-23", periods=208).strftime("%B %d, %Y") # change column headers to datetime

name = df_static["Name"] # add back necessary columns
Fund_Legal_Name = df_static["Fund Legal Name"]
FundId = df_static["FundId"]
SecId = df_static["SecId"]
ISIN = df_static["ISIN"]

df_flow_weekly.insert(0, "Name", name)
df_flow_weekly.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_flow_weekly.insert(2, "FundId", FundId)
df_flow_weekly.insert(3, "SecId", SecId)
df_flow_weekly.insert(4, "ISIN", ISIN)

# aggregate from daily to weekly returns
df_return = df_return.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Return (Day to Day) 2017-01-01 to 2017-01-01 EUR", "Return (Day to Day) 2017-01-02 to 2017-01-02 EUR", "Return (Day to Day) 2017-01-03 to 2017-01-03 EUR", "Return (Day to Day) 2020-12-31 to 2020-12-31 EUR", "Return (Day to Day) 2020-12-30 to 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_return = df_return.div(100)
df_return = df_return.add(1)
df_return_weekly = df_return.groupby([i//7 for i in range(0,1456)], axis = 1).prod()
df_return_weekly = df_return_weekly.sub(1)
df_return_weekly = df_return_weekly.mul(100)

df_return_weekly.columns = pd.date_range(start="2017-01-04", end="2020-12-23", periods=208).strftime("%B %d, %Y") # change column headers to datetime

df_return_weekly.insert(0, "Name", name) # add back necessary columns
df_return_weekly.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_return_weekly.insert(2, "FundId", FundId)
df_return_weekly.insert(3, "SecId", SecId)
df_return_weekly.insert(4, "ISIN", ISIN)

print(df_return_weekly.iloc[:, :6])


##############################################
# Aggregate from monthly to weekly TNA
##############################################

#df_tna_weekly = df_tna[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]].copy()
#forthweek = (df_tna["Net Assets - share class (Monthly) 2017-04 EUR"] - df_tna.merge(df_flow_weekly, on="SecId")["3"]) / (1 + df_tna.merge(df_return_weekly, on="SecId")["3"])
#df_tna_weekly.insert(5, "Jan-4-2017", forthweek)
#print(df_tna_weekly)

##############################################
# Data Trimming
##############################################

# delete all funds with no flow data
df_flow_weekly.replace(0, np.nan, inplace=True)
df_flow_weekly = df_flow_weekly.dropna(axis="index", how="any", thresh= 6)

# delete all funds with no return data
df_return_weekly.replace(0, np.nan, inplace=True)
df_return_weekly = df_return_weekly.dropna(axis="index", how="all", thresh=6)

# delete all weeks with no flow data
df_flow_weekly = df_flow_weekly.dropna(axis="columns", how= "all")
# nothing has changed, all weeks have at least one flow datapoint

# delete all weeks with no return data
df_return_weekly = df_return_weekly.dropna(axis="columns", how="all")
# nothing has changed, all weeks have at least one return datapoint


##############################################
# Aggregate from share class to fund level
##############################################

# aggregate from share class to fund level using FundId
df_flow_weekly_fundlevel = df_flow_weekly.groupby("FundId").sum()
#print(df_flow_weekly_fundlevel)
#df_return_weekly_fundlevel =df_return_weekly.groupby("FundId").mean() # weighted average using prior week's TNA


# check whether aggregating worked
n = len(pd.unique(df_flow_weekly["FundId"]))
#print(n)
# aggregating worked because old dataframe has 1022 unique values which equals number of rows of new dataframe
















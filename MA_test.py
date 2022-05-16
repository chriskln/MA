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
df_tna = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\monthlyTNA_0117_1220.csv", sep= ";")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\sutainability_data_012017_122020.csv", sep= ";")


##############################################
# Overview
##############################################

# initial look at all data
#print(df_flow.head)
#print(df_static.head)
#print(df_tna.head)
#print(df_return.head)
#print(df_sus.head)

# number of different funds in dataset
#print(df_static["FundId"].nunique())

# number of share classes investing in different investment areas
df_static["count"] = 1
share_class_count = df_static.groupby("Investment Area")["count"].count()
#print(share_class_count)

# number of institutional share classes
df_static["count"] = 1
insti_count = df_static.groupby(["Institutional"])["count"].count()
#print(insti_count)

# number of share classes having certain sustainability ratings as of 12/2020
df_sus["count"] = 1
sus_count = df_sus.groupby(["Morningstar Sustainability Rating™ 2020-12"])["count"].count()
#print(sus_count)

# check for duplicates
df_static = df_static.drop_duplicates(subset = "ISIN", keep = "last")
#print(share_class_count)
# no duplicates in dataframe


##############################################
# Aggregate from daily to weekly data
##############################################

# flows
df_flow = df_flow.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Estimated Share Class Net Flow (Daily) 2017-01-01 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-02 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-03 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-31 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_flow_weekly = df_flow.groupby([i//7 for i in range(0,1456)], axis = 1).sum()

# returns
df_return = df_return.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Return (Day to Day) 2017-01-01 to 2017-01-01 EUR", "Return (Day to Day) 2017-01-02 to 2017-01-02 EUR", "Return (Day to Day) 2017-01-03 to 2017-01-03 EUR", "Return (Day to Day) 2020-12-31 to 2020-12-31 EUR", "Return (Day to Day) 2020-12-30 to 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_return = df_return.div(100)
df_return = df_return.add(1)
df_return_weekly = df_return.groupby([i//7 for i in range(0,1456)], axis = 1).prod()
df_return_weekly = df_return_weekly.sub(1)
df_return_weekly = df_return_weekly.mul(100)


##############################################
# Change column headers to date format
##############################################

# flows
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

# returns
df_return_weekly.columns = pd.date_range(start="2017-01-04", end="2020-12-23", periods=208).strftime("%B %d, %Y") # change column headers to datetime

df_return_weekly.insert(0, "Name", name) # add back necessary columns
df_return_weekly.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_return_weekly.insert(2, "FundId", FundId)
df_return_weekly.insert(3, "SecId", SecId)
df_return_weekly.insert(4, "ISIN", ISIN)

# total net assets
df_tna = df_tna.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_tna.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_tna.insert(0, "Name", name) # add back necessary columns
df_tna.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_tna.insert(2, "FundId", FundId)
df_tna.insert(3, "SecId", SecId)
df_tna.insert(4, "ISIN", ISIN)

# sustainability ratings
df_sus = pd.melt(df_sus, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_sus")
print(df_sus.tail(10000))

##############################################
# Data Trimming
##############################################

# delete all share classes with no flow data
df_flow_weekly.replace(0, np.nan, inplace=True)
df_flow_weekly = df_flow_weekly.dropna(axis="index", how="any", thresh= 6)

# delete all share classes with no return data
df_return_weekly.replace(0, np.nan, inplace=True)
df_return_weekly = df_return_weekly.dropna(axis="index", how="all", thresh=6)

# delete all share classes with no tna data
df_tna.replace(0, np.nan, inplace=True)
df_tna = df_tna.dropna(axis="index", how="all", thresh=6)

# delete all weeks with no flow data
df_flow_weekly = df_flow_weekly.dropna(axis="columns", how= "all")
# nothing has changed, all weeks have at least one flow datapoint

# delete all weeks with no return data
df_return_weekly = df_return_weekly.dropna(axis="columns", how="all")
# nothing has changed, all weeks have at least one return datapoint

# delete all months with no tna data
df_tna = df_tna.dropna(axis="columns", how="all")
# nothing has changed, all months have at least one tna datapoint


##############################################
# Re-format dataframes
##############################################
df_return_weekly = pd.melt(df_return_weekly, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="weekly_return")
#print(df_return_weekly.iloc[:, -2:])

df_flow_weekly = pd.melt(df_flow_weekly, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="weekly_flow")
#print(df_flow_weekly.iloc[:, -2:])

df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")
#print(df_tna.iloc[:, -2:])

df_sus = pd.melt(df_sus, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_sus")
df_sus["Date"] = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
#print(df_sus.tail(10000))

##############################################
# Aggregate from share class to fund level
##############################################

# aggregate from share class to fund level using FundId
#df_flow_weekly_fundlevel = df_flow_weekly.groupby("FundId").sum()
#print(df_flow_weekly_fundlevel)
#df_return_weekly_fundlevel =df_return_weekly.groupby("FundId").mean() # weighted average using prior week's TNA


# check whether aggregating worked
#n = len(pd.unique(df_flow_weekly["FundId"]))
#print(n)
# aggregating worked because old dataframe has 1022 unique values which equals number of rows of new dataframe


##############################################
# Aggregate from monthly to weekly TNA
##############################################













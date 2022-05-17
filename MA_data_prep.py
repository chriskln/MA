##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

##############################################
# Loading Data
##############################################

df_flow = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dailyflow_0117_1220.csv", sep = ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\static_var.csv", sep= ";")
df_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dailyreturn_0117_1220.csv", sep= ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_tna = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\monthlyTNA_0117_1220.csv", sep= ";")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\sus_rating_abs.csv", sep= ";")
df_env = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_env_score.csv", sep= ";")
df_soc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_soc_score.csv", sep= ";")
df_gov = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_gov_score.csv", sep= ";")
df_car = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\car_risk_score.csv", sep= ";")
df_exp = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\annual_expense_ratio.csv", sep= ";")
df_star = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\star_rating.csv", sep= ";")


##############################################
# Overview
##############################################

# initial look at all data
#print(df_flow.head)
#print(df_static.head)
#print(df_tna.head)
#print(df_return.head)
#print(df_sus.head)
#print(df_exp.head)
#print(df_star.head)

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
df_static = df_static.drop(["count"], axis=1)

# number of share classes having certain sustainability ratings as of 12/2020
df_sus["count"] = 1
sus_count = df_sus.groupby(["Morningstar Sustainability Rating™ 2020-12"])["count"].count()
#print(sus_count)
df_sus = df_sus.drop(["count"], axis=1)

# check for duplicates
df_static = df_static.drop_duplicates(subset = "ISIN", keep = "last")
#print(share_class_count)
# no duplicates in dataframe


##############################################
# Flows
##############################################

# aggregate from daily to weekly data
df_flow = df_flow.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Estimated Share Class Net Flow (Daily) 2017-01-01 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-02 EUR", "Estimated Share Class Net Flow (Daily) 2017-01-03 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-31 EUR", "Estimated Share Class Net Flow (Daily) 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_flow_weekly = df_flow.groupby([i//7 for i in range(0,1456)], axis = 1).sum()

# change column headers to date format
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

# data trimming
#df_flow_weekly.replace(0, np.nan, inplace=True)
#df_flow_weekly = df_flow_weekly.dropna(axis="index", how="any", thresh= 6)

# re-format dataframe
df_flow_weekly = pd.melt(df_flow_weekly, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="weekly_flow")


##############################################
# Returns
##############################################

# aggregate from daily to weekly data
df_return = df_return.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Return (Day to Day) 2017-01-01 to 2017-01-01 EUR", "Return (Day to Day) 2017-01-02 to 2017-01-02 EUR", "Return (Day to Day) 2017-01-03 to 2017-01-03 EUR", "Return (Day to Day) 2020-12-31 to 2020-12-31 EUR", "Return (Day to Day) 2020-12-30 to 2020-12-30 EUR"]) # dropping str columns to calculate and dropping columns so that start is on Wednesday
df_return = df_return.div(100)
df_return = df_return.add(1)
df_return_weekly = df_return.groupby([i//7 for i in range(0,1456)], axis = 1).prod()
df_return_weekly = df_return_weekly.sub(1)
df_return_weekly = df_return_weekly.mul(100)

# change column headers to date format
df_return_weekly.columns = pd.date_range(start="2017-01-04", end="2020-12-23", periods=208).strftime("%B %d, %Y") # change column headers to datetime

df_return_weekly.insert(0, "Name", name) # add back necessary columns
df_return_weekly.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_return_weekly.insert(2, "FundId", FundId)
df_return_weekly.insert(3, "SecId", SecId)
df_return_weekly.insert(4, "ISIN", ISIN)

# delete all share classes with no return data
#df_return_weekly.replace(0, np.nan, inplace=True)
#df_return_weekly = df_return_weekly.dropna(axis="index", how="all", thresh=6)

# re-format dataframe
df_return_weekly = pd.melt(df_return_weekly, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="weekly_return")

# calculate prior months' return

#print(df_return_weekly.iloc[:, -2:])


##############################################
# TNA
##############################################

# change column headers to date format
df_tna = df_tna.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_tna.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_tna.insert(0, "Name", name) # add back necessary columns
df_tna.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_tna.insert(2, "FundId", FundId)
df_tna.insert(3, "SecId", SecId)
df_tna.insert(4, "ISIN", ISIN)

# delete all share classes with no tna data
#df_tna.replace(0, np.nan, inplace=True)
#df_tna = df_tna.dropna(axis="index", how="all", thresh=6)

# re-format dataframe
#df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date_tna", value_name="monthly_tna")

# delete all share classes with less than $5m tna in previous week

# obtain weekly tna

##############################################
# Sustainability Measures
##############################################

# change column headers to date format
df_sus = df_sus.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_sus.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_sus.insert(0, "Name", name) # add back necessary columns
df_sus.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_sus.insert(2, "FundId", FundId)
df_sus.insert(3, "SecId", SecId)
df_sus.insert(4, "ISIN", ISIN)

df_env = df_env.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_env.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_env.insert(0, "Name", name) # add back necessary columns
df_env.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_env.insert(2, "FundId", FundId)
df_env.insert(3, "SecId", SecId)
df_env.insert(4, "ISIN", ISIN)

df_soc = df_soc.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_soc.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_soc.insert(0, "Name", name) # add back necessary columns
df_soc.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_soc.insert(2, "FundId", FundId)
df_soc.insert(3, "SecId", SecId)
df_soc.insert(4, "ISIN", ISIN)

df_gov = df_gov.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_gov.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_gov.insert(0, "Name", name) # add back necessary columns
df_gov.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_gov.insert(2, "FundId", FundId)
df_gov.insert(3, "SecId", SecId)
df_gov.insert(4, "ISIN", ISIN)

df_car = df_car.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_car.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_car.insert(0, "Name", name) # add back necessary columns
df_car.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_car.insert(2, "FundId", FundId)
df_car.insert(3, "SecId", SecId)
df_car.insert(4, "ISIN", ISIN)

# delete all share classes with no sustainability rating
df_sus.replace(0, np.nan, inplace=True)
df_sus = df_sus.dropna(axis="index", how="all", thresh=6)


##############################################
# Controls
##############################################

# age
df_static = df_static.dropna(axis="index", how="all")
df_static["Inception Date"] = pd.to_datetime(df_static["Inception Date"], format= "%d.%m.%Y") # dtype
df_static["d_end"] = date(2020, 12, 31)
df_static["d_end"] = pd.to_datetime(df_static["d_end"], format="%Y-%m-%d") # dtype
df_static["Age"] = df_static["d_end"] - df_static["Inception Date"] # calculation
df_static["Age"] = df_static["Age"] / np.timedelta64(1, "Y") # convert to years

# star rating
df_star = df_star.drop(columns=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]) # dropping str columns to calculate
df_star.columns = pd.date_range(start="2017-01-01", end="2020-12-31", periods=48).strftime("%B, %Y")
df_star.insert(0, "Name", name) # add back necessary columns
df_star.insert(1, "Fund Legal Name", Fund_Legal_Name)
df_star.insert(2, "FundId", FundId)
df_star.insert(3, "SecId", SecId)
df_star.insert(4, "ISIN", ISIN)

df_star = df_star.dropna(axis="index", how="all")

##############################################
# Merge
##############################################

# obtain weekly tna
df_calc_tna = pd.merge(df_flow_weekly, df_return_weekly, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")

df_tna = df_tna.rename(columns={"January, 2017": "January 04, 2017", "February, 2017": "February 01, 2017"})
df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")

df_calc_tna = pd.merge(df_calc_tna, df_tna, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")

group = df_calc_tna.groupby("ISIN")
df_calc_tna["monthly_tna_lag1"] = group["monthly_tna"].shift(1)
print(df_calc_tna.iloc[:6000, -3:]) # python kennt den 01.01.17 nicht und daher alle lagged tna's nan

#df_calc_tna["monthly_tna"].fillna(0, inplace=True)
#group = df_calc_tna.groupby("ISIN")
#df_calc_tna["monthly_tna_lag1"] = group["monthly_tna"].shift
#print(df_calc_tna)

#print(df_return_weekly.iloc[:, -3:])
#df_tna_sub = df_tna["ISIN"]
#df_tna_sub =
#print(df_tna_sub)

#print(df_calc_tna.iloc[:100, -3:])

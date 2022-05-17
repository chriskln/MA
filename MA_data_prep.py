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
df_static = df_static.drop_duplicates(subset="ISIN", keep="last")
#print(share_class_count)
# no duplicates in dataframe


##############################################
# Flows
##############################################

# data trimming
df_flow.replace(0, np.nan, inplace=True)
df_flow = df_flow.dropna(axis="index", how="any", thresh=6)

# change headers to date format
df_flow = pd.melt(df_flow, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_flow")
df_flow["Date"] = df_flow["Date"].str.slice(39, 49, 1)
df_flow["Date"] = pd.to_datetime(df_flow["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly data
df_flow_weekly = df_flow.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").sum().reset_index()
df_flow_weekly = df_flow_weekly.rename(columns={"daily_flow": "weekly_flow"})
#print(df_flow_weekly)


##############################################
# Returns
##############################################

# data trimming
df_return.replace(0, np.nan, inplace=True)
df_return = df_return.dropna(axis="index", how="any", thresh=6)

# change column headers to date format
df_return = pd.melt(df_return, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_return")
df_return["Date"] = df_return["Date"].str.slice(20, 30, 1)
df_return["Date"] = pd.to_datetime(df_return["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly data
df_return["daily_return"] = df_return["daily_return"].div(100)
df_return["daily_return"] = df_return["daily_return"].add(1)
df_return_weekly = df_return.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").prod().reset_index()
df_return_weekly["daily_return"] = df_return_weekly["daily_return"].sub(1)
df_return_weekly["daily_return"] = df_return_weekly["daily_return"].mul(100)
df_return_weekly = df_return_weekly.rename(columns={"daily_return": "weekly_return"})

# calculate prior months' return

#print(df_return_weekly.iloc[:, -3:])


##############################################
# TNA
##############################################

# change column headers to date format
df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")
df_tna["Date"] = df_tna["Date"].str.slice(35, 42, 1)
df_tna["Date"] = pd.to_datetime(df_tna["Date"], format="%Y-%m-%d")

# delete all share classes with no tna data
#df_tna.replace(0, np.nan, inplace=True)
#df_tna = df_tna.dropna(axis="index", how="all", thresh=6)

# delete all share classes with less than $5m tna in previous week

# obtain weekly tna

##############################################
# Sustainability Measures
##############################################

# change column headers to date format
df_sus = pd.melt(df_sus, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_sus")
df_sus["Date"] = df_sus["Date"].str.slice(35, 42, 1)
df_sus["Date"] = pd.to_datetime(df_sus["Date"], format="%Y-%m-%d")

df_env = pd.melt(df_env, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_env")
df_env["Date"] = df_env["Date"].str.slice(35, 42, 1)
df_env["Date"] = pd.to_datetime(df_env["Date"], format="%Y-%m-%d")

df_soc = pd.melt(df_soc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_soc")
df_soc["Date"] = df_soc["Date"].str.slice(28, 35, 1)
df_soc["Date"] = pd.to_datetime(df_soc["Date"], format="%Y-%m-%d")

df_gov = pd.melt(df_gov, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_gov")
df_gov["Date"] = df_gov["Date"].str.slice(32, 39, 1)
df_gov["Date"] = pd.to_datetime(df_gov["Date"], format="%Y-%m-%d")

df_car = pd.melt(df_car, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_car")
df_car["Date"] = df_car["Date"].str.slice(18, 25, 1)
df_car["Date"] = pd.to_datetime(df_car["Date"], format="%Y-%m-%d")

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
df_star = pd.melt(df_star, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_star")
df_star["Date"] = df_star["Date"].str.slice(15, 22, 1)
df_star["Date"] = pd.to_datetime(df_star["Date"], format="%Y-%m-%d")

df_star = df_star.dropna(axis="index", how="all")

##############################################
# Merge
##############################################

# obtain weekly tna
#df_calc_tna = pd.merge(df_flow_weekly, df_return_weekly, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")

#df_tna = df_tna.rename(columns={"January, 2017": "January 04, 2017", "February, 2017": "February 01, 2017"})
#df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")

#df_calc_tna = pd.merge(df_calc_tna, df_tna, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")

#group = df_calc_tna.groupby("ISIN")
#df_calc_tna["monthly_tna_lag1"] = group["monthly_tna"].shift(1)
#print(df_calc_tna.iloc[:6000, -3:]) # python kennt den 01.01.17 nicht und daher alle lagged tna's nan

#df_calc_tna["monthly_tna"].fillna(0, inplace=True)
#group = df_calc_tna.groupby("ISIN")
#df_calc_tna["monthly_tna_lag1"] = group["monthly_tna"].shift
#print(df_calc_tna)

#print(df_return_weekly.iloc[:, -3:])
#df_tna_sub = df_tna["ISIN"]
#df_tna_sub =
#print(df_tna_sub)

#print(df_calc_tna.iloc[:100, -3:])

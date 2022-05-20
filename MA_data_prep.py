##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd
from datetime import date
from scipy.stats.mstats import winsorize

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
# no duplicates in dataframe


##############################################
# Flows
##############################################

# data trimming
#df_flow.replace(0, np.nan, inplace=True)
#df_flow = df_flow.dropna(axis="index", how="any", thresh=6)

# change headers to date format
df_flow = pd.melt(df_flow, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_flow")
df_flow["Date"] = df_flow["Date"].str.slice(39, 49, 1)
df_flow["Date"] = pd.to_datetime(df_flow["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly data
df_flow_weekly = df_flow.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").sum().reset_index()
df_flow_weekly = df_flow_weekly.rename(columns={"daily_flow": "weekly_flow"})

# winsorize data at 99% and 1% level
df_flow_weekly["weekly_flow_w"] = winsorize(df_flow_weekly["weekly_flow"], limits=(0.01, 0.01))
flow_win_check = df_flow_weekly[["weekly_flow_w","weekly_flow"]].describe() # winsorizing worked
df_flow_weekly = df_flow_weekly.drop(["weekly_flow"], axis=1)
df_flow_weekly = df_flow_weekly.rename(columns={"weekly_flow_w": "weekly_flow"})

##############################################
# Returns
##############################################

# data trimming
#df_return.replace(0, np.nan, inplace=True) # an der stelle kontraproduktiv weil 01.01.2017 wird gebraucht für tna weekly berechnung
#df_return = df_return.dropna(axis="index", how="any", thresh=6)

# change column headers to date format
df_return = pd.melt(df_return, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_return")
df_return["Date"] = df_return["Date"].str.slice(20, 30, 1)
df_return["Date"] = pd.to_datetime(df_return["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly data
df_return["daily_return"] = df_return["daily_return"].div(100)
df_return["daily_return"] = df_return["daily_return"].add(1)
df_return_weekly = df_return.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").prod().reset_index()
df_return_weekly["daily_return"] = df_return_weekly["daily_return"].sub(1)
#df_return_weekly["daily_return"] = df_return_weekly["daily_return"].mul(100)
df_return_weekly = df_return_weekly.rename(columns={"daily_return": "weekly_return"})

# winsorize data at 99% and 1% level
df_return_weekly["weekly_return_w"] = winsorize(df_return_weekly["weekly_return"], limits=(0.01, 0.01))
return_win_check = df_return_weekly[["weekly_return_w","weekly_return"]].describe() # winsorizing worked
df_return_weekly = df_return_weekly.drop(["weekly_return"], axis=1)
df_return_weekly = df_return_weekly.rename(columns={"weekly_return_w": "weekly_return"})

# calculate prior months' return

#print(df_return_weekly.iloc[:, -3:])


##############################################
# TNA
##############################################

# change column headers to date format
df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")
df_tna["Date"] = df_tna["Date"].str.slice(35, 42, 1)
df_tna["Date"] = pd.to_datetime(df_tna["Date"], format="%Y-%m-%d")
df_tna["month_year"] = pd.to_datetime(df_tna["Date"]).dt.to_period("M")

# delete all share classes with no tna data
#df_tna.replace(0, np.nan, inplace=True)
#df_tna = df_tna.dropna(axis="index", how="all", thresh=6)

# winsorize data at 99% and 1% level
df_tna.replace(0, np.nan, inplace=True)
df_tna["monthly_tna_w"] = winsorize(df_tna["monthly_tna"], limits=(0.01, 0.01), nan_policy="omit")
tna_win_check = df_tna[["monthly_tna_w", "monthly_tna"]].describe()# winsorizing worked
df_tna = df_tna.drop(columns="monthly_tna")
df_tna = df_tna.rename(columns={"monthly_tna_w": "monthly_tna"})

# get lagged tna
group = df_tna.groupby("ISIN")
df_tna["monthly_tna_lag1"] = group["monthly_tna"].shift(1)

#print(df_tna.iloc[:,-3:])

#print(df_tna.iloc[:,-2:])



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
# Obtain weekly TNA
##############################################

# merge all necessary data
df_calc_tna = pd.merge(df_flow_weekly, df_return_weekly, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")
df_calc_tna["month_year"] = pd.to_datetime(df_calc_tna["Date"]).dt.to_period("M")
df_calc_tna = pd.merge(df_calc_tna, df_tna, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "month_year"], how="left")
df_calc_tna = df_calc_tna.fillna(0)

# identifier for every new datapoint that is available at month ending
df_calc_tna["count"] = 0
#df_calc_tna.loc[df_calc_tna.monthly_tna_lag1.ne(0).groupby(df_calc_tna["ISIN"]).idxmax(), "count"] = 1
#df_calc_tna["weekly_tna"] = np.where(df_calc_tna["count"] == 1, df_calc_tna["weekly_flow"] + (1 + df_calc_tna["weekly_return"]) * df_calc_tna["monthly_tna_lag1"], 0)

for j in range(1, len(df_calc_tna)):
    if df_calc_tna.loc[j, "month_year"] != df_calc_tna.loc[j - 1, "month_year"]:
        df_calc_tna.loc[j, "count"] = 1
    else:
        df_calc_tna.loc[j, "count"] = 0

# calculation of weekly TNA
df_calc_tna.loc[0, "weekly_tna"] = 0
for i in range(0, len(df_calc_tna)):
    if df_calc_tna.loc[i, "count"] == 1:
        df_calc_tna.loc[i, "weekly_tna"] = df_calc_tna.loc[i, "weekly_flow"] + (1 + df_calc_tna.loc[i, "weekly_return"]) * df_calc_tna.loc[i, "monthly_tna_lag1"]
    elif df_calc_tna.loc[i, "monthly_tna_lag1"] != 0 and df_calc_tna.loc[i, "count"] != 1:
        df_calc_tna.loc[i, "weekly_tna"] = df_calc_tna.loc[i, "weekly_flow"] + (1 + df_calc_tna.loc[i, "weekly_return"]) * df_calc_tna.loc[i - 1, "weekly_tna"]
    elif df_calc_tna.loc[i, "monthly_tna"] == 0:
        df_calc_tna.loc[i, "weekly_tna"] = 0
    else:
        df_calc_tna.loc[i, "weekly_tna"] = 0

df_tna_weekly = df_calc_tna[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date_x", "weekly_tna"]].copy()
df_tna_weekly = df_tna_weekly.rename(columns={"Date_x": "Date"})

#print(df_calc_tna.iloc[:100, -4:])
#df_calc_tna.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_calc_tna_new.csv")

##############################################
# Translate all data from share class to fund level
##############################################

# returns
group1 = df_tna_weekly.groupby("ISIN")
df_tna_weekly["weekly_tna_lag1"] = group1["weekly_tna"].shift(1) # compute lagged weekly tna as weight for weekly return
df_return_weekly_fundlevel = pd.merge(df_return_weekly, df_tna_weekly, on=["Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="left")
df_return_weekly_fundlevel = pd.merge(df_return_weekly_fundlevel, df_static, on=["Fund Legal Name", "FundId", "SecId", "ISIN"], how="left") # obtain indicator for whether share class "primarily aimed at instis or not"
df_return_weekly_fundlevel = df_return_weekly_fundlevel.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date", "d_end", "Age"])
df_return_weekly_fundlevel["return_tna"] = df_return_weekly_fundlevel["weekly_return"] * df_return_weekly_fundlevel["weekly_tna_lag1"]
df_return_weekly_fundlevel = df_return_weekly_fundlevel.drop(columns=["weekly_tna", "weekly_return"])
df_return_weekly_fundlevel = df_return_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).sum().reset_index()
df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["return_tna"] / df_return_weekly_fundlevel["weekly_tna_lag1"] # calculate final weigthed average

# tna
df_tna_weekly = df_tna_weekly.drop(columns="weekly_tna_lag1")
df_tna_weekly_fundlevel = pd.merge(df_tna_weekly, df_static, on=["Fund Legal Name", "FundId", "SecId", "ISIN"], how="left") # obtain indicator for whether share class "primarily aimed at instis or not"
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date", "d_end", "Age"])
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).sum().reset_index() # calculate weekly tna at fund level by summing all ISIN's within a FundId
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.rename(columns={"weekly_tna": "weekly_tna_fundlevel"})

# flows
df_flow_weekly_fundlevel = pd.merge(df_flow_weekly, df_static, on=["Fund Legal Name", "FundId", "SecId", "ISIN"], how="left") # obtain indicator for whether share class "primarily aimed at instis or not"
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date", "d_end", "Age"])
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).sum().reset_index()

#print(df_return_weekly_fundlevel.iloc[:,-3:])
#print(df_return_weekly_fundlevel.iloc[:, -4:])
#df_flow_weekly_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_flow_weekly_fundlevel.csv")

##############################################
# Delete nan columns
##############################################
#df_tna.replace(0, np.nan, inplace=True)
#df_tna = df_tna.dropna(axis="index", how="all", thresh=6)
df_return_weekly_fundlevel = df_return_weekly_fundlevel.replace(0, np.nan)
df_return_weekly_fundlevel = df_return_weekly_fundlevel.drop(columns=["weekly_tna_lag1", "return_tna"])
#df_return_weekly_fundlevel = df_return_weekly_fundlevel.dropna(axis="index", how="all", subset=["weekly_return_fundlevel"], thresh=5)
df_return_weekly_fundlevel = df_return_weekly_fundlevel["weekly_return_fundlevel"].isna()
df_return_weekly_fundlevel = df_return_weekly_fundlevel.groupby("FundId").transform("all")

df_return_weekly_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_return_weekly_fundlevel.csv")

df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.replace(0, np.nan)
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.dropna(axis="index", how="all", subset=["weekly_tna_fundlevel"], thresh=6)

df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.replace(0, np.nan)
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.dropna(axis="index", how="all", subset=["weekly_flow"], thresh=6)
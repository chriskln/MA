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

df_flow = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\dailyflow_0117_1220.csv", sep = ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\static_var.csv", sep= ";")
df_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\dailyreturn_0117_1220.csv", sep= ";", dtype = {"Name": str, "Fund Legal Name": str, "FundId": str, "SecId": str, "ISIN": str})
df_m_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\monthly_return_17_20.csv", sep= ";")
df_tna = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\monthlyTNA_0117_1220.csv", sep= ";")
df_star = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\star_rating.csv", sep= ";")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\sustainability_rating.csv", sep= ";")
df_env = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\environmental_risk_score.csv", sep= ";")
df_soc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\social_risk_score.csv", sep= ";")
df_gov = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\governance_risk_score.csv", sep= ";")
df_car = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\carbon_risk_score.csv", sep= ";")


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

# number of different ISIN's in dataset
#print(df_static["ISIN"].nunique())
# 5317

# number of different funds in dataset
#print(df_static["FundId"].nunique())
# 1119

# number of share classes investing in different investment areas
df_static["count"] = 1
share_class_count = df_static.groupby("Investment Area")["count"].count()
#print(share_class_count)
#Austria                   20
#Belgium                    4
#Denmark                    6
#Euroland                 832
#Europe                  3327
#Europe (North)            87
#Europe Emerging Mkts     164
#Europe ex UK             313
#Finland                    1
#France                    19
#Germany                  220
#Greece                     4
#Italy                     36
#Norway                     4
#Slovakia                   1
#Spain                     11
#Switzerland              174
#United Kingdom           266

# number of institutional share classes
df_static["count"] = 1
insti_count = df_static.groupby(["Institutional"])["count"].count()
#print(insti_count)
df_static = df_static.drop(["count"], axis=1)
#Institutional
#No     4371
#Yes    1118

# number of share classes having a sustainability rating as of 12/2020
df_sus["count"] = 1
sus_count = df_sus.groupby(["Morningstar Sustainability Rating™ 2020-12"])["count"].count()
#print(sus_count)
df_sus = df_sus.drop(["count"], axis=1)
# Above Average    1076
# Average          1707
# Below Average     986
# High              605
# Low               235


##############################################
# Flows
##############################################

# change headers to date format
df_flow = pd.melt(df_flow, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_flow")
df_flow["Date"] = df_flow["Date"].str.slice(39, 49, 1)
df_flow["Date"] = pd.to_datetime(df_flow["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly data
df_flow_weekly = df_flow.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").sum().reset_index()
df_flow_weekly = df_flow_weekly.rename(columns={"daily_flow": "weekly_flow"})


##############################################
# Daily and monthly returns
##############################################

# change column headers to date format
df_return = pd.melt(df_return, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="daily_return")
df_return["Date"] = df_return["Date"].str.slice(20, 30, 1)
df_return["Date"] = pd.to_datetime(df_return["Date"], format="%Y-%m-%d")

df_m_return = pd.melt(df_m_return, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_return")
df_m_return["Date"] = df_m_return["Date"].str.slice(15, 22, 1)
df_m_return["Date"] = pd.to_datetime(df_m_return["Date"], format="%Y-%m-%d")
df_m_return["month_year"] = pd.to_datetime(df_m_return["Date"]).dt.to_period("M")
df_m_return = df_m_return.drop(columns=["Date"])
df_m_return = df_m_return.rename(columns={"month_year": "Date"})
df_m_return["monthly_return"] = df_m_return["monthly_return"].div(100)

# aggregate from daily to weekly data
df_return["daily_return"] = df_return["daily_return"].div(100)
df_return["daily_return"] = df_return["daily_return"].add(1)
df_return_weekly = df_return.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("W", on="Date").prod().reset_index()
df_return_weekly["daily_return"] = df_return_weekly["daily_return"].sub(1)
#df_return_weekly["daily_return"] = df_return_weekly["daily_return"].mul(100)
df_return_weekly = df_return_weekly.rename(columns={"daily_return": "weekly_return"})


##############################################
# TNA
##############################################

# change column headers to date format
df_tna = pd.melt(df_tna, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_tna")
df_tna["Date"] = df_tna["Date"].str.slice(35, 42, 1)
df_tna["Date"] = pd.to_datetime(df_tna["Date"], format="%Y-%m-%d")
df_tna["month_year"] = pd.to_datetime(df_tna["Date"]).dt.to_period("M")

# get lagged tna
group = df_tna.groupby("ISIN")
df_tna["monthly_tna_lag1"] = group["monthly_tna"].shift(1)

# get tna from next month
ggroup = df_tna.groupby("ISIN")
df_tna["monthly_tna_lag-1"] = ggroup["monthly_tna"].shift(-1)

# control for extreme reversal pattern in tna data (as in Pastor Appendix)
df_tna["d_assets"] = (df_tna["monthly_tna"] - df_tna["monthly_tna_lag1"]) / df_tna["monthly_tna_lag1"]
df_tna["rev_pattern"] = (df_tna["monthly_tna_lag-1"] - df_tna["monthly_tna"]) / (df_tna["monthly_tna"] - df_tna["monthly_tna_lag1"])

for q in range(0, len(df_tna)):
    if abs(df_tna.loc[q, "d_assets"]) >= 0.5 and -0.75 > df_tna.loc[q, "rev_pattern"] > -1.25 and df_tna.loc[q, "monthly_tna_lag1"] >= 10000000:
        df_tna.loc[q, "rev_indicator"] = 1
    else:
        df_tna.loc[q, "rev_indicator"] = 0
# results in 32 cases of extreme reversal pattern

# in these cases, set monthly tna to missing
for p in range(0, len(df_tna)):
    if df_tna.loc[p, "rev_indicator"] == 1:
        df_tna.loc[p, "monthly_tna"] = 0
    else:
        continue

df_tna = df_tna.drop(columns=["d_assets", "rev_pattern", "monthly_tna_lag-1", "rev_indicator"])


##############################################
# Obtain weekly TNA
##############################################

# merge all necessary data
df_merged = pd.merge(df_flow_weekly, df_return_weekly, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="outer")
df_merged["month_year"] = pd.to_datetime(df_merged["Date"]).dt.to_period("M")
df_merged = pd.merge(df_merged, df_tna, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "month_year"], how="outer")
df_merged = df_merged.fillna(0)
df_merged = df_merged.rename(columns={"Date_x": "Date", "weekly_flow_x": "weekly_flow"})
df_merged = df_merged.drop(columns=["Date_y"])

# identifier for every new datapoint that is available at month ending
df_merged["count"] = 0

for j in range(1, len(df_merged)):
    if df_merged.loc[j, "month_year"] != df_merged.loc[j - 1, "month_year"]:
        df_merged.loc[j, "count"] = 1
    else:
        df_merged.loc[j, "count"] = 0

# assume datapoint in 2017-01 being equal to the one of the same month
df_merged["monthly_tna_lag1"] = np.where(df_merged["monthly_tna_lag1"] == 0, df_merged["monthly_tna"], df_merged["monthly_tna_lag1"])

# calculation of weekly TNA
for i in range(0, len(df_merged)):
    if df_merged.loc[i, "monthly_tna"] == 0:
        df_merged.loc[i, "weekly_tna"] = 0
    elif df_merged.loc[i, "count"] == 1:
        df_merged.loc[i, "weekly_tna"] = df_merged.loc[i, "weekly_flow"] + (1 + df_merged.loc[i, "weekly_return"]) * df_merged.loc[i, "monthly_tna_lag1"]
    elif df_merged.loc[i, "monthly_tna_lag1"] != 0 and df_merged.loc[i, "count"] != 1:
        df_merged.loc[i, "weekly_tna"] = df_merged.loc[i, "weekly_flow"] + (1 + df_merged.loc[i, "weekly_return"]) * df_merged.loc[i - 1, "weekly_tna"]
    else:
        df_merged.loc[i, "weekly_tna"] = 0

# policy / assumption for negative weekly tna: weekly tna should equal monthly tna
for t in range(0, len(df_merged)):
    if df_merged.loc[t, "weekly_tna"] < 0:
        df_merged.loc[t, "weekly_tna"] = df_merged.loc[t, "monthly_tna"]
    else:
        continue

df_tna_weekly = df_merged[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "weekly_tna"]].copy()


df_return_weekly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_return_weekly.csv")
df_tna_weekly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_tna_weekly.csv")
df_flow_weekly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_flow_weekly.csv")
df_m_return.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_m_return.csv")
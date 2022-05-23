##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd
from sklearn import preprocessing
from datetime import date
from scipy.stats.mstats import winsorize

##############################################
# Loading Data
##############################################

df_flow_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_trimmed\\df_flow_weekly_fundlevel.csv", sep= ",")
df_return_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_trimmed\\df_return_weekly_fundlevel.csv", sep= ",")
df_tna_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_trimmed\\df_tna_weekly_fundlevel.csv", sep= ",")

df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.loc[:, ~df_flow_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_return_weekly_fundlevel = df_return_weekly_fundlevel.loc[:, ~df_return_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.loc[:, ~df_tna_weekly_fundlevel.columns.str.contains("^Unnamed")]


##############################################
# Calculate flow variables
##############################################

df_flow_weekly_fundlevel = pd.merge(df_flow_weekly_fundlevel, df_tna_weekly_fundlevel, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="left")

# 1: fund flows (See Hartzmark and Sussma, p. 2798)
group = df_flow_weekly_fundlevel.groupby(["FundId", "Institutional"])
df_flow_weekly_fundlevel["weekly_tna_fundlevel_lag1"] = group["weekly_tna_fundlevel"].shift(1)
df_flow_weekly_fundlevel["fund_flows"] = df_flow_weekly_fundlevel["weekly_flow"] / df_flow_weekly_fundlevel["weekly_tna_fundlevel_lag1"]

# 2: normalized flows (See Hartzmark and Sussma, p. 2798)
df_flow_weekly_fundlevel["Decile_Rank"] = df_flow_weekly_fundlevel.groupby("Date").weekly_tna_fundlevel.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_flow_weekly_fundlevel["normalized_flows"] = df_flow_weekly_fundlevel.groupby("Decile_Rank").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

#print(df_flow_weekly_fundlevel.iloc[:, -3:])
#df_flow_weekly_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_flow_weekly_fundlevel.csv")


##############################################
# Calculate prior month's return
##############################################

group1 = df_return_weekly_fundlevel.groupby(["FundId", "Institutional"])
df_return_weekly_fundlevel["prior_months_return"] = group1["weekly_return_fundlevel"].shift(1)
#print(df_return_weekly_fundlevel.iloc[:, -4:])


##############################################
# Add restriction on at least $5m. tna by end of 2020
##############################################

df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.set_index("FundId")[df_tna_weekly_fundlevel.groupby("FundId").apply(lambda x: all([set(x["weekly_tna_fundlevel"]) > {5000000}]))]
print(df_tna_weekly_fundlevel)
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

df_flow_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_flow_weekly_fundlevel.csv", sep= ",")
df_return_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_return_weekly_fundlevel.csv", sep= ",")
df_tna_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_tna_weekly_fundlevel.csv", sep= ",")

df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.loc[:, ~df_flow_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_return_weekly_fundlevel = df_return_weekly_fundlevel.loc[:, ~df_return_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.loc[:, ~df_tna_weekly_fundlevel.columns.str.contains("^Unnamed")]

df_return_weekly_fundlevel = df_return_weekly_fundlevel.replace(0, np.nan)
df_return_weekly_fundlevel = df_return_weekly_fundlevel["FundID", "weekly_return_fundlevel"].dropna(axis=0, how="all")
print(df_return_weekly_fundlevel)
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
# Delete nan columns
##############################################

#df_return_weekly_fundlevel = df_return_weekly_fundlevel.replace(0, np.nan)
#df_return_weekly_fundlevel = df_return_weekly_fundlevel.dropna(axis=0, how="any")

#df_return_clear = df_return_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Institutional"]).sum().reset_index()
#df_return_clear = df_return_clear.replace(0, np.nan)
#df_return_clear = df_return_clear.dropna(axis=0, how="any")

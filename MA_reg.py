##############################################
# MASTER THESIS
##############################################

##############################################
# Data Analysis
##############################################

import numpy as np
import pandas as pd
from sklearn import preprocessing
import datetime
from datetime import date
from scipy.stats.mstats import winsorize
from functools import reduce
import math

##############################################
# Loading Data
##############################################

df_final = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_final.csv", sep= ",")


# delete unnamed columns
df_final = df_final.loc[:, ~df_final.columns.str.contains("^Unnamed")]


##############################################
# Overall data trimming
##############################################

################################
# Set timeframe to 01/2019 - 12/2020
################################

# lagged tna before setting timeframe
group = df_final.groupby(["FundId", "Institutional"])
df_final["weekly_tna_fundlevel_lag1"] = group["weekly_tna_fundlevel"].shift(1)

# setting timeframe
df_final["Date"] = df_final["Date"].astype("datetime64[ns]")
df_final["month_year"] = df_final["month_year"].astype("datetime64[ns]")
start = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end = pd.to_datetime("2020-12-31", format="%Y-%m-%d")
df_final = df_final[df_final["Date"].between(start, end)].reset_index()
df_final = df_final.drop(columns=["index"])


################################
# Retain those funds having non-missing flow data
################################

df_final = df_final.groupby(["FundId", "Institutional"]).filter(lambda x: x["weekly_flow"].ne(0).all())

################################
# Add restriction on at least $1m. fund size by previous week (Hartzmark and Sussman)
################################

df_final = df_final.groupby(["FundId", "Institutional"]).filter(lambda x: (x.weekly_tna_fundlevel >= 1000000).all())

# number of funds in dataset
#print(df_final["FundId"].nunique())
################################
# Delete rows with no sustainability rating
################################



##############################################
# Calculate missing variables
##############################################

################################
# Calculate flow variables
################################

df_final["Date"] = df_final["Date"].astype("datetime64[ns]")

# 1: fund flows (See Hartzmark and Sussma, p. 2798)
df_final["fund_flows"] = df_final["weekly_flow"] / df_final["weekly_tna_fundlevel_lag1"]
df_final = df_final.drop(columns=["weekly_tna_fundlevel_lag1"])
df_final = df_final[df_final["Date"] > pd.to_datetime("2018-12-30", format="%Y-%m-%d")]

# 2: normalized flows (See Hartzmark and Sussma, p. 2798)
df_final["Decile_Rank"] = df_final.groupby("Date").weekly_tna_fundlevel.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_final["normalized_flows"] = df_final.groupby("Decile_Rank").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))


##############################################
# Summary Statistics
##############################################

df_describe = df_final[["Fund Legal Name", "FundId", "Date", "fund_flows", "normalized_flows", "weekly_tna_fundlevel",
                        "weekly_return_fundlevel", "prior_month_return", "rolling_12_months_return", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car", "Age"]].copy()
summary = df_describe.describe()
print(summary)


#print(df_final)
#df_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_final_testlook.csv")

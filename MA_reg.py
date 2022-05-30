##############################################
# MASTER THESIS
##############################################

##############################################
# Data Analysis
##############################################

import numpy as np
from sklearn import datasets
import openpyxl
import pandas as pd
import researchpy as rp
from sklearn import preprocessing
import datetime
from datetime import date
import scipy
from scipy.stats.mstats import winsorize
from scipy import stats
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

# translate weekly tna into $ million
df_final["weekly_tna_fundlevel"] = df_final["weekly_tna_fundlevel"] / 1000000


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
df_final["fund_flows"] = df_final["fund_flows"].mul(100) # values in percent

# 2: normalized flows (See Hartzmark and Sussma, p. 2798)
df_final["Decile_Rank"] = df_final.groupby("Date").weekly_tna_fundlevel.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_final["normalized_flows"] = df_final.groupby("Decile_Rank").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))


##############################################
# Summary Statistics
##############################################

# summary of most important continuous variables
df_describe = df_final[["Fund Legal Name", "FundId", "Date", "fund_flows", "normalized_flows", "weekly_tna_fundlevel",
                        "weekly_return_fundlevel", "prior_month_return", "rolling_12_months_return", "Age", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# calculate summary
summary = df_describe.describe(percentiles=[.1,.25,.5,.75,.9])
# rename columns
summary = summary.rename(columns={"fund_flows": "Weekly Net Flow (%)", "normalized_flows": "Weekly Normalized Net Flow",
                        "weekly_tna_fundlevel": "Total Net Assets ($ mio.)", "weekly_return_fundlevel": "Weekly Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months Return (%)",
                        "monthly_star": "Star Rating", "monthly_sus": "Globe Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Carbon Designation"})
# round to two decimal places
summary = summary.round(2)
# transpose
summary = summary.transpose()
# add index as a column
summary.reset_index(level=0, inplace=True)
# rename index columns
summary.rename(columns={"index": "Variable", "count": "N", "mean": "Mean", "std": "Std", "min": "Min", "10%": "P10",
                        "25%": "P25", "50%": "P50", "75%": "P75", "90%": "P90", "max": "Max"}, inplace=True)

#print(df_final)
#summary.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\tables\\summary.xlsx", index=False)

# summary of means of most important continuous variables in dependence of globe rating
summary_2 = pd.DataFrame(df_describe.groupby(["monthly_sus"])[["Fund Legal Name", "FundId", "Date", "fund_flows",
                                                               "normalized_flows", "weekly_tna_fundlevel",
                                                               "weekly_return_fundlevel", "prior_month_return",
                                                               "rolling_12_months_return", "Age", "monthly_star",
                                                               "monthly_sus", "monthly_env", "monthly_soc",
                                                               "monthly_gov", "monthly_car"]].mean())
# rename columns
summary_2 = summary_2.rename(columns={"fund_flows": "Weekly Net Flow (%)", "normalized_flows": "Weekly Normalized Net Flow",
                        "weekly_tna_fundlevel": "Total Net Assets ($ mio.)", "weekly_return_fundlevel": "Weekly Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months Return (%)",
                        "monthly_star": "Star Rating", "monthly_sus": "Globe Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Carbon Designation"})
# rename indexes
summary_2 = summary_2.rename(index={5.0: "High", 4.0: "Above Average", 3.0: "Average", 2.0: "Below Average", 1.0: "Low"})
# transpose
summary_2 = summary_2.transpose()
# calculate difference between 5 globes and 1 globe
summary_2["High-Low"] = summary_2["High"] - summary_2["Low"]
#summary_2 = summary_2.transpose()
#summary_2.reset_index(level=0, inplace=True)
#summary_2 = summary_2.rename(columns={"index": "Variable"})
#a = summary_2[summary_2.iloc[0] == summary_2.loc["High"]]
#b = summary_2[summary_2.iloc[0] == summary_2.loc["Low"]]
#T_Stat = scipy.stats.ttest_ind(summary_2.loc["Weekly Net Flow (%)", "High"], summary_2.loc["Weekly Net Flow (%)", "Low"], equal_var=True)
#t_test = rp.ttest(group1= df_final["weekly_flow"][df_final["monthly_sus"] == 5], group1_name="High", group2= df_final["weekly_flow"][df_final["monthly_sus"] == 1], group2_name="Low")

#print(t_test)

#summary_2["t-stat"] = scipy.stats.ttest_ind(summary_2["High"], summary_2["Low"], axis=1)
#print(T_Stat)
print(summary_2)
#summary_2.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\tables\\summary_test.xlsx", index=False)

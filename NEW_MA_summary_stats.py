##############################################
# MASTER THESIS
##############################################

##############################################
# Summary Statistics
##############################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import datasets
import openpyxl
import statistics
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

df_final = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_final.csv", sep= ",")

# delete unnamed and unnecessary columns
df_final = df_final.loc[:, ~df_final.columns.str.contains("^Unnamed")]
df_final = df_final.drop(columns=["year"])

# execute necessary renaming
df_final = df_final.rename(columns={"Mkt-RF": "Mkt_RF"})


##############################################
# Overall data trimming
##############################################

################################
# Set timeframe to 01/2019 - 12/2020
################################

# lagged tna before setting timeframe
group = df_final.groupby(["ISIN"])
df_final["weekly_tna_lag1"] = group["weekly_tna"].shift(1)

# setting overall timeframe
df_final["Date"] = df_final["Date"].astype("datetime64[ns]")
df_final["month_year"] = df_final["month_year"].astype("datetime64[ns]")
start = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end = pd.to_datetime("2020-12-31", format="%Y-%m-%d")
df_final = df_final[df_final["Date"].between(start, end)].reset_index()
df_final = df_final.drop(columns=["index"])


################################
# Assumption: Nan values in dividends mean that fund does not pay out
################################

df_final["weekly_div"] = df_final["weekly_div"].fillna(0)


################################
# Add restriction on at least $1m. of tna by previous week (Hartzmark and Sussman)
################################

df_final = df_final.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).filter(lambda x: (x.weekly_tna_lag1 >= 1000000).all())

# translate weekly tna into € million
df_final["weekly_tna"] = df_final["weekly_tna"] / 1000000

df_final = df_final.reset_index()
df_final = df_final.drop(columns=["index"])


################################
# Retain those funds having non-missing data
################################

df_final = df_final.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).filter(lambda x: x["weekly_flow"].ne(0).all())
df_final = df_final.loc[~df_final.ISIN.isin(df_final.loc[df_final[["utilities", "industrials", "basic_materials",
                                                                   "consumer_cyclical", "real_estate", "technology",
                                                                   "healthcare", "consumer_defensive",
                                                                   "communication_services", "financial_services",
                                                                   "energy", "large_growth", "large_value", "large_core",
                                                                   "mid_growth", "mid_value", "mid_core", "small_core",
                                                                   "small_value", "small_growth",
                                                                   "monthly_sus", "monthly_star", "monthly_env",
                                                                   "monthly_gov", "monthly_soc", "monthly_car",
                                                                   "weekly_expense"]].isna().any(axis=1), "ISIN"])]


# number of ISIN's in dataset
print(df_final["ISIN"].nunique())
# 1449


################################
# Winsorize all continuous variables at 99% and 1% levels
################################

# fund expenses
df_final["weekly_expense"] = winsorize(df_final["weekly_expense"], limits=(0.01, 0.01))

# Fama French 5 factors
df_final["Mkt_RF"] = winsorize(df_final["Mkt_RF"], limits=(0.01, 0.01))
df_final["SMB"] = winsorize(df_final["SMB"], limits=(0.01, 0.01))
df_final["HML"] = winsorize(df_final["HML"], limits=(0.01, 0.01))
df_final["RMW"] = winsorize(df_final["RMW"], limits=(0.01, 0.01))
df_final["CMA"] = winsorize(df_final["CMA"], limits=(0.01, 0.01))

# Dividends
df_final["weekly_div"] = winsorize(df_final["weekly_div"], limits=(0.01, 0.01))

# returns
df_final["weekly_return"] = winsorize(df_final["weekly_return"], limits=(0.01, 0.01))
df_final["prior_month_return"] = winsorize(df_final["prior_month_return"], limits=(0.01, 0.01))
df_final["rolling_12_months_return"] = winsorize(df_final["rolling_12_months_return"], limits=(0.01, 0.01))

# flows
df_final["weekly_flow"] = winsorize(df_final["weekly_flow"], limits=(0.01, 0.01))

# tna
df_final["weekly_tna"] = winsorize(df_final["weekly_tna"], limits=(0.01, 0.01))

# sustainability risk score
df_final["monthly_env"] = winsorize(df_final["monthly_env"], limits=(0.01, 0.01))
df_final["monthly_soc"] = winsorize(df_final["monthly_soc"], limits=(0.01, 0.01))
df_final["monthly_gov"] = winsorize(df_final["monthly_gov"], limits=(0.01, 0.01))

# carbon designation
df_final["monthly_car"] = winsorize(df_final["monthly_car"], limits=(0.01, 0.01))


##############################################
# Calculate missing variables
##############################################

################################
# Calculate normalized expense ratio
################################

# check for outliers in expense ratio data
sns.boxplot(x=df_final["weekly_expense"])
plt.show()
# plot shows several outliers on right tail

# normalized expense ratio
df_final["normalized_exp"] = df_final.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

################################
# Calculate flow variables
################################

df_final["Date"] = df_final["Date"].astype("datetime64[ns]")

# 1: fund flows (See Hartzmark and Sussma, p. 2798)
df_final["fund_flows"] = df_final["weekly_flow"] / df_final["weekly_tna_lag1"]
df_final = df_final.drop(columns=["weekly_tna_lag1"])
df_final = df_final[df_final["Date"] > pd.to_datetime("2018-12-30", format="%Y-%m-%d")]
df_final["fund_flows"] = df_final["fund_flows"].mul(100) # values in percent

# 2: normalized flows (See Hartzmark and Sussma, p. 2798)
df_final["Decile_Rank"] = df_final.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_final["normalized_flows"] = df_final.groupby("Decile_Rank").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))



# to csv
df_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_final_trimmed.csv")



##############################################
# Basic Summary Statistic (01/2019 - 12/2020)
##############################################

# summary of most important continuous variables
df_describe = df_final[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows", "normalized_flows", "weekly_tna",
                        "weekly_return", "prior_month_return", "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# calculate summary
summary = df_describe.describe(percentiles=[.25,.5,.75])

# rename columns
summary = summary.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)",
                        "monthly_star": "Star Rating", "monthly_sus": "Globe Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Low Carbon Risk Score"})

# round to two decimal places
summary = summary.round(2)

# transpose
summary = summary.transpose()

# add index as a column
summary.reset_index(level=0, inplace=True)

# drop min max
#summary = summary.drop(columns=["min", "max"])

# rename index columns
summary.rename(columns={"index": "Variable", "count": "N", "mean": "Mean", "std": "Std", "min": "Min", "max": "Max",
                        "25%": "P25", "50%": "P50", "75%": "P75"}, inplace=True)

# to excel
summary.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary.xlsx", index=False)


##############################################
# Summary Statistic in dependence of globe rating (01/2019 - 12/2020)
##############################################

# create separate dataframe
summary_2 = pd.DataFrame(df_describe.groupby(["monthly_sus"])[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN",
                                                               "Date", "fund_flows", "normalized_flows", "weekly_tna",
                                                               "weekly_return", "prior_month_return",
                                                               "rolling_12_months_return", "weekly_expense",
                                                               "Age", "monthly_star",
                                                               "monthly_env", "monthly_soc", "monthly_gov",
                                                               "monthly_car"]].describe().loc[:,(slice(None), ["count", "mean", "std"])])

# rename columns
summary_2 = summary_2.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)", "monthly_star": "Star Rating",
                        "monthly_env": "Environmental Risk Score", "monthly_soc": "Social Risk Score",
                        "monthly_gov": "Governance Risk Score", "monthly_car": "Low Carbon Risk Score"})

# rename indexes
summary_2 = summary_2.rename(index={5.0: "High", 4.0: "Above Av.", 3.0: "Av.", 2.0: "Below Av.", 1.0: "Low"})

# transpose
summary_2 = summary_2.transpose()
summary_2 = summary_2.reset_index()

# calculate difference between 5 globes and 1 globe
summary_2["High-Low"] = summary_2.loc[summary_2["level_1"] == "mean", "High"] - summary_2.loc[summary_2["level_1"] == "mean", "Low"]

# calculate t-test (t-statistic and p-value)
t_test = scipy.stats.ttest_ind_from_stats(summary_2.loc[summary_2["level_1"] == "mean", "High"],
                                          summary_2.loc[summary_2["level_1"] == "std", "High"],
                                          summary_2.loc[summary_2["level_1"] == "count", "High"],
                                          summary_2.loc[summary_2["level_1"] == "mean", "Low"],
                                          summary_2.loc[summary_2["level_1"] == "std", "Low"],
                                          summary_2.loc[summary_2["level_1"] == "count", "Low"])

# drop std and count
summary_2 = summary_2.groupby(["level_0", "level_1"]).filter(lambda x: (x["level_1"] == "mean").all())

# rename and drop
summary_2 = summary_2.drop(columns=["level_1"])
summary_2 = summary_2.rename(columns={"level_0": "Variable"})
summary_2 = summary_2.reset_index()
summary_2 = summary_2.drop(columns=["index"])

# prep t_test variable
data = np.array([[t_test[0]], [t_test[1]]])
df_ttest = pd.DataFrame(np.concatenate(data))
df_ttest = df_ttest.transpose()

# merge means and t-test results
summary_fin = pd.merge(summary_2, df_ttest, left_index=True, right_index=True)

# rename columns 0 and 1
summary_fin = summary_fin.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
summary_fin = summary_fin.round(2)

# to excel
summary_fin.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_fin.xlsx", index=False)


##############################################
# Summary Statistic in dependence of globe rating: PRE-COVID (01/01/2020 - 22/02/2020)
##############################################

# create separate dataframe
df_describe_pre = df_final[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows", "normalized_flows", "weekly_tna",
                        "weekly_return", "prior_month_return", "rolling_12_months_return", "weekly_expense",
                        "Age", "monthly_star", "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# setting time frame
df_describe_pre["Date"] = df_describe_pre["Date"].astype("datetime64[ns]")
start_pre = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_pre = pd.to_datetime("2020-02-22", format="%Y-%m-%d")
df_describe_pre = df_describe_pre[df_describe_pre["Date"].between(start_pre, end_pre)].reset_index()
df_describe_pre = df_describe_pre.drop(columns=["index"])

# get statistics of dataframe
summary_pre = pd.DataFrame(df_describe_pre.groupby(["monthly_sus"])[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows",
                                                               "normalized_flows", "weekly_tna",
                                                               "weekly_return", "prior_month_return",
                                                               "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                                                               "monthly_env", "monthly_soc", "monthly_gov",
                                                               "monthly_car"]].describe().loc[:,(slice(None), ["count", "mean", "std"])])

# rename columns
summary_pre = summary_pre.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)",
                        "monthly_star": "Star Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Low Carbon Risk Score"})

# rename indexes
summary_pre = summary_pre.rename(index={5.0: "High", 4.0: "Above Av.", 3.0: "Av.", 2.0: "Below Av.", 1.0: "Low"})

# transpose
summary_pre = summary_pre.transpose()
summary_pre = summary_pre.reset_index()

# calculate difference between 5 globes and 1 globe
summary_pre["High-Low"] = summary_pre.loc[summary_pre["level_1"] == "mean", "High"] - summary_pre.loc[summary_pre["level_1"] == "mean", "Low"]

# calculate t-test (t-statistic and p-value)
t_test_pre = scipy.stats.ttest_ind_from_stats(summary_pre.loc[summary_pre["level_1"] == "mean", "High"],
                                          summary_pre.loc[summary_pre["level_1"] == "std", "High"],
                                          summary_pre.loc[summary_pre["level_1"] == "count", "High"],
                                          summary_pre.loc[summary_pre["level_1"] == "mean", "Low"],
                                          summary_pre.loc[summary_pre["level_1"] == "std", "Low"],
                                          summary_pre.loc[summary_pre["level_1"] == "count", "Low"])

# drop std and count
summary_pre = summary_pre.groupby(["level_0", "level_1"]).filter(lambda x: (x["level_1"] == "mean").all())

# rename and drop
summary_pre = summary_pre.drop(columns=["level_1"])
summary_pre = summary_pre.rename(columns={"level_0": "Variable"})
summary_pre = summary_pre.reset_index()
summary_pre = summary_pre.drop(columns=["index"])

# prep t_test variable
data_pre = np.array([[t_test_pre[0]], [t_test_pre[1]]])
df_ttest_pre = pd.DataFrame(np.concatenate(data_pre))
df_ttest_pre = df_ttest_pre.transpose()

# merge means and t-test results
summary_pre_fin = pd.merge(summary_pre, df_ttest_pre, left_index=True, right_index=True)

# rename columns 0 and 1
summary_pre_fin = summary_pre_fin.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
summary_pre_fin = summary_pre_fin.round(2)

# to excel
summary_pre_fin.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_pre.xlsx", index=False)

##############################################
# Summary Statistic in dependence of globe rating: CRASH (23/02/2020 - 22/03/2020)
##############################################

# create separate dataframe
df_describe_crsh = df_final[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows", "normalized_flows", "weekly_tna",
                        "weekly_return", "prior_month_return", "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# setting time frame
df_describe_crsh["Date"] = df_describe_crsh["Date"].astype("datetime64[ns]")
start_crsh = pd.to_datetime("2020-02-23", format="%Y-%m-%d")
end_crsh = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_describe_crsh = df_describe_crsh[df_describe_crsh["Date"].between(start_crsh, end_crsh)].reset_index()
df_describe_crsh = df_describe_crsh.drop(columns=["index"])

# get statistics of dataframe
summary_crsh = pd.DataFrame(df_describe_crsh.groupby(["monthly_sus"])[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows",
                                                               "normalized_flows", "weekly_tna",
                                                               "weekly_return", "prior_month_return",
                                                               "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                                                               "monthly_env", "monthly_soc",
                                                               "monthly_gov", "monthly_car"]].describe().loc[:,(slice(None), ["count", "mean", "std"])])

# rename columns
summary_crsh = summary_crsh.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)",
                        "monthly_star": "Star Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Low Carbon Risk Score"})

# rename indexes
summary_crsh = summary_crsh.rename(index={5.0: "High", 4.0: "Above Av.", 3.0: "Av.", 2.0: "Below Av.", 1.0: "Low"})

# transpose
summary_crsh = summary_crsh.transpose()
summary_crsh = summary_crsh.reset_index()

# calculate difference between 5 globes and 1 globe
summary_crsh["High-Low"] = summary_crsh.loc[summary_crsh["level_1"] == "mean", "High"] - summary_crsh.loc[summary_crsh["level_1"] == "mean", "Low"]

# calculate t-test (t-statistic and p-value)
t_test_crsh = scipy.stats.ttest_ind_from_stats(summary_crsh.loc[summary_crsh["level_1"] == "mean", "High"],
                                          summary_crsh.loc[summary_crsh["level_1"] == "std", "High"],
                                          summary_crsh.loc[summary_crsh["level_1"] == "count", "High"],
                                          summary_crsh.loc[summary_crsh["level_1"] == "mean", "Low"],
                                          summary_crsh.loc[summary_crsh["level_1"] == "std", "Low"],
                                          summary_crsh.loc[summary_crsh["level_1"] == "count", "Low"])

# drop std and count
summary_crsh = summary_crsh.groupby(["level_0", "level_1"]).filter(lambda x: (x["level_1"] == "mean").all())

# rename and drop
summary_crsh = summary_crsh.drop(columns=["level_1"])
summary_crsh = summary_crsh.rename(columns={"level_0": "Variable"})
summary_crsh = summary_crsh.reset_index()
summary_crsh = summary_crsh.drop(columns=["index"])

# prep t_test variable
data_crsh = np.array([[t_test_crsh[0]], [t_test_crsh[1]]])
df_ttest_crsh = pd.DataFrame(np.concatenate(data_crsh))
df_ttest_crsh = df_ttest_crsh.transpose()

# merge means and t-test results
summary_crsh_fin = pd.merge(summary_crsh, df_ttest_crsh, left_index=True, right_index=True)

# rename columns 0 and 1
summary_crsh_fin = summary_crsh_fin.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
summary_crsh_fin = summary_crsh_fin.round(2)

# to excel
summary_crsh_fin.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_crsh.xlsx", index=False)

##############################################
# Summary Statistic in dependence of globe rating: RECOVERY (23/03/2020 - 23/08/2020)
##############################################

# create separate dataframe
df_describe_rec = df_final[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows", "normalized_flows", "weekly_tna",
                        "weekly_return", "prior_month_return", "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# setting time frame
df_describe_rec["Date"] = df_describe_rec["Date"].astype("datetime64[ns]")
start_rec = pd.to_datetime("2020-03-23", format="%Y-%m-%d")
end_rec = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_describe_rec = df_describe_rec[df_describe_rec["Date"].between(start_rec, end_rec)].reset_index()
df_describe_rec = df_describe_rec.drop(columns=["index"])

# get statistics of dataframe
summary_rec = pd.DataFrame(df_describe_rec.groupby(["monthly_sus"])[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows",
                                                               "normalized_flows", "weekly_tna",
                                                               "weekly_return", "prior_month_return",
                                                               "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                                                               "monthly_env", "monthly_soc",
                                                               "monthly_gov", "monthly_car"]].describe().loc[:,(slice(None), ["count", "mean", "std"])])

# rename columns
summary_rec = summary_rec.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)",
                        "monthly_star": "Star Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Low Carbon Risk Score"})

# rename indexes
summary_rec = summary_rec.rename(index={5.0: "High", 4.0: "Above Av.", 3.0: "Av.", 2.0: "Below Av.", 1.0: "Low"})

# transpose
summary_rec = summary_rec.transpose()
summary_rec = summary_rec.reset_index()

# calculate difference between 5 globes and 1 globe
summary_rec["High-Low"] = summary_rec.loc[summary_rec["level_1"] == "mean", "High"] - summary_rec.loc[summary_rec["level_1"] == "mean", "Low"]

# calculate t-test (t-statistic and p-value)
t_test_rec = scipy.stats.ttest_ind_from_stats(summary_rec.loc[summary_rec["level_1"] == "mean", "High"],
                                          summary_rec.loc[summary_rec["level_1"] == "std", "High"],
                                          summary_rec.loc[summary_rec["level_1"] == "count", "High"],
                                          summary_rec.loc[summary_rec["level_1"] == "mean", "Low"],
                                          summary_rec.loc[summary_rec["level_1"] == "std", "Low"],
                                          summary_rec.loc[summary_rec["level_1"] == "count", "Low"])

# drop std and count
summary_rec = summary_rec.groupby(["level_0", "level_1"]).filter(lambda x: (x["level_1"] == "mean").all())

# rename and drop
summary_rec = summary_rec.drop(columns=["level_1"])
summary_rec = summary_rec.rename(columns={"level_0": "Variable"})
summary_rec = summary_rec.reset_index()
summary_rec = summary_rec.drop(columns=["index"])

# prep t_test variable
data_rec = np.array([[t_test_rec[0]], [t_test_rec[1]]])
df_ttest_rec = pd.DataFrame(np.concatenate(data_rec))
df_ttest_rec = df_ttest_rec.transpose()

# merge means and t-test results
summary_rec_fin = pd.merge(summary_rec, df_ttest_rec, left_index=True, right_index=True)

# rename columns 0 and 1
summary_rec_fin = summary_rec_fin.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
summary_rec_fin = summary_rec_fin.round(2)

# to excel
summary_rec_fin.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_rec.xlsx", index=False)

##############################################
# Summary Statistic in dependence of globe rating: POST-RECOVERY (24/08/2020 - 31/12/2020)
##############################################

df_describe_prec = df_final[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows", "normalized_flows", "weekly_tna",
                        "weekly_return", "prior_month_return", "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                        "monthly_sus", "monthly_env", "monthly_soc", "monthly_gov", "monthly_car"]].copy()

# setting time frame
df_describe_prec["Date"] = df_describe_prec["Date"].astype("datetime64[ns]")
start_prec = pd.to_datetime("2020-08-24", format="%Y-%m-%d")
end_prec = pd.to_datetime("2020-12-31", format="%Y-%m-%d")
df_describe_prec = df_describe_prec[df_describe_prec["Date"].between(start_prec, end_prec)].reset_index()
df_describe_prec = df_describe_prec.drop(columns=["index"])

# get statistics of dataframe
summary_prec = pd.DataFrame(df_describe_prec.groupby(["monthly_sus"])[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date", "fund_flows",
                                                               "normalized_flows", "weekly_tna",
                                                               "weekly_return", "prior_month_return",
                                                               "rolling_12_months_return", "weekly_expense", "Age", "monthly_star",
                                                               "monthly_env", "monthly_soc",
                                                               "monthly_gov", "monthly_car"]].describe().loc[:,(slice(None), ["count", "mean", "std"])])

# rename columns
summary_prec = summary_prec.rename(columns={"fund_flows": "Net Flow (%)", "normalized_flows": "Normalized Net Flow",
                        "weekly_tna": "Total Net Assets (€ mio.)", "weekly_return": "Return (%)",
                        "prior_month_return": "Prior Month's Return (%)", "rolling_12_months_return": "Past 12 Months' Return (%)",
                        "weekly_expense": "Expense Ratio (%)", "Age": "Age (years)",
                        "monthly_star": "Star Rating", "monthly_env": "Environmental Risk Score",
                        "monthly_soc": "Social Risk Score", "monthly_gov": "Governance Risk Score",
                        "monthly_car": "Low Carbon Risk Score"})

# rename indexes
summary_prec = summary_prec.rename(index={5.0: "High", 4.0: "Above Av.", 3.0: "Av.", 2.0: "Below Av.", 1.0: "Low"})

# transpose
summary_prec = summary_prec.transpose()
summary_prec = summary_prec.reset_index()

# calculate difference between 5 globes and 1 globe
summary_prec["High-Low"] = summary_prec.loc[summary_prec["level_1"] == "mean", "High"] - summary_prec.loc[summary_prec["level_1"] == "mean", "Low"]

# calculate t-test (t-statistic and p-value)
t_test_prec = scipy.stats.ttest_ind_from_stats(summary_prec.loc[summary_prec["level_1"] == "mean", "High"],
                                          summary_prec.loc[summary_prec["level_1"] == "std", "High"],
                                          summary_prec.loc[summary_prec["level_1"] == "count", "High"],
                                          summary_prec.loc[summary_prec["level_1"] == "mean", "Low"],
                                          summary_prec.loc[summary_prec["level_1"] == "std", "Low"],
                                          summary_prec.loc[summary_prec["level_1"] == "count", "Low"])

# drop std and count
summary_prec = summary_prec.groupby(["level_0", "level_1"]).filter(lambda x: (x["level_1"] == "mean").all())

# rename and drop
summary_prec = summary_prec.drop(columns=["level_1"])
summary_prec = summary_prec.rename(columns={"level_0": "Variable"})
summary_prec = summary_prec.reset_index()
summary_prec = summary_prec.drop(columns=["index"])

# prep t_test variable
data_prec = np.array([[t_test_prec[0]], [t_test_prec[1]]])
df_ttest_prec = pd.DataFrame(np.concatenate(data_prec))
df_ttest_prec = df_ttest_prec.transpose()

# merge means and t-test results
summary_prec_fin = pd.merge(summary_prec, df_ttest_prec, left_index=True, right_index=True)

# rename columns 0 and 1
summary_prec_fin = summary_prec_fin.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
summary_prec_fin = summary_prec_fin.round(2)

# to excel
summary_prec_fin.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_prec.xlsx", index=False)


##############################################
# Create bigger summary table
##############################################

# rename columns in t-test dataframes
df_ttest = df_ttest.rename(columns={0: "t-statistic", 1: "p-value"})
df_ttest_crsh = df_ttest_crsh.rename(columns={0: "t-statistic", 1: "p-value"})
df_ttest_rec = df_ttest_rec.rename(columns={0: "t-statistic", 1: "p-value"})
df_ttest_prec = df_ttest_prec.rename(columns={0: "t-statistic", 1: "p-value"})

# rounding
df_ttest = df_ttest.round(2)
df_ttest_crsh = df_ttest_crsh.round(2)
df_ttest_rec = df_ttest_rec.round(2)
df_ttest_prec = df_ttest_prec.round(2)

# merge all together
summary_table = [summary_fin, df_ttest_crsh, df_ttest_rec, df_ttest_prec]
summary_fin = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), summary_table)

# merge t-test results
d = {"Overall (01/01/2019 - 31/12/2020)": df_ttest, "Crash (23/02/2020 - 22/03/2020)": df_ttest_crsh,
     "Recovery (23/03/2020 - 23/08/2020)": df_ttest_rec, "Post-Recovery (24/08/2020 - 31/12/2020)": df_ttest_prec}
t_tests = pd.concat(d.values(), axis=1, keys=d.keys())

# merge t-test results with overall summary statistic
f = summary_fin[["Low", "Below Av.", "Av.", "Above Av.", "High"]].copy()
d_2 = {"Overall means (01/01/2019 - 31/12/2020)": f}
f = pd.concat(d_2.values(), axis=1, keys=d_2.keys())

summary_total = pd.merge(f, t_tests, right_index=True, left_index=True)

# rename indexes
summary_total = summary_total.rename(index={0: "Net Flow (%)", 1: "Normalized Net Flow",
                        2: "Total Net Assets (€ mio.)", 3: "Return (%)", 4: "Prior Month's Return (%)",
                        5: "Past 12 Months' Return (%)", 6: "Expense Ratio (%)", 7: "Age (years)", 8: "Star Rating", 9: "Environmental Risk Score",
                        10: "Social Risk Score", 11: "Governance Risk Score", 12: "Low Carbon Risk Score"})

# to excel
summary_total.to_excel(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\summary_stats\\summary_total.xlsx")
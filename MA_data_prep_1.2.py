##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd
from sklearn import preprocessing
import datetime
from datetime import date
from datetime import datetime
from scipy.stats.mstats import winsorize
from functools import reduce
import math

##############################################
# Loading Data
##############################################

df_exp = pd.read_csv("C:\\csv_pc\\net_exp.csv", sep= ";")
df_static = pd.read_csv("C:\\csv_pc\\static_var.csv", sep= ";")
df_tur = pd.read_csv("C:\\csv_pc\\turnover.csv", sep= ";")


################################
# Fund Annual Expenses
################################

df_exp = pd.merge(df_exp, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_exp = df_exp.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_exp = pd.melt(df_exp, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="yearly_expense")
df_exp["Date"] = df_exp["Date"].str.slice(36, 40, 1)
df_exp["Date"] = pd.to_datetime(df_exp["Date"], format="%Y-%m-%d")
df_exp = df_exp.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"yearly_expense": "mean"}).reset_index()

for c in range(2, len(df_exp)):
    if math.isnan(df_exp.loc[c, "yearly_expense"]) == True and df_exp.loc[c, "FundId"] == df_exp.loc[c - 1, "FundId"] and df_exp.loc[c, "Institutional"] == df_exp.loc[c - 1, "Institutional"]:
        df_exp.loc[c, "yearly_expense"] = df_exp.loc[c - 1, "yearly_expense"]
    elif math.isnan(df_exp.loc[c, "yearly_expense"]) == True and df_exp.loc[c, "FundId"] == df_exp.loc[c - 2, "FundId"] and df_exp.loc[c, "Institutional"] == df_exp.loc[c - 2, "Institutional"]:
        df_exp.loc[c, "yearly_expense"] = df_exp.loc[c - 2, "yearly_expense"]
    else:
        continue

df_exp["year"] = pd.to_datetime(df_exp["Date"]).dt.to_period("Y")

# obtain weekly expense
df_exp["weekly_expense"] = df_exp["yearly_expense"] / 52
df_exp = df_exp.drop(columns=["Date", "yearly_expense"])
df_exp.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_exp_test.csv")
################################
# Fund Semi-annual Expenses
################################

# split data in cells
#df_exp_semi[[1,2,3,4,5,6,7,8,9,10,11]] = df_exp_semi["Semi-Annual Report Net Expense Ratio History"].str.split(";", n=10, expand=True)
#df_exp_semi = df_exp_semi.drop(columns=["Semi-Annual Report Net Expense Ratio History"])

# merge "Institutional" into dataframe
#df_exp_semi = pd.merge(df_exp_semi, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
#df_exp_semi = df_exp_semi.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])

# data prep
#df_exp_semi = pd.melt(df_exp_semi, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], value_name="semi_ann_expense")
#df_exp_semi = df_exp_semi.drop(columns=["variable"])
#df_exp_semi[["Date", "semi_annual_expense"]] = df_exp_semi["semi_ann_expense"].str.split(" ", n=1, expand=True)
#df_exp_semi = df_exp_semi.drop(columns=["semi_ann_expense"])
#df_exp_semi["Date"] = df_exp_semi["Date"].astype(str)
#df_exp_semi["Date"] = df_exp_semi["Date"].map(lambda x: x.lstrip("[").rstrip("]"))

# drop nan rows
#df_exp_semi = df_exp_semi.dropna(axis=0, how="any", thresh=8)

# drop rows out of time range
#df_exp_semi["Date"] = pd.to_datetime(df_exp_semi["Date"], format="%Y-%m-%d")
#df_exp_semi = df_exp_semi.drop(df_exp_semi[(df_exp_semi.Date < pd.to_datetime("2017-01-01", format="%Y-%m-%d"))].index)
#df_exp_semi = df_exp_semi.drop(df_exp_semi[(df_exp_semi.Date > pd.to_datetime("2020-12-31", format="%Y-%m-%d"))].index)

# prepare for merging
#df_exp_semi["month_year"] = pd.to_datetime(df_exp_semi["Date"]).dt.to_period("M")
#df_exp_semi = df_exp_semi.drop(columns=["Date"])
#df_exp_semi["semi_annual_expense"] = df_exp_semi["semi_annual_expense"].astype(float)

# aggregate tp fund level
#df_exp_semi_fundlevel = df_exp_semi.groupby(["Fund Legal Name", "FundId", "month_year", "Institutional"]).agg({"semi_annual_expense": "mean"}).reset_index()

# translate month_year to year
#df_exp_semi_fundlevel["month_year"] = df_exp_semi_fundlevel["month_year"].astype("datetime64[ns]")
#df_exp_semi_fundlevel["year"] = pd.to_datetime(df_exp_semi_fundlevel["month_year"]).dt.to_period("Y")

# aggregate double observations in a year by mean
#df_exp_semi_fundlevel = df_exp_semi_fundlevel.groupby(["Fund Legal Name", "FundId", "Institutional", "year"]).agg({"semi_annual_expense": "mean"}).reset_index()

# merge semi annual and annual expense ratio datasets
#df_exp_total = pd.merge(df_exp, df_exp_semi_fundlevel, on=["Fund Legal Name", "FundId", "Institutional", "year"], how="outer")

# nan policy
#for c in range(2, len(df_exp_total)):
#    if math.isnan(df_exp_total.loc[c, "yearly_expense"]) == True:
#        df_exp_total.loc[c, "yearly_expense"] = df_exp_total.loc[c, "semi_annual_expense"]
#    else:
#        continue


################################
# Turnover Ratio
################################

df_tur = pd.merge(df_tur, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_tur = df_tur.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_tur = pd.melt(df_tur, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="yearly_turn")
df_tur["Date"] = df_tur["Date"].str.slice(21, 25, 1)
df_tur["Date"] = pd.to_datetime(df_tur["Date"], format="%Y-%m-%d")
df_tur = df_tur.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"yearly_turn": "mean"}).reset_index()

for c in range(2, len(df_tur)):
    if math.isnan(df_tur.loc[c, "yearly_turn"]) == True and df_tur.loc[c, "FundId"] == df_tur.loc[c - 1, "FundId"] and df_tur.loc[c, "Institutional"] == df_tur.loc[c - 1, "Institutional"]:
        df_tur.loc[c, "yearly_turn"] = df_tur.loc[c - 1, "yearly_turn"]
    elif math.isnan(df_tur.loc[c, "yearly_turn"]) == True and df_tur.loc[c, "FundId"] == df_tur.loc[c - 2, "FundId"] and df_tur.loc[c, "Institutional"] == df_tur.loc[c - 2, "Institutional"]:
        df_tur.loc[c, "yearly_turn"] = df_tur.loc[c - 2, "yearly_turn"]
    else:
        continue

df_tur["year"] = pd.to_datetime(df_tur["Date"]).dt.to_period("Y")
df_tur["weekly_turn"] = df_tur["yearly_turn"] / 52
df_tur.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_tur_test.csv")
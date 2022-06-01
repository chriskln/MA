##############################################
# MASTER THESIS
##############################################

##############################################
# Regressions
##############################################

import numpy as np
from sklearn import datasets
import openpyxl
import statistics
import pandas as pd
import statsmodels as statsmodels
import statsmodels.formula.api as sm
import statsmodels.stats.sandwich_covariance as sw
import researchpy as rp
from sklearn import preprocessing
import datetime
from datetime import date
import scipy
from scipy.stats.mstats import winsorize
from scipy import stats
from functools import reduce
import math
import stargazer as stargazer
from stargazer.stargazer import Stargazer

##############################################
# Loading Data
##############################################

df_final_trimmed = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_final_trimmed.csv", sep= ",")

# delete unnamed columns
df_final_trimmed = df_final_trimmed.loc[:, ~df_final_trimmed.columns.str.contains("^Unnamed")]

##############################################
# Dummy Variables
##############################################

df_final_trimmed["Date"] = df_final_trimmed["Date"].astype("datetime64[ns]")
df_final_trimmed["month_year"] = df_final_trimmed["month_year"].astype("datetime64[ns]")

# dummy for timeframe COVID CRASH
for t in range(0, len(df_final_trimmed)):
    if pd.to_datetime("2020-02-23", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-03-22", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV"] = 1
    else:
        df_final_trimmed.loc[t, "COV"] = 0


# dummy for globe rating as of 31/12/2019
for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 5:
        df_final_trimmed.loc[g, "High_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "High_ESG"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 1:
        df_final_trimmed.loc[g, "Low_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "Low_ESG"] = 0


##############################################
# Interaction terms
##############################################

df_final_trimmed["High_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["Ret_COV"] = df_final_trimmed["COV"] * df_final_trimmed["weekly_return_fundlevel"]
df_final_trimmed["One_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["Twelve_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["Star_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_star"]


##############################################
# First Model
##############################################

df_reg1 = df_final_trimmed

# timeframe for reg1: 01/01/2019 - 22/03/2020
df_reg1["Date"] = df_reg1["Date"].astype("datetime64[ns]")
start_reg1 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_reg1 = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_reg1 = df_reg1[df_reg1["Date"].between(start_reg1, end_reg1)].reset_index()
df_reg1 = df_reg1.drop(columns=["index"])

# reg 1
mod1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Ret_COV + weekly_return_fundlevel + One_M_RET_COV + Twelve_M_RET_COV + rolling_12_months_return + log_tna + monthly_star + Star_COV"
reg1 = sm.ols(formula=mod1, data=df_reg1).fit()
summary_reg1 = reg1.summary()
print(summary_reg1)

# reg 2
mod2 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Ret_COV + weekly_return_fundlevel + One_M_RET_COV + Twelve_M_RET_COV + rolling_12_months_return + log_tna + monthly_star + Star_COV"
reg2 = sm.ols(formula=mod2, data=df_reg1).fit()
summary_reg2 = reg2.summary()
print(summary_reg2)

# regressionen nochmal überdenken und von den variablen her vllt mehr am paper orientieren (zb return)
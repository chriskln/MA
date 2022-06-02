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
from statsmodels.iolib.summary2 import summary_col
from IPython.core.display import HTML
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
import stargazer
from stargazer.stargazer import Stargazer

##############################################
# Loading Data
##############################################

df_final_trimmed = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_final_trimmed.csv", sep= ",")

# delete unnamed columns
df_final_trimmed = df_final_trimmed.loc[:, ~df_final_trimmed.columns.str.contains("^Unnamed")]

# execute necessary renaming
df_final_trimmed = df_final_trimmed.rename(columns={"Mkt-RF": "Mkt_RF"})

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

# dummy for firm name

# control for 5 firms that appear most in dataframe
#print(df_final_trimmed["Firm Name"].value_counts())
# Allianz Global Investors GmbH                    4576
# JPMorgan Asset Management (Europe) S.à r.l.      2912
# DWS Investment S.A.                              2808
# Universal-Investment GmbH                        2600
# AXA Funds Management S.A.                        2288

for f in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[f, "Firm Name"] == "Allianz Global Investors GmbH":
        df_final_trimmed.loc[f, "Allianz"] = 1
    else:
        df_final_trimmed.loc[f, "Allianz"] = 0

for f in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[f, "Firm Name"] == "JPMorgan Asset Management (Europe) S.à r.l.":
        df_final_trimmed.loc[f, "JPMorgan"] = 1
    else:
        df_final_trimmed.loc[f, "JPMorgan"] = 0

for f in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[f, "Firm Name"] == "DWS Investment S.A.":
        df_final_trimmed.loc[f, "DWS"] = 1
    else:
        df_final_trimmed.loc[f, "DWS"] = 0

for f in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[f, "Firm Name"] == "Universal-Investment GmbH":
        df_final_trimmed.loc[f, "Universal"] = 1
    else:
        df_final_trimmed.loc[f, "Universal"] = 0

for f in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[f, "Firm Name"] == "AXA Funds Management S.A.":
        df_final_trimmed.loc[f, "AXA"] = 1
    else:
        df_final_trimmed.loc[f, "AXA"] = 0

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

df_mod1 = df_final_trimmed

# Longer timeframe for mod1: 01/01/2019 - 22/03/2020
df_mod1["Date"] = df_mod1["Date"].astype("datetime64[ns]")
start_mod1 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod1 = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_mod1 = df_mod1[df_mod1["Date"].between(start_mod1, end_mod1)].reset_index()
df_mod1 = df_mod1.drop(columns=["index"])

fom1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + monthly_div + Age + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom2 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + monthly_div + Age + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"


reg1 = sm.ols(formula=fom1, data=df_mod1).fit()
#summary_reg1 = reg1.summary()
#print(summary_reg1)



# reg 2

reg2 = sm.ols(formula=fom2, data=df_mod1).fit()
#summary_reg2 = reg2.summary()
#print(summary_reg2)

results = summary_col([reg1, reg2], stars=True, float_format="%0.2f", model_names=["Reg\n(1)", "Reg\n(2)"],
                      info_dict={"N": lambda x: "{0:d}".format(int(x.nobs)), "R^2": lambda x: "{:.2f}".format(x.rsquared)},
                      regressor_order=["High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_return_fundlevel",
                                       "log_tna", "monthly_star", "Star_COV", "monthly_div", "Age", ])

#print(results)

stargazer = Stargazer([reg1, reg2])
stargazer.covariate_order(["High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_return_fundlevel",
                                       "log_tna", "monthly_star", "Star_COV"])
stargazer.add_line("Firm Name Controls:", ["Y", "Y"])
stargazer.add_line("Fama-French Europe 5 Factors:", ["Y", "Y"])
stargazer.add_line("Industry Controls:", ["Y", "Y"])
stargazer.add_line("Style-Fixes Effects:", ["Y", "Y"])

open('regression_test.html', 'w').write(stargazer.render_html())


##############################################
# Second Model
##############################################

df_mod2 = df_final_trimmed

# Shorter timeframe for mod2: 01/01/2020 - 22/03/2020
df_mod2["Date"] = df_mod2["Date"].astype("datetime64[ns]")
start_mod2 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod2 = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_mod2 = df_mod2[df_mod2["Date"].between(start_mod2, end_mod2)].reset_index()
df_mod2 = df_mod2.drop(columns=["index"])

# reg3
fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom4 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"



reg3 = sm.ols(formula=fom3, data=df_mod2).fit()
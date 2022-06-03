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
from stargazer.stargazer import Stargazer, LineLocation

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
       "+ Star_COV + weekly_div + Age + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom2 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
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
                                       "log_tna", "monthly_star", "Star_COV", "weekly_div", "Age", ])

#print(results)
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
fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom4 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom5 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom6 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom7 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom8 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom9 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom10= "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg3 = sm.ols(formula=fom3, data=df_mod2).fit()
reg4 = sm.ols(formula=fom4, data=df_mod2).fit()
reg5 = sm.ols(formula=fom5, data=df_mod2).fit()
reg6 = sm.ols(formula=fom6, data=df_mod2).fit()
reg7 = sm.ols(formula=fom7, data=df_mod2).fit()
reg8 = sm.ols(formula=fom8, data=df_mod2).fit()
reg9 = sm.ols(formula=fom9, data=df_mod2).fit()
reg10 = sm.ols(formula=fom10, data=df_mod2).fit()


stargazer = Stargazer([reg1, reg3, reg5, reg7, reg9])
stargazer.rename_covariates({"High_ESG_COV": "High ESG  x  COV", "Low_ESG_COV": "Low ESG  x  COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return  x  COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month Return  x  COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating  x  COV"})
stargazer.dependent_variable = " Net Flow"
stargazer.custom_columns(["Extended Timeframe\n(01/01/2019 - 22/03/2020)", "Narrow Timeframe\n(01/01/2020 - 22/03/2020)"], [1, 4])
stargazer.covariate_order(["High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return",
                           "log_tna", "monthly_star", "Star_COV"])
stargazer.add_line("Firm Name Controls:", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fama-French Europe 5 Factors:", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls:", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects:", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)

open('regression_test.html', 'w').write(stargazer.render_html())
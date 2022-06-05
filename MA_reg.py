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

# dummy for timeframe COVID OVERALL
for t in range(0, len(df_final_trimmed)):
    if pd.to_datetime("2020-02-23", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-08-23", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV"] = 1
    else:
        df_final_trimmed.loc[t, "COV"] = 0

# dummy for timeframe COVID CRASH
for t in range(0, len(df_final_trimmed)):
    if pd.to_datetime("2020-02-23", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-03-22", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV_CRASH"] = 1
    else:
        df_final_trimmed.loc[t, "COV_CRASH"] = 0

# dummy for timeframe COVID RECOVERY
for t in range(0, len(df_final_trimmed)):
    if pd.to_datetime("2020-03-23", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-08-23", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV_REC"] = 1
    else:
        df_final_trimmed.loc[t, "COV_REC"] = 0

# dummy for globe rating as of 31/12/2019
for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 5:
        df_final_trimmed.loc[g, "High_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "High_ESG"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 4:
        df_final_trimmed.loc[g, "Above_Average_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "Above_Average_ESG"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 2:
        df_final_trimmed.loc[g, "Below_Average_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "Below_Average_ESG"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "monthly_sus"] == 1:
        df_final_trimmed.loc[g, "Low_ESG"] = 1
    else:
        df_final_trimmed.loc[g, "Low_ESG"] = 0

# dummy for institutional funds
for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Institutional"] == "Yes":
        df_final_trimmed.loc[i, "Insti"] = 1
    else:
        df_final_trimmed.loc[i, "Insti"] = 0

# dummy for firm name

# control for 5 firms that appear most in observations
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
df_final_trimmed["High_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["High_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["Ret_COV"] = df_final_trimmed["COV"] * df_final_trimmed["weekly_return_fundlevel"]
df_final_trimmed["Ret_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["weekly_return_fundlevel"]
df_final_trimmed["Ret_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["weekly_return_fundlevel"]
df_final_trimmed["One_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["One_M_RET_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["One_M_RET_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["Twelve_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["Twelve_M_RET_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["Twelve_M_RET_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["Star_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_star"]
df_final_trimmed["Star_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_star"]
df_final_trimmed["Star_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_star"]
df_final_trimmed["ENV_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_env"]
df_final_trimmed["SOC_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_soc"]
df_final_trimmed["GOV_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_gov"]
df_final_trimmed["CAR_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_car"]
df_final_trimmed["Insti_High_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["High_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_High_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["High_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_High_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["High_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Low_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["Low_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Low_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["Low_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Low_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["Low_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_High_ESG"] = df_final_trimmed["High_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Low_ESG"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_COV"] = df_final_trimmed["COV"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret_COV"] = df_final_trimmed["COV"] * df_final_trimmed["weekly_return_fundlevel"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["weekly_return_fundlevel"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["weekly_return_fundlevel"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret"] = df_final_trimmed["weekly_return_fundlevel"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_One_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["prior_month_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_One_M_RET_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["prior_month_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_One_M_RET_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["prior_month_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_One_M_RET"] = df_final_trimmed["prior_month_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Twelve_M_RET_COV"] = df_final_trimmed["COV"] * df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Twelve_M_RET_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Twelve_M_RET_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Twelve_M_RET"] = df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Star_COV"] = df_final_trimmed["COV"] * df_final_trimmed["monthly_star"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Star_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_star"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Star_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_star"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Star"] = df_final_trimmed["monthly_star"] * df_final_trimmed["Insti"]


##############################################
# 1. Model: Diff in diff regression for longer timeframe with sus. ratings
##############################################

df_mod1 = df_final_trimmed

# Longer timeframe for mod1: 01/01/2019 - 23/08/2020
df_mod1["Date"] = df_mod1["Date"].astype("datetime64[ns]")
start_mod1 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod1 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod1 = df_mod1[df_mod1["Date"].between(start_mod1, end_mod1)].reset_index()
df_mod1 = df_mod1.drop(columns=["index"])

fom1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom2 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg1 = sm.ols(formula=fom1, data=df_mod1).fit()
reg2 = sm.ols(formula=fom2, data=df_mod1).fit()


##############################################
# 2. Model: Diff in diff regression for shorter timeframe with sus. ratings
##############################################

df_mod2 = df_final_trimmed

# Shorter timeframe for mod2: 01/01/2020 - 23/08/2020
df_mod2["Date"] = df_mod2["Date"].astype("datetime64[ns]")
start_mod2 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod2 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod2 = df_mod2[df_mod2["Date"].between(start_mod2, end_mod2)].reset_index()
df_mod2 = df_mod2.drop(columns=["index"])

fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom4 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom5 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom6 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom7 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom8 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom9 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom10= "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
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

# Output for dep. variable Net Flow
stargazer = Stargazer([reg1, reg3, reg5, reg7, reg9])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg2, reg4, reg6, reg8, reg10])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return x COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 3. Model: OLS regression for longer timeframe with E/S/G risk scores
##############################################

df_mod3 = df_final_trimmed

# Longer timeframe for mod3: 01/01/2019 - 23/08/2020
df_mod3["Date"] = df_mod3["Date"].astype("datetime64[ns]")
start_mod3 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod3 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod3 = df_mod3[df_mod3["Date"].between(start_mod3, end_mod3)].reset_index()
df_mod3 = df_mod3.drop(columns=["index"])


fom11 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom12 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg11 = sm.ols(formula=fom11, data=df_mod3).fit()
reg12 = sm.ols(formula=fom12, data=df_mod3).fit()


##############################################
# 4. Model: OLS regression for shorter timeframe with E/S/G risk scores
##############################################

df_mod4 = df_final_trimmed

# Shorter timeframe for mod4: 01/01/2020 - 22/03/2020
df_mod4["Date"] = df_mod4["Date"].astype("datetime64[ns]")
start_mod4 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod4 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod4 = df_mod4[df_mod4["Date"].between(start_mod4, end_mod4)].reset_index()
df_mod4 = df_mod4.drop(columns=["index"])


fom13 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom14 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom15 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom16 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom17 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom18 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom19 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom20 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg13 = sm.ols(formula=fom13, data=df_mod4).fit()
reg14 = sm.ols(formula=fom14, data=df_mod4).fit()
reg15 = sm.ols(formula=fom15, data=df_mod4).fit()
reg16 = sm.ols(formula=fom16, data=df_mod4).fit()
reg17 = sm.ols(formula=fom17, data=df_mod4).fit()
reg18 = sm.ols(formula=fom18, data=df_mod4).fit()
reg19 = sm.ols(formula=fom19, data=df_mod4).fit()
reg20 = sm.ols(formula=fom20, data=df_mod4).fit()


# Output for dep. variable Net Flow
stargazer = Stargazer([reg11, reg13, reg15, reg17, reg19])
stargazer.rename_covariates({"ENV_COV": "Environmental x COV", "SOC_COV": "Social x COV", "GOV_COV": "Governance x COV",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "ENV_COV", "SOC_COV", "GOV_COV", "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

#open('OLS_risk_scores_net_flow.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flow
stargazer = Stargazer([reg12, reg14, reg16, reg18, reg20])
stargazer.rename_covariates({"ENV_COV": "Environmental x COV", "SOC_COV": "Social x COV", "GOV_COV": "Governance x COV",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return x COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating  x  COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "ENV_COV", "SOC_COV", "GOV_COV", "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

#open('OLS_risk_scores_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 5. Model: OLS regression for longer timeframe with Carbon Designation
##############################################

df_mod5 = df_final_trimmed

# Longer timeframe for mod5: 01/01/2019 - 23/08/2020
df_mod5["Date"] = df_mod5["Date"].astype("datetime64[ns]")
start_mod5 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod5 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod5 = df_mod5[df_mod5["Date"].between(start_mod5, end_mod5)].reset_index()
df_mod5 = df_mod5.drop(columns=["index"])


fom21 = "fund_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom22 = "normalized_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg21 = sm.ols(formula=fom21, data=df_mod5).fit()
reg22 = sm.ols(formula=fom22, data=df_mod5).fit()


##############################################
# 6. Model: OLS regression for shorter timeframe with with Carbon Designation
##############################################

df_mod6 = df_final_trimmed

# Shorter timeframe for mod6: 01/01/2020 - 23/08/2020
df_mod6["Date"] = df_mod6["Date"].astype("datetime64[ns]")
start_mod6 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod6 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod6 = df_mod6[df_mod6["Date"].between(start_mod6, end_mod6)].reset_index()
df_mod6 = df_mod6.drop(columns=["index"])


fom23 = "fund_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom24 = "normalized_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom25 = "fund_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom26 = "normalized_flows ~ CAR_COV + monthly_car + weekly_return_fundlevel + Ret_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom27 = "fund_flows ~ CAR_COV + monthly_car + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom28 = "normalized_flows ~ CAR_COV + monthly_car + prior_month_return + One_M_RET_COV + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom29 = "fund_flows ~ CAR_COV + monthly_car + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom30 = "normalized_flows ~ CAR_COV + monthly_car + Twelve_M_RET_COV + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg23 = sm.ols(formula=fom23, data=df_mod6).fit()
reg24 = sm.ols(formula=fom24, data=df_mod6).fit()
reg25 = sm.ols(formula=fom25, data=df_mod6).fit()
reg26 = sm.ols(formula=fom26, data=df_mod6).fit()
reg27 = sm.ols(formula=fom27, data=df_mod6).fit()
reg28 = sm.ols(formula=fom28, data=df_mod6).fit()
reg29 = sm.ols(formula=fom29, data=df_mod6).fit()
reg30 = sm.ols(formula=fom30, data=df_mod6).fit()


# Output for dep. variable Net Flow
stargazer = Stargazer([reg21, reg23, reg25, reg27, reg29])
stargazer.rename_covariates({"CAR_COV": "Low Carbon Designation x COV", "monthly_car": "Low Carbon Designation",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "CAR_COV", "monthly_car", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

#open('OLS_carb_design_net_flow.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flow
stargazer = Stargazer([reg22, reg24, reg26, reg28, reg30])
stargazer.rename_covariates({"CAR_COV": "Low Carbon Designation x COV", "monthly_car": "Low Carbon Designation",
                             "weekly_div": "Dividends", "Ret_COV": "Return x  COV", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return x COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "CAR_COV", "monthly_car", "Ret_COV", "weekly_return_fundlevel",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

#open('OLS_carb_design_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 7. Model: Diff in diff regression for longer timeframe with sus. rating distinguishing between multiple sub-timeframes
##############################################

df_mod7 = df_final_trimmed

# Longer timeframe for mod7: 01/01/2019 - 23/08/2020
df_mod7["Date"] = df_mod7["Date"].astype("datetime64[ns]")
start_mod7 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod7 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod7 = df_mod7[df_mod7["Date"].between(start_mod7, end_mod7)].reset_index()
df_mod7 = df_mod7.drop(columns=["index"])

fom31 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom32 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg31 = sm.ols(formula=fom31, data=df_mod7).fit()
reg32 = sm.ols(formula=fom32, data=df_mod7).fit()


##############################################
# 8. Model: Diff in diff regression for shorter timeframe with sus. rating distinguishing between multiple sub-timeframes
##############################################

df_mod8 = df_final_trimmed

# Shorter timeframe for mod8: 01/01/2020 - 23/08/2020
df_mod8["Date"] = df_mod8["Date"].astype("datetime64[ns]")
start_mod8 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod8 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod8 = df_mod8[df_mod8["Date"].between(start_mod8, end_mod8)].reset_index()
df_mod8 = df_mod8.drop(columns=["index"])

fom33 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom34 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom35 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV_CRASH + Ret_COV_REC + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom36 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Ret_COV_CRASH + Ret_COV_REC + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom37 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV_CRASH + One_M_RET_COV_REC + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom38 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + prior_month_return + One_M_RET_COV_CRASH + One_M_RET_COV_REC + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom39 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom40= "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG +Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC + rolling_12_months_return + log_tna + weekly_div + monthly_star" \
       "+ Star_COV_CRASH + Star_COV_REC + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg33 = sm.ols(formula=fom33, data=df_mod8).fit()
reg34 = sm.ols(formula=fom34, data=df_mod8).fit()
reg35 = sm.ols(formula=fom35, data=df_mod8).fit()
reg36 = sm.ols(formula=fom36, data=df_mod8).fit()
reg37 = sm.ols(formula=fom37, data=df_mod8).fit()
reg38 = sm.ols(formula=fom38, data=df_mod8).fit()
reg39 = sm.ols(formula=fom39, data=df_mod8).fit()
reg40 = sm.ols(formula=fom40, data=df_mod8).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg31, reg33, reg35, reg37, reg39])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Interactions", ["N", "N", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Interaction", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_subtime.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg32, reg34, reg36, reg38, reg40])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return_fundlevel": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "monthly_star": "Star Rating", "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Interactions", ["N", "N", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Interaction", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_subtime.html', 'w').write(stargazer.render_html())


##############################################
# 9. Model: OLS regression PRE-COVID LONG with sus. rating in 4 cats
##############################################

df_mod9 = df_final_trimmed

# Shorter timeframe for mod9: 01/01/2019 - 22/02/2020
df_mod9["Date"] = df_mod9["Date"].astype("datetime64[ns]")
start_mod9 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod9 = pd.to_datetime("2020-02-22", format="%Y-%m-%d")
df_mod9 = df_mod9[df_mod9["Date"].between(start_mod9, end_mod9)].reset_index()
df_mod9 = df_mod9.drop(columns=["index"])

fom41 = "fund_flows ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG + weekly_return_fundlevel" \
       "+ prior_month_return + rolling_12_months_return + log_tna + monthly_star + Star_COV + weekly_div + Age" \
       "+ index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom42 = "normalized_flows ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG + weekly_return_fundlevel" \
       "+ prior_month_return + rolling_12_months_return + log_tna + monthly_star + Star_COV + weekly_div + Age" \
       "+ index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

##############################################
# 10. Model: OLS regression PRE-COVID SHORT with sus. rating in 4 cats
##############################################

df_mod10 = df_final_trimmed

# Shorter timeframe for mod10: 01/01/2020 - 22/02/2020
df_mod10["Date"] = df_mod10["Date"].astype("datetime64[ns]")
start_mod10 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod10 = pd.to_datetime("2020-02-22", format="%Y-%m-%d")
df_mod10 = df_mod10[df_mod10["Date"].between(start_mod10, end_mod10)].reset_index()
df_mod10 = df_mod10.drop(columns=["index"])


##############################################
# 11. Model: OLS regression CRASH with sus. rating in 4 cats
##############################################

df_mod11 = df_final_trimmed

# Shorter timeframe for mod11: 22/02/2020 - 22/03/2020
df_mod11["Date"] = df_mod11["Date"].astype("datetime64[ns]")
start_mod11 = pd.to_datetime("2020-02-23", format="%Y-%m-%d")
end_mod11 = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_mod11 = df_mod11[df_mod11["Date"].between(start_mod11, end_mod11)].reset_index()
df_mod11 = df_mod11.drop(columns=["index"])


##############################################
# 12. Model: OLS regression RECOVERY with sus. rating in 4 cats
##############################################

df_mod12 = df_final_trimmed

# Shorter timeframe for mod12: 23/03/2020 - 23/08/2020
df_mod12["Date"] = df_mod12["Date"].astype("datetime64[ns]")
start_mod12 = pd.to_datetime("2020-03-23", format="%Y-%m-%d")
end_mod12 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod12 = df_mod12[df_mod12["Date"].between(start_mod12, end_mod12)].reset_index()
df_mod12 = df_mod12.drop(columns=["index"])


reg41 = sm.ols(formula=fom41, data=df_mod9).fit()
reg42 = sm.ols(formula=fom42, data=df_mod9).fit()
reg43 = sm.ols(formula=fom41, data=df_mod10).fit()
reg44 = sm.ols(formula=fom42, data=df_mod10).fit()
reg45 = sm.ols(formula=fom41, data=df_mod11).fit()
reg46 = sm.ols(formula=fom42, data=df_mod11).fit()
reg47 = sm.ols(formula=fom41, data=df_mod12).fit()
reg48 = sm.ols(formula=fom42, data=df_mod12).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg41, reg43, reg45, reg47])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended PRE-COVID (01. Jan '19 - 22. Feb '20)",
                          "Narrow PRE-COVID (01. Jan '20 - 22. Feb '20)", "COVID CRASH (23. Feb '20 - 22. Mar '20)",
                          "COVID RECOVERY (23. Mar '20 - 23. Aug '20)"], [1, 1, 1, 1])
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return_fundlevel", "prior_month_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_net_flow_subtime.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg42, reg44, reg46, reg48])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended PRE-COVID (01. Jan '19 - 22. Feb '20)",
                          "Narrow PRE-COVID (01. Jan '20 - 22. Feb '20)", "COVID CRASH (23. Feb '20 - 22. Mar '20)",
                          "COVID RECOVERY (23. Mar '20 - 23. Aug '20)"], [1, 1, 1, 1])
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return_fundlevel", "prior_month_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_subtime.html', 'w').write(stargazer.render_html())


##############################################
# 13. Model: Diff in diff regression insti vs. retail with shorter timeframe with sus. rating with COV
##############################################

df_mod13 = df_final_trimmed

# Longer timeframe for mod13: 01/01/2019 - 23/08/2020
df_mod13["Date"] = df_mod13["Date"].astype("datetime64[ns]")
start_mod13 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod13 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod13 = df_mod13[df_mod13["Date"].between(start_mod13, end_mod13)].reset_index()
df_mod13 = df_mod13.drop(columns=["index"])

fom51 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV + Insti_Ret + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom52 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV + Insti_Ret + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg51 = sm.ols(formula=fom51, data=df_mod13).fit()
reg52 = sm.ols(formula=fom52, data=df_mod13).fit()


##############################################
# 14. Model: Diff in diff regression insti vs. retail with longer timeframe with sus. rating with COV
##############################################

df_mod14 = df_final_trimmed

# Shorter timeframe for mod14: 01/01/2020 - 23/08/2020
df_mod14["Date"] = df_mod14["Date"].astype("datetime64[ns]")
start_mod14 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod14 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod14 = df_mod14[df_mod14["Date"].between(start_mod14, end_mod14)].reset_index()
df_mod14 = df_mod14.drop(columns=["index"])

fom53 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV + Insti_Ret + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom54 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV + Insti_Ret + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom55 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + Insti_One_M_RET_COV + Insti_One_M_RET + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom56 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + prior_month_return + Insti_One_M_RET_COV + Insti_One_M_RET + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom57 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + rolling_12_months_return + Insti_Twelve_M_RET_COV + Insti_Twelve_M_RET + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"
fom58 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + rolling_12_months_return + Insti_Twelve_M_RET_COV + Insti_Twelve_M_RET + log_tna + monthly_star" \
       "+ Insti_Star_COV + Insti_Star + Star_COV + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS + Universal + AXA + Mkt_RF + SMB + HML + RMW" \
       "+ CMA + RF + growth + value + large_cap + mid_cap + small_cap + large_growth + large_value + mid_growth + mid_value + small_growth" \
       "+ small_value + utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare" \
       "+ consumer_defensive + communication_services + financial_services + energy"

reg53 = sm.ols(formula=fom53, data=df_mod14).fit()
reg54 = sm.ols(formula=fom54, data=df_mod14).fit()
reg55 = sm.ols(formula=fom55, data=df_mod14).fit()
reg56 = sm.ols(formula=fom56, data=df_mod14).fit()
reg57 = sm.ols(formula=fom57, data=df_mod14).fit()
reg58 = sm.ols(formula=fom58, data=df_mod14).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg51, reg53, reg55, reg57])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Insti_High_ESG_COV": "High ESG x COV x Institutional",
                             "Insti_Low_ESG_COV": "Low ESG x COV x Institutional", "Low_ESG_COV": "Low ESG x COV",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV": "COV x Institutional", "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,3])
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV", "Insti_Low_ESG_COV", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV",
                           "Insti", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return x COV x Insti Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV x Insti Interaction", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_insti.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg52, reg54, reg56, reg58])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Insti_High_ESG_COV": "High ESG x COV x Institutional",
                             "Insti_Low_ESG_COV": "Low ESG x COV x Institutional", "Low_ESG_COV": "Low ESG x COV",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV": "COV x Institutional", "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,3])
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV", "Insti_Low_ESG_COV", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV",
                           "Insti", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return x COV x Insti Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV x Insti Interaction", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_insti.html', 'w').write(stargazer.render_html())


##############################################
# 15. Model: Diff in diff regression insti vs. retail with longer timeframe with sus. rating distinguishing between different timeframes
##############################################

df_mod15 = df_final_trimmed

# Longer timeframe for mod15: 01/01/2019 - 23/08/2020
df_mod15["Date"] = df_mod13["Date"].astype("datetime64[ns]")
start_mod15 = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end_mod15 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod15 = df_mod15[df_mod15["Date"].between(start_mod15, end_mod15)].reset_index()
df_mod15 = df_mod15.drop(columns=["index"])

fom61 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV_CRASH" \
        "+ Insti_Ret_COV_REC + Insti_Ret + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom62 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV_CRASH" \
        "+ Insti_Ret_COV_REC + Insti_Ret + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"

reg61 = sm.ols(formula=fom61, data=df_mod15).fit()
reg62 = sm.ols(formula=fom62, data=df_mod15).fit()


##############################################
# 16. Model: Diff in diff regression insti vs. retail with shorter timeframe with sus. rating distinguishing between different timeframes
##############################################

df_mod16 = df_final_trimmed

# Shorter timeframe for mod16: 01/01/2020 - 23/08/2020
df_mod16["Date"] = df_mod16["Date"].astype("datetime64[ns]")
start_mod16 = pd.to_datetime("2020-01-01", format="%Y-%m-%d")
end_mod16 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod16 = df_mod16[df_mod16["Date"].between(start_mod16, end_mod16)].reset_index()
df_mod16 = df_mod16.drop(columns=["index"])

fom63 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV_CRASH" \
        "+ Insti_Ret_COV_REC + Insti_Ret + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom64 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return_fundlevel + Insti_Ret_COV_CRASH" \
        "+ Insti_Ret_COV_REC + Insti_Ret + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom65 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + prior_month_return + Insti_One_M_RET_COV_CRASH" \
        "+ Insti_One_M_RET_COV_REC + Insti_One_M_RET + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom66 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + prior_month_return + Insti_One_M_RET_COV_CRASH" \
        "+ Insti_One_M_RET_COV_REC + Insti_One_M_RET + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom67 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + rolling_12_months_return + Insti_Twelve_M_RET_COV_CRASH" \
        "+ Insti_Twelve_M_RET_COV_REC + Insti_Twelve_M_RET + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"
fom68 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC" \
        "+ Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti + High_ESG_COV_CRASH + High_ESG_COV_REC" \
        "+ Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + rolling_12_months_return + Insti_Twelve_M_RET_COV_CRASH" \
        "+ Insti_Twelve_M_RET_COV_REC + Insti_Twelve_M_RET + log_tna + monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC" \
        "+ Insti_Star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator + Allianz + JPMorgan + DWS" \
        "+ Universal + AXA + Mkt_RF + SMB + HML + RMW + CMA + RF + growth + value + large_cap + mid_cap + small_cap" \
        "+ large_growth + large_value + mid_growth + mid_value + small_growth + small_value + utilities + industrials" \
        "+ basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive" \
        "+ communication_services + financial_services + energy"

reg63 = sm.ols(formula=fom63, data=df_mod16).fit()
reg64 = sm.ols(formula=fom64, data=df_mod16).fit()
reg65 = sm.ols(formula=fom65, data=df_mod16).fit()
reg66 = sm.ols(formula=fom66, data=df_mod16).fit()
reg67 = sm.ols(formula=fom67, data=df_mod16).fit()
reg68 = sm.ols(formula=fom68, data=df_mod16).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg61, reg63, reg65, reg67])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Insti_High_ESG_COV_CRASH": "High ESG x COV (CRASH) x Institutional", "Insti_High_ESG_COV_REC": "High ESG x COV (RECOVERY) x Institutional",
                             "Insti_Low_ESG_COV_CRASH": "Low ESG x COV (CRASH) x Institutional", "Insti_Low_ESG_COV_REC": "Low ESG x COV (RECOVERY) x Institutional",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV_CRASH": "COV (CRASH) x Institutional", "Insti_COV_REC": "COV (RECOVERY) x Institutional",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,3])
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV_CRASH", "Insti_High_ESG_COV_REC", "Insti_Low_ESG_COV_CRASH",
                           "Insti_Low_ESG_COV_REC", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV_CRASH", "Insti_COV_REC",
                           "Insti", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC", "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return x COV x Insti Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV x Insti Interaction", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_insti_subtime.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg62, reg64, reg66, reg68])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Insti_High_ESG_COV_CRASH": "High ESG x COV (CRASH) x Institutional", "Insti_High_ESG_COV_REC": "High ESG x COV (RECOVERY) x Institutional",
                             "Insti_Low_ESG_COV_CRASH": "Low ESG x COV (CRASH) x Institutional", "Insti_Low_ESG_COV_REC": "Low ESG x COV (RECOVERY) x Institutional",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV_CRASH": "COV (CRASH) x Institutional", "Insti_COV_REC": "COV (RECOVERY) x Institutional",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return_fundlevel": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe\n(01. Jan '19 - 23. Aug '20)", "Narrow Timeframe\n(01. Jan '20 - 23. Aug '20)"], [1,3])
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV_CRASH", "Insti_High_ESG_COV_REC", "Insti_Low_ESG_COV_CRASH",
                           "Insti_Low_ESG_COV_REC", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV_CRASH", "Insti_COV_REC",
                           "Insti", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC", "High_ESG", "Low_ESG"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Style-Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Controls", ["Weekly", "Weekly", "Prior Month", "Prior 12 Months"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return x COV x Insti Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV x Insti Interaction", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_insti_subtime.html', 'w').write(stargazer.render_html())
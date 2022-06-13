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

df_final_trimmed = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_final_trimmed.csv", sep= ",")

# delete unnamed columns
df_final_trimmed = df_final_trimmed.loc[:, ~df_final_trimmed.columns.str.contains("^Unnamed")]


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

# dummy for globe ratings
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

# dummies for Global Categories
for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Equity Miscellaneous":
        df_final_trimmed.loc[g, "Equity_Mis"] = 1
    else:
        df_final_trimmed.loc[g, "Equity_Mis"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Europe Emerging Markets Equity":
        df_final_trimmed.loc[g, "Eur_EM"] = 1
    else:
        df_final_trimmed.loc[g, "Eur_EM"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Europe Equity Large Cap":
        df_final_trimmed.loc[g, "Eur_Large"] = 1
    else:
        df_final_trimmed.loc[g, "Eur_Large"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Europe Equity Mid/Small Cap":
        df_final_trimmed.loc[g, "Eur_Mid_Small"] = 1
    else:
        df_final_trimmed.loc[g, "Eur_Mid_Small"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Healthcare Sector Equity":
        df_final_trimmed.loc[g, "Health"] = 1
    else:
        df_final_trimmed.loc[g, "Health"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Infrastructure Sector Equity":
        df_final_trimmed.loc[g, "Infra"] = 1
    else:
        df_final_trimmed.loc[g, "Infra"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Long/Short Equity":
        df_final_trimmed.loc[g, "LS_E"] = 1
    else:
        df_final_trimmed.loc[g, "LS_E"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Real Estate Sector Equity":
        df_final_trimmed.loc[g, "Real"] = 1
    else:
        df_final_trimmed.loc[g, "Real"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "Technology Sector Equity":
        df_final_trimmed.loc[g, "Tech"] = 1
    else:
        df_final_trimmed.loc[g, "Tech"] = 0

for g in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[g, "Global Category"] == "UK Equity Large Cap":
        df_final_trimmed.loc[g, "UK"] = 1
    else:
        df_final_trimmed.loc[g, "UK"] = 0


##############################################
# Interaction terms
##############################################

df_final_trimmed["High_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV"] = df_final_trimmed["COV"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["High_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["High_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["High_ESG"]
df_final_trimmed["Low_ESG_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["Low_ESG"]
df_final_trimmed["Ret_COV"] = df_final_trimmed["COV"] * df_final_trimmed["weekly_return"]
df_final_trimmed["Ret_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["weekly_return"]
df_final_trimmed["Ret_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["weekly_return"]
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
df_final_trimmed["Insti_Ret_COV"] = df_final_trimmed["COV"] * df_final_trimmed["weekly_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["weekly_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["weekly_return"] * df_final_trimmed["Insti"]
df_final_trimmed["Insti_Ret"] = df_final_trimmed["weekly_return"] * df_final_trimmed["Insti"]
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

fom1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + weekly_tna + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom2 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + weekly_tna + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"

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

fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom4 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom5 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom6 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom7 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ prior_month_return + One_M_RET_COV + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom8 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ prior_month_return + One_M_RET_COV + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom9 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ Twelve_M_RET_COV + rolling_12_months_return + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"
fom10= "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ Twelve_M_RET_COV + rolling_12_months_return + weekly_tna + weekly_div + monthly_star + Star_COV + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UK"

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
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "weekly_tna": "Total Net Assets (€ mio.)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "weekly_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg2, reg4, reg6, reg8, reg10])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return x COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "weekly_tna": "Total Net Assets (€ mio.)", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.custom_columns(["Extended Timeframe (01. Jan '19 - 23. Aug '20)", "Narrow Timeframe (01. Jan '20 - 23. Aug '20)"], [1,4])
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 3. Model: OLS regression for longer timeframe with E/S/G risk scores
##############################################


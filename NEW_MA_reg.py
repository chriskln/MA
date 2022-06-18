##############################################
# MASTER THESIS
##############################################

##############################################
# Regressions
##############################################

import numpy as np
from IPython.core.display_functions import display
from sklearn import datasets
import imgkit as im
import openpyxl
import statistics
import pandas as pd
from html2image import Html2Image
hti = Html2Image()
import matplotlib.pyplot as plt
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
        df_final_trimmed.loc[g, "UKE"] = 1
    else:
        df_final_trimmed.loc[g, "UKE"] = 0


# dummies for Investment Area
for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Austria":
        df_final_trimmed.loc[i, "AT"] = 1
    else:
        df_final_trimmed.loc[i, "AT"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Belgium":
        df_final_trimmed.loc[i, "BEL"] = 1
    else:
        df_final_trimmed.loc[i, "BEL"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Denmark":
        df_final_trimmed.loc[i, "DEN"] = 1
    else:
        df_final_trimmed.loc[i, "DEN"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Euroland":
        df_final_trimmed.loc[i, "EURO"] = 1
    else:
        df_final_trimmed.loc[i, "EURO"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Europe":
        df_final_trimmed.loc[i, "EUR"] = 1
    else:
        df_final_trimmed.loc[i, "EUR"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Europe (North)":
        df_final_trimmed.loc[i, "EURN"] = 1
    else:
        df_final_trimmed.loc[i, "EURN"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Europe Emerging Mkts":
        df_final_trimmed.loc[i, "EUREM"] = 1
    else:
        df_final_trimmed.loc[i, "EUREM"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Europe ex UK":
        df_final_trimmed.loc[i, "EURUK"] = 1
    else:
        df_final_trimmed.loc[i, "EURUK"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Finland":
        df_final_trimmed.loc[i, "FIN"] = 1
    else:
        df_final_trimmed.loc[i, "FIN"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "France":
        df_final_trimmed.loc[i, "FR"] = 1
    else:
        df_final_trimmed.loc[i, "FR"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Germany":
        df_final_trimmed.loc[i, "GER"] = 1
    else:
        df_final_trimmed.loc[i, "GER"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Greece":
        df_final_trimmed.loc[i, "GRE"] = 1
    else:
        df_final_trimmed.loc[i, "GRE"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Italy":
        df_final_trimmed.loc[i, "IT"] = 1
    else:
        df_final_trimmed.loc[i, "IT"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Norway":
        df_final_trimmed.loc[i, "NOR"] = 1
    else:
        df_final_trimmed.loc[i, "NOR"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Slovakia":
        df_final_trimmed.loc[i, "SVK"] = 1
    else:
        df_final_trimmed.loc[i, "SVK"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Spain":
        df_final_trimmed.loc[i, "ESP"] = 1
    else:
        df_final_trimmed.loc[i, "ESP"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "Switzerland":
        df_final_trimmed.loc[i, "CH"] = 1
    else:
        df_final_trimmed.loc[i, "CH"] = 0

for i in range(0, len(df_final_trimmed)):
    if df_final_trimmed.loc[i, "Investment Area"] == "United Kingdom":
        df_final_trimmed.loc[i, "UK"] = 1
    else:
        df_final_trimmed.loc[i, "UK"] = 0


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
# 1. Model:
# Diff in diff regression
# longer timeframe (01/01/2019 - 23/08/2020)
# globe rating
##############################################

df_mod1 = df_final_trimmed

# Longer timeframe for mod1: 01/10/2019 - 23/08/2020
df_mod1["Date"] = df_mod1["Date"].astype("datetime64[ns]")
start_mod1 = pd.to_datetime("2019-10-01", format="%Y-%m-%d")
end_mod1 = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_mod1 = df_mod1[df_mod1["Date"].between(start_mod1, end_mod1)].reset_index()
df_mod1 = df_mod1.drop(columns=["index"])

# NET FLOW, weekly & prior month's return (with interaction), no controls
fom1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), no controls
fom2 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), some controls
fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), all controls
fom4 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return + Ret_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (no interaction), Star Rating (no interaction), no controls
fom5 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), no controls
fom6 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), some controls
fom7 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), all controls
fom8 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return + Ret_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg1 = sm.ols(formula=fom1, data=df_mod1).fit()
reg2 = sm.ols(formula=fom2, data=df_mod1).fit()
reg3 = sm.ols(formula=fom3, data=df_mod1).fit()
reg4 = sm.ols(formula=fom4, data=df_mod1).fit()
reg5 = sm.ols(formula=fom5, data=df_mod1).fit()
reg6 = sm.ols(formula=fom6, data=df_mod1).fit()
reg7 = sm.ols(formula=fom7, data=df_mod1).fit()
reg8 = sm.ols(formula=fom8, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg1, reg2, reg3, reg4])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Net Expense Ratio", "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg5, reg6, reg7, reg8])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV", "High_ESG": "High ESG", "weekly_div": "Dividends",
                             "Low_ESG": "Low ESG", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return x COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Net Expense Ratio",
                             "monthly_star": "Star Rating", "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 2. Model:
# Diff in diff regression
# longer timeframe (01/01/2019 - 23/08/2020)
# E/S/G risk scores
##############################################

# NET FLOW, return (no interaction), Star Rating (no interaction), no controls
fom11 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator"

# NET FLOW, return (with interaction), Star Rating (with interaction), no controls
fom12 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator"

# NET FLOW, return (with interaction), Star Rating (with interaction), some controls
fom13 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value"

# NET FLOW, return (with interaction), Star Rating (with interaction), all controls
fom14 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (no interaction), Star Rating (no interaction), no controls
fom15 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), no controls
fom16 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), some controls
fom17 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), all controls
fom18 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg11 = sm.ols(formula=fom11, data=df_mod1).fit()
reg12 = sm.ols(formula=fom12, data=df_mod1).fit()
reg13 = sm.ols(formula=fom13, data=df_mod1).fit()
reg14 = sm.ols(formula=fom14, data=df_mod1).fit()
reg15 = sm.ols(formula=fom15, data=df_mod1).fit()
reg16 = sm.ols(formula=fom16, data=df_mod1).fit()
reg17 = sm.ols(formula=fom17, data=df_mod1).fit()
reg18 = sm.ols(formula=fom18, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg11, reg12, reg13, reg14])
stargazer.rename_covariates({"ENV_COV": "Environmental x COV", "SOC_COV": "Social x COV", "GOV_COV": "Governance x COV",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "ENV_COV", "SOC_COV", "GOV_COV", "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_net_flow.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg15, reg16, reg17, reg18])
stargazer.rename_covariates({"ENV_COV": "Environmental x COV", "SOC_COV": "Social x COV", "GOV_COV": "Governance x COV",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "ENV_COV", "SOC_COV", "GOV_COV", "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 3. Model
# Diff in diff regression
# longer timeframe (01/01/2019 - 23/08/2020)
# Carbon Risk Score
##############################################

# NET FLOW, return (no interaction), Star Rating (no interaction), no controls
fom21 = "fund_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator"

# NET FLOW, return (with interaction), Star Rating (with interaction), no controls
fom22 = "fund_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator"

# NET FLOW, return (with interaction), Star Rating (with interaction), some controls
fom23 = "fund_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value"

# NET FLOW, return (with interaction), Star Rating (with interaction), all controls
fom24 = "fund_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (no interaction), Star Rating (no interaction), no controls
fom25 = "normalized_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), no controls
fom26 = "normalized_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), some controls
fom27 = "normalized_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), all controls
fom28 = "normalized_flows ~ CAR_COV + monthly_car" \
       "+ weekly_return + prior_month_return + rolling_12_months_return + Ret_COV + One_M_RET_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg21 = sm.ols(formula=fom21, data=df_mod1).fit()
reg22 = sm.ols(formula=fom22, data=df_mod1).fit()
reg23 = sm.ols(formula=fom23, data=df_mod1).fit()
reg24 = sm.ols(formula=fom24, data=df_mod1).fit()
reg25 = sm.ols(formula=fom25, data=df_mod1).fit()
reg26 = sm.ols(formula=fom26, data=df_mod1).fit()
reg27 = sm.ols(formula=fom27, data=df_mod1).fit()
reg28 = sm.ols(formula=fom28, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg21, reg22, reg23, reg24])
stargazer.rename_covariates({"CAR_COV": "Low Carbon Designation x COV", "monthly_car": "Low Carbon Designation",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "CAR_COV", "monthly_car", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_carb_design_net_flow.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg25, reg26, reg27, reg28])
stargazer.rename_covariates({"CAR_COV": "Low Carbon Designation x COV", "monthly_car": "Low Carbon Designation",
                             "weekly_div": "Dividends", "Ret_COV": "Return x COV", "weekly_return": "Return",
                             "One_M_RET_COV": "Prior Month's Return x COV", "Twelve_M_RET_COV": "Prior 12 Months' Return  x  COV",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "CAR_COV", "monthly_car", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["N", "N", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["N", "N", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_carb_design_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 4. Model
# Diff in diff regression
# longer timeframe (01/01/2019 - 23/08/2020)
# Globe Rating
# distinguishing between multiple sub-timeframes
##############################################

# NET FLOW, return (no interaction), Star Rating (no interaction), no controls
fom31 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), no controls
fom32 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Ret_COV_CRASH + Ret_COV_REC + One_M_RET_COV_CRASH + One_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), some controls
fom33 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, return (with interaction), Star Rating (with interaction), all controls
fom34 = "fund_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return + Ret_COV_CRASH + Ret_COV_REC + Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (no interaction), Star Rating (no interaction), no controls
fom35 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), no controls
fom36 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Ret_COV_CRASH + Ret_COV_REC + One_M_RET_COV_CRASH + One_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), some controls
fom37 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, return (with interaction), Star Rating (with interaction), all controls
fom38 = "normalized_flows ~ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return + Ret_COV_CRASH + Ret_COV_REC + Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg31 = sm.ols(formula=fom31, data=df_mod1).fit()
reg32 = sm.ols(formula=fom32, data=df_mod1).fit()
reg33 = sm.ols(formula=fom33, data=df_mod1).fit()
reg34 = sm.ols(formula=fom34, data=df_mod1).fit()
reg35 = sm.ols(formula=fom35, data=df_mod1).fit()
reg36 = sm.ols(formula=fom36, data=df_mod1).fit()
reg37 = sm.ols(formula=fom37, data=df_mod1).fit()
reg38 = sm.ols(formula=fom38, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg31, reg32, reg33, reg34])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG"])
stargazer.add_line("Weekly Return Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Past Return Controls", ["1M", "1M", "12M", "12M"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Interaction", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_subtime.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg35, reg36, reg37, reg38])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG"])
stargazer.add_line("Weekly Return Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Past Return Controls", ["1M", "1M", "12M", "12M"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Interaction", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_subtime.html', 'w').write(stargazer.render_html())


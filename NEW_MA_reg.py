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

# count of industry membership of five- and one-globe funds
df_count_one = df_final_trimmed[(df_final_trimmed.monthly_sus == 1)]
df_count_one["count"] = 1
sus_count = df_count_one.groupby(["Global Category"])["count"].count()
print(sus_count)
df_count_one = df_count_one.drop(["count"], axis=1)

df_count_two = df_final_trimmed[(df_final_trimmed.monthly_sus == 2)]
df_count_two["count"] = 1
sus_count = df_count_two.groupby(["Global Category"])["count"].count()
print(sus_count)
df_count_two = df_count_two.drop(["count"], axis=1)

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
    if pd.to_datetime("2020-03-23", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-06-07", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV_REC"] = 1
    else:
        df_final_trimmed.loc[t, "COV_REC"] = 0

# dummy for timeframe COVID RECOVERY 2
for t in range(0, len(df_final_trimmed)):
    if pd.to_datetime("2020-06-08", format="%Y-%m-%d") <= df_final_trimmed.loc[t, "Date"] <= pd.to_datetime("2020-08-23", format="%Y-%m-%d"):
        df_final_trimmed.loc[t, "COV_REC2"] = 1
    else:
        df_final_trimmed.loc[t, "COV_REC2"] = 0

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
df_final_trimmed["ENV_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_env"]
df_final_trimmed["SOC_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_soc"]
df_final_trimmed["GOV_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_gov"]
df_final_trimmed["CAR_COV_CRASH"] = df_final_trimmed["COV_CRASH"] * df_final_trimmed["monthly_car"]
df_final_trimmed["ENV_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_env"]
df_final_trimmed["SOC_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_soc"]
df_final_trimmed["GOV_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_gov"]
df_final_trimmed["CAR_COV_REC"] = df_final_trimmed["COV_REC"] * df_final_trimmed["monthly_car"]
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
df_final_trimmed["High_ESG_One_M_RET"] = df_final_trimmed["High_ESG"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["Low_ESG_One_M_RET"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["prior_month_return"]
df_final_trimmed["High_ESG_One_M_RET_COV"] = df_final_trimmed["High_ESG"] * df_final_trimmed["prior_month_return"] * df_final_trimmed["COV"]
df_final_trimmed["Low_ESG_One_M_RET_COV"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["prior_month_return"] * df_final_trimmed["COV"]
df_final_trimmed["One_M_RET_Star_COV"] = df_final_trimmed["prior_month_return"] * df_final_trimmed["monthly_star"] * df_final_trimmed["COV"]
df_final_trimmed["One_M_RET_Star"] = df_final_trimmed["prior_month_return"] * df_final_trimmed["monthly_star"]
df_final_trimmed["High_ESG_PAST_RET"] = df_final_trimmed["High_ESG"] * df_final_trimmed["prior_week_return"]
df_final_trimmed["Low_ESG_PAST_RET"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["prior_week_return"]
df_final_trimmed["High_ESG_PAST_RET_COV"] = df_final_trimmed["High_ESG"] * df_final_trimmed["prior_week_return"] * df_final_trimmed["COV"]
df_final_trimmed["Low_ESG_PAST_RET_COV"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["prior_week_return"] * df_final_trimmed["COV"]
df_final_trimmed["PAST_RET_Star_COV"] = df_final_trimmed["prior_week_return"] * df_final_trimmed["monthly_star"] * df_final_trimmed["COV"]
df_final_trimmed["PAST_RET_Star"] = df_final_trimmed["prior_week_return"] * df_final_trimmed["monthly_star"]
df_final_trimmed["PAST_RET_COV"] = df_final_trimmed["prior_week_return"] * df_final_trimmed["COV"]
df_final_trimmed["High_ESG_12M_RET"] = df_final_trimmed["High_ESG"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["Low_ESG_12M_RET"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["rolling_12_months_return"]
df_final_trimmed["High_ESG_12M_RET_COV"] = df_final_trimmed["High_ESG"] * df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["COV"]
df_final_trimmed["Low_ESG_12M_RET_COV"] = df_final_trimmed["Low_ESG"] * df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["COV"]
df_final_trimmed["Star_12M_RET_COV"] = df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["monthly_star"] * df_final_trimmed["COV"]
df_final_trimmed["Star_12M_RET"] = df_final_trimmed["rolling_12_months_return"] * df_final_trimmed["monthly_star"]



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

# NET FLOW, no interactions for controls, 1 M. Return
fom1 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, with interactions for controls, 1 M. Return
fom2 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, no interactions for controls, 12 M. Return
fom3 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, with interactions for controls, 12 M. Return
fom4 = "fund_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return + Ret_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no interactions for controls, 1 M. Return
fom5 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with interactions for controls, 1 M. Return
fom6 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no interactions for controls, 12 M. Return
fom7 = "normalized_flows ~ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with interactions for controls, 12 M. Return
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
stargazer.title("Panel A")
stargazer.dependent_variable = " Net Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
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
stargazer.title("Panel B")
stargazer.dependent_variable = " Normalized Flow"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return",
                           "One_M_RET_COV", "prior_month_return", "Twelve_M_RET_COV", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 2. Model:
# Diff in diff regression
# longer timeframe (01/01/2019 - 23/08/2020)
# E/S/G risk scores
##############################################

# NET FLOW, no interactions for controls, 1 M. Return
fom11 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, interactions for controls, 1 M. Return
fom12 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, no interactions for controls, 12 M. Return
fom13 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, interactions for controls, 12 M. Return
fom14 = "fund_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + rolling_12_months_return + Ret_COV + Twelve_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no interactions for controls, 1 M. Return
fom15 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + prior_month_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with interactions for controls, 1 M. Return
fom16 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + Ret_COV + prior_month_return + One_M_RET_COV" \
       "+ log_tna + normalized_exp + monthly_star + Star_COV + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no interactions for controls, 12 M. Return
fom17 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + rolling_12_months_return" \
       "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
       "+ Allianz + JPMorgan + DWS + Universal + AXA" \
       "+ Mkt_RF + SMB + HML + RMW + CMA" \
       "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
       "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
       "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
       "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with interactions for controls, 12 M. Return
fom18 = "normalized_flows ~ ENV_COV + SOC_COV + GOV_COV + monthly_env + monthly_soc + monthly_gov" \
       "+ weekly_return + rolling_12_months_return + Ret_COV + Twelve_M_RET_COV" \
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
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_risk_scores_net_flow.html', 'w').write(stargazer.render_html())


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
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_risk_scores_normalized_flow.html', 'w').write(stargazer.render_html())


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
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
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
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_carb_design_normalized_flow.html', 'w').write(stargazer.render_html())


##############################################
# 4. Model
# Diff in diff regression
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
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Net Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC","Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG", "Ret_COV_CRASH", "Ret_COV_REC", "weekly_return", "One_M_RET_COV_CRASH",
                           "One_M_RET_COV_REC", "prior_month_return", "Twelve_M_RET_COV_CRASH", "Twelve_M_RET_COV_REC",
                           "rolling_12_months_return", "weekly_div", "log_tna", "normalized_exp", "Star_COV_CRASH",
                           "Star_COV_REC", "monthly_star", "Age", "index_indicator"])
#stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
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
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_COV_CRASH", "High_ESG_COV_REC","Low_ESG_COV_CRASH", "Low_ESG_COV_REC",
                           "High_ESG", "Low_ESG", "Ret_COV_CRASH", "Ret_COV_REC", "weekly_return", "One_M_RET_COV_CRASH",
                           "One_M_RET_COV_REC", "prior_month_return", "Twelve_M_RET_COV_CRASH", "Twelve_M_RET_COV_REC",
                           "rolling_12_months_return", "weekly_div", "log_tna", "normalized_exp", "Star_COV_CRASH",
                           "Star_COV_REC", "monthly_star", "Age", "index_indicator"])
#stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_subtime.html', 'w').write(stargazer.render_html())


##############################################
# 5. Model
# OLS regression
# different timeframes
# Globe Rating
##############################################

df_pre = df_final_trimmed
# set timeframe
df_pre["Date"] = df_pre["Date"].astype("datetime64[ns]")
start_pre = pd.to_datetime("2019-10-01", format="%Y-%m-%d")
end_pre = pd.to_datetime("2020-02-22", format="%Y-%m-%d")
df_pre = df_pre[df_pre["Date"].between(start_pre, end_pre)].reset_index()
df_pre = df_pre.drop(columns=["index"])

# normalized flow update
df_pre["Decile_Rank_pre"] = df_pre.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_pre["normalized_flows_pre"] = df_pre.groupby("Decile_Rank_pre").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
df_pre["normalized_exp_pre"] = df_pre.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

df_crash = df_final_trimmed
# set timeframe
df_crash["Date"] = df_crash["Date"].astype("datetime64[ns]")
start_crash = pd.to_datetime("2020-02-23", format="%Y-%m-%d")
end_crash = pd.to_datetime("2020-03-22", format="%Y-%m-%d")
df_crash = df_crash[df_crash["Date"].between(start_crash, end_crash)].reset_index()
df_crash = df_crash.drop(columns=["index"])

# normalized flow update
df_crash["Decile_Rank_crash"] = df_crash.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_crash["normalized_flows_crash"] = df_crash.groupby("Decile_Rank_crash").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
df_crash["normalized_exp_crash"] = df_crash.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

df_rec = df_final_trimmed
# set timeframe
df_rec["Date"] = df_rec["Date"].astype("datetime64[ns]")
start_rec = pd.to_datetime("2020-03-23", format="%Y-%m-%d")
end_rec = pd.to_datetime("2020-08-23", format="%Y-%m-%d")
df_rec = df_rec[df_rec["Date"].between(start_rec, end_rec)].reset_index()
df_rec = df_rec.drop(columns=["index"])

# normalized flow update
df_rec["Decile_Rank_rec"] = df_rec.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_rec["normalized_flows_rec"] = df_rec.groupby("Decile_Rank_rec").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
df_rec["normalized_exp_rec"] = df_rec.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

# percentage net flows
fom40 = "fund_flows ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# normalized flows
fom41a = "normalized_flows_pre ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_pre + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom41b = "normalized_flows_crash ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_crash + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom41c = "normalized_flows_rec ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_rec + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg40 = sm.ols(formula=fom40, data=df_pre).fit()
reg41 = sm.ols(formula=fom41a, data=df_pre).fit()
reg42 = sm.ols(formula=fom40, data=df_crash).fit()
reg43 = sm.ols(formula=fom41b, data=df_crash).fit()
reg44 = sm.ols(formula=fom40, data=df_rec).fit()
reg45 = sm.ols(formula=fom41c, data=df_rec).fit()


# Output for dep. variable Percentage Net Flows
stargazer = Stargazer([reg40, reg42, reg44])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_net_flow_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flows
stargazer = Stargazer([reg41])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_pre": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_pre", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_pre.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg43])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_crash": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_crash", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_crash.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg45])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_rec": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_rec", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_rec.html', 'w').write(stargazer.render_html())

##############################################
# 6. Model
# Triple-diff. regressions
# insti vs. retail
# Globe Rating
##############################################

# % NET FLOW, prior month's return, without COV interactions
fom42 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, prior month's return, with COV interactions
fom43 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET_COV + Insti_One_M_RET + Insti_Ret_COV + Insti_Ret + log_tna + Ret_COV + One_M_RET_COV" \
        "+ monthly_star + Insti_Star_COV + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, past 12 months' return, without COV interactions
fom44 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + rolling_12_months_return" \
        "+ Insti_Twelve_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, past 12 months return, with COV interactions
fom45 = "fund_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + rolling_12_months_return" \
        "+ Insti_Twelve_M_RET_COV + Insti_Twelve_M_RET + Insti_Ret_COV + Insti_Ret + log_tna + Ret_COV + Twelve_M_RET_COV" \
        "+ monthly_star + Insti_Star_COV + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, prior month's return, without COV interactions
fom46 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, prior month's return, with COV interactions
fom47 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET_COV + Insti_One_M_RET + Insti_Ret_COV + Insti_Ret + log_tna + Ret_COV + One_M_RET_COV" \
        "+ monthly_star + Insti_Star_COV + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, past 12 months' return, without COV interactions
fom48 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + rolling_12_months_return" \
        "+ Insti_Twelve_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, past 12 months return, with COV interactions
fom49 = "normalized_flows ~ Insti_High_ESG_COV + Insti_Low_ESG_COV + Insti_High_ESG + Insti_Low_ESG + Insti_COV + Insti" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + weekly_return + rolling_12_months_return" \
        "+ Insti_Twelve_M_RET_COV + Insti_Twelve_M_RET + Insti_Ret_COV + Insti_Ret + log_tna + Ret_COV + Twelve_M_RET_COV" \
        "+ monthly_star + Insti_Star_COV + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg42 = sm.ols(formula=fom42, data=df_mod1).fit()
reg43 = sm.ols(formula=fom43, data=df_mod1).fit()
reg44 = sm.ols(formula=fom44, data=df_mod1).fit()
reg45 = sm.ols(formula=fom45, data=df_mod1).fit()
reg46 = sm.ols(formula=fom46, data=df_mod1).fit()
reg47 = sm.ols(formula=fom47, data=df_mod1).fit()
reg48 = sm.ols(formula=fom48, data=df_mod1).fit()
reg49 = sm.ols(formula=fom49, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg42, reg43, reg44, reg45])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Insti_High_ESG_COV": "High ESG x COV x Institutional",
                             "Insti_Low_ESG_COV": "Low ESG x COV x Institutional", "Low_ESG_COV": "Low ESG x COV",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional",
                             "Insti": "Institutional", "Insti_Ret_COV": "Institutional x COV",
                             "Insti_COV": "COV x Institutional", "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV", "Insti_Low_ESG_COV", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV",
                           "Insti", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Insti_Ret_COV", "Ret_COV", "Insti_Ret", "weekly_return",
                           "Insti_One_M_RET_COV", "One_M_RET_COV", "Insti_One_M_RET", "prior_month_return",
                           "Insti_Twelve_M_RET_COV", "Twelve_M_RET_COV", "Insti_Twelve_M_RET", "rolling_12_months_return",
                           "weekly_div", "log_tna", "normalized_exp", "Insti_Star_COV", "Insti_Star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_insti.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg46, reg47, reg48, reg49])
stargazer.rename_covariates({"High_ESG_COV": "High ESG x COV", "Insti_High_ESG_COV": "High ESG x COV x Institutional",
                             "Insti_Low_ESG_COV": "Low ESG x COV x Institutional", "Low_ESG_COV": "Low ESG x COV",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV": "COV x Institutional", "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV", "Insti_Low_ESG_COV", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV",
                           "Insti", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Insti_Ret_COV", "Ret_COV", "Insti_Ret", "weekly_return",
                           "Insti_One_M_RET_COV", "One_M_RET_COV", "Insti_One_M_RET", "prior_month_return",
                           "Insti_Twelve_M_RET_COV", "Twelve_M_RET_COV", "Insti_Twelve_M_RET", "rolling_12_months_return",
                           "weekly_div", "log_tna", "normalized_exp", "Insti_Star_COV", "Insti_Star", "Star_COV", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_insti.html', 'w').write(stargazer.render_html())


##############################################
# 7. Model
# Triple-diff. regressions
# distinguishing between multiple sub-timeframes (insti vs. retail)
# Globe Rating
##############################################

# % NET FLOW, prior month's return, without COV interactions
fom50 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, prior month's return, with COV interactions
fom51 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET_COV_CRASH + Insti_One_M_RET_COV_REC + Insti_One_M_RET + Insti_Ret_COV_CRASH + Insti_Ret_COV_REC + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, past 12 months' return, without COV interactions
fom52 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_Twelve_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, past 12 months return, with COV interactions
fom53 = "fund_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_Twelve_M_RET_COV_CRASH + Insti_Twelve_M_RET_COV_REC + Insti_Twelve_M_RET + Insti_Ret_COV_CRASH + Insti_Ret_COV_REC + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC + Insti_Star + Star_COV_CRASH + Star_COV_REC + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, prior month's return, without COV interactions
fom54 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, prior month's return, with COV interactions
fom55 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_One_M_RET_COV_CRASH + Insti_One_M_RET_COV_REC + Insti_One_M_RET + Insti_Ret_COV_CRASH + Insti_Ret_COV_REC + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC + Insti_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, past 12 months' return, without COV interactions
fom56 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_Twelve_M_RET + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, past 12 months return, with COV interactions
fom57 = "normalized_flows ~ Insti_High_ESG_COV_CRASH + Insti_High_ESG_COV_REC + Insti_Low_ESG_COV_CRASH + Insti_Low_ESG_COV_REC + Insti_High_ESG + Insti_Low_ESG + Insti_COV_CRASH + Insti_COV_REC + Insti" \
        "+ High_ESG_COV_CRASH + High_ESG_COV_REC + Low_ESG_COV_CRASH + Low_ESG_COV_REC + High_ESG + Low_ESG + weekly_return + prior_month_return" \
        "+ Insti_Twelve_M_RET_COV_CRASH + Insti_Twelve_M_RET_COV_REC + Insti_Twelve_M_RET + Insti_Ret_COV_CRASH + Insti_Ret_COV_REC + Insti_Ret + log_tna" \
        "+ monthly_star + Insti_Star_COV_CRASH + Insti_Star_COV_REC + Insti_Star + Star_COV_CRASH + Star_COV_REC + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg50 = sm.ols(formula=fom50, data=df_mod1).fit()
reg51 = sm.ols(formula=fom51, data=df_mod1).fit()
reg52 = sm.ols(formula=fom52, data=df_mod1).fit()
reg53 = sm.ols(formula=fom53, data=df_mod1).fit()
reg54 = sm.ols(formula=fom54, data=df_mod1).fit()
reg55 = sm.ols(formula=fom55, data=df_mod1).fit()
reg56 = sm.ols(formula=fom56, data=df_mod1).fit()
reg57 = sm.ols(formula=fom57, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg50, reg51, reg52, reg53])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Insti_High_ESG_COV_CRASH": "High ESG x COV (CRASH) x Institutional", "Insti_High_ESG_COV_REC": "High ESG x COV (RECOVERY) x Institutional",
                             "Insti_Low_ESG_COV_CRASH": "Low ESG x COV (CRASH) x Institutional", "Insti_Low_ESG_COV_REC": "Low ESG x COV (RECOVERY) x Institutional",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV_CRASH": "COV (CRASH) x Institutional", "Insti_COV_REC": "COV (RECOVERY) x Institutional",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV_CRASH", "Insti_High_ESG_COV_REC", "Insti_Low_ESG_COV_CRASH",
                           "Insti_Low_ESG_COV_REC", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV_CRASH", "Insti_COV_REC",
                           "Insti", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC", "High_ESG", "Low_ESG"])
stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Institutional Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return COV Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Institutional Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating COV Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_net_flow_insti_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg54, reg55, reg56, reg57])
stargazer.rename_covariates({"High_ESG_COV_CRASH": "High ESG x COV (CRASH)", "High_ESG_COV_REC": "High ESG x COV (RECOVERY)",
                             "Insti_High_ESG_COV_CRASH": "High ESG x COV (CRASH) x Institutional", "Insti_High_ESG_COV_REC": "High ESG x COV (RECOVERY) x Institutional",
                             "Insti_Low_ESG_COV_CRASH": "Low ESG x COV (CRASH) x Institutional", "Insti_Low_ESG_COV_REC": "Low ESG x COV (RECOVERY) x Institutional",
                             "Low_ESG_COV_CRASH": "Low ESG x COV (CRASH)", "Low_ESG_COV_REC": "Low ESG x COV (RECOVERY)",
                             "Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional", "Insti": "Institutional",
                             "Insti_COV_CRASH": "COV (CRASH) x Institutional", "Insti_COV_REC": "COV (RECOVERY) x Institutional",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG_COV_CRASH", "Insti_High_ESG_COV_REC", "Insti_Low_ESG_COV_CRASH",
                           "Insti_Low_ESG_COV_REC", "Insti_High_ESG", "Insti_Low_ESG", "Insti_COV_CRASH", "Insti_COV_REC",
                           "Insti", "High_ESG_COV_CRASH", "High_ESG_COV_REC", "Low_ESG_COV_CRASH", "Low_ESG_COV_REC", "High_ESG", "Low_ESG"])
stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return Institutional Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Return COV Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating Institutional Interactions", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating COV Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_normalized_flow_insti_subtime.html', 'w').write(stargazer.render_html())


##############################################
# 8. Model
# OLS regression
# distinguishing between multiple sub-timeframes (insti vs. retail)
# Globe Rating
##############################################

# pre-covid
#df_pre = df_pre.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).filter(lambda x: (x.Institutional == "Yes").all())
# normalized flow update
#df_pre["Decile_Rank_pre2"] = df_pre.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
#df_pre["normalized_flows_pre2"] = df_pre.groupby("Decile_Rank_pre2").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
#df_pre["normalized_exp_pre2"] = df_pre.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

# crash
#df_crash = df_crash.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).filter(lambda x: (x.Institutional == "Yes").all())
# normalized flow update
#df_crash["Decile_Rank_crash2"] = df_crash.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
#df_crash["normalized_flows_crash2"] = df_crash.groupby("Decile_Rank_crash2").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
#df_crash["normalized_exp_crash2"] = df_crash.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

# recovery
#df_rec = df_rec.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).filter(lambda x: (x.Institutional == "Yes").all())
# normalized flow update
#df_rec["Decile_Rank_rec2"] = df_rec.groupby(["Date"]).weekly_tna.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
#df_rec["normalized_flows_rec2"] = df_rec.groupby("Decile_Rank_rec2").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))
# normalized net expense ratio update
#df_rec["normalized_exp_rec2"] = df_rec.groupby("Date").weekly_expense.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

#print(df_rec["ISIN"].nunique())

# percentage net flows
fom58 = "fund_flows ~ Insti_High_ESG + Insti_Low_ESG + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Insti" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# normalized flows
fom59a = "normalized_flows_pre ~ Insti_High_ESG + Insti_Low_ESG + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Insti" \
        "+ log_tna + normalized_exp_pre + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom59b = "normalized_flows_crash ~ Insti_High_ESG + Insti_Low_ESG + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Insti" \
        "+ log_tna + normalized_exp_crash + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom59c = "normalized_flows_rec ~ Insti_High_ESG + Insti_Low_ESG + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return + Insti" \
        "+ log_tna + normalized_exp_rec + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg58 = sm.ols(formula=fom58, data=df_pre).fit()
reg59 = sm.ols(formula=fom59a, data=df_pre).fit()
reg60 = sm.ols(formula=fom58, data=df_crash).fit()
reg61 = sm.ols(formula=fom59b, data=df_crash).fit()
reg62 = sm.ols(formula=fom58, data=df_rec).fit()
reg63 = sm.ols(formula=fom59c, data=df_rec).fit()


# Output for dep. variable Percentage Net Flows
stargazer = Stargazer([reg58, reg60, reg62])
stargazer.rename_covariates({"Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional",
                             "Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "Insti": "Institutional",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG", "Insti_Low_ESG", "High_ESG", "Low_ESG", "Insti",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Categroy Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_net_flow_insti_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flows
stargazer = Stargazer([reg59])
stargazer.rename_covariates({"Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional",
                             "Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "Insti": "Institutional",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_pre": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG", "Insti_Low_ESG", "High_ESG", "Low_ESG", "Insti",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_pre", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_insti_pre.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg61])
stargazer.rename_covariates({"Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional",
                             "Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "Insti": "Institutional",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_crash": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG", "Insti_Low_ESG", "High_ESG", "Low_ESG", "Insti",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_crash", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_insti_crash.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg63])
stargazer.rename_covariates({"Insti_High_ESG": "High ESG x Institutional", "Insti_Low_ESG": "Low ESG x Institutional",
                             "Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "Insti": "Institutional",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp_rec": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "Insti_High_ESG", "Insti_Low_ESG", "High_ESG", "Low_ESG", "Insti",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_rec", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_normalized_flow_insti_rec.html', 'w').write(stargazer.render_html())


##############################################
# 9. Model
# Diff in diff regression
# E/S/G risk scores
# distinguishing between multiple sub-timeframes
##############################################

# NET FLOW, no COV interactions, 1 M. return
fom70 = "fund_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, COV interactions, 1 M. return
fom71 = "fund_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return + Ret_COV_CRASH + Ret_COV_REC + One_M_RET_COV_CRASH + One_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, no COV interactions, 12 M. return
fom72 = "fund_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NET FLOW, COV interactions, 12 M. return
fom73 = "fund_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + rolling_12_months_return + Ret_COV_CRASH + Ret_COV_REC + Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no COV interactions, 1 M. return
fom74 = "normalized_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, COV interactions, 1 M. return
fom75 = "normalized_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return + Ret_COV_CRASH + Ret_COV_REC + One_M_RET_COV_CRASH + One_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, no COV interactions, 12 M. return
fom76 = "normalized_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, COV interactions, 12 M. return
fom77 = "normalized_flows ~ ENV_COV_CRASH + ENV_COV_REC + SOC_COV_CRASH + SOC_COV_REC + GOV_COV_CRASH + GOV_COV_REC + monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + rolling_12_months_return + Ret_COV_CRASH + Ret_COV_REC + Twelve_M_RET_COV_CRASH + Twelve_M_RET_COV_REC" \
        "+ log_tna + normalized_exp + monthly_star + Star_COV_CRASH + Star_COV_REC + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg70 = sm.ols(formula=fom70, data=df_mod1).fit()
reg71 = sm.ols(formula=fom71, data=df_mod1).fit()
reg72 = sm.ols(formula=fom72, data=df_mod1).fit()
reg73 = sm.ols(formula=fom73, data=df_mod1).fit()
reg74 = sm.ols(formula=fom74, data=df_mod1).fit()
reg75 = sm.ols(formula=fom75, data=df_mod1).fit()
reg76 = sm.ols(formula=fom76, data=df_mod1).fit()
reg77 = sm.ols(formula=fom77, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg70, reg71, reg72, reg73])
stargazer.rename_covariates({"ENV_COV_CRASH": "Environmental x COV (CRASH)", "ENV_COV_REC": "Environmental x COV (REC)",
                             "SOC_COV_CRASH": "Social x COV (CRASH)", "SOC_COV_REC": "Social x COV (REC)",
                             "GOV_COV_CRASH": "Governance x COV (CRASH)", "GOV_COV_REC": "Governance x COV (REC)",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "weekly_div": "Dividends", "normalized_exp": "Normalized Net Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "ENV_COV_CRASH", "ENV_COV_REC", "SOC_COV_CRASH", "SOC_COV_REC", "GOV_COV_CRASH", "GOV_COV_REC",
                           "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV_CRASH", "Ret_COV_REC", "weekly_return", "One_M_RET_COV_CRASH",
                           "One_M_RET_COV_REC", "prior_month_return", "Twelve_M_RET_COV_CRASH", "Twelve_M_RET_COV_REC",
                           "rolling_12_months_return", "weekly_div", "log_tna", "normalized_exp", "Star_COV_CRASH",
                           "Star_COV_REC", "monthly_star", "Age", "index_indicator"])
#stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_risk_scores_net_flow_subtime.html', 'w').write(stargazer.render_html())


# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg74, reg75, reg76, reg77])
stargazer.rename_covariates({"ENV_COV_CRASH": "Environmental x COV (CRASH)", "ENV_COV_REC": "Environmental x COV (REC)",
                             "SOC_COV_CRASH": "Social x COV (CRASH)", "SOC_COV_REC": "Social x COV (REC)",
                             "GOV_COV_CRASH": "Governance x COV (CRASH)", "GOV_COV_REC": "Governance x COV (REC)",
                             "monthly_env": "Environmental", "monthly_soc": "Social", "monthly_gov": "Governance",
                             "Ret_COV_CRASH": "Return x COV (CRASH)", "Ret_COV_REC": "Return x COV (RECOVERY)", "weekly_return": "Return",
                             "One_M_RET_COV_CRASH": "Prior Month's Return x COV (CRASH)", "One_M_RET_COV_REC": "Prior Month's Return x COV (RECOVERY)",
                             "Twelve_M_RET_COV_CRASH": "Prior 12 Months' Return x COV (CRASH)", "Twelve_M_RET_COV_REC": "Prior 12 Months' Return x COV (RECOVERY)",
                             "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "weekly_div": "Dividends", "normalized_exp": "Normalized Net Expense Ratio", "monthly_star": "Star Rating",
                             "Star_COV_CRASH": "Star Rating x COV (CRASH)", "Star_COV_REC": "Star Rating x COV (RECOVERY)", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "ENV_COV_CRASH", "ENV_COV_REC", "SOC_COV_CRASH", "SOC_COV_REC", "GOV_COV_CRASH", "GOV_COV_REC",
                           "monthly_env", "monthly_soc", "monthly_gov", "Ret_COV_CRASH", "Ret_COV_REC", "weekly_return", "One_M_RET_COV_CRASH",
                           "One_M_RET_COV_REC", "prior_month_return", "Twelve_M_RET_COV_CRASH", "Twelve_M_RET_COV_REC",
                           "rolling_12_months_return", "weekly_div", "log_tna", "normalized_exp", "Star_COV_CRASH",
                           "Star_COV_REC", "monthly_star", "Age", "index_indicator"])
#stargazer.add_line("Return Controls", ["W/1M", "W/1M", "W/12M", "W/12M"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Return Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Star Rating Interactions", ["N", "Y", "N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
#stargazer.add_line("Other Controls", ["Y", "Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('diff_in_diff_risk_scores_normalized_flow_subtime.html', 'w').write(stargazer.render_html())

##############################################
# 10. Model
# OLS regression
# different timeframes
# Globe Rating
##############################################

# percentage net flows
fom80 = "fund_flows ~ monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# normalized flows
fom81a = "normalized_flows_pre ~ monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_pre + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom81b = "normalized_flows_crash ~ monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_crash + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom81c = "normalized_flows_rec ~ monthly_env + monthly_soc + monthly_gov" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_rec + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg80 = sm.ols(formula=fom80, data=df_pre).fit()
reg81 = sm.ols(formula=fom81a, data=df_pre).fit()
reg82 = sm.ols(formula=fom80, data=df_crash).fit()
reg83 = sm.ols(formula=fom81b, data=df_crash).fit()
reg84 = sm.ols(formula=fom80, data=df_rec).fit()
reg85 = sm.ols(formula=fom81c, data=df_rec).fit()


# Output for dep. variable Percentage Net Flows
stargazer = Stargazer([reg80, reg82, reg84])
stargazer.rename_covariates({"monthly_env": "Environmental", "monthly_soc": "Social",
                             "monthly_gov": "Governance", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "monthly_env", "monthly_soc", "monthly_gov",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_net_flow_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flows
stargazer = Stargazer([reg81])
stargazer.rename_covariates({"monthly_env": "Environmental", "monthly_soc": "Social",
                             "monthly_gov": "Governance", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "normalized_exp_pre": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "monthly_env", "monthly_soc", "monthly_gov",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_pre", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_normalized_flow_pre.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg83])
stargazer.rename_covariates({"monthly_env": "Environmental", "monthly_soc": "Social",
                             "monthly_gov": "Governance", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "normalized_exp_crash": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "monthly_env", "monthly_soc", "monthly_gov",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_crash", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_normalized_flow_crash.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg85])
stargazer.rename_covariates({"monthly_env": "Environmental", "monthly_soc": "Social",
                             "monthly_gov": "Governance", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return",
                             "prior_month_return": "Prior Month's Return", "log_tna": "log(TNA)",
                             "normalized_exp_rec": "Normalized Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "monthly_env", "monthly_soc", "monthly_gov",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_rec", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_risk_scores_normalized_flow_rec.html', 'w').write(stargazer.render_html())


##############################################
# 11. Model
# OLS regression
# different timeframes (prior month's return)
# Globe Rating
##############################################

# percentage net flows
fom90 = "fund_flows ~ High_ESG_One_M_RET + Low_ESG_One_M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# normalized flows
fom91a = "normalized_flows_pre ~ High_ESG_One_M_RET + Low_ESG_One_M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_pre + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom91b = "normalized_flows_crash ~ High_ESG_One_M_RET + Low_ESG_One_M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_crash + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom91c = "normalized_flows_rec ~ High_ESG_One_M_RET + Low_ESG_One_M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp_rec + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg90 = sm.ols(formula=fom90, data=df_pre).fit()
reg91 = sm.ols(formula=fom91a, data=df_pre).fit()
reg92 = sm.ols(formula=fom90, data=df_crash).fit()
reg93 = sm.ols(formula=fom91b, data=df_crash).fit()
reg94 = sm.ols(formula=fom90, data=df_rec).fit()
reg95 = sm.ols(formula=fom91c, data=df_rec).fit()


# Output for dep. variable Percentage Net Flows
stargazer = Stargazer([reg90, reg92, reg94])
stargazer.rename_covariates({"High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_return_net_flow_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flows
stargazer = Stargazer([reg91])
stargazer.rename_covariates({"High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_pre": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_pre", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_return_normalized_flow_pre.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg93])
stargazer.rename_covariates({"High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_crash": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_crash", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_return_normalized_flow_crash.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg95])
stargazer.rename_covariates({"High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_rec": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp_rec", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_return_normalized_flow_rec.html', 'w').write(stargazer.render_html())


##############################################
# 12. Model
# Triple-diff. regressions
# past monthly return
# Globe Rating
##############################################

# % NET FLOW, without COV interactions for controls
fom110 = "fund_flows ~ High_ESG_One_M_RET_COV + Low_ESG_One_M_RET_COV + High_ESG_One_M_RET + Low_ESG_One_M_RET + prior_month_return + weekly_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + One_M_RET_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, with COV interactions for controls
fom111 = "fund_flows ~ High_ESG_One_M_RET_COV + Low_ESG_One_M_RET_COV + High_ESG_One_M_RET + Low_ESG_One_M_RET + One_M_RET_COV + prior_month_return + weekly_return + Ret_COV" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + One_M_RET_Star_COV + One_M_RET_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, without COV interactions for controls
fom112 = "normalized_flows ~ High_ESG_One_M_RET_COV + Low_ESG_One_M_RET_COV + High_ESG_One_M_RET + Low_ESG_One_M_RET + prior_month_return + weekly_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + One_M_RET_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with COV interactions for controls
fom113 = "normalized_flows ~ High_ESG_One_M_RET_COV + Low_ESG_One_M_RET_COV + High_ESG_One_M_RET + Low_ESG_One_M_RET + One_M_RET_COV + prior_month_return + weekly_return + Ret_COV" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + One_M_RET_Star_COV + One_M_RET_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"


reg110 = sm.ols(formula=fom110, data=df_mod1).fit()
reg111 = sm.ols(formula=fom111, data=df_mod1).fit()
reg112 = sm.ols(formula=fom112, data=df_mod1).fit()
reg113 = sm.ols(formula=fom113, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg110, reg111])
stargazer.rename_covariates({"High_ESG_One_M_RET_COV": "High ESG x 1 M. Return x COV", "Low_ESG_One_M_RET_COV": "Low ESG x 1 M. Return x COV",
                             "High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "One_M_RET_COV": "1 M. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "weekly_return": "Return", "Ret_COV": "Return x COV",
                             "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "One_M_RET_Star_COV": "1 M. Return x Star Rating x COV", "One_M_RET_Star": "1 M. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET_COV", "Low_ESG_One_M_RET_COV", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "One_M_RET_COV",
                           "prior_month_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return", "weekly_div",
                           "log_tna", "normalized_exp", "One_M_RET_Star_COV", "Star_COV", "One_M_RET_Star", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 1 M. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_net_flow_past_m_return.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg112, reg113])
stargazer.rename_covariates({"High_ESG_One_M_RET_COV": "High ESG x 1 M. Return x COV", "Low_ESG_One_M_RET_COV": "Low ESG x 1 M. Return x COV",
                             "High_ESG_One_M_RET": "High ESG x 1 M. Return", "Low_ESG_One_M_RET": "Low ESG x 1 M. Return",
                             "One_M_RET_COV": "1 M. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "weekly_return": "Return", "Ret_COV": "Return x COV",
                             "normalized_exp": "Normalized Net Expense Ratio",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "One_M_RET_Star_COV": "1 M. Return x Star Rating x COV", "One_M_RET_Star": "1 M. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_One_M_RET_COV", "Low_ESG_One_M_RET_COV", "High_ESG_One_M_RET", "Low_ESG_One_M_RET", "One_M_RET_COV",
                           "prior_month_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "Ret_COV", "weekly_return", "weekly_div",
                           "log_tna", "normalized_exp", "One_M_RET_Star_COV", "Star_COV", "One_M_RET_Star", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 1 M. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_normalized_flow_past_m_return.html', 'w').write(stargazer.render_html())

##############################################
# 12. Model
# Triple-diff. regressions
# past weekly return
# Globe Rating
##############################################

# % NET FLOW, without COV interactions for controls
fom120 = "fund_flows ~ High_ESG_PAST_RET_COV + Low_ESG_PAST_RET_COV + High_ESG_PAST_RET + Low_ESG_PAST_RET + prior_week_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + PAST_RET_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, with COV interactions for controls
fom121 = "fund_flows ~ High_ESG_PAST_RET_COV + Low_ESG_PAST_RET_COV + High_ESG_PAST_RET + Low_ESG_PAST_RET + PAST_RET_COV + prior_week_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + PAST_RET_Star_COV + PAST_RET_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, without COV interactions for controls
fom122 = "normalized_flows ~ High_ESG_PAST_RET_COV + Low_ESG_PAST_RET_COV + High_ESG_PAST_RET + Low_ESG_PAST_RET + prior_week_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + PAST_RET_Star + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with COV interactions for controls
fom123 = "normalized_flows ~ High_ESG_PAST_RET_COV + Low_ESG_PAST_RET_COV + High_ESG_PAST_RET + Low_ESG_PAST_RET + PAST_RET_COV + prior_week_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna" \
        "+ monthly_star + PAST_RET_Star_COV + PAST_RET_Star + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"


reg120 = sm.ols(formula=fom120, data=df_mod1).fit()
reg121 = sm.ols(formula=fom121, data=df_mod1).fit()
reg122 = sm.ols(formula=fom122, data=df_mod1).fit()
reg123 = sm.ols(formula=fom123, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg120, reg121])
stargazer.rename_covariates({"High_ESG_PAST_RET_COV": "High ESG x 1 W. Return x COV", "Low_ESG_PAST_RET_COV": "Low ESG x 1 W. Return x COV",
                             "High_ESG_PAST_RET": "High ESG x 1 W. Return", "Low_ESG_PAST_RET": "Low ESG x 1 W. Return",
                             "PAST_RET_COV": "1 W. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "normalized_exp": "Norm. Net Expense Ratio",
                             "prior_week_return": "1 W. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "PAST_RET_Star_COV": "1 W. Return x Star Rating x COV", "PAST_RET_Star": "1 W. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_PAST_RET_COV", "Low_ESG_PAST_RET_COV", "High_ESG_PAST_RET", "Low_ESG_PAST_RET", "PAST_RET_COV",
                           "prior_week_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_div",
                           "log_tna", "normalized_exp", "PAST_RET_Star_COV", "Star_COV", "PAST_RET_Star", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 1 W. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_net_flow_past_w_return.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg122, reg123])
stargazer.rename_covariates({"High_ESG_PAST_RET_COV": "High ESG x 1 W. Return x COV", "Low_ESG_PAST_RET_COV": "Low ESG x 1 W. Return x COV",
                             "High_ESG_PAST_RET": "High ESG x 1 W. Return", "Low_ESG_PAST_RET": "Low ESG x 1 W. Return",
                             "PAST_RET_COV": "1 W. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "normalized_exp": "Norm. Net Expense Ratio",
                             "prior_week_return": "1 W. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "PAST_RET_Star_COV": "1 W. Return x Star Rating x COV", "PAST_RET_Star": "1 W. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_PAST_RET_COV", "Low_ESG_PAST_RET_COV", "High_ESG_PAST_RET", "Low_ESG_PAST_RET", "PAST_RET_COV",
                           "prior_week_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_div",
                           "log_tna", "normalized_exp", "PAST_RET_Star_COV", "Star_COV", "PAST_RET_Star", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 1 W. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_normalized_flow_past_w_return.html', 'w').write(stargazer.render_html())



##############################################
# 13. Model
# Triple-diff. regressions
# past 12 months return
# Globe Rating
##############################################

# % NET FLOW, without COV interactions for controls
fom130 = "fund_flows ~ High_ESG_12M_RET_COV + Low_ESG_12M_RET_COV + High_ESG_12M_RET + Low_ESG_12M_RET + rolling_12_months_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna + weekly_return" \
        "+ monthly_star + Star_12M_RET + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# % NET FLOW, with COV interactions for controls
fom131 = "fund_flows ~ High_ESG_12M_RET_COV + Low_ESG_12M_RET_COV + High_ESG_12M_RET + Low_ESG_12M_RET + Twelve_M_RET_COV + rolling_12_months_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna + weekly_return + Ret_COV" \
        "+ monthly_star + Star_12M_RET_COV + Star_12M_RET + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, without COV interactions for controls
fom132 = "normalized_flows ~ High_ESG_12M_RET_COV + Low_ESG_12M_RET_COV + High_ESG_12M_RET + Low_ESG_12M_RET + rolling_12_months_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna + weekly_return" \
        "+ monthly_star + Star_12M_RET + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# NORMALIZED FLOW, with COV interactions for controls
fom133 = "normalized_flows ~ High_ESG_12M_RET_COV + Low_ESG_12M_RET_COV + High_ESG_12M_RET + Low_ESG_12M_RET + Twelve_M_RET_COV + rolling_12_months_return" \
        "+ High_ESG_COV + Low_ESG_COV + High_ESG + Low_ESG + log_tna + weekly_return + Ret_COV" \
        "+ monthly_star + Star_12M_RET_COV + Star_12M_RET + Star_COV + normalized_exp + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"


reg130 = sm.ols(formula=fom130, data=df_mod1).fit()
reg131 = sm.ols(formula=fom131, data=df_mod1).fit()
reg132 = sm.ols(formula=fom132, data=df_mod1).fit()
reg133 = sm.ols(formula=fom133, data=df_mod1).fit()

# Output for dep. variable Net Flow
stargazer = Stargazer([reg130, reg131])
stargazer.rename_covariates({"High_ESG_12M_RET_COV": "High ESG x 12 M. Return x COV", "Low_ESG_12M_RET_COV": "Low ESG x 12 M. Return x COV",
                             "High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "Twelve_M_RET_COV": "12 M. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "weekly_return": "Return", "Ret_COV": "Return x COV",
                             "normalized_exp": "Norm. Net Expense Ratio",
                             "rolling_12_months_return": "12 M. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "Star_12M_RET_COV": "12 M. Return x Star Rating x COV", "Star_12M_RET": "12 M. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Percentage Net Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET_COV", "Low_ESG_12M_RET_COV", "High_ESG_12M_RET", "Low_ESG_12M_RET", "Twelve_M_RET_COV",
                           "rolling_12_months_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_return", "Ret_COV", "weekly_div",
                           "log_tna", "normalized_exp", "Star_12M_RET_COV", "Star_COV", "Star_12M_RET", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 12 M. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_net_flow_past_12m_return.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normailized Flow
stargazer = Stargazer([reg132, reg133])
stargazer.rename_covariates({"High_ESG_12M_RET_COV": "High ESG x 12 M. Return x COV", "Low_ESG_12M_RET_COV": "Low ESG x 12 M. Return x COV",
                             "High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "Twelve_M_RET_COV": "12 M. Return x COV", "High_ESG_COV": "High ESG x COV", "Low_ESG_COV": "Low ESG x COV",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends", "weekly_return": "Return", "Ret_COV": "Return x COV",
                             "normalized_exp": "Norm. Net Expense Ratio",
                             "rolling_12_months_return": "12 M. Return", "log_tna": "log(TNA)", "monthly_star": "Star Rating",
                             "Star_12M_RET_COV": "12 M. Return x Star Rating x COV", "Star_12M_RET": "12 M. Return x Star Rating",
                             "Star_COV": "Star Rating x COV", "index_indicator": "Index Fund"})
stargazer.dependent_variable = " Normalized Flows"
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET_COV", "Low_ESG_12M_RET_COV", "High_ESG_12M_RET", "Low_ESG_12M_RET", "Twelve_M_RET_COV",
                           "rolling_12_months_return", "High_ESG_COV", "Low_ESG_COV", "High_ESG", "Low_ESG", "weekly_return", "Ret_COV", "weekly_div",
                           "log_tna", "normalized_exp", "Star_12M_RET_COV", "Star_COV", "Star_12M_RET", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Star Rating", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x COV", ["N", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Star Rating x 12 M. Return", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("FF. Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Other Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('triple_diff_normalized_flow_past_12m_return.html', 'w').write(stargazer.render_html())


##############################################
# 14. Model
# OLS regression
# different timeframes (past 12 months' return)
# Globe Rating
##############################################

# percentage net flows
fom90 = "fund_flows ~ High_ESG_12M_RET + Low_ESG_12M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

# normalized flows
fom91a = "normalized_flows_pre ~ High_ESG_12M_RET + Low_ESG_12M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp_pre + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom91b = "normalized_flows_crash ~ High_ESG_12M_RET + Low_ESG_12M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp_crash + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"
fom91c = "normalized_flows_rec ~ High_ESG_12M_RET + Low_ESG_12M_RET + High_ESG + Low_ESG" \
        "+ weekly_return + rolling_12_months_return" \
        "+ log_tna + normalized_exp_rec + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg90 = sm.ols(formula=fom90, data=df_pre).fit()
reg91 = sm.ols(formula=fom91a, data=df_pre).fit()
reg92 = sm.ols(formula=fom90, data=df_crash).fit()
reg93 = sm.ols(formula=fom91b, data=df_crash).fit()
reg94 = sm.ols(formula=fom90, data=df_rec).fit()
reg95 = sm.ols(formula=fom91c, data=df_rec).fit()


# Output for dep. variable Percentage Net Flows
stargazer = Stargazer([reg90, reg92, reg94])
stargazer.rename_covariates({"High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET", "Low_ESG_12M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_12_return_net_flow_subtime.html', 'w').write(stargazer.render_html())

# Output for dep. variable Normalized Flows
stargazer = Stargazer([reg91])
stargazer.rename_covariates({"High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_pre": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET", "Low_ESG_12M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp_pre", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_12_return_normalized_flow_pre.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg93])
stargazer.rename_covariates({"High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_crash": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET", "Low_ESG_12M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp_crash", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_12_return_normalized_flow_crash.html', 'w').write(stargazer.render_html())

stargazer = Stargazer([reg95])
stargazer.rename_covariates({"High_ESG_12M_RET": "High ESG x 12 M. Return", "Low_ESG_12M_RET": "Low ESG x 12 M. Return",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "12 M. Return",
                             "prior_month_return": "1 M. Return", "log_tna": "log(TNA)",
                             "normalized_exp_rec": "Norm. Net Expense Ratio", "monthly_star": "Star Rating",
                             "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG_12M_RET", "Low_ESG_12M_RET", "High_ESG", "Low_ESG",
                           "weekly_return", "rolling_12_months_return", "weekly_div",
                           "log_tna", "normalized_exp_rec", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("FF. Europe 5 Factors", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fund Provider", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Global Category Controls", ["Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_past_12_return_normalized_flow_rec.html', 'w').write(stargazer.render_html())
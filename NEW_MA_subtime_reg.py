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
# 5. Model
# OLS regression
# different timeframes
# Globe Rating
##############################################

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
fom41 = "normalized_flows ~ High_ESG + Low_ESG + Above_Average_ESG + Below_Average_ESG" \
        "+ weekly_return + prior_month_return" \
        "+ log_tna + normalized_exp + monthly_star + weekly_div + Age + index_indicator" \
        "+ Allianz + JPMorgan + DWS + Universal + AXA" \
        "+ Mkt_RF + SMB + HML + RMW + CMA" \
        "+ small_core + mid_core + large_core + large_growth + large_value + mid_growth + mid_value + small_growth + small_value" \
        "+ utilities + industrials + basic_materials + consumer_cyclical + real_estate + technology + healthcare + consumer_defensive + communication_services + financial_services + energy" \
        "+ Equity_Mis + Eur_EM + Eur_Large + Eur_Mid_Small + Health + Infra + LS_E + Real + Tech + UKE" \
        "+ AT + BEL + DEN + EURO + EUR + EURN + EUREM + EURUK + FIN + FR + GER + GRE + IT + NOR + SVK + ESP + CH + UK"

reg40 = sm.ols(formula=fom40, data=df_final_trimmed).fit()
reg41 = sm.ols(formula=fom41, data=df_final_trimmed).fit()
#reg42 = sm.ols(formula=fom40, data=df_final_trimmed).fit()
#reg43 = sm.ols(formula=fom41, data=df_final_trimmed).fit()
#reg44 = sm.ols(formula=fom40, data=df_final_trimmed).fit()
#reg45 = sm.ols(formula=fom41, data=df_final_trimmed).fit()

# Output for dep. variable Percentage Net Flows & Normalized FLows
stargazer = Stargazer([reg40, reg41])
stargazer.rename_covariates({"Above_Average_ESG": "Above Average ESG", "Below_Average_ESG": "Below Average ESG",
                             "High_ESG": "High ESG", "Low_ESG": "Low ESG", "weekly_div": "Dividends",
                             "weekly_return": "Return", "rolling_12_months_return": "Prior 12 Months' Return", "prior_month_return": "Prior Month's Return",
                             "log_tna": "log(TNA)", "normalized_exp": "Normalized Expense Ratio", "monthly_star": "Star Rating", "index_indicator": "Index Fund"})
stargazer.column_separators = True
stargazer.covariate_order(["Intercept", "High_ESG", "Above_Average_ESG", "Below_Average_ESG", "Low_ESG",
                           "weekly_return", "prior_month_return", "weekly_div",
                           "log_tna", "normalized_exp", "monthly_star", "Age", "index_indicator"])
stargazer.add_line("Fama-French Europe 5 Factors", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Firm Name Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Style Exposures", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Investment Area Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Industry Controls", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.add_line("Fixed Effects", ["Y", "Y"], LineLocation.FOOTER_TOP)
stargazer.show_r2 = False

open('OLS_pre_subtime.html', 'w').write(stargazer.render_html())
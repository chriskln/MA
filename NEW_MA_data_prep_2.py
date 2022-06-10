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

df_flow_weekly = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_flow_weekly.csv", sep= ",")
df_return_weekly = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_return_weekly.csv", sep= ",")
df_tna_weekly = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_tna_weekly.csv", sep= ",")
df_m_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_1\\df_m_return.csv", sep= ",")
df_exp = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\net_exp.csv", sep= ";")
df_tur = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\turnover.csv", sep= ";")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\sus_rating_abs.csv", sep= ";")
df_env = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_env_score.csv", sep= ";")
df_soc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_soc_score.csv", sep= ";")
df_gov = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_gov_score.csv", sep= ";")
df_car = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\car_risk_score.csv", sep= ";")
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\static_var.csv", sep= ";")
df_static_add = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\controls_add.csv", sep= ";")
df_star = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\star_rating.csv", sep= ";")
df_div = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dividend.csv", sep= ";")
df_fix = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects.csv", sep= ";")
df_rank = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\annual_rank_category.csv", sep= ";")
df_size = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\daily_fund_size.csv", sep= ";")
df_exl = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\exclusions_screening.csv", sep= ";")
df_eff = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\Europe_5_Factors_Daily.csv", sep= ",")
df_static = pd.merge(df_static, df_static_add, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")

# investment style exposures
df_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\growth.csv", sep= ";")
df_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\value.csv", sep= ";")
df_large = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\largecap.csv", sep= ";")
df_mid = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\midcap.csv", sep= ";")
df_small = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\smallcap.csv", sep= ";")
df_large_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\largecap_growth.csv", sep= ";")
df_large_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\largecap_value.csv", sep= ";")
df_large_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\largecap_core.csv", sep= ";")
df_mid_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\midcap_growth.csv", sep= ";")
df_mid_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\midcap_value.csv", sep= ";")
df_mid_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\midcap_core.csv", sep= ";")
df_small_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\smallcap_growth.csv", sep= ";")
df_small_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\smallcap_value.csv", sep= ";")
df_small_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\stylefixedeffects\\smallcap_core.csv", sep= ";")

# industry controls
df_bm = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\basicmaterials.csv", sep= ";")
df_cs = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\communicationservices.csv", sep= ";")
df_cc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\consumercyclical.csv", sep= ";")
df_en = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\energy.csv", sep= ";")
df_cd = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\consumerdefensive.csv", sep= ";")
df_fs = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\financialservices.csv", sep= ";")
df_hc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\healthcare.csv", sep= ";")
df_in = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\industrials.csv", sep= ";")
df_re = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\realestate.csv", sep= ";")
df_tc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\technology.csv", sep= ";")
df_ut = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\industry controls\\utilities.csv", sep= ";")

# delete unnamed columns
df_flow_weekly = df_flow_weekly.loc[:, ~df_flow_weekly.columns.str.contains("^Unnamed")]
df_return_weekly = df_return_weekly.loc[:, ~df_return_weekly.columns.str.contains("^Unnamed")]
df_tna_weekly_fundlevel = df_tna_weekly.loc[:, ~df_tna_weekly.columns.str.contains("^Unnamed")]
df_m_return = df_m_return.loc[:, ~df_m_return.columns.str.contains("^Unnamed")]

##############################################
# Controls
##############################################

################################
# Past Returns
################################

# prior month return
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].add(1)
df_return_weekly["Date"] = df_return_weekly["Date"].astype("datetime64[ns]")
df_return_monthly = df_return_weekly.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("M", on="Date").mean().reset_index()
df_return_monthly = df_return_monthly.rename(columns={"weekly_return": "monthly_return_calc"})

group1 = df_return_monthly.groupby(["ISIN"])
df_return_monthly["prior_month_return"] = group1["monthly_return_calc"].shift(1)

# rolling 12 months return
df_return_monthly["rolling_12_months_return"] = df_return_monthly.groupby(["ISIN"])["monthly_return_calc"].transform(lambda x: x.rolling(12).mean())

df_m_return["Date"] = df_m_return["Date"].astype("datetime64[ns]")
df_m_return["Date"] = pd.to_datetime(df_m_return["Date"], format="%Y-%m")
df_m_return = df_m_return.rename(columns={"Date": "month_year"})
df_return_monthly["month_year"] = pd.to_datetime(df_return_monthly["Date"]).dt.to_period("M")
df_return_monthly = df_return_monthly.drop(columns=["Date"])
df_return_monthly = pd.merge(df_return_monthly, df_m_return, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "month_year"], how="outer")
df_return_monthly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_return_monthly_fundlevel_test.csv")

# back to decimal format
df_return_monthly["rolling_12_months_return"] = df_return_monthly["rolling_12_months_return"].sub(1)
df_return_monthly["prior_month_return"] = df_return_monthly["prior_month_return"].sub(1)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].sub(1)

# convert to % values
df_return_monthly["rolling_12_months_return"] = df_return_monthly["rolling_12_months_return"].mul(100)
df_return_monthly["prior_month_return"] = df_return_monthly["prior_month_return"].mul(100)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].mul(100)

# change date format for later merging
#df_return_monthly_fundlevel["month_year"] = pd.to_datetime(df_return_monthly_fundlevel["Date"]).dt.to_period("M")
#df_return_monthly = df_return_monthly.drop(columns=["Date"])
df_return_monthly["month_year"] = df_return_monthly["month_year"].astype("datetime64[ns]")
df_return_monthly = df_return_monthly.rename(columns={"month_year": "Date"})
#df_return_monthly = df_return_monthly.drop(columns=["month_year"])

df_return_monthly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_return_monthly_fundlevel_test_2.csv")
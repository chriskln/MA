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
# Investment Style Exposure
################################

df_growth = pd.melt(df_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="growth")
df_growth["Date"] = df_growth["Date"].str.slice(29, 36, 1)
df_growth["Date"] = pd.to_datetime(df_growth["Date"], format="%Y-%m-%d")

df_value = pd.melt(df_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="value")
df_value["Date"] = df_value["Date"].str.slice(28, 35, 1)
df_value["Date"] = pd.to_datetime(df_value["Date"], format="%Y-%m-%d")

df_large = pd.melt(df_large, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="large_cap")
df_large["Date"] = df_large["Date"].str.slice(32, 39, 1)
df_large["Date"] = pd.to_datetime(df_large["Date"], format="%Y-%m-%d")

df_mid = pd.melt(df_mid, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="mid_cap")
df_mid["Date"] = df_mid["Date"].str.slice(30, 37, 1)
df_mid["Date"] = pd.to_datetime(df_mid["Date"], format="%Y-%m-%d")

df_small = pd.melt(df_small, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_cap")
df_small["Date"] = df_small["Date"].str.slice(32, 39, 1)
df_small["Date"] = pd.to_datetime(df_small["Date"], format="%Y-%m-%d")

df_large_growth = pd.melt(df_large_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="large_growth")
df_large_growth["Date"] = df_large_growth["Date"].str.slice(35, 42, 1)
df_large_growth["Date"] = pd.to_datetime(df_large_growth["Date"], format="%Y-%m-%d")

df_large_value = pd.melt(df_large_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="large_value")
df_large_value["Date"] = df_large_value["Date"].str.slice(34, 41, 1)
df_large_value["Date"] = pd.to_datetime(df_large_value["Date"], format="%Y-%m-%d")

df_large_core = pd.melt(df_large_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="large_core")
df_large_core["Date"] = df_large_core["Date"].str.slice(33, 40, 1)
df_large_core["Date"] = pd.to_datetime(df_large_core["Date"], format="%Y-%m-%d")

df_mid_growth = pd.melt(df_mid_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="mid_growth")
df_mid_growth["Date"] = df_mid_growth["Date"].str.slice(33, 40, 1)
df_mid_growth["Date"] = pd.to_datetime(df_mid_growth["Date"], format="%Y-%m-%d")

df_mid_value = pd.melt(df_mid_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="mid_value")
df_mid_value["Date"] = df_mid_value["Date"].str.slice(32, 39, 1)
df_mid_value["Date"] = pd.to_datetime(df_mid_value["Date"], format="%Y-%m-%d")

df_mid_core = pd.melt(df_mid_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="mid_core")
df_mid_core["Date"] = df_mid_core["Date"].str.slice(31, 38, 1)
df_mid_core["Date"] = pd.to_datetime(df_mid_core["Date"], format="%Y-%m-%d")

df_small_growth = pd.melt(df_small_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_growth")
df_small_growth["Date"] = df_small_growth["Date"].str.slice(35, 42, 1)
df_small_growth["Date"] = pd.to_datetime(df_small_growth["Date"], format="%Y-%m-%d")

df_small_value = pd.melt(df_small_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_value")
df_small_value["Date"] = df_small_value["Date"].str.slice(34, 41, 1)
df_small_value["Date"] = pd.to_datetime(df_small_value["Date"], format="%Y-%m-%d")

df_small_core = pd.melt(df_small_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_core")
df_small_core["Date"] = df_small_core["Date"].str.slice(33, 40, 1)
df_small_core["Date"] = pd.to_datetime(df_small_core["Date"], format="%Y-%m-%d")

inv_style_exp = [df_growth, df_value, df_large, df_mid, df_small, df_large_growth, df_large_value, df_mid_growth, df_mid_value, df_small_growth, df_small_value, df_large_core, df_small_core, df_mid_core]
df_fixed = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="inner"), inv_style_exp)
df_fixed.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_fixed_test_bef.csv")

# fill nan values with most actual value
df_fixed = df_fixed.groupby("Name", "Fund Legal Name", "FundId", "SecId")
df_fixed = df_fixed["growth"].fillna(method="ffill")

df_fixed.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_fixed_test_aft.csv")


################################
# Past Returns
################################

# prior month return
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].add(1)
df_return_weekly["Date"] = df_return_weekly["Date"].astype("datetime64[ns]")
df_return_monthly = df_return_weekly.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("M", on="Date").prod().reset_index()
df_return_monthly = df_return_monthly.rename(columns={"weekly_return": "monthly_return_calc"})

group1 = df_return_monthly.groupby(["ISIN"])
df_return_monthly["prior_month_return"] = group1["monthly_return_calc"].shift(1)

# rolling 12 months return
df_return_monthly["rolling_12_months_return"] = df_return_monthly.groupby(["ISIN"])["monthly_return_calc"].transform(lambda x: x.rolling(12).mean())

# create prior month's return and rolling 12 months return backup
df_m_return["Date"] = pd.to_datetime(df_m_return["Date"]).dt.to_period("M")
df_return_monthly["Date"] = pd.to_datetime(df_return_monthly["Date"]).dt.to_period("M")
df_return_monthly = pd.merge(df_return_monthly, df_m_return, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="outer")
df_return_monthly["rolling_12_months_return_backup"] = df_return_monthly.groupby(["ISIN"])["monthly_return"].transform(lambda x: x.rolling(12).mean())
group2 = df_return_monthly.groupby(["ISIN"])
df_return_monthly["prior_month_return_backup"] = group2["monthly_return"].shift(1)

# back to decimal format
df_return_monthly["rolling_12_months_return"] = df_return_monthly["rolling_12_months_return"].sub(1)
df_return_monthly["monthly_return_calc"] = df_return_monthly["monthly_return_calc"].sub(1)
df_return_monthly["prior_month_return"] = df_return_monthly["prior_month_return"].sub(1)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].sub(1)

# convert to % values
df_return_monthly["rolling_12_months_return"] = df_return_monthly["rolling_12_months_return"].mul(100)
df_return_monthly["rolling_12_months_return_backup"] = df_return_monthly["rolling_12_months_return_backup"].mul(100)
df_return_monthly["monthly_return_calc"] = df_return_monthly["monthly_return_calc"].mul(100)
df_return_monthly["monthly_return"] = df_return_monthly["monthly_return"].mul(100)
df_return_monthly["prior_month_return"] = df_return_monthly["prior_month_return"].mul(100)
df_return_monthly["prior_month_return_backup"] = df_return_monthly["prior_month_return_backup"].mul(100)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].mul(100)

df_return_monthly = df_return_monthly.rename(columns={"month_year": "Date"})

# if monthly return is nan, use backup
for r in range(0,len(df_return_monthly)):
    if math.isnan(df_return_monthly.loc[r, "monthly_return_calc"]) == True:
        df_return_monthly.loc[r, "monthly_return_calc"] = df_return_monthly.loc[r, "monthly_return"]
    else:
        continue

# if rolling 12 months return is nan, use backup
for r in range(0,len(df_return_monthly)):
    if math.isnan(df_return_monthly.loc[r, "rolling_12_months_return"]) == True:
        df_return_monthly.loc[r, "rolling_12_months_return"] = df_return_monthly.loc[r, "rolling_12_months_return_backup"]
    else:
        continue

# if prior month's return is nan, use backup
for r in range(0,len(df_return_monthly)):
    if math.isnan(df_return_monthly.loc[r, "prior_month_return"]) == True:
        df_return_monthly.loc[r, "prior_month_return"] = df_return_monthly.loc[r, "prior_month_return_backup"]
    else:
        continue

df_return_monthly = df_return_monthly.drop(columns=["monthly_return", "monthly_return_calc", "rolling_12_months_return_backup", "prior_month_return_backup"])


################################
# Index Fund Check
################################

# index fund indicator
df_index_fund = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Index Fund"]].copy()
df_index_fund["name_check"] = df_index_fund["Name"].str.contains("Index", na=False)

for f in range(0, len(df_index_fund)):
    if df_index_fund.loc[f, "name_check"] == True or df_index_fund.loc[f, "Index Fund"] == "Yes":
        df_index_fund.loc[f, "index_indicator"] = 1
    else:
        df_index_fund.loc[f, "index_indicator"] = 0


################################
# Fama and French 5 Factor Europe Returns
################################

# data prep
df_eff["Date"] = pd.to_datetime(df_eff["Date"], format="%Y%m%d")
start = pd.to_datetime("2017-01-01", format="%Y-%m-%d")
end = pd.to_datetime("2020-12-31", format="%Y-%m-%d")
df_eff = df_eff[df_eff["Date"].between(start, end)].reset_index()
df_eff = df_eff.drop(columns=["index"])

# from daily to weekly data by taking means
df_eff["Mkt-RF"] = df_eff["Mkt-RF"].div(100)
df_eff["SMB"] = df_eff["SMB"].div(100)
df_eff["HML"] = df_eff["HML"].div(100)
df_eff["RMW"] = df_eff["RMW"].div(100)
df_eff["CMA"] = df_eff["CMA"].div(100)
df_eff["RF"] = df_eff["RF"].div(100)

df_eff["Mkt-RF"] = df_eff["Mkt-RF"].add(1)
df_eff["SMB"] = df_eff["SMB"].add(1)
df_eff["HML"] = df_eff["HML"].add(1)
df_eff["RMW"] = df_eff["RMW"].add(1)
df_eff["CMA"] = df_eff["CMA"].add(1)
df_eff["RF"] = df_eff["RF"].add(1)

df_eff_weekly = df_eff.resample("W", on="Date").prod().reset_index()

df_eff_weekly["Mkt-RF"] = df_eff_weekly["Mkt-RF"].sub(1)
df_eff_weekly["SMB"] = df_eff_weekly["SMB"].sub(1)
df_eff_weekly["HML"] = df_eff_weekly["HML"].sub(1)
df_eff_weekly["RMW"] = df_eff_weekly["RMW"].sub(1)
df_eff_weekly["CMA"] = df_eff_weekly["CMA"].sub(1)
df_eff_weekly["RF"] = df_eff_weekly["RF"].sub(1)

df_eff_weekly["Mkt-RF"] = df_eff_weekly["Mkt-RF"].mul(100)
df_eff_weekly["SMB"] = df_eff_weekly["SMB"].mul(100)
df_eff_weekly["HML"] = df_eff_weekly["HML"].mul(100)
df_eff_weekly["RMW"] = df_eff_weekly["RMW"].mul(100)
df_eff_weekly["CMA"] = df_eff_weekly["CMA"].mul(100)
df_eff_weekly["RF"] = df_eff_weekly["RF"].mul(100)
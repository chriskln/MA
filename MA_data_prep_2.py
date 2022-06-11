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

df_flow_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_flow_weekly_fundlevel.csv", sep= ",")
df_return_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_return_weekly_fundlevel.csv", sep= ",")
df_return_weekly = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_return_weekly.csv", sep= ",")
df_tna_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_tna_weekly_fundlevel.csv", sep= ",")
df_tna_monthly = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_tna_monthly.csv", sep= ",")
df_m_return_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_m_return_fundlevel.csv", sep= ",")
df_m_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_m_return.csv", sep= ",")
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
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.loc[:, ~df_flow_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_return_weekly_fundlevel = df_return_weekly_fundlevel.loc[:, ~df_return_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.loc[:, ~df_tna_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_return_weekly = df_return_weekly.loc[:, ~df_return_weekly.columns.str.contains("^Unnamed")]


##############################################
# Controls
##############################################

################################
# Fund Annual Expenses
################################

df_exp = pd.merge(df_exp, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_exp = df_exp.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area",
                                    "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_exp = pd.melt(df_exp, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="yearly_expense")
df_exp["Date"] = df_exp["Date"].str.slice(36, 40, 1)
df_exp["Date"] = pd.to_datetime(df_exp["Date"], format="%Y-%m-%d")
df_exp = df_exp.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"yearly_expense": "mean"}).reset_index()

for c in range(2, len(df_exp)):
    if math.isnan(df_exp.loc[c, "yearly_expense"]) == True and df_exp.loc[c, "FundId"] == df_exp.loc[c - 1, "FundId"] and df_exp.loc[c, "Institutional"] == df_exp.loc[c - 1, "Institutional"]:
        df_exp.loc[c, "yearly_expense"] = df_exp.loc[c - 1, "yearly_expense"]
    elif math.isnan(df_exp.loc[c, "yearly_expense"]) == True and df_exp.loc[c, "FundId"] == df_exp.loc[c - 2, "FundId"] and df_exp.loc[c, "Institutional"] == df_exp.loc[c - 2, "Institutional"]:
        df_exp.loc[c, "yearly_expense"] = df_exp.loc[c - 2, "yearly_expense"]
    else:
        continue

df_exp["year"] = pd.to_datetime(df_exp["Date"]).dt.to_period("Y")

# obtain weekly expense
df_exp["weekly_expense"] = df_exp["yearly_expense"] / 52
df_exp = df_exp.drop(columns=["Date", "yearly_expense"])


################################
# Turnover Ratio
################################

df_tur = pd.merge(df_tur, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_tur = df_tur.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area",
                                    "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_tur = pd.melt(df_tur, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="yearly_turn")
df_tur["Date"] = df_tur["Date"].str.slice(21, 25, 1)
df_tur["Date"] = pd.to_datetime(df_tur["Date"], format="%Y-%m-%d")
df_tur = df_tur.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"yearly_turn": "mean"}).reset_index()

for c in range(2, len(df_tur)):
    if math.isnan(df_tur.loc[c, "yearly_turn"]) == True and df_tur.loc[c, "FundId"] == df_tur.loc[c - 1, "FundId"] and df_tur.loc[c, "Institutional"] == df_tur.loc[c - 1, "Institutional"]:
        df_tur.loc[c, "yearly_turn"] = df_tur.loc[c - 1, "yearly_turn"]
    elif math.isnan(df_tur.loc[c, "yearly_turn"]) == True and df_tur.loc[c, "FundId"] == df_tur.loc[c - 2, "FundId"] and df_tur.loc[c, "Institutional"] == df_tur.loc[c - 2, "Institutional"]:
        df_tur.loc[c, "yearly_turn"] = df_tur.loc[c - 2, "yearly_turn"]
    else:
        continue

#df_tur["year"] = pd.to_datetime(df_tur["Date"]).dt.to_period("Y")
#df_tur["weekly_turn"] = df_tur["yearly_turn"] / 52


################################
# Index Fund Check
################################

# index fund indicator
df_index_fund = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Index Fund"]].copy()
df_index_fund["name_check"] = df_index_fund["Name"].str.contains("Index", na=False)

for f in range(0, len(df_index_fund)):
    if df_index_fund.loc[f, "name_check"] == True or df_index_fund.loc[f, "Index Fund"] == "Yes":
        df_index_fund.loc[f, "index_indicator"] = 1
    else:
        df_index_fund.loc[f, "index_indicator"] = 0

# if one share class is index, keep this indicator for FundId
df_index_fund = df_index_fund.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"index_indicator": "max"}).reset_index()


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


################################
# Investment Style Exposure
################################

df_growth = pd.merge(df_growth, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_growth = df_growth.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_growth = pd.melt(df_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="growth")
df_growth["Date"] = df_growth["Date"].str.slice(29, 36, 1)
df_growth["Date"] = pd.to_datetime(df_growth["Date"], format="%Y-%m-%d")
df_growth = df_growth.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"growth": "first"}).reset_index()

df_value = pd.merge(df_value, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_value = df_value.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_value = pd.melt(df_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="value")
df_value["Date"] = df_value["Date"].str.slice(28, 35, 1)
df_value["Date"] = pd.to_datetime(df_value["Date"], format="%Y-%m-%d")
df_value = df_value.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"value": "first"}).reset_index()

df_large = pd.merge(df_large, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_large = df_large.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_large = pd.melt(df_large, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="large_cap")
df_large["Date"] = df_large["Date"].str.slice(32, 39, 1)
df_large["Date"] = pd.to_datetime(df_large["Date"], format="%Y-%m-%d")
df_large = df_large.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"large_cap": "first"}).reset_index()

df_mid = pd.merge(df_mid, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_mid = df_mid.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_mid = pd.melt(df_mid, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="mid_cap")
df_mid["Date"] = df_mid["Date"].str.slice(30, 37, 1)
df_mid["Date"] = pd.to_datetime(df_mid["Date"], format="%Y-%m-%d")
df_mid = df_mid.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"mid_cap": "first"}).reset_index()

df_small = pd.merge(df_small, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_small = df_small.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_small = pd.melt(df_small, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="small_cap")
df_small["Date"] = df_small["Date"].str.slice(32, 39, 1)
df_small["Date"] = pd.to_datetime(df_small["Date"], format="%Y-%m-%d")
df_small = df_small.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"small_cap": "first"}).reset_index()

df_large_growth = pd.merge(df_large_growth, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_large_growth = df_large_growth.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_large_growth = pd.melt(df_large_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="large_growth")
df_large_growth["Date"] = df_large_growth["Date"].str.slice(35, 42, 1)
df_large_growth["Date"] = pd.to_datetime(df_large_growth["Date"], format="%Y-%m-%d")
df_large_growth = df_large_growth.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"large_growth": "first"}).reset_index()

df_large_value = pd.merge(df_large_value, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_large_value = df_large_value.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_large_value = pd.melt(df_large_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="large_value")
df_large_value["Date"] = df_large_value["Date"].str.slice(34, 41, 1)
df_large_value["Date"] = pd.to_datetime(df_large_value["Date"], format="%Y-%m-%d")
df_large_value = df_large_value.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"large_value": "first"}).reset_index()

df_large_core = pd.merge(df_large_core, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_large_core = df_large_core.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_large_core = pd.melt(df_large_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="large_core")
df_large_core["Date"] = df_large_core["Date"].str.slice(33, 40, 1)
df_large_core["Date"] = pd.to_datetime(df_large_core["Date"], format="%Y-%m-%d")
df_large_core = df_large_core.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"large_core": "first"}).reset_index()

df_mid_growth = pd.merge(df_mid_growth, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_mid_growth = df_mid_growth.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_mid_growth = pd.melt(df_mid_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="mid_growth")
df_mid_growth["Date"] = df_mid_growth["Date"].str.slice(33, 40, 1)
df_mid_growth["Date"] = pd.to_datetime(df_mid_growth["Date"], format="%Y-%m-%d")
df_mid_growth = df_mid_growth.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"mid_growth": "first"}).reset_index()

df_mid_value = pd.merge(df_mid_value, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_mid_value = df_mid_value.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_mid_value = pd.melt(df_mid_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="mid_value")
df_mid_value["Date"] = df_mid_value["Date"].str.slice(32, 39, 1)
df_mid_value["Date"] = pd.to_datetime(df_mid_value["Date"], format="%Y-%m-%d")
df_mid_value = df_mid_value.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"mid_value": "first"}).reset_index()

df_mid_core = pd.merge(df_mid_core, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_mid_core = df_mid_core.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_mid_core = pd.melt(df_mid_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="mid_core")
df_mid_core["Date"] = df_mid_core["Date"].str.slice(31, 38, 1)
df_mid_core["Date"] = pd.to_datetime(df_mid_core["Date"], format="%Y-%m-%d")
df_mid_core = df_mid_core.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"mid_core": "first"}).reset_index()

df_small_growth = pd.merge(df_small_growth, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_small_growth = df_small_growth.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_small_growth = pd.melt(df_small_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="small_growth")
df_small_growth["Date"] = df_small_growth["Date"].str.slice(35, 42, 1)
df_small_growth["Date"] = pd.to_datetime(df_small_growth["Date"], format="%Y-%m-%d")
df_small_growth = df_small_growth.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"small_growth": "first"}).reset_index()

df_small_value = pd.merge(df_small_value, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_small_value = df_small_value.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_small_value = pd.melt(df_small_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="small_value")
df_small_value["Date"] = df_small_value["Date"].str.slice(34, 41, 1)
df_small_value["Date"] = pd.to_datetime(df_small_value["Date"], format="%Y-%m-%d")
df_small_value = df_small_value.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"small_value": "first"}).reset_index()

df_small_core = pd.merge(df_small_core, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_small_core = df_small_core.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_small_core = pd.melt(df_small_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="small_core")
df_small_core["Date"] = df_small_core["Date"].str.slice(33, 40, 1)
df_small_core["Date"] = pd.to_datetime(df_small_core["Date"], format="%Y-%m-%d")
df_small_core = df_small_core.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"small_core": "first"}).reset_index()

style_fixed_effects = [df_growth, df_value, df_large, df_mid, df_small, df_large_growth, df_large_value, df_mid_growth, df_mid_value, df_small_growth, df_small_value, df_large_core, df_small_core, df_mid_core]
df_fixed = reduce(lambda left, right: pd.merge(left, right, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="inner"), style_fixed_effects)

# fill nan values with most actual value
for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "growth"] = df_fixed.loc[c - 1, "growth"]
    elif math.isnan(df_fixed.loc[c, "growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "growth"] = df_fixed.loc[c - 2, "growth"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "value"] = df_fixed.loc[c - 1, "value"]
    elif math.isnan(df_fixed.loc[c, "value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "value"] = df_fixed.loc[c - 2, "value"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "large_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "large_cap"] = df_fixed.loc[c - 1, "large_cap"]
    elif math.isnan(df_fixed.loc[c, "large_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "large_cap"] = df_fixed.loc[c - 2, "large_cap"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "mid_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "mid_cap"] = df_fixed.loc[c - 1, "mid_cap"]
    elif math.isnan(df_fixed.loc[c, "mid_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "mid_cap"] = df_fixed.loc[c - 2, "mid_cap"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "small_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "small_cap"] = df_fixed.loc[c - 1, "small_cap"]
    elif math.isnan(df_fixed.loc[c, "small_cap"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "small_cap"] = df_fixed.loc[c - 2, "small_cap"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "large_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "large_growth"] = df_fixed.loc[c - 1, "large_growth"]
    elif math.isnan(df_fixed.loc[c, "large_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "large_growth"] = df_fixed.loc[c - 2, "large_growth"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "large_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "large_value"] = df_fixed.loc[c - 1, "large_value"]
    elif math.isnan(df_fixed.loc[c, "large_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "large_value"] = df_fixed.loc[c - 2, "large_value"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "mid_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "mid_growth"] = df_fixed.loc[c - 1, "mid_growth"]
    elif math.isnan(df_fixed.loc[c, "mid_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "mid_growth"] = df_fixed.loc[c - 2, "mid_growth"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "mid_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "mid_value"] = df_fixed.loc[c - 1, "mid_value"]
    elif math.isnan(df_fixed.loc[c, "mid_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "mid_value"] = df_fixed.loc[c - 2, "mid_value"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "small_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "small_growth"] = df_fixed.loc[c - 1, "small_growth"]
    elif math.isnan(df_fixed.loc[c, "small_growth"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "small_growth"] = df_fixed.loc[c - 2, "small_growth"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "small_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "small_value"] = df_fixed.loc[c - 1, "small_value"]
    elif math.isnan(df_fixed.loc[c, "small_value"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "small_value"] = df_fixed.loc[c - 2, "small_value"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "small_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "small_core"] = df_fixed.loc[c - 1, "small_core"]
    elif math.isnan(df_fixed.loc[c, "small_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "small_core"] = df_fixed.loc[c - 2, "small_core"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "mid_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "mid_core"] = df_fixed.loc[c - 1, "mid_core"]
    elif math.isnan(df_fixed.loc[c, "mid_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "mid_core"] = df_fixed.loc[c - 2, "mid_core"]
    else:
        continue

for c in range(2, len(df_fixed)):
    if math.isnan(df_fixed.loc[c, "large_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 1, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 1, "Institutional"]:
        df_fixed.loc[c, "large_core"] = df_fixed.loc[c - 1, "large_core"]
    elif math.isnan(df_fixed.loc[c, "large_core"]) == True and df_fixed.loc[c, "FundId"] == df_fixed.loc[c - 2, "FundId"] and df_fixed.loc[c, "Institutional"] == df_fixed.loc[c - 2, "Institutional"]:
        df_fixed.loc[c, "large_core"] = df_fixed.loc[c - 2, "large_core"]
    else:
        continue

################################
# Industry Controls
################################

df_bm = pd.merge(df_bm, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_bm = df_bm.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_bm = pd.melt(df_bm, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="basic_materials")
df_bm["Date"] = df_bm["Date"].str.slice(44, 51, 1)
df_bm["Date"] = pd.to_datetime(df_bm["Date"], format="%Y-%m-%d")
df_bm = df_bm.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"basic_materials": "first"}).reset_index()

df_cs = pd.merge(df_cs, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_cs = df_cs.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_cs = pd.melt(df_cs, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="communication_services")
df_cs["Date"] = df_cs["Date"].str.slice(51, 58, 1)
df_cs["Date"] = pd.to_datetime(df_cs["Date"], format="%Y-%m-%d")
df_cs = df_cs.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"communication_services": "first"}).reset_index()

df_cc = pd.merge(df_cc, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_cc = df_cc.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_cc = pd.melt(df_cc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="consumer_cyclical")
df_cc["Date"] = df_cc["Date"].str.slice(46, 53, 1)
df_cc["Date"] = pd.to_datetime(df_cc["Date"], format="%Y-%m-%d")
df_cc = df_cc.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"consumer_cyclical": "first"}).reset_index()

df_en = pd.merge(df_en, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_en = df_en.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_en = pd.melt(df_en, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="energy")
df_en["Date"] = df_en["Date"].str.slice(35, 42, 1)
df_en["Date"] = pd.to_datetime(df_en["Date"], format="%Y-%m-%d")
df_en = df_en.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"energy": "first"}).reset_index()

df_cd = pd.merge(df_cd, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_cd = df_cd.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_cd = pd.melt(df_cd, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="consumer_defensive")
df_cd["Date"] = df_cd["Date"].str.slice(47, 54, 1)
df_cd["Date"] = pd.to_datetime(df_cd["Date"], format="%Y-%m-%d")
df_cd = df_cd.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"consumer_defensive": "first"}).reset_index()

df_fs = pd.merge(df_fs, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_fs = df_fs.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_fs = pd.melt(df_fs, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="financial_services")
df_fs["Date"] = df_fs["Date"].str.slice(47, 54, 1)
df_fs["Date"] = pd.to_datetime(df_fs["Date"], format="%Y-%m-%d")
df_fs = df_fs.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"financial_services": "first"}).reset_index()

df_hc = pd.merge(df_hc, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_hc = df_hc.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_hc = pd.melt(df_hc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="healthcare")
df_hc["Date"] = df_hc["Date"].str.slice(39, 46, 1)
df_hc["Date"] = pd.to_datetime(df_hc["Date"], format="%Y-%m-%d")
df_hc = df_hc.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"healthcare": "first"}).reset_index()

df_in = pd.merge(df_in, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_in = df_in.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_in = pd.melt(df_in, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="industrials")
df_in["Date"] = df_in["Date"].str.slice(40, 47, 1)
df_in["Date"] = pd.to_datetime(df_in["Date"], format="%Y-%m-%d")
df_in = df_in.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"industrials": "first"}).reset_index()

df_re = pd.merge(df_re, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_re = df_re.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_re = pd.melt(df_re, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="real_estate")
df_re["Date"] = df_re["Date"].str.slice(40, 47, 1)
df_re["Date"] = pd.to_datetime(df_re["Date"], format="%Y-%m-%d")
df_re = df_re.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"real_estate": "first"}).reset_index()

df_tc = pd.merge(df_tc, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_tc = df_tc.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_tc = pd.melt(df_tc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="technology")
df_tc["Date"] = df_tc["Date"].str.slice(39, 46, 1)
df_tc["Date"] = pd.to_datetime(df_tc["Date"], format="%Y-%m-%d")
df_tc = df_tc.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"technology": "first"}).reset_index()

df_ut = pd.merge(df_ut, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_ut = df_ut.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_ut = pd.melt(df_ut, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="utilities")
df_ut["Date"] = df_ut["Date"].str.slice(38, 45, 1)
df_ut["Date"] = pd.to_datetime(df_ut["Date"], format="%Y-%m-%d")
df_ut = df_ut.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"utilities": "first"}).reset_index()

industry_controls = [df_ut, df_in, df_bm, df_cc, df_re, df_tc, df_hc, df_cd, df_cs, df_fs, df_en]
df_ind = reduce(lambda left, right: pd.merge(left, right, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="inner"), industry_controls)

# fill nan values with most actual value
for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "basic_materials"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "basic_materials"] = df_ind.loc[c - 1, "basic_materials"]
    elif math.isnan(df_ind.loc[c, "basic_materials"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "basic_materials"] = df_ind.loc[c - 2, "basic_materials"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "communication_services"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "communication_services"] = df_ind.loc[c - 1, "communication_services"]
    elif math.isnan(df_ind.loc[c, "communication_services"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "communication_services"] = df_ind.loc[c - 2, "communication_services"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "consumer_cyclical"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "consumer_cyclical"] = df_ind.loc[c - 1, "consumer_cyclical"]
    elif math.isnan(df_ind.loc[c, "consumer_cyclical"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "consumer_cyclical"] = df_ind.loc[c - 2, "consumer_cyclical"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "energy"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "energy"] = df_ind.loc[c - 1, "energy"]
    elif math.isnan(df_ind.loc[c, "energy"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "energy"] = df_ind.loc[c - 2, "energy"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "consumer_defensive"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "consumer_defensive"] = df_ind.loc[c - 1, "consumer_defensive"]
    elif math.isnan(df_ind.loc[c, "consumer_defensive"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "consumer_defensive"] = df_ind.loc[c - 2, "consumer_defensive"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "financial_services"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "financial_services"] = df_ind.loc[c - 1, "financial_services"]
    elif math.isnan(df_ind.loc[c, "financial_services"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "financial_services"] = df_ind.loc[c - 2, "financial_services"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "healthcare"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "healthcare"] = df_ind.loc[c - 1, "healthcare"]
    elif math.isnan(df_ind.loc[c, "healthcare"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "healthcare"] = df_ind.loc[c - 2, "healthcare"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "industrials"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "industrials"] = df_ind.loc[c - 1, "industrials"]
    elif math.isnan(df_ind.loc[c, "industrials"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "industrials"] = df_ind.loc[c - 2, "industrials"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "real_estate"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "real_estate"] = df_ind.loc[c - 1, "real_estate"]
    elif math.isnan(df_ind.loc[c, "real_estate"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "real_estate"] = df_ind.loc[c - 2, "real_estate"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "technology"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "technology"] = df_ind.loc[c - 1, "technology"]
    elif math.isnan(df_ind.loc[c, "technology"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "technology"] = df_ind.loc[c - 2, "technology"]
    else:
        continue

for c in range(2, len(df_ind)):
    if math.isnan(df_ind.loc[c, "utilities"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 1, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 1, "Institutional"]:
        df_ind.loc[c, "utilities"] = df_ind.loc[c - 1, "utilities"]
    elif math.isnan(df_ind.loc[c, "utilities"]) == True and df_ind.loc[c, "FundId"] == df_ind.loc[c - 2, "FundId"] and df_ind.loc[c, "Institutional"] == df_ind.loc[c - 2, "Institutional"]:
        df_ind.loc[c, "utilities"] = df_ind.loc[c - 2, "utilities"]
    else:
        continue


################################
# Dividend
################################

df_div = pd.merge(df_div, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_div = df_div.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])

df_div = pd.melt(df_div, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="monthly_div")
df_div["Date"] = df_div["Date"].str.slice(17, 24, 1)
df_div["Date"] = pd.to_datetime(df_div["Date"], format="%Y-%m-%d")
df_div = df_div.groupby(["Fund Legal Name", "FundId", "Institutional", "Date"]).agg({"monthly_div": "sum"}).reset_index()

# solution for nan values
df_div["year"] = pd.to_datetime(df_div["Date"]).dt.to_period("Y")
df_div["monthly_div"] = df_div["monthly_div"].replace(0, np.nan)
df_div = df_div.dropna(axis=0, how="any", thresh=6)
df_div = df_div.drop(columns=["Date"])
df_div = df_div.groupby(["Fund Legal Name", "FundId", "Institutional", "year"]).agg({"monthly_div": "sum"}).reset_index()
df_div = df_div.rename(columns={"monthly_div": "yearly_div"})
df_div["weekly_div"] = df_div["yearly_div"] / 52
df_div = df_div.drop(columns=["yearly_div"])


################################
# Firm Name
################################

df_firm_name = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Firm Name"]].copy()
df_firm_name = df_firm_name.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"Firm Name": "first"}).reset_index()


################################
# Age
################################

# obtain age of fund taking 31.12.2020 as reference
df_age = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Inception Date"]].copy()
df_age["Inception Date"] = pd.to_datetime(df_age["Inception Date"], format= "%d.%m.%Y") # dtype
df_age["d_end"] = date(2020, 12, 31)
df_age["d_end"] = pd.to_datetime(df_age["d_end"], format="%Y-%m-%d") # dtype
df_age["Age"] = df_age["d_end"] - df_age["Inception Date"] # calculation
df_age["Age"] = df_age["Age"] / np.timedelta64(1, "Y") # convert to years
df_age = df_age.drop(columns=["Inception Date", "d_end"])

# aggregate Age from share class to fund level (oldest share class)
df_age_fundlevel = df_age.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"Age": "max"}).reset_index()


################################
# Other static controls
################################

df_static_control = df_static.drop(columns=["Global Broad Category Group", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Index Fund", "Inception Date", "Valuation Country"])
df_static_control = df_static_control.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"Global Category": "first"}).reset_index()


################################
# Star Rating
################################

# star rating
df_star = pd.melt(df_star, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_star")
df_star["Date"] = df_star["Date"].str.slice(15, 22, 1)
df_star["Date"] = pd.to_datetime(df_star["Date"], format="%Y-%m-%d")
df_star = df_star.fillna(6)
df_star_fundlevel = pd.merge(df_star, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_star_fundlevel = df_star_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_star": "min"}).reset_index()
df_star_fundlevel = df_star_fundlevel.replace(6, np.nan)


################################
# Fill nan values in weekly flows by calculation
################################

#df_flow_weekly_fundlevel = pd.merge(df_flow_weekly_fundlevel, df_return_weekly_fundlevel, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="left")
#df_flow_weekly_fundlevel = pd.merge(df_flow_weekly_fundlevel, df_tna_weekly_fundlevel, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="left")

#group = df_flow_weekly_fundlevel.groupby(["FundId", "Institutional"])
#df_flow_weekly_fundlevel["weekly_tna_fundlevel_lag1"] = group["weekly_tna_fundlevel"].shift(1)

#for f in range(0, len(df_flow_weekly_fundlevel)):
#    if (df_flow_weekly_fundlevel.loc[f, "weekly_flow"] == np.nan or df_flow_weekly_fundlevel.loc[f, "weekly_flow"] == 0) \
#            and math.isnan(df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel"]) == False \
#            and df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel"] != 0\
#            and math.isnan(df_flow_weekly_fundlevel.loc[f, "weekly_return_fundlevel"]) == False \
#            and df_flow_weekly_fundlevel.loc[f, "weekly_return_fundlevel"] != 0\
#            and math.isnan(df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel_lag1"]) == False \
#            and df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel_lag1"] != 0:
#        df_flow_weekly_fundlevel.loc[f, "weekly_flow"] = df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel"] - (1 + df_flow_weekly_fundlevel.loc[f, "weekly_return_fundlevel"]) * df_flow_weekly_fundlevel.loc[f, "weekly_tna_fundlevel_lag1"]
#    else:
#        continue

#df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(columns=["weekly_tna_fundlevel_lag1", "weekly_tna_fundlevel", "weekly_return_fundlevel"])


################################
# Past Returns
################################

# calculate prior month return using weekly return
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].add(1)
df_return_weekly["Date"] = df_return_weekly["Date"].astype("datetime64[ns]")
df_return_monthly = df_return_weekly.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("M", on="Date").prod().reset_index()
df_return_monthly = df_return_monthly.rename(columns={"weekly_return": "calc_monthly_return"})

group1 = df_return_monthly.groupby(["ISIN"])
df_return_monthly["calc_prior_month_return"] = group1["calc_monthly_return"].shift(1)

#df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["weekly_return_fundlevel"].add(1)
#df_return_weekly_fundlevel["Date"] = df_return_weekly_fundlevel["Date"].astype("datetime64[ns]")
#df_return_monthly_fundlevel = df_return_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Institutional"]).resample("M", on="Date").mean().reset_index()
#df_return_monthly_fundlevel = df_return_monthly_fundlevel.rename(columns={"weekly_return_fundlevel": "trans_monthly_return_fundlevel"})

#group1 = df_return_monthly_fundlevel.groupby(["FundId", "Institutional"])
#df_return_monthly_fundlevel["prior_month_return"] = group1["trans_monthly_return_fundlevel"].shift(1)

# calculate rolling 12 months return
df_return_monthly["calc_rolling_12_months_return"] = df_return_monthly.groupby(["ISIN"])["calc_monthly_return"].transform(lambda x: x.cumprod(12))

# obtain prior month's return from monthly return
group = df_m_return.groupby(["ISIN"])
df_m_return["prior_month_return"] = group["monthly_return"].shift(1)

# obtain 12 months rolling return from monthly return
df_m_return["monthly_return"] = df_m_return["monthly_return"].div(100)
df_m_return["monthly_return"] = df_m_return["monthly_return"].add(1)
df_m_return["rolling_12_months_return"] = df_m_return.groupby(["ISIN"])["monthly_return"].transform(lambda x: x.rolling(12).prod())

# return controls from share class to fundlevel
df_m_return["Date"] = df_m_return["Date"].astype("datetime64[ns]")
start = pd.to_datetime("2019-01-01", format="%Y-%m-%d")
end = pd.to_datetime("2020-12-31", format="%Y-%m-%d")
df_m_return = df_m_return[df_m_return["Date"].between(start, end)].reset_index()
df_m_return = df_m_return.drop(columns=["index"]) # setting time frame matched to return data

df_m_return = df_m_return.groupby(["ISIN"]).filter(lambda x: x["prior_month_return"].ne(np.nan).all())
df_m_return = df_m_return.groupby(["ISIN"]).filter(lambda x: x["rolling_12_months_return"].ne(np.nan).all())

df_m_return = pd.merge(df_m_return, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_m_return = df_m_return.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area",
                                    "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])
df_m_return_fundlevel = df_m_return.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).mean().reset_index()

# transfrom all formats to %
df_m_return["monthly_return"] = df_m_return["monthly_return"].sub(1)
df_m_return["monthly_return"] = df_m_return["monthly_return"].mul(100)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].mul(100)
df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["weekly_return_fundlevel"].mul(100)

df_return_monthly.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_return_monthly_fundlevel_test.csv")
df_m_return_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_m_return_fundlevel_test.csv")

#df_m_return["Date"] = df_m_return["Date"].astype("datetime64[ns]")
#df_m_return["month_year"] = pd.to_datetime(df_m_return["Date"]).dt.to_period("M")
#df_return_monthly_fundlevel["month_year"] = pd.to_datetime(df_return_monthly_fundlevel["Date"]).dt.to_period("M")
#df_return_monthly_fundlevel = pd.merge(df_return_monthly_fundlevel, df_m_return_fundlevel, on=["Fund Legal Name", "FundId", "Institutional", "month_year"])
#df_return_monthly_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_return_monthly_fundlevel_test.csv")

# back to decimal format
#df_return_monthly_fundlevel["rolling_12_months_return"] = df_return_monthly_fundlevel["rolling_12_months_return"].sub(1)
#df_return_monthly_fundlevel["prior_month_return"] = df_return_monthly_fundlevel["prior_month_return"].sub(1)
#df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["weekly_return_fundlevel"].sub(1)

# convert to % values
#df_return_monthly_fundlevel["rolling_12_months_return"] = df_return_monthly_fundlevel["rolling_12_months_return"].mul(100)
#df_return_monthly_fundlevel["prior_month_return"] = df_return_monthly_fundlevel["prior_month_return"].mul(100)
#df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["weekly_return_fundlevel"].mul(100)

# change date format for later merging
#df_return_monthly_fundlevel["month_year"] = pd.to_datetime(df_return_monthly_fundlevel["Date"]).dt.to_period("M")
#df_return_monthly_fundlevel = df_return_monthly_fundlevel.drop(columns=["Date"])
#df_return_monthly_fundlevel["Date"] = df_return_monthly_fundlevel["month_year"].astype("datetime64[ns]")
#df_return_monthly_fundlevel = df_return_monthly_fundlevel.drop(columns=["month_year"])


##############################################
# Fund Size
##############################################

# delete unnecessary columns and data
df_size = df_size.drop(columns=["Name"])
df_size = df_size.drop_duplicates(subset="FundId", keep="first")

# change column headers to date format
df_size = pd.melt(df_size, id_vars=["Fund Legal Name", "FundId"], var_name="Date", value_name="daily_size")
df_size["Date"] = df_size["Date"].str.slice(44, 54, 1)
df_size["Date"] = pd.to_datetime(df_size["Date"], format="%Y-%m-%d")

# aggregate from daily to weekly size data
df_size_weekly = df_size.groupby(["Fund Legal Name", "FundId"]).resample("W", on="Date").agg({"daily_size": "last"}).reset_index()
df_size_weekly = df_size_weekly.rename(columns={"daily_size": "weekly_size"})


##############################################
# Compare Fund Size and TNA
##############################################

# format change
df_tna_weekly_fundlevel["Date"] = df_tna_weekly_fundlevel["Date"].astype("datetime64[ns]")
# drop year 2016 from TNA dataframe
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.groupby(["FundId", "Institutional"]).filter(lambda x: (x["Date"] >= pd.to_datetime("2017-01-01", format="%Y-%m-%d")).all())
# merging
df_tna_weekly_fundlevel = pd.merge(df_tna_weekly_fundlevel, df_size_weekly, on=["Fund Legal Name", "FundId", "Date"], how="left")


# replace nan and zero values in tna by fund size under certain conditions
for k in range(1, len(df_tna_weekly_fundlevel) - 1):
    if (math.isnan(df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"]) == True or df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == 0) and (df_tna_weekly_fundlevel.loc[k, "Institutional"] == "Yes" and df_tna_weekly_fundlevel.loc[k, "Institutional"] != df_tna_weekly_fundlevel.loc[k - 1, "Institutional"] and df_tna_weekly_fundlevel.loc[k, "Date"] == df_tna_weekly_fundlevel.loc[k - 1, "Date"]) and df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == df_tna_weekly_fundlevel.loc[k + 1, "weekly_tna_fundlevel"]:
        continue
    elif (math.isnan(df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"]) == True or df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == 0) and (df_tna_weekly_fundlevel.loc[k, "Institutional"] == "No" and df_tna_weekly_fundlevel.loc[k, "Institutional"] != df_tna_weekly_fundlevel.loc[k + 1, "Institutional"] and df_tna_weekly_fundlevel.loc[k, "Date"] == df_tna_weekly_fundlevel.loc[k + 1, "Date"]) and df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == df_tna_weekly_fundlevel.loc[k + 1, "weekly_tna_fundlevel"]:
        continue
    elif (math.isnan(df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"]) == True or df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == 0) and (df_tna_weekly_fundlevel.loc[k, "Institutional"] == "Yes" and df_tna_weekly_fundlevel.loc[k, "Institutional"] != df_tna_weekly_fundlevel.loc[k - 1, "Institutional"] and df_tna_weekly_fundlevel.loc[k, "Date"] == df_tna_weekly_fundlevel.loc[k - 1, "Date"]) and df_tna_weekly_fundlevel.loc[k, "weekly_size"] >= df_tna_weekly_fundlevel.loc[k - 1, "weekly_tna_fundlevel"]:
        df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] = df_tna_weekly_fundlevel.loc[k, "weekly_size"] - df_tna_weekly_fundlevel.loc[k - 1, "weekly_tna_fundlevel"]
    elif (math.isnan(df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"]) == True or df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == 0) and (df_tna_weekly_fundlevel.loc[k, "Institutional"] == "No" and df_tna_weekly_fundlevel.loc[k, "Institutional"] != df_tna_weekly_fundlevel.loc[k + 1, "Institutional"] and df_tna_weekly_fundlevel.loc[k, "Date"] == df_tna_weekly_fundlevel.loc[k + 1, "Date"]) and df_tna_weekly_fundlevel.loc[k, "weekly_size"] >= df_tna_weekly_fundlevel.loc[k + 1, "weekly_tna_fundlevel"]:
        df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] = df_tna_weekly_fundlevel.loc[k, "weekly_size"] - df_tna_weekly_fundlevel.loc[k + 1, "weekly_tna_fundlevel"]
    elif (math.isnan(df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"]) == True or df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] == 0) and df_tna_weekly_fundlevel.loc[k, "Institutional"] == df_tna_weekly_fundlevel.loc[k - 1, "Institutional"]:
        df_tna_weekly_fundlevel.loc[k, "weekly_tna_fundlevel"] = df_tna_weekly_fundlevel.loc[k, "weekly_size"]
    else:
        continue


##############################################
# Retain those funds having at least one non-missing flow datapoint (AT THE END WHEN EVERYTHING IS MERGED !!!!)
##############################################

#df_flow_weekly_fundlevel["nan_indicator"] = df_flow_weekly_fundlevel.groupby(["FundId", "Institutional"])["weekly_flow"].transform(lambda x: x.head(210).sum())
#df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(df_flow_weekly_fundlevel[(df_flow_weekly_fundlevel.nan_indicator == 0)].index)
#df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(columns="nan_indicator")


##############################################
# Add restriction on at least $1m. fund size by previous week (Hartzmark and Sussman) (AT THE END WHEN EVERYTHING IS MERGED !!!!)
##############################################

#group = df_size_weekly.groupby(["FundId"])
#df_size_weekly["weekly_size_lag1"] = group["weekly_size"].shift(1)

#for f in range(0, len(df_size_weekly)):
#    if df_size_weekly.loc[f, "weekly_size_lag1"] < 1000000:
#        df_size_weekly.loc[f, "size_indicator"] = 1
#    else:
#        continue

#df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.drop(df_tna_weekly_fundlevel[(df_tna_weekly_fundlevel.weekly_tna_lag1 < 1000000)].index)
#df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.drop(columns="weekly_tna_lag1")


##############################################
# Calculate log of tna
##############################################

#print(df_tna_weekly_fundlevel)

#df_tna_weekly_fundlevel = df_tna_weekly_fundlevel["weekly_tna_fundlevel"].fillna(0)

for d in range(0, len(df_tna_weekly_fundlevel)):
    if df_tna_weekly_fundlevel.loc[d, "weekly_tna_fundlevel"] == 0 or math.isnan(df_tna_weekly_fundlevel.loc[d, "weekly_tna_fundlevel"]) == True:
        continue
    else:
        df_tna_weekly_fundlevel.loc[d, "log_tna"] = np.log(df_tna_weekly_fundlevel.loc[d, "weekly_tna_fundlevel"])


##############################################
# Sustainability Measures
##############################################

# change column headers to date format
df_sus = pd.melt(df_sus, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_sus")
df_sus["Date"] = df_sus["Date"].str.slice(35, 42, 1)
df_sus["Date"] = pd.to_datetime(df_sus["Date"], format="%Y-%m-%d")

df_env = pd.melt(df_env, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_env")
df_env["Date"] = df_env["Date"].str.slice(35, 42, 1)
df_env["Date"] = pd.to_datetime(df_env["Date"], format="%Y-%m-%d")

df_soc = pd.melt(df_soc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_soc")
df_soc["Date"] = df_soc["Date"].str.slice(28, 35, 1)
df_soc["Date"] = pd.to_datetime(df_soc["Date"], format="%Y-%m-%d")

df_gov = pd.melt(df_gov, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_gov")
df_gov["Date"] = df_gov["Date"].str.slice(32, 39, 1)
df_gov["Date"] = pd.to_datetime(df_gov["Date"], format="%Y-%m-%d")

df_car = pd.melt(df_car, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_car")
df_car["Date"] = df_car["Date"].str.slice(18, 25, 1)
df_car["Date"] = pd.to_datetime(df_car["Date"], format="%Y-%m-%d")

# translate string into numeric scores (5 = High, ... , 1 = Low)
df_sus_fundlevel = pd.merge(df_sus, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_sus_fundlevel = df_sus_fundlevel.drop(columns=["Name", "Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
for i in range(0, len(df_sus_fundlevel)):
    if df_sus_fundlevel.loc[i, "monthly_sus"] == "High":
        df_sus_fundlevel.loc[i, "monthly_sus"] = 5
    elif df_sus_fundlevel.loc[i, "monthly_sus"] == "Above Average":
        df_sus_fundlevel.loc[i, "monthly_sus"] = 4
    elif df_sus_fundlevel.loc[i, "monthly_sus"] == "Average":
        df_sus_fundlevel.loc[i, "monthly_sus"] = 3
    elif df_sus_fundlevel.loc[i, "monthly_sus"] == "Below Average":
        df_sus_fundlevel.loc[i, "monthly_sus"] = 2
    elif df_sus_fundlevel.loc[i, "monthly_sus"] == "Low":
        df_sus_fundlevel.loc[i, "monthly_sus"] = 1
    else:
        df_sus_fundlevel.loc[i, "monthly_sus"] = df_sus_fundlevel.loc[i, "monthly_sus"]
df_sus_fundlevel["monthly_sus"] = pd.to_numeric(df_sus_fundlevel["monthly_sus"])

# aggregate from share class to fundlevel (retaining minimum rating)
#df_sus_fundlevel = df_sus_fundlevel.drop(df_sus_fundlevel[(df_sus_fundlevel.Date < pd.to_datetime("08.01.2018"))].index) # no sus rating in dataframe before august 2018
df_sus_fundlevel = df_sus_fundlevel.fillna(6)
df_sus_fundlevel = df_sus_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_sus": "min"}).reset_index()
df_sus_fundlevel = df_sus_fundlevel.replace(6, np.nan)

df_env_fundlevel = pd.merge(df_env, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_env_fundlevel = df_env_fundlevel.drop(columns=["Name", "Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_env_fundlevel = df_env_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_env": "max"}).reset_index()

df_soc_fundlevel = pd.merge(df_soc, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_soc_fundlevel = df_soc_fundlevel.drop(columns=["Name", "Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_soc_fundlevel = df_soc_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_soc": "max"}).reset_index()

df_gov_fundlevel = pd.merge(df_gov, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_gov_fundlevel = df_gov_fundlevel.drop(columns=["Name", "Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_gov_fundlevel = df_gov_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_gov": "max"}).reset_index()

df_car_fundlevel = pd.merge(df_car, df_static, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_car_fundlevel = df_car_fundlevel.drop(columns=["Name", "Global Broad Category Group", "Global Category", "Investment Area", "Inception Date"])
df_car_fundlevel = df_car_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_car": "max"}).reset_index()


################################
# Fill NaN's in columns with most actual value
################################

# star rating
for c in range(2, len(df_star_fundlevel)):
    if math.isnan(df_star_fundlevel.loc[c, "monthly_star"]) == True and df_star_fundlevel.loc[c, "FundId"] == df_star_fundlevel.loc[c - 1, "FundId"] and df_star_fundlevel.loc[c, "Institutional"] == df_star_fundlevel.loc[c - 1, "Institutional"]:
        df_star_fundlevel.loc[c, "monthly_star"] = df_star_fundlevel.loc[c - 1, "monthly_star"]
    elif math.isnan(df_star_fundlevel.loc[c, "monthly_star"]) == True and df_star_fundlevel.loc[c, "FundId"] == df_star_fundlevel.loc[c - 2, "FundId"] and df_star_fundlevel.loc[c, "Institutional"] == df_star_fundlevel.loc[c - 2, "Institutional"]:
        df_star_fundlevel.loc[c, "monthly_star"] = df_star_fundlevel.loc[c - 2, "monthly_star"]
    else:
        continue

#for c in range(len(df_star_fundlevel) - 2, 0, -1):
#    if math.isnan(df_star_fundlevel.loc[c, "monthly_star"]) == True and df_star_fundlevel.loc[c, "FundId"] == df_star_fundlevel.loc[c + 1, "FundId"] and df_star_fundlevel.loc[c, "Institutional"] == df_star_fundlevel.loc[c + 1, "Institutional"]:
#        df_star_fundlevel.loc[c, "monthly_star"] = df_star_fundlevel.loc[c + 1, "monthly_star"]
#    elif math.isnan(df_star_fundlevel.loc[c, "monthly_star"]) == True and df_star_fundlevel.loc[c, "FundId"] == df_star_fundlevel.loc[c + 2, "FundId"] and df_star_fundlevel.loc[c, "Institutional"] == df_star_fundlevel.loc[c + 2, "Institutional"]:
#        df_star_fundlevel.loc[c, "monthly_star"] = df_star_fundlevel.loc[c + 2, "monthly_star"]
#    else:
#        continue

# carbon designation
for c in range(2, len(df_car_fundlevel)):
    if math.isnan(df_car_fundlevel.loc[c, "monthly_car"]) == True and df_car_fundlevel.loc[c, "FundId"] == df_car_fundlevel.loc[c - 1, "FundId"] and df_car_fundlevel.loc[c, "Institutional"] == df_car_fundlevel.loc[c - 1, "Institutional"]:
        df_car_fundlevel.loc[c, "monthly_car"] = df_car_fundlevel.loc[c - 1, "monthly_car"]
    elif math.isnan(df_car_fundlevel.loc[c, "monthly_car"]) == True and df_car_fundlevel.loc[c, "FundId"] == df_car_fundlevel.loc[c - 2, "FundId"] and df_car_fundlevel.loc[c, "Institutional"] == df_car_fundlevel.loc[c - 2, "Institutional"]:
        df_car_fundlevel.loc[c, "monthly_car"] = df_car_fundlevel.loc[c - 2, "monthly_car"]
    else:
        continue

#for c in range(len(df_car_fundlevel) - 2, 0, -1):
#    if math.isnan(df_car_fundlevel.loc[c, "monthly_car"]) == True and df_car_fundlevel.loc[c, "FundId"] == df_car_fundlevel.loc[c + 1, "FundId"] and df_car_fundlevel.loc[c, "Institutional"] == df_car_fundlevel.loc[c + 1, "Institutional"]:
#        df_car_fundlevel.loc[c, "monthly_car"] = df_car_fundlevel.loc[c + 1, "monthly_car"]
#    elif math.isnan(df_car_fundlevel.loc[c, "monthly_car"]) == True and df_car_fundlevel.loc[c, "FundId"] == df_car_fundlevel.loc[c + 2, "FundId"] and df_car_fundlevel.loc[c, "Institutional"] == df_car_fundlevel.loc[c + 2, "Institutional"]:
#        df_car_fundlevel.loc[c, "monthly_car"] = df_car_fundlevel.loc[c + 2, "monthly_car"]
#    else:
#        continue

# sustainability rating
for c in range(2, len(df_sus_fundlevel)):
    if math.isnan(df_sus_fundlevel.loc[c, "monthly_sus"]) == True and df_sus_fundlevel.loc[c, "FundId"] == df_sus_fundlevel.loc[c - 1, "FundId"] and df_sus_fundlevel.loc[c, "Institutional"] == df_sus_fundlevel.loc[c - 1, "Institutional"]:
        df_sus_fundlevel.loc[c, "monthly_sus"] = df_sus_fundlevel.loc[c - 1, "monthly_sus"]
    elif math.isnan(df_sus_fundlevel.loc[c, "monthly_sus"]) == True and df_sus_fundlevel.loc[c, "FundId"] == df_sus_fundlevel.loc[c - 2, "FundId"] and df_sus_fundlevel.loc[c, "Institutional"] == df_sus_fundlevel.loc[c - 2, "Institutional"]:
        df_sus_fundlevel.loc[c, "monthly_sus"] = df_sus_fundlevel.loc[c - 2, "monthly_sus"]
    else:
        continue

#for c in range(len(df_sus_fundlevel) - 2, 0, -1):
#    if math.isnan(df_sus_fundlevel.loc[c, "monthly_sus"]) == True and df_sus_fundlevel.loc[c, "FundId"] == df_sus_fundlevel.loc[c + 1, "FundId"] and df_sus_fundlevel.loc[c, "Institutional"] == df_sus_fundlevel.loc[c + 1, "Institutional"]:
#        df_sus_fundlevel.loc[c, "monthly_sus"] = df_sus_fundlevel.loc[c + 1, "monthly_sus"]
#    elif math.isnan(df_sus_fundlevel.loc[c, "monthly_sus"]) == True and df_sus_fundlevel.loc[c, "FundId"] == df_sus_fundlevel.loc[c + 2, "FundId"] and df_sus_fundlevel.loc[c, "Institutional"] == df_sus_fundlevel.loc[c + 2, "Institutional"]:
#        df_sus_fundlevel.loc[c, "monthly_sus"] = df_sus_fundlevel.loc[c + 2, "monthly_sus"]
#    else:
#       continue

# environmental risk score
for c in range(2, len(df_env_fundlevel)):
    if math.isnan(df_env_fundlevel.loc[c, "monthly_env"]) == True and df_env_fundlevel.loc[c, "FundId"] == df_env_fundlevel.loc[c - 1, "FundId"] and df_env_fundlevel.loc[c, "Institutional"] == df_env_fundlevel.loc[c - 1, "Institutional"]:
        df_env_fundlevel.loc[c, "monthly_env"] = df_env_fundlevel.loc[c - 1, "monthly_env"]
    elif math.isnan(df_env_fundlevel.loc[c, "monthly_env"]) == True and df_env_fundlevel.loc[c, "FundId"] == df_env_fundlevel.loc[c - 2, "FundId"] and df_env_fundlevel.loc[c, "Institutional"] == df_env_fundlevel.loc[c - 2, "Institutional"]:
        df_env_fundlevel.loc[c, "monthly_env"] = df_env_fundlevel.loc[c - 2, "monthly_env"]
    else:
        continue

#for c in range(len(df_env_fundlevel) - 2, 0, -1):
#    if math.isnan(df_env_fundlevel.loc[c, "monthly_env"]) == True and df_env_fundlevel.loc[c, "FundId"] == df_env_fundlevel.loc[c + 1, "FundId"] and df_env_fundlevel.loc[c, "Institutional"] == df_env_fundlevel.loc[c + 1, "Institutional"]:
#        df_env_fundlevel.loc[c, "monthly_env"] = df_env_fundlevel.loc[c + 1, "monthly_env"]
#    elif math.isnan(df_env_fundlevel.loc[c, "monthly_env"]) == True and df_env_fundlevel.loc[c, "FundId"] == df_env_fundlevel.loc[c + 2, "FundId"] and df_env_fundlevel.loc[c, "Institutional"] == df_env_fundlevel.loc[c + 2, "Institutional"]:
#        df_env_fundlevel.loc[c, "monthly_env"] = df_env_fundlevel.loc[c + 2, "monthly_env"]
#    else:
#        continue

# social risk score
for c in range(2, len(df_soc_fundlevel)):
    if math.isnan(df_soc_fundlevel.loc[c, "monthly_soc"]) == True and df_soc_fundlevel.loc[c, "FundId"] == df_soc_fundlevel.loc[c - 1, "FundId"] and df_soc_fundlevel.loc[c, "Institutional"] == df_soc_fundlevel.loc[c - 1, "Institutional"]:
        df_soc_fundlevel.loc[c, "monthly_soc"] = df_soc_fundlevel.loc[c - 1, "monthly_soc"]
    elif math.isnan(df_soc_fundlevel.loc[c, "monthly_soc"]) == True and df_soc_fundlevel.loc[c, "FundId"] == df_soc_fundlevel.loc[c - 2, "FundId"] and df_soc_fundlevel.loc[c, "Institutional"] == df_soc_fundlevel.loc[c - 2, "Institutional"]:
        df_soc_fundlevel.loc[c, "monthly_soc"] = df_soc_fundlevel.loc[c - 2, "monthly_soc"]
    else:
        continue

#for c in range(len(df_soc_fundlevel) - 2, 0, -1):
#    if math.isnan(df_soc_fundlevel.loc[c, "monthly_soc"]) == True and df_soc_fundlevel.loc[c, "FundId"] == df_soc_fundlevel.loc[c + 1, "FundId"] and df_soc_fundlevel.loc[c, "Institutional"] == df_soc_fundlevel.loc[c + 1, "Institutional"]:
#        df_soc_fundlevel.loc[c, "monthly_soc"] = df_soc_fundlevel.loc[c + 1, "monthly_soc"]
#    elif math.isnan(df_soc_fundlevel.loc[c, "monthly_soc"]) == True and df_soc_fundlevel.loc[c, "FundId"] == df_soc_fundlevel.loc[c + 2, "FundId"] and df_soc_fundlevel.loc[c, "Institutional"] == df_soc_fundlevel.loc[c + 2, "Institutional"]:
#        df_soc_fundlevel.loc[c, "monthly_soc"] = df_soc_fundlevel.loc[c + 2, "monthly_soc"]
#    else:
#        continue

# governance risk score
for c in range(2, len(df_gov_fundlevel)):
    if math.isnan(df_gov_fundlevel.loc[c, "monthly_gov"]) == True and df_gov_fundlevel.loc[c, "FundId"] == df_gov_fundlevel.loc[c - 1, "FundId"] and df_gov_fundlevel.loc[c, "Institutional"] == df_gov_fundlevel.loc[c - 1, "Institutional"]:
        df_gov_fundlevel.loc[c, "monthly_gov"] = df_gov_fundlevel.loc[c - 1, "monthly_gov"]
    elif math.isnan(df_gov_fundlevel.loc[c, "monthly_gov"]) == True and df_gov_fundlevel.loc[c, "FundId"] == df_gov_fundlevel.loc[c - 2, "FundId"] and df_gov_fundlevel.loc[c, "Institutional"] == df_gov_fundlevel.loc[c - 2, "Institutional"]:
        df_gov_fundlevel.loc[c, "monthly_gov"] = df_gov_fundlevel.loc[c - 2, "monthly_gov"]
    else:
        continue

#for c in range(len(df_gov_fundlevel) - 2, 0, -1):
#    if math.isnan(df_gov_fundlevel.loc[c, "monthly_gov"]) == True and df_gov_fundlevel.loc[c, "FundId"] == df_gov_fundlevel.loc[c + 1, "FundId"] and df_gov_fundlevel.loc[c, "Institutional"] == df_gov_fundlevel.loc[c + 1, "Institutional"]:
#        df_gov_fundlevel.loc[c, "monthly_gov"] = df_gov_fundlevel.loc[c + 1, "monthly_gov"]
#    elif math.isnan(df_gov_fundlevel.loc[c, "monthly_gov"]) == True and df_gov_fundlevel.loc[c, "FundId"] == df_gov_fundlevel.loc[c + 2, "FundId"] and df_gov_fundlevel.loc[c, "Institutional"] == df_gov_fundlevel.loc[c + 2, "Institutional"]:
#        df_gov_fundlevel.loc[c, "monthly_gov"] = df_gov_fundlevel.loc[c + 2, "monthly_gov"]
#    else:
#        continue


##############################################
# Merge datasets
##############################################
df_flow_weekly_fundlevel["Date"] = df_flow_weekly_fundlevel["Date"].astype("datetime64[ns]")
df_return_weekly_fundlevel["Date"] = df_return_weekly_fundlevel["Date"].astype("datetime64[ns]")

# list all dataframes
all_weekly_dataframes = [df_flow_weekly_fundlevel, df_return_weekly_fundlevel, df_tna_weekly_fundlevel]
all_monthly_dataframes = [df_sus_fundlevel, df_env_fundlevel, df_soc_fundlevel, df_gov_fundlevel, df_car_fundlevel, df_star_fundlevel, df_fixed, df_ind, df_return_monthly_fundlevel]
all_fixed_dataframes = [df_index_fund, df_firm_name, df_age_fundlevel, df_static_control]

# merge dataframes with respect to their timeframe
df_weekly_final = reduce(lambda left, right: pd.merge(left, right, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="outer"), all_weekly_dataframes)
df_monthly_final = reduce(lambda left, right: pd.merge(left, right, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="outer"), all_monthly_dataframes)
df_fixed_final = reduce(lambda left, right: pd.merge(left, right, on=["Fund Legal Name", "FundId", "Institutional"], how="outer"), all_fixed_dataframes)

# merge all
df_weekly_final["month_year"] = pd.to_datetime(df_weekly_final["Date"]).dt.to_period("M")
df_weekly_final["year"] = pd.to_datetime(df_weekly_final["Date"]).dt.to_period("Y")
df_monthly_final["month_year"] = pd.to_datetime(df_monthly_final["Date"]).dt.to_period("M")
df_monthly_final = df_monthly_final.drop(columns=["Date"])

df_weekly_final = pd.merge(df_weekly_final, df_exp, on=["Fund Legal Name", "FundId", "year", "Institutional"], how="left")
df_weekly_final = pd.merge(df_weekly_final, df_div, on=["Fund Legal Name", "FundId", "year", "Institutional"], how="left")
df_final = pd.merge(df_weekly_final, df_monthly_final, on=["Fund Legal Name", "FundId", "month_year", "Institutional"], how="left")
df_final = pd.merge(df_final, df_fixed_final, on=["Fund Legal Name", "FundId", "Institutional"], how="left")
df_final = pd.merge(df_final, df_eff_weekly, on=["Date"], how="left")

# store in csv
df_weekly_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_weekly_final.csv")
df_monthly_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_monthly_final.csv")
df_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\final_dataframes\\df_final.csv")

# number of funds in dataset before overall trimming
print(df_final["FundId"].nunique())
# 1119


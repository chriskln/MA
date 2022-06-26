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
df_exp = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\expense_ratio.csv", sep= ";")
df_tur = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\turnover.csv", sep= ";")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\sustainability_rating.csv", sep= ";")
df_env = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\environmental_risk_score.csv", sep= ";")
df_soc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\social_risk_score.csv", sep= ";")
df_gov = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\governance_risk_score.csv", sep= ";")
df_car = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\carbon_risk_score.csv", sep= ";")
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\static_var.csv", sep= ";")
df_static_add = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\controls_add.csv", sep= ";")
df_star = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\star_rating.csv", sep= ";")
df_div = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\dividend.csv", sep= ";")
df_eff = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\Europe_5_Factors_Daily.csv", sep= ",")
df_static = pd.merge(df_static, df_static_add, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")

# investment style exposures
df_large_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\large_growth.csv", sep= ";")
df_large_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\large_value.csv", sep= ";")
df_large_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\large_core.csv", sep= ";")
df_mid_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\mid_growth.csv", sep= ";")
df_mid_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\mid_value.csv", sep= ";")
df_mid_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\mid_core.csv", sep= ";")
df_small_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\small_growth.csv", sep= ";")
df_small_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\small_value.csv", sep= ";")
df_small_core = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\small_core.csv", sep= ";")
df_growth = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\growth.csv", sep= ";")
df_value = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\value.csv", sep= ";")
df_mid = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\midcap.csv", sep= ";")
df_small = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\smallcap.csv", sep= ";")
df_large = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\largecap.csv", sep= ";")

# industry controls
df_bm = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\basicmaterials.csv", sep= ";")
df_cs = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\communicationservices.csv", sep= ";")
df_cc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\consumercyclical.csv", sep= ";")
df_en = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\energy.csv", sep= ";")
df_cd = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\consumerdefensive.csv", sep= ";")
df_fs = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\financialservices.csv", sep= ";")
df_hc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\healthcare.csv", sep= ";")
df_in = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\industrials.csv", sep= ";")
df_re = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\realestate.csv", sep= ";")
df_tc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\technology.csv", sep= ";")
df_ut = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\data_raw\\utilities.csv", sep= ";")

# delete unnamed columns
df_flow_weekly = df_flow_weekly.loc[:, ~df_flow_weekly.columns.str.contains("^Unnamed")]
df_return_weekly = df_return_weekly.loc[:, ~df_return_weekly.columns.str.contains("^Unnamed")]
df_tna_weekly = df_tna_weekly.loc[:, ~df_tna_weekly.columns.str.contains("^Unnamed")]
df_m_return = df_m_return.loc[:, ~df_m_return.columns.str.contains("^Unnamed")]

##############################################
# Controls
##############################################

################################
# Industry Controls
################################

df_bm = pd.melt(df_bm, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="basic_materials")
df_bm["Date"] = df_bm["Date"].str.slice(44, 51, 1)
df_bm["Date"] = pd.to_datetime(df_bm["Date"], format="%Y-%m-%d")

df_cs = pd.melt(df_cs, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="communication_services")
df_cs["Date"] = df_cs["Date"].str.slice(51, 58, 1)
df_cs["Date"] = pd.to_datetime(df_cs["Date"], format="%Y-%m-%d")

df_cc = pd.melt(df_cc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="consumer_cyclical")
df_cc["Date"] = df_cc["Date"].str.slice(46, 53, 1)
df_cc["Date"] = pd.to_datetime(df_cc["Date"], format="%Y-%m-%d")

df_en = pd.melt(df_en, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="energy")
df_en["Date"] = df_en["Date"].str.slice(35, 42, 1)
df_en["Date"] = pd.to_datetime(df_en["Date"], format="%Y-%m-%d")

df_cd = pd.melt(df_cd, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="consumer_defensive")
df_cd["Date"] = df_cd["Date"].str.slice(47, 54, 1)
df_cd["Date"] = pd.to_datetime(df_cd["Date"], format="%Y-%m-%d")

df_fs = pd.melt(df_fs, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="financial_services")
df_fs["Date"] = df_fs["Date"].str.slice(47, 54, 1)
df_fs["Date"] = pd.to_datetime(df_fs["Date"], format="%Y-%m-%d")

df_hc = pd.melt(df_hc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="healthcare")
df_hc["Date"] = df_hc["Date"].str.slice(39, 46, 1)
df_hc["Date"] = pd.to_datetime(df_hc["Date"], format="%Y-%m-%d")

df_in = pd.melt(df_in, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="industrials")
df_in["Date"] = df_in["Date"].str.slice(40, 47, 1)
df_in["Date"] = pd.to_datetime(df_in["Date"], format="%Y-%m-%d")

df_re = pd.melt(df_re, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="real_estate")
df_re["Date"] = df_re["Date"].str.slice(40, 47, 1)
df_re["Date"] = pd.to_datetime(df_re["Date"], format="%Y-%m-%d")

df_tc = pd.melt(df_tc, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="technology")
df_tc["Date"] = df_tc["Date"].str.slice(39, 46, 1)
df_tc["Date"] = pd.to_datetime(df_tc["Date"], format="%Y-%m-%d")

df_ut = pd.melt(df_ut, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="utilities")
df_ut["Date"] = df_ut["Date"].str.slice(38, 45, 1)
df_ut["Date"] = pd.to_datetime(df_ut["Date"], format="%Y-%m-%d")

industry_controls = [df_ut, df_in, df_bm, df_cc, df_re, df_tc, df_hc, df_cd, df_cs, df_fs, df_en]
df_ind = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="inner"), industry_controls)

# forward fill values from the past into future
df_ind["basic_materials"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["basic_materials"].transform(lambda x: x.ffill())
df_ind["communication_services"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["communication_services"].transform(lambda x: x.ffill())
df_ind["consumer_cyclical"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["consumer_cyclical"].transform(lambda x: x.ffill())
df_ind["energy"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["energy"].transform(lambda x: x.ffill())
df_ind["consumer_defensive"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["consumer_defensive"].transform(lambda x: x.ffill())
df_ind["financial_services"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["financial_services"].transform(lambda x: x.ffill())
df_ind["healthcare"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["healthcare"].transform(lambda x: x.ffill())
df_ind["industrials"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["industrials"].transform(lambda x: x.ffill())
df_ind["real_estate"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["real_estate"].transform(lambda x: x.ffill())
df_ind["technology"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["technology"].transform(lambda x: x.ffill())
df_ind["utilities"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["utilities"].transform(lambda x: x.ffill())

# backward fill future values into past
#df_ind["basic_materials"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["basic_materials"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["communication_services"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["communication_services"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["consumer_cyclical"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["consumer_cyclical"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["energy"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["energy"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["consumer_defensive"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["consumer_defensive"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["financial_services"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["financial_services"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["healthcare"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["healthcare"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["industrials"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["industrials"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["real_estate"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["real_estate"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["technology"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["technology"].transform(lambda x: x.fillna(method="bfill"))
#df_ind["utilities"] = df_ind.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["utilities"].transform(lambda x: x.fillna(method="bfill"))


################################
# Investment Style Exposure
################################

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

df_growth = pd.melt(df_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="growth")
df_growth["Date"] = df_growth["Date"].str.slice(29, 36, 1)
df_growth["Date"] = pd.to_datetime(df_growth["Date"], format="%Y-%m-%d")

df_value = pd.melt(df_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="value")
df_value["Date"] = df_value["Date"].str.slice(28, 35, 1)
df_value["Date"] = pd.to_datetime(df_value["Date"], format="%Y-%m-%d")

df_small = pd.melt(df_small, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small")
df_small["Date"] = df_small["Date"].str.slice(32, 39, 1)
df_small["Date"] = pd.to_datetime(df_small["Date"], format="%Y-%m-%d")

df_mid = pd.melt(df_mid, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="mid")
df_mid["Date"] = df_mid["Date"].str.slice(30, 37, 1)
df_mid["Date"] = pd.to_datetime(df_mid["Date"], format="%Y-%m-%d")

df_large = pd.melt(df_large, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="large")
df_large["Date"] = df_large["Date"].str.slice(32, 39, 1)
df_large["Date"] = pd.to_datetime(df_large["Date"], format="%Y-%m-%d")

df_small_core = pd.melt(df_small_core, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_core")
df_small_core["Date"] = df_small_core["Date"].str.slice(33, 40, 1)
df_small_core["Date"] = pd.to_datetime(df_small_core["Date"], format="%Y-%m-%d")

df_small_value = pd.melt(df_small_value, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_value")
df_small_value["Date"] = df_small_value["Date"].str.slice(34, 41, 1)
df_small_value["Date"] = pd.to_datetime(df_small_value["Date"], format="%Y-%m-%d")

df_small_growth = pd.melt(df_small_growth, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="small_growth")
df_small_growth["Date"] = df_small_growth["Date"].str.slice(35, 42, 1)
df_small_growth["Date"] = pd.to_datetime(df_small_growth["Date"], format="%Y-%m-%d")

inv_style_exp = [df_large, df_mid, df_small, df_growth, df_value, df_large_growth, df_large_value, df_mid_growth,
                 df_mid_value, df_small_growth, df_small_value, df_large_core, df_small_core, df_mid_core]
df_fixed = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="outer"), inv_style_exp)

# forward fill values from the past into future
df_fixed["large_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_growth"].transform(lambda x: x.ffill())
df_fixed["large_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_value"].transform(lambda x: x.ffill())
df_fixed["large_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_core"].transform(lambda x: x.ffill())
df_fixed["mid_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_growth"].transform(lambda x: x.ffill())
df_fixed["mid_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_value"].transform(lambda x: x.ffill())
df_fixed["mid_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_core"].transform(lambda x: x.ffill())
df_fixed["small_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_growth"].transform(lambda x: x.ffill())
df_fixed["small_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_value"].transform(lambda x: x.ffill())
df_fixed["small_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_core"].transform(lambda x: x.ffill())
df_fixed["growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["growth"].transform(lambda x: x.ffill())
df_fixed["value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["value"].transform(lambda x: x.ffill())
df_fixed["small"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small"].transform(lambda x: x.ffill())
df_fixed["large"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large"].transform(lambda x: x.ffill())
df_fixed["mid"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid"].transform(lambda x: x.ffill())

# backward fill future values into past
#df_fixed["large_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_growth"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["large_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_value"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["large_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large_core"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["mid_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_growth"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["mid_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_value"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["mid_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid_core"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["small_growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_growth"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["small_value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_value"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["small_core"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small_core"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["growth"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["growth"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["value"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["value"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["small"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["small"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["mid"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["mid"].transform(lambda x: x.fillna(method="bfill"))
#df_fixed["large"] = df_fixed.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["large"].transform(lambda x: x.fillna(method="bfill"))


################################
# Past Returns
################################

# prior week's return
groupgroup = df_return_weekly.groupby(["ISIN"])
df_return_weekly["prior_week_return"] = groupgroup["weekly_return"].shift(1)

# prior month return
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].add(1)
df_return_weekly["Date"] = df_return_weekly["Date"].astype("datetime64[ns]")
df_return_monthly = df_return_weekly.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]).resample("M", on="Date").prod().reset_index()
df_return_monthly = df_return_monthly.rename(columns={"weekly_return": "monthly_return_calc"})
df_return_monthly = df_return_monthly.drop(columns=["prior_week_return"])

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
df_return_weekly["prior_week_return"] = df_return_weekly["prior_week_return"].sub(1)

# convert to % values
df_return_monthly["rolling_12_months_return"] = df_return_monthly["rolling_12_months_return"].mul(100)
df_return_monthly["rolling_12_months_return_backup"] = df_return_monthly["rolling_12_months_return_backup"].mul(100)
df_return_monthly["monthly_return_calc"] = df_return_monthly["monthly_return_calc"].mul(100)
df_return_monthly["monthly_return"] = df_return_monthly["monthly_return"].mul(100)
df_return_monthly["prior_month_return"] = df_return_monthly["prior_month_return"].mul(100)
df_return_monthly["prior_month_return_backup"] = df_return_monthly["prior_month_return_backup"].mul(100)
df_return_weekly["weekly_return"] = df_return_weekly["weekly_return"].mul(100)
df_return_weekly["prior_week_return"] = df_return_weekly["prior_week_return"].mul(100)

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
# Calculate log of total net assets
################################

for d in range(0, len(df_tna_weekly)):
    if df_tna_weekly.loc[d, "weekly_tna"] == 0 or math.isnan(df_tna_weekly.loc[d, "weekly_tna"]) == True:
        continue
    else:
        df_tna_weekly.loc[d, "log_tna"] = np.log(df_tna_weekly.loc[d, "weekly_tna"])


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
# Fund Annual Expenses
################################

df_exp = pd.melt(df_exp, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="yearly_expense")
df_exp["Date"] = df_exp["Date"].str.slice(36, 40, 1)
df_exp["Date"] = pd.to_datetime(df_exp["Date"], format="%Y-%m-%d")
df_exp["year"] = pd.to_datetime(df_exp["Date"]).dt.to_period("Y")

# obtain weekly expense
df_exp["weekly_expense"] = df_exp["yearly_expense"] / 52
df_exp = df_exp.drop(columns=["Date", "yearly_expense"])

# forward fill values from the past into future
df_exp["weekly_expense"] = df_exp.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["weekly_expense"].transform(lambda x: x.ffill())

# backward fill future values into past
#df_exp["weekly_expense"] = df_exp.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["weekly_expense"].transform(lambda x: x.fillna(method="bfill"))


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

df_index_fund = df_index_fund.drop(columns=["name_check", "Index Fund"])


################################
# Dividend
################################

df_div = pd.melt(df_div, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_div")
df_div["Date"] = df_div["Date"].str.slice(17, 24, 1)
df_div["Date"] = pd.to_datetime(df_div["Date"], format="%Y-%m-%d")

# solution for nan values
df_div["year"] = pd.to_datetime(df_div["Date"]).dt.to_period("Y")
df_div["monthly_div"] = df_div["monthly_div"].replace(0, np.nan)
df_div = df_div.dropna(axis=0, how="any", thresh=5)
df_div = df_div.drop(columns=["Date"])
df_div = df_div.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "year"]).agg({"monthly_div": "sum"}).reset_index()
df_div = df_div.rename(columns={"monthly_div": "yearly_div"})
df_div["weekly_div"] = df_div["yearly_div"] / 52
df_div = df_div.drop(columns=["yearly_div"])


################################
# Firm Name
################################

df_firm_name = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Firm Name"]].copy()


################################
# Age
################################

# obtain age of fund taking 23/08/2020 as reference
df_age = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Inception Date"]].copy()
df_age["Inception Date"] = pd.to_datetime(df_age["Inception Date"], format= "%d.%m.%Y") # dtype
df_age["d_end"] = date(2020, 1, 1)
df_age["d_end"] = pd.to_datetime(df_age["d_end"], format="%Y-%m-%d") # dtype
df_age["Age"] = df_age["d_end"] - df_age["Inception Date"] # calculation
df_age["Age"] = df_age["Age"] / np.timedelta64(1, "Y") # convert to years
df_age = df_age.drop(columns=["Inception Date", "d_end"])


################################
# Other static controls
################################

df_static_control = df_static.drop(columns=["Global Broad Category Group", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Index Fund", "Inception Date", "Valuation Country"])


################################
# Star Rating
################################

# star rating
df_star = pd.melt(df_star, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], var_name="Date", value_name="monthly_star")
df_star["Date"] = df_star["Date"].str.slice(15, 22, 1)
df_star["Date"] = pd.to_datetime(df_star["Date"], format="%Y-%m-%d")

# forward fill values from the past into future
df_star["monthly_star"] = df_star.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_star"].transform(lambda x: x.ffill())

# backward fill future values into the past
#df_star["monthly_star"] = df_star.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_star"].transform(lambda x: x.fillna(method="bfill"))


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
for i in range(0, len(df_sus)):
    if df_sus.loc[i, "monthly_sus"] == "High":
        df_sus.loc[i, "monthly_sus"] = 5
    elif df_sus.loc[i, "monthly_sus"] == "Above Average":
        df_sus.loc[i, "monthly_sus"] = 4
    elif df_sus.loc[i, "monthly_sus"] == "Average":
        df_sus.loc[i, "monthly_sus"] = 3
    elif df_sus.loc[i, "monthly_sus"] == "Below Average":
        df_sus.loc[i, "monthly_sus"] = 2
    elif df_sus.loc[i, "monthly_sus"] == "Low":
        df_sus.loc[i, "monthly_sus"] = 1
    else:
        df_sus.loc[i, "monthly_sus"] = df_sus.loc[i, "monthly_sus"]
df_sus["monthly_sus"] = pd.to_numeric(df_sus["monthly_sus"])

# forward fill values from the past into future
df_sus["monthly_sus"] = df_sus.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_sus"].transform(lambda x: x.ffill())
df_car["monthly_car"] = df_car.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_car"].transform(lambda x: x.ffill())
df_env["monthly_env"] = df_env.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_env"].transform(lambda x: x.ffill())
df_soc["monthly_soc"] = df_soc.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_soc"].transform(lambda x: x.ffill())
df_gov["monthly_gov"] = df_gov.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_gov"].transform(lambda x: x.ffill())

# backward fill future values into past
#df_sus["monthly_sus"] = df_sus.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_sus"].transform(lambda x: x.fillna(method="bfill"))
#df_car["monthly_car"] = df_car.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_car"].transform(lambda x: x.fillna(method="bfill"))
#df_env["monthly_env"] = df_env.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_env"].transform(lambda x: x.fillna(method="bfill"))
#df_soc["monthly_soc"] = df_soc.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_soc"].transform(lambda x: x.fillna(method="bfill"))
#df_gov["monthly_gov"] = df_gov.groupby(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"])["monthly_gov"].transform(lambda x: x.fillna(method="bfill"))


##############################################
# Merge
##############################################

df_sus["Date"] = pd.to_datetime(df_sus["Date"]).dt.to_period("M")
df_env["Date"] = pd.to_datetime(df_env["Date"]).dt.to_period("M")
df_soc["Date"] = pd.to_datetime(df_soc["Date"]).dt.to_period("M")
df_gov["Date"] = pd.to_datetime(df_gov["Date"]).dt.to_period("M")
df_car["Date"] = pd.to_datetime(df_car["Date"]).dt.to_period("M")
df_star["Date"] = pd.to_datetime(df_star["Date"]).dt.to_period("M")
df_fixed["Date"] = pd.to_datetime(df_fixed["Date"]).dt.to_period("M")
df_ind["Date"] = pd.to_datetime(df_ind["Date"]).dt.to_period("M")

df_flow_weekly["Date"] = df_flow_weekly["Date"].astype("datetime64[ns]")
df_return_weekly["Date"] = df_return_weekly["Date"].astype("datetime64[ns]")
df_tna_weekly["Date"] = df_tna_weekly["Date"].astype("datetime64[ns]")

all_weekly_dataframes = [df_flow_weekly, df_return_weekly, df_tna_weekly]
all_monthly_dataframes = [df_sus, df_env, df_soc, df_gov, df_car, df_star, df_fixed, df_ind, df_return_monthly]
all_fixed_dataframes = [df_index_fund, df_firm_name, df_age, df_static_control]

df_weekly_final = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="outer"), all_weekly_dataframes)
df_monthly_final = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Date"], how="outer"), all_monthly_dataframes)
df_fixed_final = reduce(lambda left, right: pd.merge(left, right, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="outer"), all_fixed_dataframes)

# merge all
df_weekly_final["month_year"] = pd.to_datetime(df_weekly_final["Date"]).dt.to_period("M")
df_monthly_final = df_monthly_final.rename(columns={"Date": "month_year"})
df_weekly_final["year"] = pd.to_datetime(df_weekly_final["Date"]).dt.to_period("Y")

df_weekly_final = pd.merge(df_weekly_final, df_div, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "year"], how="left")
df_weekly_final = pd.merge(df_weekly_final, df_exp, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "year"], how="left")
df_final = pd.merge(df_weekly_final, df_monthly_final, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "month_year"], how="left")
df_final = pd.merge(df_final, df_fixed_final, on=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"], how="left")
df_final = pd.merge(df_final, df_eff_weekly, on=["Date"], how="left")

# store all final dataframes in csv files
df_weekly_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_weekly_final.csv")
df_monthly_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_monthly_final.csv")
df_final.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes_prep_2\\df_final.csv")

# number of ISIN's in dataset before overall trimming
print(df_final["ISIN"].nunique())
# 5317
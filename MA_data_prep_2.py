##############################################
# MASTER THESIS
##############################################

##############################################
# Data Preparation
##############################################

import numpy as np
import pandas as pd
from sklearn import preprocessing
from datetime import date
from scipy.stats.mstats import winsorize

##############################################
# Loading Data
##############################################

df_flow_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_flow_weekly_fundlevel.csv", sep= ",")
df_return_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_return_weekly_fundlevel.csv", sep= ",")
df_tna_weekly_fundlevel = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dataframes\\df_tna_weekly_fundlevel.csv", sep= ",")
df_sus = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\sus_rating_abs.csv", sep= ";")
df_env = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_env_score.csv", sep= ";")
df_soc = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_soc_score.csv", sep= ";")
df_gov = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\por_gov_score.csv", sep= ";")
df_car = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\car_risk_score.csv", sep= ";")
df_static = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\static_var.csv", sep= ";")
df_static_add = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\controls_add.csv", sep= ";")
df_star = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\star_rating.csv", sep= ";")
df_div = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\dividend.csv", sep= ";")

df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.loc[:, ~df_flow_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_return_weekly_fundlevel = df_return_weekly_fundlevel.loc[:, ~df_return_weekly_fundlevel.columns.str.contains("^Unnamed")]
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.loc[:, ~df_tna_weekly_fundlevel.columns.str.contains("^Unnamed")]


##############################################
# Controls
##############################################

################################
# Index Fund Check
################################

# index fund indicator
df_static = pd.merge(df_static, df_static_add, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_index_fund = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Index Fund"]].copy()
df_index_fund["name_check"] = df_index_fund["Name"].str.contains("Index", na=False)

for f in range(0, len(df_index_fund)):
    if df_index_fund.loc[f, "name_check"] == True or df_index_fund.loc[f, "Index Fund"] == "Yes":
        df_index_fund.loc[f, "index_indicator"] = 1
    else:
        df_index_fund.loc[f, "index_indicator"] = 0

df_index_fund = df_index_fund.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"index_indicator": "max"}).reset_index()


################################
# Dividend
################################

df_div = pd.merge(df_div, df_static, on=(["Name", "Fund Legal Name", "FundId", "SecId", "ISIN"]), how="left")
df_div = df_div.drop(columns=["Global Broad Category Group", "Global Category", "Investment Area", "Country Available for Sale", "Manager History", "Manager Name", "Firm Name", "Inception Date", "Index Fund", "Valuation Country"])

df_div = pd.melt(df_div, id_vars=["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional"], var_name="Date", value_name="monthly_div")
df_div["Date"] = df_div["Date"].str.slice(17, 24, 1)
df_div["Date"] = pd.to_datetime(df_div["Date"], format="%Y-%m-%d")
df_div = df_div.groupby(["Fund Legal Name", "FundId", "Institutional", "Date"]).agg({"monthly_div": "sum"}).reset_index()


################################
# Firm Name
################################

df_firm_name = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Firm Name"]].copy()
df_firm_name = df_firm_name.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"Firm Name": "first"}).reset_index()


################################
# Age
################################

# aggregate inception date from share class to fund level (minimum value)
df_age = df_static[["Name", "Fund Legal Name", "FundId", "SecId", "ISIN", "Institutional", "Inception Date"]].copy()
df_age_fundlevel = df_age.groupby(["Fund Legal Name", "FundId", "Institutional"]).agg({"Inception Date": "min"}).reset_index()

# obtain age of fund taking 31.12.2020 as reference
df_age_fundlevel["Inception Date"] = pd.to_datetime(df_age_fundlevel["Inception Date"], format= "%d.%m.%Y") # dtype
df_age_fundlevel["d_end"] = date(2020, 12, 31)
df_age_fundlevel["d_end"] = pd.to_datetime(df_age_fundlevel["d_end"], format="%Y-%m-%d") # dtype
df_age_fundlevel["Age"] = df_age_fundlevel["d_end"] - df_age_fundlevel["Inception Date"] # calculation
df_age_fundlevel["Age"] = df_age_fundlevel["Age"] / np.timedelta64(1, "Y") # convert to years


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
# Past Returns
################################

# prior month return
df_return_weekly_fundlevel["weekly_return_fundlevel"] = df_return_weekly_fundlevel["weekly_return_fundlevel"].add(1)
df_return_weekly_fundlevel["Date"] = df_return_weekly_fundlevel["Date"].astype("datetime64[ns]")
df_return_monthly_fundlevel = df_return_weekly_fundlevel.groupby(["Fund Legal Name", "FundId", "Institutional"]).resample("M", on="Date").mean().reset_index()
df_return_monthly_fundlevel = df_return_monthly_fundlevel.rename(columns={"weekly_return_fundlevel": "monthly_return_fundlevel"})

group1 = df_return_monthly_fundlevel.groupby(["FundId", "Institutional"])
df_return_monthly_fundlevel["prior_month_return"] = group1["monthly_return_fundlevel"].shift(1)

# rolling 12 months return
df_return_monthly_fundlevel["rolling_12_months_return"] = df_return_monthly_fundlevel.groupby(["FundId", "Institutional"])["monthly_return_fundlevel"].transform(lambda x: x.rolling(12).mean())


##############################################
# Retain those funds having at least one non-missing flow datapoint
##############################################

df_flow_weekly_fundlevel["nan_indicator"] = df_flow_weekly_fundlevel.groupby(["FundId", "Institutional"])["weekly_flow"].transform(lambda x: x.head(210).sum())
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(df_flow_weekly_fundlevel[(df_flow_weekly_fundlevel.nan_indicator == 0)].index)
df_flow_weekly_fundlevel = df_flow_weekly_fundlevel.drop(columns="nan_indicator")


##############################################
# Add restriction on at least $1m. tna by previous week (Hartzmark and Sussman)
##############################################

group = df_tna_weekly_fundlevel.groupby(["FundId", "Institutional"])
df_tna_weekly_fundlevel["weekly_tna_lag1"] = group["weekly_tna_fundlevel"].shift(1)

df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.drop(df_tna_weekly_fundlevel[(df_tna_weekly_fundlevel.weekly_tna_lag1 < 1000000)].index)
df_tna_weekly_fundlevel = df_tna_weekly_fundlevel.drop(columns="weekly_tna_lag1")


##############################################
# Calculate log of tna
##############################################

df_tna_weekly_fundlevel["log_tna"] = np.log(df_tna_weekly_fundlevel["weekly_tna_fundlevel"])


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
df_sus_fundlevel = df_sus_fundlevel.drop(df_sus_fundlevel[(df_sus_fundlevel.Date < pd.to_datetime("08.01.2018"))].index) # no sus rating in dataframe before august 2018
df_sus_fundlevel = df_sus_fundlevel.fillna(6)
df_sus_fundlevel = df_sus_fundlevel.groupby(["Fund Legal Name", "FundId", "Date", "Institutional"]).agg({"monthly_sus": "min"}).reset_index()
df_sus_fundlevel = df_sus_fundlevel.replace(6, np.nan)


##############################################
# Merge datasets
##############################################

df_final = pd.merge(df_flow_weekly_fundlevel, df_tna_weekly_fundlevel, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="inner")
#print(df_final)

# number of funds in dataset
#print(df_final["FundId"].nunique())

##############################################
# Calculate flow variables
##############################################

df_flow_weekly_fundlevel = pd.merge(df_flow_weekly_fundlevel, df_tna_weekly_fundlevel, on=["Fund Legal Name", "FundId", "Date", "Institutional"], how="left")

# 1: fund flows (See Hartzmark and Sussma, p. 2798)
group = df_flow_weekly_fundlevel.groupby(["FundId", "Institutional"])
df_flow_weekly_fundlevel["weekly_tna_fundlevel_lag1"] = group["weekly_tna_fundlevel"].shift(1)
df_flow_weekly_fundlevel["fund_flows"] = df_flow_weekly_fundlevel["weekly_flow"] / df_flow_weekly_fundlevel["weekly_tna_fundlevel_lag1"]

# 2: normalized flows (See Hartzmark and Sussma, p. 2798)
df_flow_weekly_fundlevel["Decile_Rank"] = df_flow_weekly_fundlevel.groupby("Date").weekly_tna_fundlevel.apply(lambda x: pd.qcut(x, 10, duplicates="drop", labels=False))
df_flow_weekly_fundlevel["normalized_flows"] = df_flow_weekly_fundlevel.groupby("Decile_Rank").weekly_flow.apply(lambda x: pd.qcut(x, 100, duplicates="drop", labels=False))

#print(df_flow_weekly_fundlevel.iloc[:, -3:])
#df_flow_weekly_fundlevel.to_csv(r"C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv_2\\df_flow_weekly_fundlevel.csv")



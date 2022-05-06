##############################################
# MASTER THESIS
##############################################

##############################################
# Modules & Functions
##############################################

import csv
import numpy as np
import pandas as pd

##############################################
# Loading Data
##############################################


df_flow = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv\\dailyflow012019_012021.csv", sep = ";")
df_return = pd.read_csv("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv\\dailyreturn012019_012021.csv", sep = ";")


##############################################
# Code
##############################################

# control
# print(df_flow.head)
# print(df_return.head)

# delete all funds with no flow data
df_flow = df_flow.dropna(axis="index", how= "all", thresh=3)
df_return = df_return.dropna(axis="index", how= "all", thresh=3)

# delete all days with no flow data (closed stock market)
df_flow = df_flow.dropna(axis="columns", how= "all")
df_return = df_return.dropna (axis="columns", how="all")

print(df_return)
print(df_flow)



#for line in df_flow:
#    data = line.strip().split(";")
#    data = [x.replace("Estimated Share Class Net Flow (Daily) ", "") for x in data]
#    data = [x.replace(" Base Currency", "") for x in data]
#    print(df_flow)
#with open("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv\\dailyflow012019_012021.csv") as f:








import csv
from datetime import date, datetime, timedelta

with open("C:\\Users\\klein\\OneDrive\\Dokumente\\Master Thesis\\csv\\dailyflow012019_012021.csv") as f:
    for line in f:
        data = line.strip().split(";")
        data = [x.replace("Estimated Share Class Net Flow (Daily) ", "") for x in data]
        data = [x.replace(" Base Currency", "") for x in data]








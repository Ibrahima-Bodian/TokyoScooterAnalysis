import pandas as pd


cal=pd.read_csv("calendrier.csv", sep=";")
meteo=pd.read_csv("meteo.csv", sep=";")
loc=pd.read_csv("locations.csv", sep=";", header=0)

cal["Date"]=cal["Date_Hour"].astype(str).str[:10]

meteo["Date"]=meteo["Date"].astype(str).str[:10]

loc["Date"]=loc["Date"].astype(str).str[:10]

merged=pd.merge(meteo, cal, on="Date", how="outer", suffixes=("_meteo", "_cal"))
merged=pd.merge(merged, loc, on="Date", how="outer")

# 4. Export du résultat
merged.to_csv("fusion.csv", index=False)

print("Fusion terminée. Le fichier 'fusion.csv' a été créé.")

import pandas as pd

# 1. Lecture des fichiers
# Remplacez les chemins par le chemin réel de vos fichiers.
# On suppose que calendrier.csv et meteo.csv utilisent le séparateur ";" et qu'ils ont un en-tête.
cal = pd.read_csv("calendrier.csv", sep=";")
meteo = pd.read_csv("meteo.csv", sep=";")
# Pour locations.csv, d'après votre exemple, il semble n'avoir qu'une seule colonne "Date" contenant des timestamps.
loc = pd.read_csv("locations.csv", sep=";", header=0)

# 2. Extraction de la clé "Date"
# Pour calendrier.csv, on crée la colonne "Date" à partir de "Date_Hour"
cal["Date"] = cal["Date_Hour"].astype(str).str[:10]

# Pour meteo.csv, nous utilisons (ou extrayons) la colonne "Date" déjà présente
meteo["Date"] = meteo["Date"].astype(str).str[:10]

# Pour locations.csv, on extrait la partie "YYYY-MM-DD" du timestamp
loc["Date"] = loc["Date"].astype(str).str[:10]

# 3. Fusion des données par la clé "Date"
# La jointure externe (outer join) permet de conserver toutes les dates
merged = pd.merge(meteo, cal, on="Date", how="outer", suffixes=("_meteo", "_cal"))
merged = pd.merge(merged, loc, on="Date", how="outer")

# 4. Export du résultat
merged.to_csv("unified.csv", index=False)

print("Fusion terminée. Le fichier 'unified.csv' a été créé.")

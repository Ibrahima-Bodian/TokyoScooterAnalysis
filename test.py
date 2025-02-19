import requests
import re
from collections import defaultdict

# --- Configuration de la requête ---
port = 8080  # Choisissez le port approprié (ici 8080)
data_id = 1
gp_id = "B_30cf3d7d"

# Définissez la plage de dates souhaitée
start_date = "2017-12-01"
end_date = "2017-12-03"

# On construit l'URL en utilisant les paramètres start_date et end_date
url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}&start_date={start_date}&end_date={end_date}"
print("Requête URL :", url)

response = requests.get(url)
print("Statut :", response.status_code)

if response.status_code != 200:
    print("Erreur lors de la récupération des données.")
    exit(1)

# --- Sauvegarde de la réponse brute ---
data_text = response.text
with open("all_data.csv", "w", encoding="utf-8") as f:
    f.write(data_text)
print("Les données brutes ont été enregistrées dans all_data.csv.")

# --- Traitement des données ---

# 1. Séparation des timestamps par date
# On considère que les lignes contenant un timestamp ISO sont du type "YYYY-MM-DDTHH:MM:SS.sssZ"
pattern_iso = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$')

# Dictionnaire : clé = date (YYYY-MM-DD), valeur = liste de timestamps
times_data = defaultdict(list)

lines = data_text.splitlines()
for line in lines:
    line = line.strip()
    if pattern_iso.match(line):
        date_part = line[:10]  # extraction des 10 premiers caractères (YYYY-MM-DD)
        times_data[date_part].append(line)

# Sauvegarder les timestamps dans des fichiers séparés par date
for date, timestamps in times_data.items():
    filename = f"times_{date}.csv"
    with open(filename, "w", encoding="utf-8") as f:
        for ts in timestamps:
            f.write(ts + "\n")
    print(f"Données de timestamps pour le {date} enregistrées dans {filename}")

# 2. Extraction du bloc météo et du bloc calendrier (si présents)
# On se base sur l'en-tête pour détecter ces blocs.
weather_lines = []
calendar_lines = []
in_weather = False
in_calendar = False

for line in lines:
    stripped_line = line.strip()
    
    # Détection de l'en-tête du bloc météo
    if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
        in_weather = True
        in_calendar = False
        weather_lines.append(stripped_line)
        continue
    # Détection de l'en-tête du bloc calendrier
    if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
        in_calendar = True
        in_weather = False
        calendar_lines.append(stripped_line)
        continue
    
    # Fin du bloc si ligne vide ou début d'un nouveau bloc
    if stripped_line == "":
        in_weather = False
        in_calendar = False
        continue
    
    if in_weather:
        weather_lines.append(stripped_line)
    elif in_calendar:
        calendar_lines.append(stripped_line)

# Sauvegarder le bloc météo
if weather_lines:
    with open("weather.csv", "w", encoding="utf-8") as f:
        for line in weather_lines:
            f.write(line + "\n")
    print("Les données météo ont été enregistrées dans weather.csv.")
else:
    print("Aucune donnée météo trouvée.")

# Sauvegarder le bloc calendrier
if calendar_lines:
    with open("calendar.csv", "w", encoding="utf-8") as f:
        for line in calendar_lines:
            f.write(line + "\n")
    print("Les données calendrier ont été enregistrées dans calendar.csv.")
else:
    print("Aucune donnée calendrier trouvée.")

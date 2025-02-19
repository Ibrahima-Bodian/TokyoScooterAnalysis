import requests
import time

# Configuration de base
ports = [8080, 8090, 8100]
gp_id = "B_30cf3d7d"

# Listes globales pour stocker les données récupérées
times_data = []    # Contiendra des timestamps (ex. "2017-12-01T00:00:19" après nettoyage)
weather_data = []  # Contiendra des lignes du type "Date\tTemperature\tHumidity\tWind.speed\tVisibility\tDew.point.temperature"
location_data = [] # Contiendra des lignes du type "Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"

weather_header = None

# Boucle sur data_id sans limite fixe : on arrête lorsque 100 data_id consécutifs ne renvoient aucune donnée
data_id = 1
no_data_count = 0
threshold = 100

while no_data_count < threshold:
    data_found = False
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            continue

        data_found = True
        lines = response.text.splitlines()
        mode = None

        for line in lines:
            stripped_line = line.strip()
            
            # Détection du bloc weather
            if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
                if weather_header is None:
                    weather_header = stripped_line
                    weather_data.append(weather_header)
                mode = "weather"
                continue
            
            # Détection du bloc location (calendrier)
            # On se base sur le début de la ligne et la présence de "Seasons"
            if stripped_line.startswith("Date_Hour") and "Seasons" in stripped_line:
                if not location_data:
                    location_data.append(stripped_line)
                mode = "location"
                continue
            
            # Détection du bloc times
            if stripped_line.startswith("Date :"):
                if not times_data:
                    times_data.append(stripped_line)
                mode = "times"
                continue
            
            # Ajout des données selon le mode courant
            if mode == "times" and stripped_line.endswith(".000Z") and not stripped_line.startswith("Date :"):
                # Supprime le suffixe ".000Z"
                cleaned_line = stripped_line.replace(".000Z", "")
                times_data.append(cleaned_line)
            elif mode == "weather":
                if stripped_line == weather_header:
                    continue
                weather_data.append(stripped_line)
            elif mode == "location":
                location_data.append(stripped_line)
            else:
                pass

    if data_found:
        no_data_count = 0
    else:
        no_data_count += 1
    data_id += 1

# --- Fusion dans un seul fichier CSV unifié ---
# En-tête unique :
# Timestamp,Temperature,Humidity,Wind.speed,Visibility,Dew.point.temperature,Seasons,Holiday,Functioning.Day
unified_header = "Timestamp,Temperature,Humidity,Wind.speed,Visibility,Dew.point.temperature,Seasons,Holiday,Functioning.Day"
unified_rows = [unified_header]

# Traitement des données weather
# La première ligne de weather_data est l'en-tête et sera ignorée pour les lignes de données
for i, row in enumerate(weather_data):
    if i == 0:
        continue
    parts = row.split("\t")
    if len(parts) >= 6:
        # Pour weather, on remplit les 6 premières colonnes et on laisse vides les 3 dernières
        new_row = f"{parts[0].strip()},{parts[1].strip()},{parts[2].strip()},{parts[3].strip()},{parts[4].strip()},{parts[5].strip()},,,"
        unified_rows.append(new_row)

# Traitement des données times
# On ignore l'en-tête ("Date : ...") et on insère le timestamp dans la colonne Timestamp
for row in times_data:
    if row.startswith("Date :"):
        continue
    new_row = f"{row.strip()},,,,,,,,"
    unified_rows.append(new_row)

# Traitement des données location
# On ignore l'en-tête ("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day")
# Pour location, on supprime la deuxième colonne (Date) et on conserve :
# Date_Hour (pour Timestamp), Seasons, Holiday, Functioning.Day
for row in location_data:
    if row.startswith("Date_Hour"):
        continue
    parts = row.split("\t")
    if len(parts) >= 5:
        new_row = f"{parts[0].strip()},,,,,{parts[2].strip()},{parts[3].strip()},{parts[4].strip()}"
        unified_rows.append(new_row)

# Écriture dans le fichier CSV unifié
with open("unified.csv", "w", encoding="utf-8") as f:
    for row in unified_rows:
        f.write(row + "\n")

print("Extraction et fusion terminées !")

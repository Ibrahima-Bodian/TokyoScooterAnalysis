import requests
import os

ports = [8080, 8090, 8100]
gp_id = "B_30cf3d7d"

# 1) Lire les fichiers existants et stocker les lignes déjà présentes dans un set
times_known = set()
weather_known = set()
location_known = set()

# Si les fichiers existent déjà, on lit leur contenu
if os.path.exists("times.csv"):
    with open("times.csv", "r", encoding="utf-8") as f:
        for line in f:
            times_known.add(line.rstrip("\n"))

if os.path.exists("weather.csv"):
    with open("weather.csv", "r", encoding="utf-8") as f:
        for line in f:
            weather_known.add(line.rstrip("\n"))

if os.path.exists("location.csv"):
    with open("location.csv", "r", encoding="utf-8") as f:
        for line in f:
            location_known.add(line.rstrip("\n"))

# 2) Préparer des listes pour les nouvelles données à ajouter
new_times = []
new_weather = []
new_location = []

weather_header = None

data_id = 1
no_data_count = 0
threshold = 100  # On s'arrête après 100 data_id consécutifs sans données

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

            # Bloc weather
            if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
                if weather_header is None:
                    weather_header = stripped_line
                    # On ajoute l'en-tête seulement si on ne l'a pas déjà
                    if weather_header not in weather_known:
                        new_weather.append(weather_header)
                        weather_known.add(weather_header)
                mode = "weather"
                continue

            # Bloc location
            if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                # Ajout de l'en-tête si on ne l'a pas déjà
                if stripped_line not in location_known:
                    new_location.append(stripped_line)
                    location_known.add(stripped_line)
                mode = "location"
                continue

            # Bloc times
            if stripped_line.startswith("Date :"):
                if stripped_line not in times_known:
                    new_times.append(stripped_line)
                    times_known.add(stripped_line)
                mode = "times"
                continue

            # Ajout selon le mode
            if mode == "times" and stripped_line.endswith(".000Z") and not stripped_line.startswith("Date :"):
                if stripped_line not in times_known:
                    new_times.append(stripped_line)
                    times_known.add(stripped_line)
            elif mode == "weather":
                if stripped_line != weather_header and stripped_line not in weather_known:
                    new_weather.append(stripped_line)
                    weather_known.add(stripped_line)
            elif mode == "location":
                if stripped_line not in location_known:
                    new_location.append(stripped_line)
                    location_known.add(stripped_line)
            else:
                pass

    if data_found:
        no_data_count = 0
    else:
        no_data_count += 1
    data_id += 1

# 3) Écriture des *nouvelles* lignes en mode append
# On n'efface pas les anciennes, on ajoute juste celles qu'on n'avait pas
if new_times:
    with open("times.csv", "a", encoding="utf-8") as f:
        for t in new_times:
            f.write(t + "\n")

if new_weather:
    with open("weather.csv", "a", encoding="utf-8") as f:
        for w in new_weather:
            f.write(w + "\n")

if new_location:
    with open("location.csv", "a", encoding="utf-8") as f:
        for c in new_location:
            f.write(c + "\n")

print("Extraction terminée (ajout uniquement des nouvelles lignes).")

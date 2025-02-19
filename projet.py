"""import requests

ports = [8080]
data_id = 3
gp_id = "B_30cf3d7d"

for port in ports:
    url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
    response = requests.get(url)  # HTTP

    print(f"Port {port} -> status code : {response.status_code}")
    # Afficher la réponse brute pour voir ce qui est effectivement renvoyé
    print("Contenu de la réponse :")
    print(response.text)  # Ceci vous montrera exactement ce que vous recevez

"""
import requests

# Configuration de base
ports = [8080, 8090, 8100]
gp_id = "B_30cf3d7d"

# Listes globales pour stocker les données récupérées
times_data = []
weather_data = []
calendar_data = []

# Pour stocker l'en-tête weather lors de la première occurrence
weather_header = None

# Boucle sur data_id sans limite fixe, on arrête lorsque l'on rencontre 100 data_id consécutifs sans données
data_id = 1
no_data_count = 0
threshold = 100  # Nombre de data_id consécutifs sans données pour arrêter la boucle

while no_data_count < threshold:
    data_found = False
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            continue

        # On considère que l'ID a donné des données si au moins une requête retourne 200
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

            # Détection du bloc calendar
            if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                if not calendar_data:
                    calendar_data.append(stripped_line)
                mode = "calendar"
                continue

            # Détection du bloc times
            if stripped_line.startswith("Date :"):
                if not times_data:
                    times_data.append(stripped_line)
                mode = "times"
                continue

            # Ajout des données selon le mode courant
            if mode == "times" and stripped_line.endswith(".000Z") and not stripped_line.startswith("Date :"):
                times_data.append(stripped_line)
            elif mode == "weather":
                if stripped_line == weather_header:
                    continue
                weather_data.append(stripped_line)
            elif mode == "calendar":
                calendar_data.append(stripped_line)
            else:
                pass

    if data_found:
        no_data_count = 0
    else:
        no_data_count += 1
    data_id += 1

# Écriture dans des fichiers séparés
with open("times.csv", "w", encoding="utf-8") as f:
    for t in times_data:
        f.write(t + "\n")

with open("weather.csv", "w", encoding="utf-8") as f:
    for w in weather_data:
        f.write(w + "\n")

with open("calendar.csv", "w", encoding="utf-8") as f:
    for c in calendar_data:
        f.write(c + "\n")

print("Extraction terminée !")

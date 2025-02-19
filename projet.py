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
# Plage de data_id à tester (à adapter selon votre contexte)
data_ids = range(1, 909)
gp_id = "B_30cf3d7d"

# Listes globales pour stocker les données récupérées
times_data = []
weather_data = []
calendar_data = []

for data_id in data_ids:
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            # On passe au port suivant s'il n'y a pas de 200
            continue

        # Récupération du texte et séparation en lignes
        lines = response.text.splitlines()

        # Variable pour suivre le bloc courant (weather, calendar, times)
        mode = None

        for line in lines:
            stripped_line = line.strip()
            
            # Bloc "weather" : on détecte l'en-tête attendu
            if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
                mode = "weather"
                weather_data.append(stripped_line)
                continue
            
            # Bloc "calendar" : on détecte l'en-tête attendu
            if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                mode = "calendar"
                calendar_data.append(stripped_line)
                continue
            
            # Bloc "times" : si la ligne commence par "Date :" ou se termine par ".000Z"
            if stripped_line.startswith("Date :") or stripped_line.endswith(".000Z"):
                mode = "times"
                times_data.append(stripped_line)
                continue
            
            # Selon le mode courant, on ajoute la ligne dans la liste correspondante
            if mode == "weather":
                weather_data.append(stripped_line)
            elif mode == "calendar":
                calendar_data.append(stripped_line)
            elif mode == "times":
                times_data.append(stripped_line)
            else:
                # Ligne non classée (on peut choisir de l'ignorer ou la traiter différemment)
                pass

# --- Écriture des données récupérées dans des fichiers séparés ---
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

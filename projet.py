"""import requests

ports = [8080]
data_id = 3
gp_id = "B_30cf3d7d"

for port in ports:
    url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
    response = requests.get(url)  # HTTP, sans verify=False
    print(f"Port {port} -> status code : {response.status_code}")

    #les données en JSON peutetre
    data=response.json()
    print("Données :", data)
"""

import requests

# Définition de nos ports, data_id, gp_id
ports = [8080, 8090, 8100]
data_id = 1
gp_id = "B_30cf3d7d"

# Listes globales pour stocker les données de tous les ports
times_data = []
weather_data = []
calendar_data = []

for port in ports:
    url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
    response = requests.get(url)
    
    print(f"Port {port} -> status code : {response.status_code}")
    if response.status_code != 200:
        # On passe au port suivant s'il n'y a pas de 200
        continue
    
    # Récupération du texte et séparation en lignes
    lines = response.text.splitlines()
    
    # Petite variable pour suivre le bloc courant
    mode = None
    
    for line in lines:
        # Nettoyage d'éventuels espaces
        stripped_line = line.strip()
        
        # --- DÉTECTER LES EN-TÊTES ---
        # Ajuster ces conditions selon la forme réelle de vos en-têtes / lignes.
        
        # 1) Bloc "weather"
        # Exemple d'en-tête : "Date	Temperature	Humidity	Wind.speed"
        if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
            mode = "weather"
            # On ajoute l'en-tête dans weather_data
            weather_data.append(stripped_line)
            # On passe à la ligne suivante
            continue
        
        # 2) Bloc "calendar"
        # Exemple d'en-tête : "Date_Hour	Date	Seasons	Holiday	Functioning.Day"
        if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
            mode = "calendar"
            calendar_data.append(stripped_line)
            continue
        
        # 3) Bloc "times"
        # Si la ligne commence par "Date :" ou si elle se termine par ".000Z"
        if stripped_line.startswith("Date :") or stripped_line.endswith(".000Z"):
            mode = "times"
            times_data.append(stripped_line)
            continue
        
        # --- SUIVI DU MODE EN COURS ---
        if mode == "weather":
            weather_data.append(stripped_line)
        elif mode == "calendar":
            calendar_data.append(stripped_line)
        elif mode == "times":
            times_data.append(stripped_line)
        else:
            # On peut ignorer ou afficher les lignes non classées
            pass

# --- À la fin des boucles, on écrit tout dans des fichiers séparés ---
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

import requests
import time

ports = [8080, 8100]  # Ports pour locations et calendrier
gp_id = "B_30cf3d7d"

# Initialisation des listes avec l'en-tête souhaité
locations_data = ["Date"]
calendrier_data = ["Date_Hour;Seasons;Holiday;Functioning.Day"]

# On démarre avec data_id = 1 et on continue tant que nous obtenons des données
data_id = 1
consecutive_no_data = 0
threshold = 10  # Si 10 data_id consécutifs ne renvoient aucune donnée, on considère que c'est fini

while consecutive_no_data < threshold:
    data_found = False
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        # Pour éviter les erreurs 429
        time.sleep(0.030)
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            continue

        data_found = True
        lines = response.text.splitlines()
        for line in lines:
            stripped_line = line.strip()
            # Pour le port 8100 (calendrier)
            if port == 8100:
                # On s'attend à une ligne d'en-tête "Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"
                # On ne récupère que les données (en supprimant la colonne "Date", qui est la 2ème)
                if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                    # Ajout de l'en-tête déjà effectuée au départ, on l'ignore ici
                    continue
                parts = stripped_line.split("\t")
                if len(parts) >= 5:
                    # Conserver uniquement Date_Hour, Seasons, Holiday, Functioning.Day
                    new_line = ";".join([parts[0].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip()])
                    calendrier_data.append(new_line)
            # Pour le port 8080 (locations)
            elif port == 8080:
                # On ignore l'en-tête "Date :" et on récupère uniquement les lignes de données
                if stripped_line.startswith("Date :"):
                    continue
                locations_data.append(stripped_line)
    if data_found:
        consecutive_no_data = 0
    else:
        consecutive_no_data += 1
    data_id += 1

# Boucle pour récupérer les données météo sur le port 8090
meteo_data = ["Date;Temperature;Humidity;Wind.speed;Visibility;Dew.point.temperature"]
data_id = 1
consecutive_no_data = 0
while consecutive_no_data < threshold:
    url = f"http://172.22.215.130:8090/?id={data_id}&token={gp_id}"
    time.sleep(0.030)
    response = requests.get(url)
    print(f"Data ID {data_id} sur port 8090 -> status code : {response.status_code}")
    if response.status_code != 200:
        consecutive_no_data += 1
        data_id += 1
        continue

    consecutive_no_data = 0
    lines = response.text.splitlines()
    for line in lines:
        stripped_line = line.strip()
        # On ignore l'en-tête "Date\tTemperature\tHumidity\tWind.speed" si présent
        if stripped_line.startswith("Date\tTemperature\tHumidity\tWind.speed"):
            continue
        # Remplacer les tabulations par des points-virgules pour correspondre à l'en-tête
        meteo_data.append(stripped_line.replace("\t", ";"))
    data_id += 1

# Écriture dans les fichiers CSV
with open("locations.csv", "w", encoding="utf-8") as f:
    for l in locations_data:
        f.write(l + "\n")

with open("calendrier.csv", "w", encoding="utf-8") as f:
    for c in calendrier_data:
        f.write(c + "\n")

with open("meteo.csv", "w", encoding="utf-8") as f:
    for m in meteo_data:
        f.write(m + "\n")

print("Extraction terminée !")

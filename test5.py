import requests
import time

ports = [8080, 8100]  # Ports pour locations et calendrier
meteo_port = 8090  # Port pour météo
gp_id = "B_30cf3d7d"

# Initialisation des listes avec l'en-tête souhaité
locations_data = ["Date"]
calendrier_data = ["Date_Hour;Seasons;Holiday;Functioning.Day"]
meteo_data = []  # On ne met pas l'en-tête ici pour l'instant

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
            # Traitement des données pour les ports de calendrier et locations
            if port == 8100 and not stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                parts = stripped_line.split("\t")
                new_line = ";".join([parts[0], parts[2], parts[3], parts[4]])
                calendrier_data.append(new_line)
            elif port == 8080 and not stripped_line.startswith("Date :"):
                locations_data.append(stripped_line)

    if data_found:
        consecutive_no_data = 0
    else:
        consecutive_no_data += 1
    data_id += 1

# Traitement spécifique pour les données météo
meteo_header_detected = False
data_id = 1
consecutive_no_data = 0
while consecutive_no_data < threshold:
    url = f"http://172.22.215.130:{meteo_port}/?id={data_id}&token={gp_id}"
    time.sleep(0.030)
    response = requests.get(url)
    print(f"Data ID {data_id} on port {meteo_port} -> status code : {response.status_code}")
    if response.status_code != 200:
        consecutive_no_data += 1
        data_id += 1
        continue

    consecutive_no_data = 0
    lines = response.text.splitlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("Date_Hour") and not meteo_header_detected:
            meteo_data.append(stripped_line.replace("\t", ";"))  # Ajouter l'en-tête une seule fois
            meteo_header_detected = True
        elif not stripped_line.startswith("Date_Hour"):
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

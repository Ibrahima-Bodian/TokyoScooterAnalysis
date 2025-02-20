import requests
import time

ports = [8080, 8100]  # Ports pour locations et calendrier
meteo_port = 8090     # Port pour météo
gp_id = "B_30cf3d7d"

# Initialisation des listes avec l'en-tête souhaité
locations_data = ["Date"]
calendrier_data = ["Date_Hour;Seasons;Holiday;Functioning.Day"]
meteo_data = []  # L'en-tête sera ajoutée une seule fois

# On démarre avec data_id = 1 et on continue tant que nous obtenons des données
data_id = 1
consecutive_no_data = 0
threshold = 10  # Si 10 data_id consécutifs ne renvoient aucune donnée, on considère que c'est fini

while consecutive_no_data < threshold:
    data_found = False
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        time.sleep(0.030)
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            continue

        data_found = True
        lines = response.text.splitlines()
        for line in lines:
            stripped_line = line.strip()
            if port == 8100:
                # Pour le port calendrier, on ignore l'en-tête et on conserve uniquement Date_Hour, Seasons, Holiday, Functioning.Day
                if stripped_line.startswith("Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"):
                    continue
                parts = stripped_line.split("\t")
                if len(parts) >= 5:
                    new_line = ";".join([parts[0].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip()])
                    calendrier_data.append(new_line)
                else:
                    print(f"Ligne ignorée sur port 8100 pour data_id {data_id} (colonnes insuffisantes): {stripped_line}")
            elif port == 8080:
                # Pour le port locations, on ignore la ligne d'en-tête "Date :"
                if stripped_line.startswith("Date :"):
                    continue
                locations_data.append(stripped_line)
    if data_found:
        consecutive_no_data = 0
    else:
        consecutive_no_data += 1
    data_id += 1

#########################################
# Traitement spécifique pour les données météo sur le port 8090
#########################################

meteo_header_detected = False
data_id = 1
consecutive_no_data = 0

while consecutive_no_data < threshold:
    url = f"http://172.22.215.130:{meteo_port}/?id={data_id}&token={gp_id}"
    time.sleep(0.030)
    response = requests.get(url)
    print(f"Data ID {data_id} sur port {meteo_port} -> status code : {response.status_code}")
    if response.status_code != 200:
        consecutive_no_data += 1
        data_id += 1
        continue

    consecutive_no_data = 0
    lines = response.text.splitlines()
    for line in lines:
        stripped_line = line.strip()
        # Si la ligne commence par "Date_Hour", on la considère comme en-tête de meteo
        if stripped_line.startswith("Date_Hour"):
            if meteo_header_detected:
                continue  # On ignore les en-têtes répétés
            else:
                meteo_data.append(stripped_line.replace("\t", ";"))
                meteo_header_detected = True
                continue
        # Ajouter les lignes de données en remplaçant les tabulations par des points-virgules
        meteo_data.append(stripped_line.replace("\t", ";"))
    data_id += 1

#########################################
# Écriture dans les fichiers CSV
#########################################

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

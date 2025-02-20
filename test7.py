import requests
import time

ports = [8080,8100]

x=1
y=5

data_ids = range(x,y)
gp_id = "B_30cf3d7d"

#structure des données pour chaque port
met_line="Date_Hour\tDate\tHour\tTemperature\tHumidity\tWind_speed\tVisibility\tDew_point_temperature\tSolar_Radiation\tRainfall\tSnowfall"

cal_line="Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"

loc_struc="Date"
loc_line="Date :"

locations_data = [loc_line]
meteo_data = [met_line]
calendrier_data = [cal_line]

for data_id in data_ids:
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        #pour éviter les erreurs 429
        time.sleep(0.030)
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            # On passe au port suivant s'il n'y a pas de 200
            continue
            
                # Récupération du texte et séparation en lignes
        lines = response.text.splitlines()

        for line in lines:
            stripped_line = line.strip()
            
            # 2) Bloc "calendrier"
            # en-tête : "Date_Hour	Date	Seasons	Holiday	Functioning.Day"
            if port==8100 and not stripped_line.startswith(cal_line):
                calendrier_data.append(stripped_line.replace("NA",""))
                continue
            
            # 3) Bloc "locations"
            if port==8080 and not stripped_line.startswith(loc_line):
                locations_data.append(stripped_line.replace("NA",""))
                continue
 
                

if x!=1:
	x=(x-1)*24+1
	
if y!=1:
	y=(y-1)*24+1

data_ids = range(x,y)

for data_id in data_ids:
	url = f"http://172.22.215.130:8090/?id={data_id}&token={gp_id}"
	time.sleep(0.030)
	response = requests.get(url)
	print(f"Data ID {data_id} sur port 8090 -> status code : {response.status_code}")
	if response.status_code != 200:
		# On passe au port suivant s'il n'y a pas de 200
		continue

	# Récupération du texte et séparation en lignes
	lines = response.text.splitlines()

	for line in lines:
		stripped_line = line.strip()
		
		# 1) Bloc "meteo"
		# en-tête : "Date	Temperature	Humidity	Wind.speed"
		if not stripped_line.startswith(met_line):
			meteo_data.append(stripped_line.replace("NA",""))
			continue
		


# --- Écriture des données récupérées dans des fichiers séparés ---
with open("locations.csv", "w", encoding="utf-8") as f:
    for l in locations_data:
        f.write(l + "\n")

with open("meteo.csv", "w", encoding="utf-8") as f:
    for m in meteo_data:
        f.write(m + "\n")

with open("calendrier.csv", "w", encoding="utf-8") as f:
    for c in calendrier_data:
        f.write(c + "\n")

print("Extraction terminée !")


import requests
import time

ports = [8080,8090]

#Informations affichées :
print ("Système d'extraction de données métérologiques et de location de scooters de Tokyo.\n version comp.20-02-2025\n")

#Demande à l'opérateur d'intégrer l'intervalle des jours exportés :
x=input("Id de départ d'extraction (1 = 01/12/2017) : ")
y=input("Id de fin d'extraction (min = Id départ) : ")
#x-> premier id pris en compte  1=01/12/2017
#y-> dernier+1 id pris en compte
x=int(x)
y=int(y)+1
#compteur du nombre d'erreurs de réponse serveur
eh=0

data_ids = range(x,y)
#token d'accès du groupe
gp_id = "B_30cf3d7d"

#vérification de la validité du token auprès de l'opérateur :
vef=input("\nLe token d'identification doit-il être mis à jour ? (N/Y)\n")
if vef=="Y" or vef=="y":
    gp_id=input("Nouveau token : ")

#structure des données pour chaque port 
#8080->locations (chaque location identifiée par son heure, un id correspondant à une heure d'une journée) 
#8090->météo (donne les données météo, données sur une heure par id)
#8100->calendrier (info sur les caractéristique du jour concerné, un jour par id)
met_line="Date_Hour\tDate\tHour\tTemperature\tHumidity\tWind_speed\tVisibility\tDew_point_temperature\tSolar_Radiation\tRainfall\tSnowfall"

cal_line="Date_Hour\tDate\tSeasons\tHoliday\tFunctioning.Day"

loc_struc="Date"
loc_line="Date :"

locations_data = [loc_line]
meteo_data = [met_line]
calendrier_data = [cal_line]

# --- Récupération des calendrier ---
for data_id in data_ids:
    url = f"http://172.22.215.130:8100/?id={data_id}&token={gp_id}"
    #pour éviter les erreurs 429
    time.sleep(0.060)
    response = requests.get(url)
    print(f"Data ID {data_id} sur port 8100 -> status code : {response.status_code}")
    if response.status_code != 200:
        eh=eh+1
        # On passe au port suivant s'il n'y a pas de 200
        continue
        
    # Récupération du texte et séparation en lignes
    lines = response.text.splitlines()

    for line in lines:
        stripped_line = line.strip()
        
        # 1) Bloc "calendrier"
        if not stripped_line.startswith(cal_line):
            calendrier_data.append(stripped_line.replace("NA",""))
            continue
 
                
#transformation de x et y pour correspondre à la gestion heure par heure au lieu de jour par jour
if x!=1:
	x=(x-1)*24+1
	
y=(y-1)*24+1

data_ids = range(x,y)

# --- Récupération des données météo et locations ---
for data_id in data_ids:
    for port in ports:
        url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
        time.sleep(0.060)
        response = requests.get(url)
        print(f"Data ID {data_id} sur port {port} -> status code : {response.status_code}")
        if response.status_code != 200:
            # On passe au port suivant s'il n'y a pas de 200
            eh=eh+1
            continue

        # Récupération du texte et séparation en lignes
        lines = response.text.splitlines()

        for line in lines:
            stripped_line = line.strip()
            
            # 2) Bloc "meteo"
            if port==8090 and not stripped_line.startswith(met_line):
                meteo_data.append(stripped_line.replace("NA",""))
                continue

            # 3) Bloc "locations"
            if port==8080 and not stripped_line.startswith(loc_line):
                locations_data.append(stripped_line)
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

print("Extraction terminée.")
eh=str(eh)
print("Nombre d'exports échoués : "+eh)


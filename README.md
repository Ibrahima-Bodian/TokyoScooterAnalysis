# TokyoScooterAnalysis
Analyse des données de location de trottinettes à Tokyo avec un focus sur les impacts météorologiques pour prévoir les tendances.


import requests
import urllib3

# Pour ignorer les avertissements liés à un certificat auto-signé
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Tester chaque port pour trouver le bon
possible_ports = [8080, 8090, 8100]
data_id = "DATA_ID"  # À adapter
gp_id = "GP_ID"      # À adapter

import requests import urllib3 

Pour ignorer les avertissements liés à un certificat auto-signé (utilisé en test) 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

Liste des ports possibles 

possible_ports = [8080, 8090, 8100] 

Identifiants à adapter 

data_id = "DATA_ID" # Ex. "locations_trottinettes" gp_id = "GP_ID" # Ex. "votre_groupe_id" 

for port in possible_ports: # Construction de l'URL url = f"https://172.22.215.130:{port}/{data_id}?ID={gp_id}" 

# Envoi de la requête GET 
response = requests.get(url, verify=False)  # verify=False pour ignorer les erreurs SSL 
 
# Vérification du code de statut 
if response.status_code == 200: 
    print(f"Succès sur le port {port} !") 
     
    # Supposons que les données soient au format JSON 
    data = response.json() 
    print("Exemple de données :", data) 
     
    # On arrête la boucle une fois qu'on a trouvé le bon port 
    break 
else: 
    print(f"Échec sur le port {port} (code HTTP : {response.status_code})") 
 

 import requests

ports = [8080, 8090, 8100]
data_id = "DATA_ID"
gp_id = "B_30cf3d7d"  # ou ce que vous utilisez

for port in ports:
    url = f"http://172.22.215.130:{port}/{data_id}?ID={gp_id}"
    response = requests.get(url)  # HTTP, sans verify=False
    print(f"Port {port} -> status code : {response.status_code}")
git add .
git commit -m "Ajout de la fonctionnalité X"
git push -u origin master


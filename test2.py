import requests

port = 8100
data_id = 800 # Vous pouvez ajuster cet identifiant si besoin
gp_id = "B_30cf3d7d"

url = f"http://172.22.215.130:{port}/?id={data_id}&token={gp_id}"
#print("URL utilisée :", url)

response = requests.get(url)
print(f"Status code : {response.status_code} ")
print("Contenu de la réponse :")
print(response.text)

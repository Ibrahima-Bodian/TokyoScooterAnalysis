import sqlite3
#pour utiliser sqlite
import pandas as pd
from pandas import read_csv
pd.options.mode.copy_on_write = True 
#pour empêcher des mentions d'erreurs lors de la complétien des cellules vides

print ("Système de création de base de données SQL, nettoyage et complétion des données csv.\n version comp.20-03-2025\n")

#SECTION IMPORTATION ET COMPLETION DES DONNEES
#---------------------------------------------------------

#locations : export des données csv
loc=read_csv("locations.csv", sep=";")

#calendrier : export des données csv ; création d'un tableau de détection des cellules vides
#création d'une liste des colonnes
cal=read_csv("calendrier.csv", sep=";")
detcal=cal.isnull()
colcal=["Seasons","Holiday","Functioning_Day"]


#météo : export des données csv ; création d'un tableau de détection des cellules vides
#création d'une liste des colonnes
met=read_csv("meteo.csv", sep=";")
detmet=met.isnull()
colmet=["Temperature", "Humidity","Wind_speed","Visibility","Dew_point_temperature","Solar_Radiation","Rainfall","Snowfall"]

#le code fontionne aussi si on remplace tous les ".loc[i,element]" par "[element][i]".
#mais python affiche une "pré-erreur" (une alerte pour les cas où les solutions changeront pour la nouvelle version de python)
#qui recommande d'utiliser "loc"
#pour empêcher l'erreur d'apparaitre j'ai changé le options de python n insérant au début
#pd.options.mode.copy_on_write = True
# et utiliser la façon de code loc

for element in colcal:
    for i in range(len(cal)):
        if detcal.loc[i,element] == True:
            cal.loc[i,element]=cal.loc[(i-1),element]

for element in colmet:
    for i in range(len(met)):
        if detmet.loc[i,element] == True:
            met.loc[i,element]=(met.loc[(i-1),element]+met.loc[(i+1),element])/2

#---------------------------------------------------------


#Connection, ou création de la database 'base.db'
connection = sqlite3.connect('base.db')

#création du "cursor" qui pemettra d'envoyer des commandes vers le SQL
cursor = connection.cursor()

#SECTION CREATION DES TABLES
#---------------------------------------------------------

print ("Etape 1/3 :")
a=input("Créer la base de données, ou passer à l'étape suivante ? (Y/N)\n")

if a=="Y" or a=="y":
    a=1

if a==1:
    #commande sql pour la création de la table
    sql_command = """CREATE TABLE calendrier ( 
    Date_Hour VARCHAR(30), 
    Date DATE,
    Seasons VARCHAR(20), 
    Holiday VARCHAR(30),
    Functionning_Day VARCHAR(3));"""

    #executer la commande sql
    cursor.execute(sql_command)

    #commande sql pour la création de la table
    sql_command = """CREATE TABLE meteo ( 
    Date_Hour VARCHAR(30), 
    Date DATE,
    Hour INTEGER,
    Temperature FLOAT, 
    Humidity INTEGER,
    Wind_speed FLOAT,
    Visibility INTEGER,
    Dew_point_temperature FLOAT,
    Solar_Radiation FLOAT,
    Rainfall FLOAT,
    Snowfall FLOAT);"""

    #executer la commande sql
    cursor.execute(sql_command)

    #commande sql pour la création de la table
    sql_command = """CREATE TABLE locations ( 
    Date_Hour VARCHAR(30));"""

    #executer la commande sql
    cursor.execute(sql_command)

#---------------------------------------------------------

#SECTION INTEGRATION DES DONNEES
#---------------------------------------------------------

print ("\nEtape 2/3 :")
b=input("Remplir la base de données, ou passer à l'étape suivante ? (Y/N)\n")

if b=="Y" or b=="y":
    b=1

if b==1:
    #intégration du csv calendrier
    for i in range(len(cal)):
        cursor.execute(f'INSERT INTO calendrier VALUES ("{cal.Date_Hour[i]}", "{cal.Date[i]}", "{cal.Seasons[i]}", "{cal.Holiday[i]}", "{cal.Functioning_Day[i]}")')

    #intégration du csv meteo
    for i in range(len(met)):
        cursor.execute(f'INSERT INTO meteo VALUES ("{met.Date_Hour[i]}","{met.Date[i]}", "{met.Hour[i]}", "{met.Temperature[i]}", "{met.Humidity[i]}", "{met.Wind_speed[i]}","{met.Visibility[i]}", "{met.Dew_point_temperature[i]}","{met.Solar_Radiation[i]}", "{met.Rainfall[i]}","{met.Snowfall[i]}")')

    #intégration du csv locations
    for i in range(len(loc)):
        cursor.execute(f'INSERT INTO locations VALUES ("{loc.Date[i]}")')


#---------------------------------------------------------
print ("\nEtape 3/3 :")
c=input("Nettoyer et compléter les fichiers csv, ou passer à l'étape suivante ? (Y/N)\n")

if c=="Y" or c=="y":
    c=1

if c==1:
    cal["Jour"]=pd.to_datetime(cal['Date']).dt.isocalendar().day
    cal["Jour"]=cal["Jour"].astype(str)
    for i in range(len(cal)):
        if cal.loc[i,"Jour"]=="1":
            x="Lundi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="2":
            x="Mardi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="3":
            x="Mercredi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="4":
            x="Jeudi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="5":
            x="Vendredi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="6":
            x="Samedi"
            cal.loc[i,"Jour"]=x
        if cal.loc[i,"Jour"]=="7":
            x="Dimanche"
            cal.loc[i,"Jour"]=x

    cal.to_csv('calendrier4.csv',sep=";", index=False)  
    met.to_csv('meteo4.csv',sep=";", index=False)  
    loc.to_csv('locations4.csv',sep=";", index=False)  

 
# IMPORTANT : Sauvegarde des opérations, sinon rien ne sera fait dans la base
connection.commit()

#déconnexion
connection.close()

if a+b+c!=3:
    print("\nBon ben, merci d'être passé ?")
else:
    print("\nTraitement complet")

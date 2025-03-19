import sqlite3
import pandas as pd
from pandas import read_csv
#pour utiliser sqlite

#Connection, ou création de la database 'base.db'
connection = sqlite3.connect('base.db')

#création du "cursor" qui pemettra d'envoyer des commandes vers le SQL
cursor = connection.cursor()

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

cal=read_csv("calendrier.csv", sep=";")
for i in range(len(cal)-1):
    cursor.execute(f'INSERT INTO calendrier VALUES ("{cal.Date_Hour[i]}", "{cal.Date[i]}", "{cal.Seasons[i]}", "{cal.Holiday[i]}", "{cal.Functioning_Day[i]}")')

#met=read_csv("meteo.csv", sep=";")
#for i in range(len(met)-1):
#    cursor.execute(f'INSERT INTO meteo VALUES ("{met.Date_Hour[i]}","{met.Date[i]}", {met.Hour[i]}, {met.Temperature[i]}, {met.Humidity[i]}, {met.Wind_speed[i]}, {met.Dew_point_temperature[i]},{met.Solar_Radiation[i]}, {met.Rainfall[i]}, {met.Snowfall[i]})')
#PROBLEME A CORRIGER : les valeurs nulles sont rentrées en texte "nan" j'ai l'impression, dès que je peux corriger ça c'est parfait


loc=read_csv("locations.csv", sep=";")
for i in range(len(loc)-1):
    cursor.execute(f'INSERT INTO locations VALUES ("{loc.Date[i]}")')


# SQL command to insert the data in the table
#sql_command = """INSERT INTO first VALUES (23, "Poisson","Frit");"""
#cursor.execute(sql_command)
 
# another SQL command to insert the data in the table
#sql_command = """INSERT INTO first VALUES (2, "Lotte", "Pleureuse");"""
#cursor.execute(sql_command)
 
# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()



#déconnexion
connection.close()
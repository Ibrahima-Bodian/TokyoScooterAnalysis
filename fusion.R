install.packages("data.table")  # à faire une seule fois
library(data.table)


# On suppose que vos fichiers sont nommés "weather.csv", "times.csv", "location.csv"
# et qu'ils se trouvent dans le répertoire de travail courant

weather <- fread("meteo.csv")   # Pour un gros volume, fread est plus rapide que read.csv
times   <- fread("calendrier.csv", fill = TRUE) 
location <- fread("locations.csv", fill = TRUE)


head(weather)
head(times)
head(location)


# Renommer la colonne
setnames(times, old = "Date", new = "Timestamp")

# Supprimer le préfixe "Date : " si nécessaire 
# (si la première ligne est "Date : 2017-12-01T00:00:00")
times[, Timestamp := gsub("^Date : ", "", Timestamp)]

# Enlever le suffixe .000Z si présent
times[, Timestamp := gsub("\\.000Z$", "", Timestamp)]

# Extraire la date => col. "Date" au format YYYY-MM-DD
times[, Date := tstrsplit(Timestamp, "T")[[1]]]  # split sur "T" et prend le premier élément
times[, Date := as.IDate(Date, format = "%Y-%m-%d")]


location[, Date := as.IDate(Date, format = "%Y-%m-%d")]


# 1) Merge weather + location par la clé "Date"
# En data.table, on peut faire :
setkey(weather, Date)     # indexer la table weather par la colonne Date
setkey(location, Date)    # indexer la table location par la colonne Date

# On fait un merge "full" => on veut toutes les dates
mergedWL <- merge(weather, location, by = "Date", all = TRUE, allow.cartesian = TRUE)

# 2) Merge avec times
setkey(times, Date)
unified <- merge(mergedWL, times, by = "Date", all = TRUE, allow.cartesian = TRUE)


dim(unified)
head(unified)

# Enfin, on écrit dans un CSV
fwrite(unified, "unified.csv")
"""





"

# Installer data.table si nécessaire (à faire une seule fois)
# install.packages("data.table")
library(data.table)

# Lecture des fichiers
# weather.csv : séparateur ;, avec en-tête
weather <- fread("meteo.csv", sep = ";", header = TRUE)
# Vérifier la structure
print(head(weather))

# times.csv : on suppose qu'il n'a qu'une colonne et éventuellement pas d'en-tête
# Si votre fichier contient une ligne d'en-tête "Date : ..." à ignorer, on l'indique ici
times <- fread("locations.csv", header = FALSE, fill = TRUE)
setnames(times, "V1", "Timestamp")
# Nettoyage : supprimer le préfixe "Date : " s'il existe, et le suffixe ".000Z" le cas échéant
times[, Timestamp := gsub("^Date : ", "", Timestamp)]
times[, Timestamp := gsub("\\.000Z$", "", Timestamp)]
# Extraire la date (partie avant "T")
times[, Date := tstrsplit(Timestamp, "T")[[1]]]
times[, Date := as.IDate(Date, format = "%Y-%m-%d")]
print(head(times))

# location.csv : séparateur tabulation
location <- fread("locations.csv", sep = "\t", header = TRUE, fill = TRUE)
# Convertir la colonne Date en type Date
location[, Date := as.IDate(Date, format = "%Y-%m-%d")]
print(head(location))

# Convertir la colonne Date de weather en type Date (si ce n'est pas déjà le cas)
weather[, Date := as.IDate(Date, format = "%Y-%m-%d")]
print(head(weather))

# Fusionner weather et location par la clé "Date" (jointure complète)
setkey(weather, Date)
setkey(location, Date)
mergedWL <- merge(weather, location, by = "Date", all = TRUE, allow.cartesian = TRUE)

# Fusionner le résultat avec times par la clé "Date"
setkey(times, Date)
unified <- merge(mergedWL, times, by = "Date", all = TRUE, allow.cartesian = TRUE)

# Afficher la dimension et quelques lignes pour vérification
print(dim(unified))
print(head(unified))

# Écrire le tableau unifié dans un fichier CSV
fwrite(unified, "unified.csv")

cat("Fusion terminée. Le fichier 'unified.csv' a été créé.\n")
"""

# Installer et charger data.table (à faire une seule fois)
# install.packages("data.table")
library(data.table)

# -------------------------
# Lecture et prétraitement
# -------------------------

# 1) Calendrier
# Fichier "calendrier.csv" avec séparateur ";"
cal <- fread("calendrier.csv", sep=";", header=TRUE)
# Le fichier contient : Date_Hour;Seasons;Holiday;Functioning.Day
# On crée une colonne Date en extrayant les 10 premiers caractères de Date_Hour
cal[, Date := as.IDate(substr(Date_Hour, 1, 10), format="%Y-%m-%d")]
# On peut éventuellement réorganiser les colonnes si besoin
setcolorder(cal, c("Date", setdiff(names(cal), "Date")))
print(head(cal))

# 2) Meteo
# Fichier "meteo.csv" avec séparateur ";" et un en-tête
meteo <- fread("meteo.csv", sep=";", header=TRUE)
# On suppose que le fichier contient déjà une colonne Date (format "YYYY-MM-DD")
meteo[, Date := as.IDate(Date, format="%Y-%m-%d")]
print(head(meteo))

# 3) Locations
# Fichier "locations.csv" avec en-tête "Date" et des timestamps comme "2017-12-01T00:00:19.000Z"
loc <- fread("locations.csv", sep=",", header=TRUE)
# Si le séparateur n'est pas la virgule, ajustez le paramètre sep (par exemple, sep="\t")
# On crée une colonne Date en extrayant la partie avant "T"
loc[, Date := as.IDate(substr(Date, 1, 10), format="%Y-%m-%d")]
print(head(loc))

# -------------------------
# Fusion
# -------------------------

# On va fusionner par la clé "Date". Étant donné que chaque fichier peut contenir plusieurs lignes par date,
# la jointure sera un produit cartésien pour les lignes associées à la même date.
# data.table est très efficace pour traiter des volumes importants.

# Fusionner d'abord meteo et calendrier par Date
setkey(meteo, Date)
setkey(cal, Date)
mergedWL <- merge(meteo, cal, by="Date", all=TRUE, allow.cartesian=TRUE)

# Puis fusionner le résultat avec locations
setkey(loc, Date)
unified <- merge(mergedWL, loc, by="Date", all=TRUE, allow.cartesian=TRUE)

# Afficher quelques informations pour vérification
cat("Dimensions du tableau fusionné :", dim(unified), "\n")
print(head(unified))

# -------------------------
# Export
# -------------------------
# Écriture dans un fichier CSV unifié
fwrite(unified, "unified.csv")
cat("Fusion terminée. Le fichier 'unified.csv' a été créé.\n")

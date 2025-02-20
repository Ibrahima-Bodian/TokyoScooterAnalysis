install.packages("data.table")  # à faire une seule fois
library(data.table)

# On suppose que vos fichiers sont nommés "weather.csv", "times.csv", "location.csv"
# et qu'ils se trouvent dans le répertoire de travail courant

weather <- fread("weather.csv")   # Pour un gros volume, fread est plus rapide que read.csv
times   <- fread("times.csv", fill = TRUE) 
location <- fread("location.csv", fill = TRUE)


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

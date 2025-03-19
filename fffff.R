# install.packages("data.table")
library(data.table)

# 1) Lecture des fichiers
weather<-fread("meteo.csv", sep=";", header=TRUE)
cal<-fread("calendrier.csv", sep=";", header=TRUE)
loc<-fread("locations.csv", sep=";", header=TRUE)

# Afficher un aperçu
print(head(weather))
print(head(cal))
print(head(loc))

cal[, Date := as.IDate(substr(Date_Hour, 1, 10), format="%Y-%m-%d")]

weather[, Date := as.IDate(Date, format="%Y-%m-%d")]

# On extrait la partie "YYYY-MM-DD" (les 10 premiers caractères).
loc[, Date := as.IDate(substr(Date, 1, 10), format="%Y-%m-%d")]

# Vérifier les colonnes créées
print(head(cal[, .(Date_Hour, Date)]))
print(head(weather[, .(Date)]))
print(head(loc[, .(Date)]))

setkey(weather, Date)
setkey(cal, Date)
mergedWL<-merge(weather, cal, by="Date", all=TRUE, allow.cartesian=TRUE)

setkey(loc, Date)
fusion<-merge(mergedWL, loc, by="Date", all=TRUE, allow.cartesian=TRUE)

cat("Dimensions du tableau unifié :", dim(fusion), "\n")
print(head(fusion))

# 4) Export
fwrite(fusion, "fusion.csv")
cat("Fusion terminée. Le fichier 'fusion.csv' a été créé.\n")

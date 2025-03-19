import csv
import re
import sys

# --------------------------------------------------------------------
# Fonctions d'aide
# --------------------------------------------------------------------
def is_iso_datetime(dt_str):
    """
    Vérifie si dt_str ressemble à YYYY-MM-DDTHH:MM:SS(.xxx)?Z?
    """
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?$"
    return bool(re.match(pattern, dt_str.strip()))

def is_iso_date(d_str):
    """
    Vérifie si c'est un format YYYY-MM-DD.
    """
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, d_str.strip()))

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# --------------------------------------------------------------------
# Validation du fichier meteo.csv
# --------------------------------------------------------------------
def validate_meteo(file_path):
    """
    Vérifie que meteo.csv possède 11 colonnes par ligne et que
    certaines colonnes respectent les formats attendus.

    On ignore la ligne 1 (header).
    On fait un résumé du nombre de lignes qui contiennent des NA.
    """
    errors = []
    na_lines = set()  # on stocke le numéro de ligne qui contient un NA
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        line_num = 0
        for row in reader:
            line_num += 1
            # Ignorer la première ligne (en-tête)
            if line_num == 1:
                continue

            # Vérifier le nombre de colonnes
            if len(row) != 11:
                errors.append(f"Ligne {line_num}: Nombre de colonnes incorrect ({len(row)}) => {row}")
                continue

            # row = [Date_Hour, Date, Hour, Temperature, Humidity, Wind_speed,
            #        Visibility, Dew_point_temperature, Solar_Radiation,
            #        Rainfall, Snowfall]

            # 0) Date_Hour
            if not is_iso_datetime(row[0]):
                errors.append(f"Ligne {line_num}: Date_Hour invalide => {row[0]}")
            # 1) Date
            if not is_iso_date(row[1]):
                errors.append(f"Ligne {line_num}: Date invalide => {row[1]}")
            # 2) Hour
            if not (is_integer(row[2]) and 0 <= int(row[2]) <= 23):
                errors.append(f"Ligne {line_num}: Hour invalide => {row[2]}")
            # 3..10 => numeric
            for col_index in range(3, 11):
                if row[col_index].strip().upper() == "NA":
                    # On considère que c'est un "NA" explicite
                    errors.append(f"Ligne {line_num}: Valeur non numérique (col {col_index+1}) => NA")
                    na_lines.add(line_num)
                else:
                    # Vérifier si c'est un float valide
                    if not is_float(row[col_index]):
                        errors.append(f"Ligne {line_num}: Valeur non numérique (col {col_index+1}) => {row[col_index]}")
    return errors, na_lines

# --------------------------------------------------------------------
# Validation du fichier calendrier.csv
# --------------------------------------------------------------------
def validate_calendrier(file_path):
    """
    Vérifie que calendrier.csv possède 4 colonnes et ignore la première ligne (header).
    """
    errors = []
    na_lines = set()
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        line_num = 0
        for row in reader:
            line_num += 1
            # Ignorer la première ligne (header)
            if line_num == 1:
                continue

            # Vérifier le nombre de colonnes
            if len(row) != 4:
                errors.append(f"Ligne {line_num}: Nombre de colonnes incorrect ({len(row)}) => {row}")
                continue

            # row = [Date_Hour, Seasons, Holiday, Functioning.Day]
            # Date_Hour
            if not is_iso_datetime(row[0]):
                errors.append(f"Ligne {line_num}: Date_Hour invalide => {row[0]}")

            # Vous pouvez ajouter des checks sur Seasons, Holiday, Functioning.Day
            # (par ex. if row[1].strip() not in ["Winter","Spring","Summer","Autumn"]: ...)
            # Pour les "NA", si c'est littéralement "NA", on peut le signaler :
            for col_index in range(4):
                if row[col_index].strip().upper() == "NA":
                    errors.append(f"Ligne {line_num}: Valeur NA inattendue (col {col_index+1}) => NA")
                    na_lines.add(line_num)
    return errors, na_lines

# --------------------------------------------------------------------
# Validation du fichier locations.csv
# --------------------------------------------------------------------
def validate_locations(file_path):
    """
    Vérifie que locations.csv possède 1 colonne par ligne,
    et que la valeur est un datetime ISO valide.

    On ignore la première ligne (header).
    """
    errors = []
    na_lines = set()
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        line_num = 0
        for row in reader:
            line_num += 1
            # Ignorer la première ligne (header)
            if line_num == 1:
                continue

            if len(row) != 1:
                errors.append(f"Ligne {line_num}: Nombre de colonnes != 1 => {row}")
                continue

            # Vérifie le format ISO
            val = row[0].strip()
            if val.upper() == "NA":
                errors.append(f"Ligne {line_num}: Valeur NA inattendue => NA")
                na_lines.add(line_num)
            elif not is_iso_datetime(val):
                errors.append(f"Ligne {line_num}: Format datetime invalide => {val}")
    return errors, na_lines

# --------------------------------------------------------------------
def main():
    print("Validation de meteo.csv...")
    meteo_errors, meteo_na = validate_meteo("meteo.csv")
    if meteo_errors:
        print("Erreurs détectées dans meteo.csv :")
        for e in meteo_errors:
            print(" -", e)
    else:
        print("Aucune erreur détectée dans meteo.csv !")
    print(f"Nombre de lignes contenant des 'NA' dans meteo.csv : {len(meteo_na)}")

    print("\nValidation de calendrier.csv...")
    cal_errors, cal_na = validate_calendrier("calendrier.csv")
    if cal_errors:
        print("Erreurs détectées dans calendrier.csv :")
        for e in cal_errors:
            print(" -", e)
    else:
        print("Aucune erreur détectée dans calendrier.csv !")
    print(f"Nombre de lignes contenant des 'NA' dans calendrier.csv : {len(cal_na)}")

    print("\nValidation de locations.csv...")
    loc_errors, loc_na = validate_locations("locations.csv")
    if loc_errors:
        print("Erreurs détectées dans locations.csv :")
        for e in loc_errors:
            print(" -", e)
    else:
        print("Aucune erreur détectée dans locations.csv !")
    print(f"Nombre de lignes contenant des 'NA' dans locations.csv : {len(loc_na)}")

    print("\nValidation terminée.")

if __name__ == "__main__":
    main()

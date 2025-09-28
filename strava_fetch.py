import requests
import os
import json
import time
import pandas as pd
ACCESS_TOKEN =  "f185a2d9690e189ad6d66471fa9cf8cd6fc10eb4"
# Paramètres
per_page = 200  # nombre d'activités à récupérer
page = 1
# URL de l'API Strava
url = f"https://www.strava.com/api/v3/athlete/activities"

# Liste pour stocker les courses à pied
all_runs = []

# Requête API
params = {
    "per_page": per_page,
    "page": page
}
while True :
    response = requests.get(url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, params=params)

    if response.status_code != 200:
        print(f"Erreur: {response.status_code}, {response.text}")
        break

    activities = response.json()
        # Filtrer uniquement les courses à pied
    runs = [act for act in activities if act["sport_type"] == "Run"]
    all_runs.extend(runs)
    
    if len(activities) < per_page : 
        break
    page += 1
    params["page"] = page
    # Pause pour éviter de dépasser le quota Strava
    time.sleep(10)

print(f"Nombre de courses récupérées : {len(all_runs)}")

# Nom du fichier de sauvegarde
output_file = "all_runs.json"

# Écriture dans le fichier
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_runs, f, indent=4, ensure_ascii=False)

print(f"{len(all_runs)} runs sauvegardées dans {output_file}")

# Lecture du JSON
with open("all_runs.json", "r", encoding="utf-8") as f:
    all_runs_data = json.load(f)

# Conversion en DataFrame
df_runs = pd.DataFrame(all_runs_data)

# Vérification rapide
print(df_runs.shape)        # Nombre de lignes et colonnes
print(df_runs.head())       # Aperçu des premières lignes
print(df_runs.columns)      # Liste des colonnes disponibles
    
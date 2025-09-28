# ---------------------------------------
# LOO + GradientBoosting sur marathons
# ---------------------------------------

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import timedelta
import matplotlib.pyplot as plt

# Charger le dataset
df = pd.read_csv("marathons_csv")

# Cible : temps marathon (en secondes)
y = df["perf_sec"]

# Features : mêmes que LinearRegression
X = df[[ 
    "km_tot", "km_life", "suffer_taper", "ratio_taper", "nb_sorties", "nb_sorties_20k", "nb_sorties_30k",
    "sortie_longue_max", "allure_moy", "suffer_score_moy",
    "ratio_volume_last_month", "long_run_last_month", 
]]

# Initialisation du modèle Random Forest
model = GradientBoostingRegressor(n_estimators=300, random_state=42)

# Leave-One-Out Cross Validation
loo = LeaveOneOut()
y_true, y_pred = [], []

for train_idx, test_idx in loo.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    y_true.append(y_test.values[0])
    y_pred.append(pred[0])

# Conversion en arrays
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Métriques
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

# Résultats
print("\n=== Résultats Gradient Boosting ===")
print(f"Erreur absolue moyenne : {mae:.1f} sec (~{mae/60:.1f} min)")
print(f"R² : {r2:.3f}")

# Affichage détaillé
print("\n--- Détail des prédictions ---")
for i in range(len(y_true)):
    real_td = timedelta(seconds=int(y_true[i]))
    pred_td = timedelta(seconds=int(y_pred[i]))
    delta = int(y_pred[i] - y_true[i])
    delta_td = timedelta(seconds=abs(delta))
    sign = "+" if delta >= 0 else "-"
    
    print(f"Marathon {i+1} : Réel = {real_td}, Prédit = {pred_td}, Erreur = {sign}{delta_td}")

# Visualisation
plt.scatter(y_true/60, y_pred/60, label="Prédictions")
plt.plot([min(y_true/60), max(y_true/60)], [min(y_true/60), max(y_true/60)], 
         linestyle="--", color="red", label="Idéal")
plt.xlabel("Temps réel (min)")
plt.ylabel("Temps prédit (min)")
plt.title("Réel vs Prédit — Gradient Boosting")
plt.legend()
plt.show()

print("\n--- Importance des variables (tri décroissant) ---")
importances = list(zip(X.columns, model.feature_importances_))
importances_sorted = sorted(importances, key=lambda x: x[1], reverse=True)

for name, imp in importances_sorted:
    print(f"{name:25s}: {imp:.3f}")

# Récupérer noms et importances triées
features, importances = zip(*importances_sorted)

plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel("Importance")
plt.title("Importance des variables (Gradient Boosting)")
plt.gca().invert_yaxis()  # Pour afficher la variable la plus importante en haut
plt.tight_layout()

plt.show()

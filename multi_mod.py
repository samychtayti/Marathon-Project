# ---------------------------------------
# Comparatif multi-modèles (Leave-One-Out)
# ---------------------------------------

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, r2_score
# XGBoost et LightGBM
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# Charger ton dataset
df = pd.read_csv("C:/Users/SamyC/AppData/Local/Programs/Python_lea/strava/marathons_features.csv")

# Cible : temps marathon en secondes
y = df["perf_sec"]

# Features : ajuste la liste selon tes colonnes
X = df[[ 
    "km_tot", "km_life", "suffer_taper", "ratio_taper", "nb_sorties", "nb_sorties_20k", "nb_sorties_30k",
    "sortie_longue_max", "allure_moy", "suffer_score_moy",
    "ratio_volume_last_month", "long_run_last_month", 
]]

# Liste des modèles à comparer
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1),
    "ElasticNet": ElasticNet(alpha=0.1, l1_ratio=0.5),
    "RandomForest": RandomForestRegressor(n_estimators=300, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=300, random_state=42),
    "KNN": KNeighborsRegressor(n_neighbors=2),  # avec 5 points, attention au choix de k
    "XGBoost": XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42),
    "LightGBM": LGBMRegressor(n_estimators=300, learning_rate=0.05, max_depth=-1, random_state=42)
}

results = []

# Leave-One-Out
loo = LeaveOneOut()

for name, model in models.items():
    y_true, y_pred = [], []
    
    for train_idx, test_idx in loo.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        
        y_true.append(y_test.values[0])
        y_pred.append(pred[0])
    
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    results.append([name, mae, mae/60, r2])

# Résultats en DataFrame
results_df = pd.DataFrame(results, columns=["Modèle", "MAE (sec)", "MAE (min)", "R²"])
print("\n=== Résultats comparatifs ===")
print(results_df)

import matplotlib.pyplot as plt

# Trier les modèles par MAE pour lisibilité
results_df_sorted = results_df.sort_values("MAE (sec)")

plt.figure(figsize=(10, 6))
plt.barh(results_df_sorted["Modèle"], results_df_sorted["MAE (min)"])
plt.xlabel("Erreur absolue moyenne (minutes)")
plt.title("Comparaison des modèles (Leave-One-Out)")
plt.gca().invert_yaxis()  # Pour avoir le meilleur en haut
plt.tight_layout()
plt.show()

# Trier les modèles par R²
plt.figure(figsize=(10, 6))
plt.barh(results_df["Modèle"], results_df["R²"])
plt.xlabel("R²")
plt.title("Comparaison des modèles (Leave-One-Out)")
plt.axvline(0, color="red", linestyle="--")  # ligne de référence baseline
plt.tight_layout()
plt.show()


# 🏃 Marathon Performance Prediction (Strava + Machine Learning)

## 🎯 Objectif

Prédire mes performances marathon à partir de mes données Strava (6 mois d’entraînement avant chaque course).
Ce projet est à la fois :

* Un **exercice de formation personnelle** en Data Science & Machine Learning appliqués au sport.
* Un **MVP** montrant comment les données d’entraînement peuvent être exploitées pour estimer (et à terme optimiser) la performance en course sur route.

---

## 📂 Structure du projet

```
.
├── strava_auth.py            # Authentification + refresh token Strava
├── strava_fetch.py           # Récupération des activités via API Strava
├── build_marathon_dataset.py # Feature engineering (6 mois avant chaque marathon)
├── multi_mod.py              # Comparaison multi-modèles avec Leave-One-Out
├── loo_GBR_marathon.py       # Analyse détaillée GradientBoosting (baseline)
├── data/                     # Données dérivées (CSV anonymisés)
└── README.md                 # Ce document
```

---

## 📊 Données utilisées

* Source : API Strava (mes données personnelles)
* **Fenêtre de 180 jours** avant chaque marathon
* Exemples de features construites :

  * `km_tot` : volume total
  * `km_life` : kilométrage cumulé à vie
  * `nb_sorties_20k`, `nb_sorties_30k` : sorties longues
  * `sortie_longue_max` : distance max
  * `allure_moy`, `suffer_score_moy` : intensité et régularité
  * `ratio_taper`, `suffer_taper` : gestion de l’affûtage
  * `perf_sec` : temps marathon en secondes (cible)

---

## 🧑‍💻 Méthodologie

1. **Feature engineering** via `build_marathon_dataset.py`
2. **Validation Leave-One-Out** (LOO) → adaptée à mon petit dataset (5 marathons)
3. **Comparaison de 9 modèles** de régression :

   * LinearRegression, Ridge, Lasso, ElasticNet
   * RandomForest, GradientBoosting
   * KNN, XGBoost, LightGBM
4. **Évaluation** avec MAE (minutes) et R²

---

## ✅ Résultats principaux

| Modèle           | MAE (min) | R²   |
| ---------------- | --------- | ---- |
| GradientBoosting | **4.4**   | 0.32 |
| KNN              | 5.3       | 0.15 |
| Autres modèles   | >6 min    | ≤0   |

* **Baseline retenue : GradientBoosting**
* Erreurs faibles (±4 min en moyenne), mais **forte sous-estimation sur mon premier marathon** (débutant, volume faible, taper limité).
* **Features clés identifiées** : `km_tot`, `allure_moy`, `suffer_score_moy`, `km_life`.

---

## 🔍 Limites & perspectives

* **Dataset personnel (5 marathons)** → faible généralisation
* **Pas de cas de “mur” ou blessure** → défaillances impossibles à anticiper
* Modèle robuste en conditions normales, mais **ne prédit pas l’imprévisible**

**Pistes d’amélioration :**

* Enrichissement avec **streams Strava** (variabilité allure, zones de FC, régularité pacing)
* Intégration de la **météo** et du **profil de parcours**
* Tests sur dataset multi-athlètes → généralisation à d’autres coureurs
* Déploiement d’un **dashboard interactif (Streamlit/Dash)** pour visualiser les prédictions

---

## 👤 Auteur

Projet personnel de reconversion vers la Data Science appliquée au sport.
Objectif : démontrer des compétences en **Machine Learning, analyse sportive, et storytelling data**.

---


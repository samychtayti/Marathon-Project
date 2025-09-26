import pandas as pd
from pathlib import Path

# --- Fonction (copiée de ce qu'on a vu) ---
def build_marathon_dataset(df, window_days=180):
    marathons = df[
        (df["distance"] >= 41500) & (df["distance"] <= 43000)
    ].copy()
    marathons["start_date"] = pd.to_datetime(marathons["start_date"])
    
    marathon_rows = []

    for _, marathon in marathons.iterrows():
        m_date = marathon["start_date"]

        # Fenêtre 6 mois
        mask_1 = (
            (pd.to_datetime(df["start_date"]) >= m_date - pd.Timedelta(days=window_days)) &
            (pd.to_datetime(df["start_date"]) < m_date)
        )
        window_df = df.loc[mask_1]

        # Kilométrage à vie
        mask_2 = (
            (pd.to_datetime(df["start_date"]) < m_date)
        )
        life_df = df.loc[mask_2]

        # Taper : deux dernières semaines
        mask_taper = (
            (pd.to_datetime(df["start_date"]) >= m_date - pd.Timedelta(days=13)) &
            (pd.to_datetime(df["start_date"]) < m_date)
        )
        taper_df = df.loc[mask_taper]
        # Agrégations
        
        km_life = life_df["distance"].sum() / 1000
        km_tot = window_df["distance"].sum() / 1000
        nb_sorties = window_df.shape[0]
        km_hebdo = window_df.groupby(
            pd.to_datetime(window_df["start_date"]).dt.isocalendar().week
        )["distance"].sum() / 1000
        km_hebdo_mean = km_hebdo.mean()
        km_hebdo_std = km_hebdo.std()

        long_runs_20k = window_df[window_df["distance"] >= 20000]
        long_runs_30k = window_df[window_df["distance"] >= 30000]
        nb_sorties_20k = long_runs_20k.shape[0]
        nb_sorties_30k = long_runs_30k.shape[0]
        allure_moy_sorties_20k = (
            long_runs_20k["pace_min_per_km"].mean() if not long_runs_20k.empty else None
        )
        sortie_longue_max = window_df["distance"].max() / 1000 if not window_df.empty else None

        allure_moy = window_df["pace_min_per_km"].mean()
        fc_moy = window_df["average_heartrate"].mean()
        suffer_score_moy = window_df["suffer_score"].mean()

        last_month_mask = (
            (pd.to_datetime(df["start_date"]) >= m_date - pd.Timedelta(days=44)) &
            (pd.to_datetime(df["start_date"]) < m_date  - pd.Timedelta(days=13))
        )
        last_month_df = df.loc[last_month_mask]
        ratio_volume_last_month = (
            last_month_df["distance"].sum() / window_df["distance"].sum()
            if window_df["distance"].sum() > 0 else None
        )
        long_run_last_month = (
            last_month_df["distance"].max() / 1000 if not last_month_df.empty else None
        )
        km_taper = taper_df["distance"].sum() / 1000
        suffer_taper = taper_df["suffer_score"].mean() if not taper_df.empty else 0
        ratio_taper = (
            km_taper / last_month_df["distance"].sum()
        )

        denivele_tot = window_df["total_elevation_gain"].sum()

        marathon_rows.append({
            "marathon_id": marathon["id"],
            "date": m_date,
            "perf_sec": marathon["moving_time"],
            "km_life" : km_life,
            "km_tot": km_tot,
            "suffer_taper" : suffer_taper,
            "ratio_taper" : ratio_taper,
            "nb_sorties": nb_sorties,
            "km_hebdo_mean": km_hebdo_mean,
            "km_hebdo_std": km_hebdo_std,
            "nb_sorties_20k": nb_sorties_20k,
            "nb_sorties_30k": nb_sorties_30k,
            "allure_moy_sorties_20k": allure_moy_sorties_20k,
            "sortie_longue_max": sortie_longue_max,
            "allure_moy": allure_moy,
            "fc_moy": fc_moy,
            "suffer_score_moy": suffer_score_moy,
            "ratio_volume_last_month": ratio_volume_last_month,
            "long_run_last_month": long_run_last_month,
            "denivele_tot": denivele_tot
        })
    
    
    df_out = pd.DataFrame(marathon_rows)
    return df_out



# --- Utilisation ---
if __name__ == "__main__":
    # Charger ton dataset filtré
    csv_path = Path(r"C:\Users\SamyC\AppData\Local\Programs\Python_lea\strava\runs_filtered.csv")
    df_runs_filtered = pd.read_csv(csv_path)

    # Construire dataset marathons
    df_marathons_features = build_marathon_dataset(df_runs_filtered, window_days=180)

    # Sauvegarder
    out_path = csv_path.parent / "marathons_features.csv"
    df_marathons_features.to_csv(out_path, index=False, encoding="utf-8")

    print(f"✅ Dataset marathons sauvegardé : {out_path}")
    print(df_marathons_features.head())

import requests
import time
import json
import os

activities_url = f"https://www.strava.com/api/v3/athlete/activities?per_page=1"
##  Vérifier sur le token est valide 
def check_token(access_token, expires_at, activities_url):
    """
    Retourne True si le token est (a) pas encore expiré ET (b) accepté par l'API.
    Retourne False sinon.
    """
    # 1) Vérifier qu'on a bien un expires_at valide
    if expires_at is None:
        print("⚠️ Pas d'expires_at fourni -> considérer le token invalide.")
        return False

    # 2) Comparaison temporelle : si expiré, on n'appelle pas l'API
    now = time.time()
    if now >= expires_at:
        print("Token expiré (timestamp dépassé).")
        return False

    # 3) Si pas expiré selon expires_at, on fait un appel test à l'API
    try:
        resp = requests.get(activities_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
    except requests.RequestException as e:
        # Erreur réseau / timeout
        print("Erreur réseau lors du test du token :", e)
        return False

    # 4) Interpréter le status_code renvoyé
    if resp.status_code == 200:
        # Tout est OK : token accepté par l'API
        print("Token valide ✅")
        return True
    elif resp.status_code == 401:
        # Token invalide / expiré côté Strava
        print("Token rejeté par l'API (401) — il faut rafraîchir.")
        return False
    else:
        # Cas inattendu : on logue pour débogage et on considère le token non utilisable
        print(f"Code HTTP inattendu {resp.status_code} — réponse (début) : {resp.text[:200]}")
        return False
    

# Requête token
def refresh_access_token(client_id, client_secret, refresh_token, token_file) : 
    ## On envoie les infos à l'API
    url_post = f"https://www.strava.com/oauth/token" 
    response = requests.post(
        url_post,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    if response.status_code == 200:
            token_data = response.json()
            print("Nouveaux tokens reçus ✅")

            # Sauvegarde dans tokens.json
            with open(token_file, "w") as f:
                json.dump(token_data, f, indent=4)

            return token_data
    else:
            print(f"Erreur {response.status_code} : {response.text}")
            return None    
    
## Utilise les fonctions check et refresh 
def get_valid_token(client_id, client_secret, access_token, refresh_token, expires_at, token_file):
    if not check_token(access_token, expires_at, activities_url):
        token_data = refresh_access_token(client_id, client_secret, refresh_token, token_file)
        if token_data:
            return token_data["access_token"]
        else:
            return None
    return access_token

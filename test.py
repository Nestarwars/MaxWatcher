import requests
import time
import datetime
from trajets import *

# api_links = [
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=100&refine=origine%3A%22PARIS%20(intramuros)%22&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=100&refine=destination%3A%22LYON%20(intramuros)%22&refine=origine%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=20&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22MASSY%20TGV%22',
# ]


# response = requests.get("https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=100&refine=origine%3A%22PARIS%20(intramuros)%22&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22")

# result = response.json()

# for line in result["results"] :
#     print('-'.join([line['date'],line['heure_depart']]))

# for line in result['results'] :
#     trajet = Trajet(line)
#     print(trajet)

# trajet1 = Trajet(result["results"][0])
# trajet2 = Trajet(result["results"][1])

# print(trajet1)
# print(trajet2)
# print(trajet1==trajet2)
# print(trajet1>t rajet2)

# T = TrajetsTGVmax([])
# T.get(api_links)

# print(T.select_date("13-05-2024").sorted())

import requests
from datetime import datetime
import json

def get_sncf_trains(departure_station, arrival_station, travel_date):
    # Clé API SNCF (inscription nécessaire sur https://api.sncf.com)
    API_KEY = 'votre-cle-api'
    
    # Fonction pour rechercher l'ID d'une gare par son nom
    def get_station_id(station_name):
        # Encoder la clé API en base64 pour l'authentification
        auth = requests.auth.HTTPBasicAuth(API_KEY, '')
        
        # URL de l'API pour rechercher les gares
        url = f"https://api.sncf.com/v1/coverage/sncf/places?q={station_name}"
        
        response = requests.get(url, auth=auth)
        data = response.json()
        
        # Récupérer l'ID de la première gare correspondante
        if 'places' in data and len(data['places']) > 0:
            return data['places'][0]['id']
        return None

    # Convertir les noms de gares en IDs
    departure_id = get_station_id(departure_station)
    arrival_id = get_station_id(arrival_station)
    
    if not departure_id or not arrival_id:
        return "Gare non trouvée"

    # Formater la date pour l'API
    date_formatted = travel_date.strftime("%Y%m%dT000000")
    
    # URL de l'API pour rechercher les trajets
    url = f"https://api.sncf.com/v1/coverage/sncf/journeys"
    
    # Paramètres de la requête
    params = {
        "from": departure_id,
        "to": arrival_id,
        "datetime": date_formatted,
        "data_freshness": "realtime"
    }
    
    # Authentification avec la clé API
    auth = requests.auth.HTTPBasicAuth(API_KEY, '')
    
    # Effectuer la requête
    response = requests.get(url, auth=auth, params=params)
    
    if response.status_code != 200:
        return f"Erreur lors de la requête: {response.status_code}"
    
    data = response.json()
    
    # Liste pour stocker les résultats
    available_trains = []
    
    # Parcourir les trajets trouvés
    for journey in data.get('journeys', []):
        for section in journey.get('sections', []):
            if section.get('type') == 'public_transport':
                train_info = {
                    'departure_time': section['departure_date_time'],
                    'arrival_time': section['arrival_date_time'],
                    'train_number': section.get('display_informations', {}).get('headsign', ''),
                    'train_type': section.get('display_informations', {}).get('commercial_mode', ''),
                }
                
                # Vérifier la disponibilité des places MaxJeune
                fares = journey.get('fare', {}).get('links', [])
                for fare in fares:
                    if 'MaxJeune' in fare.get('id', ''):
                        train_info['maxjeune_available'] = True
                        train_info['price'] = fare.get('price', {}).get('value', 'N/A')
                        break
                else:
                    train_info['maxjeune_available'] = False
                    
                available_trains.append(train_info)
    
    return available_trains

# Exemple d'utilisation
if __name__ == "__main__":
    departure = input("Gare de départ: ")
    arrival = input("Gare d'arrivée: ")
    date_str = input("Date du voyage (format: YYYY-MM-DD): ")
    
    try:
        travel_date = datetime.strptime(date_str, "%Y-%m-%d")
        results = get_sncf_trains(departure, arrival, travel_date)
        
        if isinstance(results, list):
            print("\nTrajets disponibles:")
            for train in results:
                departure_time = datetime.strptime(train['departure_time'], "%Y%m%dT%H%M%S").strftime("%H:%M")
                arrival_time = datetime.strptime(train['arrival_time'], "%Y%m%dT%H%M%S").strftime("%H:%M")
                
                print(f"\nTrain {train['train_type']} {train['train_number']}")
                print(f"Départ: {departure_time} - Arrivée: {arrival_time}")
                if train['maxjeune_available']:
                    print(f"Tarif MaxJeune disponible: {train['price']}€")
                else:
                    print("Tarif MaxJeune non disponible")
        else:
            print(results)
            
    except ValueError:
        print("Format de date invalide")
import requests
import time
import datetime
from trajets import *

api_links = [
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=100&refine=origine%3A%22PARIS%20(intramuros)%22&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=100&refine=destination%3A%22LYON%20(intramuros)%22&refine=origine%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=20&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22MASSY%20TGV%22',
]


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

T = TrajetsTGVmax([])
T.get(api_links)

print(T.select_date("13-05-2024").sorted())
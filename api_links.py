import requests
import pickle

ParisLyon_api_links = [
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22PARIS%20(intramuros)%22&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=destination%3A%22LYON%20(intramuros)%22&refine=origine%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22MASSY%20TGV%22',
]

LyonParis_api_links = [
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22PARIS%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
    'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22MASSY%20TGV%22',
]

api_prefix = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=od_happy_card%3A%22OUI%22"

stations_link = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?select=origine&group_by=origine&limit=-1"


def api_format(name):
    api_name = "%3A%22" + name.replace(" ","%20") + "%22"
    return api_name

class Stations:
    def __init__(self) -> None:
        try : 
            response = requests.get(stations_link).json()
            stations = []
            for entry in response["results"]:
                if not entry['origine'] == None : 
                    stations.append(entry['origine'])
        except requests.exceptions.ConnectionError:
            with open('__pycache__/stations_backup.pickle','rb') as f:
                stations = pickle.load(f)
        self.list = stations
        self.api_names = {}
        for station in self.list :
            self.api_names[station] = api_format(station)

    def __repr__(self):
        string = ""
        for i,station in enumerate(self.list) :
            string += f"{i}".rjust(4) + f" | {station} \n" 
        return string

    def api_link_from_stations(self, org, dest):
        if org not in self.list or dest not in self.list :
            raise ValueError("No such station")
        org_api     = self.api_names[org]
        dest_api    = self.api_names[dest]
        return api_prefix + "&refine=origine" + org_api + "&refine=destination" + dest_api
         


if __name__ == "__main__":
    S = Stations()
    
    with open("__pycache__/stations_backup.pickle",'wb') as f :
        pickle.dump(S.list, f)

    print(S.api_link_from_stations("LYON (intramuros)", "PARIS (intramuros)"))
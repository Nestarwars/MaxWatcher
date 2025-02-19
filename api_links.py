import requests
import pickle

# ParisLyon_api_links = [
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22PARIS%20(intramuros)%22&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=destination%3A%22LYON%20(intramuros)%22&refine=origine%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=destination%3A%22LYON%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22MASSY%20TGV%22',
# ]

# LyonParis_api_links = [
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22PARIS%20(intramuros)%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22MARNE%20LA%20VALLEE%20CHESSY%22&refine=od_happy_card%3A%22OUI%22',
#     'https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=od_happy_card%3A%22OUI%22&refine=origine%3A%22LYON%20(intramuros)%22&refine=destination%3A%22MASSY%20TGV%22',
# ]

stations_groups = {
    'GRAND_PARIS' : ["PARIS (intramuros)", "MASSY TGV", "MARNE LA VALLEE CHESSY"],
    'GRAND_LYON' : ["LYON (intramuros)", "LYON-SAINT EXUPERY TGV"],
}

api_prefix = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?limit=-1&refine=od_happy_card%3A%22OUI%22"

stations_link = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/tgvmax/records?select=origine&group_by=origine&limit=-1"

def api_format(name):
    api_name = "%3A%22" + name.replace(" ","%20") + "%22"
    return api_name

class Stations:
    def __init__(self, list=[]) -> None:
        self.list = list
        self.api_names = {}
        for station in self.list :
            self.api_names[station] = api_format(station) 

    def get_stations(self) :
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

    def api_links_from_stations(self, orgs, dests):
        api_links = []
        for org in orgs:
            for dest in dests:
                if org not in self.list or dest not in self.list :
                    raise ValueError("No such station" + org + dest)
                org_api     = self.api_names[org]
                dest_api    = self.api_names[dest]
                api_links.append(api_prefix + "&refine=origine" + org_api + "&refine=destination" + dest_api)
        return api_links
    
    def search(self, request):
        matching = [station for station in self.list if request in station]
        return Stations(matching)
    
class StationsGraph:
    def __init__(self):
        pass

    def add_station(self, station:str, destinations:dict):
        pass
    
    def find_paths(self, orig, dest):
        pass

    def quickest_path(self, orig, dest):
        pass

if __name__ == "__main__":
    S = Stations()
    S.get_stations()
    
    with open("__pycache__/stations_backup.pickle",'wb') as f :
        pickle.dump(S.list, f)

    print(S)
    print(" --- GARES SAUVEGARDEES --- \n")

    print(S.search("LYON"))
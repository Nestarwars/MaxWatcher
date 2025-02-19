import datetime
import requests

def OrdonneHeureDepart(liste_trajets):
    pass

class Trajet:
    def __init__(self, ligneTrajet):
        time_depart         = '/'.join([ligneTrajet['date'],ligneTrajet['heure_depart']])
        time_arrivee        = '/'.join([ligneTrajet['date'],ligneTrajet['heure_arrivee']])
        self.time_depart    = datetime.datetime.strptime(time_depart,'%Y-%m-%d/%H:%M')
        self.time_arrivee   = datetime.datetime.strptime(time_arrivee,'%Y-%m-%d/%H:%M')
        self.depart         = ligneTrajet["origine"]
        self.arrivee        = ligneTrajet["destination"]

    def __repr__(self) -> str:
        return ' | '.join([self.time_depart.strftime("%d-%m-%Y"),self.time_depart.strftime("%H:%M").ljust(10),self.time_arrivee.strftime("%H:%M").ljust(10),self.depart.ljust(30),self.arrivee.ljust(30)])
    
    def __gt__(self,other):
        return self.time_depart > other.time_depart
    
    def __ge__(self,other):
        return self.time_depart >= other.time_depart
    
    def __lt__(self,other):
        return self.time_depart < other.time_depart
    
    def __le__(self,other):
        return self.time_depart <= other.time_depart
    
    def __eq__(self,other):
        return self.time_depart == other.time_depart
    
    def duration(self):
        return self.time_arrivee - self.time_depart

####################################################

class TrajetsTGVmax:
    def __init__(self, liste_trajets=[]):
        self.liste_trajets = liste_trajets

    def get(self, api_links,limit_results=100000):
        liste_trajets = []
        for link in api_links : 
            response = requests.get(link).json()
            nbr_results = response['total_count']
            offset = 0
            while response['results'] != [] and limit_results > 0:
                for line in response['results']:
                    trajet = Trajet(line)
                    liste_trajets.append(trajet)
                offset += 100
                limit_results -= 100
                response = requests.get(link+'&offset='+str(offset)).json()
            
            # result = requests.get(link).json()['results']
            # for line in result :
            #     trajet = Trajet(line)
            #     liste_trajets.append(trajet)

        self.liste_trajets = liste_trajets

    def __repr__(self):
        r =  'DATE       | DEPART     | ARRIVEE    | GARE DEPART                    | GARE ARRIVEE                     \n'
        r += '---------------------------------------------------------------------------------------------------------\n'
        for trajet in self.liste_trajets :
            r += str(trajet) + '\n'
        r += '---------------------------------------------------------------------------------------------------------\n'
        r += ' TOTAL TRAJETS DISPO MAXJEUNE : '+str(len(self.liste_trajets))
        return r
    
    def size(self):
        return len(self.liste_trajets)
    
    def sorted(self):
        return TrajetsTGVmax(sorted(self.liste_trajets))
    
    def remove_double(self):
        clean_list = []
        for trajet in self.liste_trajets:
            flag = False
            for ref in clean_list :
                if ref.time_depart == trajet.time_depart and ref.depart == trajet.depart and ref.arrivee == trajet.arrivee :
                    flag = True
            if not flag :
                clean_list.append(trajet)
        return TrajetsTGVmax(clean_list)
    
    def select_date(self,date_str,format="%d-%m-%Y"):
        selected_date = datetime.datetime.strptime(date_str,format)
        selected_trajets = []
        for trajet in self.liste_trajets:
            if trajet.time_depart.strftime("%d-%m-%Y") == selected_date.strftime("%d-%m-%Y"):
                selected_trajets.append(trajet)
        return TrajetsTGVmax(selected_trajets)  

    def select_from_hour(self,hour_str,format="%H"):
        selected_hour = datetime.datetime.strptime(hour_str,format)
        selected_trajets = []
        for trajet in self.liste_trajets:
            if trajet.time_depart.hour >= selected_hour.hour:
                selected_trajets.append(trajet)
        return TrajetsTGVmax(selected_trajets)
    
############################

class Itineraire:
    def __init__(self,stops):
        pass



############################

if __name__ == '__main__' :
    from api_links import *
    trajets_test = TrajetsTGVmax()

    trajets_test.get([api_prefix],limit_results=300)

    print(trajets_test)

    trajetA = trajets_test.liste_trajets[0]

    print(trajetA)
    print(trajetA.duration())
    pass
from trajets import *
from api_links import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--orig',  dest='origin'     , type=str, default='LYON (intramuros)')
parser.add_argument('--dest',  dest='destination', type=str, default='PARIS (intramuros)')
parser.add_argument('--date',  dest='date'       , type=str, default='')
parser.add_argument('--fhour', dest='fhour'      , type=str, default='')
parser.add_argument('--search',dest='search'     , type=str, default='')

if __name__ == '__main__':
    args = parser.parse_args()
    stations = Stations()
    stations.get_stations()
    output = TrajetsTGVmax()

    if args.search :
        print(stations.search(args.search))
        
        exit()
        
    if args.origin in stations_groups :
        origins = stations_groups[args.origin]
    else : 
        origins = [args.origin]
    
    if args.destination in stations_groups :
        destinations = stations_groups[args.destination]
    else : 
        destinations = [args.destination]

    if args.destination or args.origin or args.date: 
        if args.origin in stations_groups :
            origins = stations_groups[args.origin]
        else : 
            origins = [args.origin]
        
        if args.destination in stations_groups :
            destinations = stations_groups[args.destination]
        else : 
            destinations = [args.destination]

        api_links = stations.api_links_from_stations(origins, destinations)
        
        output.get(api_links)
        # if args.destination == 'paris':
        #     output = TrajetsTGVmax()
        #     output.get(LyonParis_api_links)
        # if args.destination == 'lyon':
        #     output = TrajetsTGVmax()
        #     output.get(ParisLyon_api_links)
        if args.date :
            dates = args.date.split('+')
            for date in dates :
                filtered = output.select_date(date)
                if args.fhour != '':
                    print(filtered.select_from_hour(args.fhour).sorted().remove_double())
                    print('\n')
                else :
                    print(filtered.sorted().remove_double())
                print('\n')
        else:
            print(output.sorted().remove_double())
        
    else : 
        print(stations.search(args.search.upper()))
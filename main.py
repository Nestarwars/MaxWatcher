from trajets import *
from api_links import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dest', dest='destination', type=str, default='paris')
parser.add_argument('--date', dest='date'       , type=str, default='')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.destination == 'paris':
        output = TrajetsTGVmax()
        output.get(LyonParis_api_links)
    if args.destination == 'lyon':
        output = TrajetsTGVmax()
        output.get(ParisLyon_api_links)
    if args.date != '':
        output = output.select_date(args.date)
    print(output.sorted().remove_double())

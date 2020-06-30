from pprint import pprint
from datetime import datetime

import pymongo
import csv
import re


def read_data(artist_info, csv_name):
    with open(csv_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            line['Цена'] = int(line['Цена'])
            line['Дата'] = datetime.strptime(f'{line["Дата"]}.2020', '%d.%m.%Y')
            result = artist_info.insert_one(line)

    return result


def find_cheapest(artist_info):
    return list(artist_info.find().sort("Цена", pymongo.ASCENDING))[0]


def find_by_name(artist_info, artist_name):
    raw_name = r'{}'.format(artist_name)
    regex_name = re.compile(raw_name)
    result = artist_info.find({'Исполнитель': {'$in': [regex_name]}})
    return list(result.sort("Цена", pymongo.ASCENDING))


def sort_by_date(artist_info):
    return list(artist_info.find().sort("Дата", pymongo.ASCENDING))


if __name__ == '__main__':
    client = pymongo.MongoClient()
    db_client = client['test_db']

    print('Заполнение БД...')
    artist_info = db_client['artist']
    read_data(artist_info, 'artists.csv')
    print()

    print('Поиск самого дешевого билета...')
    cheapest_ticket = find_cheapest(artist_info)
    pprint(cheapest_ticket)
    print()

    print('Сортировка базы по дате мерприятия...')
    pprint(sort_by_date(artist_info))
    print()

    print('Поиск билетов на исполнителя...')
    print('Test#1')
    pprint(find_by_name(artist_info, 'Звери'))
    print('Test#2')
    pprint(find_by_name(artist_info, 'Th'))
    print('Test#3')
    pprint(find_by_name(artist_info, 'Z'))

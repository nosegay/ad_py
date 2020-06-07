from collections import OrderedDict

import csv
import re


def read_csv(csv_file):
    with open(csv_file, encoding='utf8') as fp:
        rows = csv.reader(fp, delimiter=",")
        csv_data = list(rows)

    return csv_data


def write_csv(csv_file, headers, csv_data):
    with open(csv_file, 'w', newline='') as fp:
        fc = csv.DictWriter(fp, delimiter=',', fieldnames=headers)
        fc.writeheader()
        fc.writerows(csv_data)


def rewrite_phone(phone):
    if phone == '':
        return ''

    numbers = re.search('(7|8)+\D*([0-9]{3})\D*([0-9]{3})\D*([0-9]{2})\D*([0-9]{2})\D*([0-9]{1,5})?', phone)
    new_phone = f'+7({numbers.group(2)}){numbers.group(3)}-{numbers.group(4)}-{numbers.group(5)}'

    if numbers.group(6) is not None:
        new_phone += f' доб.{numbers.group(6)}'

    return new_phone


def add_field(_dict, field_name, value):
    if field_name not in _dict.keys() and value != '':
        _dict[field_name] = value


def form_contact(contacts_dict, contact_data):
    names = ' '.join(contact_data[0:3]).strip()
    organization = contact_data[3]
    position = contact_data[4]
    phone = contact_data[5]
    email = contact_data[6]

    split_names = re.match('([\w]*)\s?([\w]*)\s?([\w]*)', names)
    if split_names.group(1) not in contacts_dict.keys():
        contacts_dict[split_names.group(1)] = dict()
        contacts_list[split_names.group(1)]['lastname'] = split_names.group(1)

    add_field(contacts_list[split_names.group(1)], 'firstname', split_names.group(2))
    add_field(contacts_list[split_names.group(1)], 'surname', split_names.group(3))
    add_field(contacts_list[split_names.group(1)], 'organization', organization)
    add_field(contacts_list[split_names.group(1)], 'position', position)
    add_field(contacts_list[split_names.group(1)], 'phone', rewrite_phone(phone))
    add_field(contacts_list[split_names.group(1)], 'email', email)


if __name__ == '__main__':
    raw_contacts_list = read_csv('phonebook_raw.csv')
    headers = raw_contacts_list[0]

    contacts_list = dict()
    for contact in raw_contacts_list[1:]:
        form_contact(contacts_list, contact)

    sorted_contacts = OrderedDict(sorted(contacts_list.items(), key=lambda x: x[0]))
    write_csv('phonebook.csv', headers, sorted_contacts.values())

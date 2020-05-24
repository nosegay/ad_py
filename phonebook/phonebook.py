class Contact:
    def __init__(self, name, surname, number, *args, **kwargs):
        self.name = name
        self.surname = surname
        self.number = number
        if len(args) == 0:
            self.favorite_contact = False
        else:
            self.favorite_contact = args[0]
        self.footnotes = dict()
        for param_name, param_value in kwargs.items():
            self.footnotes[param_name] = param_value

    def __str__(self):
        contact_str = f'Имя: {self.name}\n' \
                      f'Фамилия: {self.surname}\n' \
                      f'Телефон: {self.number}\n'

        contact_str += 'В избранных: '
        if self.favorite_contact:
            contact_str += str(self.favorite_contact)
        else:
            contact_str += 'нет'

        contact_str += f'\nДополнительная информация:'
        if len(self.footnotes) == 0:
            contact_str += ' нет'
        else:
            contact_str += '\n'
            for param_name, param_value in self.footnotes.items():
                contact_str += f'\t\t{param_name} : {param_value}\n'

        return contact_str


class PhoneBook:
    def __init__(self, title):
        self.title = title
        self.contacts = list()

    def show_contacts(self):
        output = '__Телефонная книга__\n'
        output += f'Всего контактов: {len(self.contacts)}\n\n'
        for ctr, person in enumerate(self.contacts):
            output += f'Контакт #{ctr+1}\n'
            output += str(person)
            output += '\n'

        print(output)

    def add_contact(self, name, *args, **kwargs):
        if isinstance(name, Contact):
            self.contacts.append(name)
        else:
            new_contact = Contact(name, *args, **kwargs)
            self.contacts.append(new_contact)

    def delete_contact_by_number(self, number):
        person = None
        for contact in self.contacts:
            if contact.number == number:
                person = contact

        if person is None:
            print(f'Контакта с номером {number} в телефонной книге не найдено.\n')
        else:
            self.contacts.remove(person)
            print(f'Из телефонной книги удален следующий контакт:\n{person}\n')

    def find_all_favorite_numbers(self):
        favorite_list = list()
        for contact in self.contacts:
            if contact.favorite_contact:
                favorite_list.append(contact.favorite_contact)

        return favorite_list

    def find_contact(self, name, surname):
        for contact in self.contacts:
            if contact.name == name and contact.surname == surname:
                return contact

        return 'Контакт не найден'

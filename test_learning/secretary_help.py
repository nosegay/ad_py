from pprint import pprint


DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

DIRECTORIES = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006', '5400 028765', '5455 002299'],
    '3': []
}


class SecretaryHelper:
    def __init__(self):
        self.documents = DOCUMENTS.copy()
        self.directories = DIRECTORIES.copy()

    def get_doc_info(self, number):
        for doc in self.documents:
            if doc['number'] == number:
                return doc

        return None

    @staticmethod
    def command_help():
        print('p - people - по номеру документа вывести его владельца\n'
              'l - list - вывести всю доступную информацию по документам\n'
              's - shelf -  по номеру документа вывести полку, на которой он находится\n'
              'a - add - добавление нового документа в каталог и на полку\n'
              'd - delete - полное удаление документа по его номеру\n'
              'm - move - перемещение документа на новую полку\n'
              'as - add shelf - добавление нового документа\n'
              'ls - list shelf - вывод перечня полок\n'
              'q - quit - выход из программы')

    def get_doc_owner(self):
        doc_number = input('\tВведите номер документа: ')
        doc_info = self.get_doc_info(doc_number)
        if self.get_doc_info(doc_number) is None:
            print('\tДокумента с таким номер в базе не найдено!')
        else:
            print(f'\t{doc_info["name"]}')

    def list_all_docs(self):
        for doc in self.documents:
            output_str = '\t'
            for param in doc.values():
                output_str += param + ' '
            print(output_str)

    def get_doc_location(self):
        doc_number = input('\tВведите номер документа: ')
        shelf = self.find_doc_shelf(doc_number)
        if shelf is not None:
            print(f'\t{shelf}')
        else:
            print('\tДокумента с таким номером не найдено!')

    def find_doc_shelf(self, doc_number):
        for shelf in self.directories:
            if doc_number in self.directories[shelf]:
                return shelf

        return None

    def add_new_doc(self):
        print('\tДля добавления нового документа укажите следующие параметры:')
        doc_number = input('\tномер документа: ')
        while self.get_doc_info(doc_number) is not None:
            print('\t\tДокумент с таким номером уже существует!')
            substitute_flag = input('\t\tЗаменить на новый (y/n)? ').lower()
            if substitute_flag == 'n':
                doc_number = input('\t\tвведите другой номер документа: ')
            else:
                break

        doc_type = input('\tтип документа: ')
        owner_name = input('\tимя владельца: ')
        shelf_number = input('\tномер полки, на которую документ будет помещен: ')
        while shelf_number not in self.directories.keys():
            print('\t\tТакой полки не найдено!')
            shelf_add_flag = input('\t\tДобавить полку в учет (y/n)? ').lower()
            if shelf_add_flag == 'n':
                shelf_number = input('\t\tвведите номер полки заново: ')
            else:
                self.directories[shelf_number] = list()
                break

        self.documents.append({"type": doc_type, "number": doc_number, "name": owner_name})
        self.directories[shelf_number].append(doc_number)

    def delete_doc(self):
        doc_number = input('\tВведите номер документа: ')
        doc_info = self.get_doc_info(doc_number)
        if doc_info is None:
            print('\tДокумента с указанным номером в базе не найдено!')
        else:
            self.documents.remove(doc_info)
            shelf = self.find_doc_shelf(doc_number)
            self.directories[shelf].remove(doc_number)

    def change_doc_location(self):
        doc_number = input('\tВведите номер документа: ')
        for shelf in self.directories:
            if doc_number in self.directories[shelf]:
                shelf_number = input('\tУкажите номер целевой полки: ')
                if shelf_number not in self.directories.keys():
                    new_shelf_flag = input('\tУказанная полка не подучетна. Добавить (y/n)? ')
                    if new_shelf_flag == 'y':
                        self.directories[shelf].remove(doc_number)
                        self.directories[shelf_number] = [doc_number]
                    else:
                        return
                else:
                    self.directories[shelf].remove(doc_number)
                    self.directories[shelf_number].append(doc_number)
                return

        print('\tУказанного документа не найдено в системе хранения!')

    def add_shelf(self):
        shelf_number = input('\tВведите номер новой полки: ')
        if shelf_number in self.directories.keys():
            print('\tПолка с таким номером уже существует!')
        else:
            self.directories[shelf_number] = list()

    def list_all_shelfs(self):
        pprint(self.directories)


if __name__ == '__main__':
    helper = SecretaryHelper()
    command = input('Введите команду (h - для вывода доступного списка команд): ')
    while not command == 'q':
        if command == 'h':
            helper.command_help()
        elif command == 'p':
            helper.get_doc_owner()
        elif command == 'l':
            helper.list_all_docs()
        elif command == 's':
            helper.get_doc_location()
        elif command == 'a':
            helper.add_new_doc()
        elif command == 'd':
            helper.delete_doc()
        elif command == 'm':
            helper.change_doc_location()
        elif command == 'as':
            helper.add_shelf()
        elif command == 'ls':
            helper.list_all_shelfs()
        elif command == 'q':
            break

        command = input('Введите команду (h - для вывода доступного списка команд): ')

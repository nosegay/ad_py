import phonebook


contact_1 = phonebook.Contact('Василий', 'Иванов', 89213457896, email='vivanov@post.ru')
contact_2 = phonebook.Contact('Пётр', 'Сидоров', 756392, 89213457896, email='sidorov@post.ru', vk='vk.com/1234455433',
                              home=998877)

telephone_book = phonebook.PhoneBook('Новая телефонная книга')
telephone_book.add_contact(contact_1)
telephone_book.add_contact(contact_2)
telephone_book.add_contact('Иван', 'Конюхов', 83246544466, 332211, email='ik@post.ru')
telephone_book.add_contact('Unknown', 'number', 88001239090)
telephone_book.show_contacts()

telephone_book.delete_contact_by_number(88001239090)
telephone_book.show_contacts()

print('Список избранных номеров:')
print(telephone_book.find_all_favorite_numbers())
print()

print('Поиск контакта: Василий Иванов')
print(telephone_book.find_contact('Василий', 'Иванов'))


print('Поиск контакта: Ульяна Иванова')
print(telephone_book.find_contact('Ульяна', 'Иванова'))

from vkinder import VKinder, API_VK
from vkinder_user import VKinderUser
from vkinder_db.db_functionality import VKinderDB

import json


def launch_vkinder_app():
    print('Добро пожаловать во VKinder!')
    user_id, token = VKinder.app_enter()

    main_user = VKinderUser(user_id, token)
    running_VKinder = VKinder(main_user)

    main_user_id = VKinderDB.get_existent_user(running_VKinder.user)
    if main_user_id is not None:
        print(f'С возвращением, {running_VKinder.user.name}!')
    else:
        unknown_fields = running_VKinder.user.get_extended_info()
        print(f'Здравствуйте, {running_VKinder.user.name}!')
        if unknown_fields:
            running_VKinder.user.ask_extended_info()
        VKinderDB.add_user(running_VKinder.user)
        print('Поздравляем! Вы успешно добавлены в базу')

    print('Поиск подходящих людей...')
    offset = VKinderDB.count_suggestions()

    json_output = list()
    partner_list = list()
    for partner in running_VKinder.search_partner(offset):
        if len(partner_list) == 10:
            break

        partner_user = VKinderUser(partner['id'], running_VKinder.user.token, name=f'{partner["first_name"]} '
                                   f'{partner["last_name"]}')
        if partner_user.get_photos() == -1:
            continue

        partner_list.append(partner_user)
        json_output.append(partner_user.get_dict())

        VKinderDB.add_suggestion(**partner_user.get_dict())

    with open(f'{running_VKinder.user.id}.json', 'w') as f:
        json.dump(json_output, f, indent=2)

    print('Для Вас сформирован список потенциальных партнеров.')


def main():
    if API_VK is None:
        print('Для корректной работы программы в коде должен быть задан ID приложения '
              '(<API_VK>, module "vkinder.py", line 18)')
        exit(1)
    launch_vkinder_app()


if __name__ == '__main__':
    main()

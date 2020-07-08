from vkinder import VKinder
from vkinder_user import VKinderUser
from vkinder_db.db_functionality import VKinderDB
from pathlib import Path

import json


def launch_vkinder_app(api_id, db_name, db_user, db_user_pwd, token, user_id):
    print('Добро пожаловать во VKinder!')
    if token is None:
        try:
            user_id, token = VKinder.app_enter(api_id)
        except VKinder.Error as e:
            print(e)
            return

        write_config(api_id, db_name, db_user, db_user_pwd, token, user_id)

    main_user = VKinderUser(user_id, token)
    running_VKinder = VKinder(main_user)

    vki_db = VKinderDB(db_name, db_user, db_user_pwd)

    main_user_id = vki_db.get_existent_user(running_VKinder.user)
    if main_user_id:
        print(f'С возвращением, {running_VKinder.user.name}!')
    else:
        unknown_fields = running_VKinder.user.get_extended_info()
        print(f'Здравствуйте, {running_VKinder.user.name}!')
        if unknown_fields:
            running_VKinder.user.ask_extended_info()
        vki_db.add_user(running_VKinder.user)
        print('Поздравляем! Вы успешно добавлены в базу')

    print('Поиск подходящих людей...')
    offset = vki_db.count_suggestions(running_VKinder.user.vk_id)

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

        vki_db.add_suggestion(running_VKinder.user.vk_id, **partner_user.get_dict())

    with open(f'{running_VKinder.user.vk_id}.json', 'w') as f:
        json.dump(json_output, f, indent=2)

    print('Для Вас сформирован список потенциальных партнеров.')


def read_config():
    with open('config.json', encoding='utf8') as fp:
        json_data = json.load(fp)

    api_id = json_data['api_id']
    db_name = json_data['db_name']
    db_user = json_data['db_user']
    db_user_pwd = json_data['db_user_pwd']
    try:
        user_token = json_data['user_token']
        user_id = json_data['user_id']
    except KeyError:
        user_token = None
        user_id = None

    return api_id, db_name, db_user, db_user_pwd, user_token, user_id


def write_config(api_id, db_name, db_user, db_user_pwd, user_token, user_id):
    with open('config.json', 'w', encoding='utf8') as fp:
        json.dump({'api_id': api_id, 'db_name': db_name, 'db_user': db_user,
                   'db_user_pwd': db_user_pwd, 'user_token': user_token, 'user_id': user_id},
                  fp, indent=4)


def main():
    api_id, db_name, db_user, db_user_pwd, user_token, user_id = read_config()

    if api_id is None:
        print('Для корректной работы программы в файле <config.json> должен быть задан ID приложения')
        exit(1)

    launch_vkinder_app(api_id, db_name, db_user, db_user_pwd, user_token, user_id)


if __name__ == '__main__':
    main()

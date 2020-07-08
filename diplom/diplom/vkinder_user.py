from datetime import datetime
from copy import deepcopy
from pprint import pprint
from vkinder import VKinder, Error
from dateutil.relativedelta import relativedelta


RELATION = {1: 'не женат/не замужем', 2: 'есть друг/есть подруга', 3: 'помолвлен/помолвлена', 4:'женат/замужем',
            5: 'всё сложно', 6: 'в активном поиске', 7: 'влюблён/влюблена', 8: 'в гражданском браке'}


class VKinderUser:
    def __init__(self, user_id, token=None, name=None, age=None, sex=None, city=None, status=None):
        self.token = token
        self.name = name
        self.age = age
        self.sex = sex
        self.city = city
        self.status = status
        if isinstance(user_id, int) or isinstance(user_id, str) and user_id.isdigit():
            self.vk_id = user_id
        else:
            self.get_id(user_id)
        self.photos = None

    def get_id(self, name):
        params = deepcopy(VKinder.params)
        params['user_ids'] = name

        resp = VKinder.execute(name, self.token, 'users.get', params)

        self.vk_id = resp.json()['response'][0]['vk_id']

    def get_extended_info(self):
        params = deepcopy(VKinder.params)
        params['fields'] = ','.join(['bdate', 'sex', 'city', 'relation'])
        params['user_ids'] = self.vk_id

        resp = VKinder.execute(self.vk_id, self.token, 'users.get', params)
        unknown_fields = False

        self.name = f"{resp.json()['response'][0]['first_name']} {resp.json()['response'][0]['last_name']}"
        try:
            bdate = datetime.strptime(resp.json()['response'][0]['bdate'], '%d.%m.%Y')
            self.age = relativedelta(datetime.today(), bdate).years
        except ValueError or KeyError:
            unknown_fields = True

        if resp.json()['response'][0]['sex'] == 0:
            unknown_fields = True
        else:
            self.sex = resp.json()['response'][0]['sex']

        try:
            self.city = resp.json()['response'][0]['city']['vk_id']
        except KeyError:
            unknown_fields = True

        if resp.json()['response'][0]['relation'] == 0:
            unknown_fields = True
        else:
            self.status = resp.json()['response'][0]['relation']

        return unknown_fields

    def ask_extended_info(self):
        print('Для формировани профиля и поиска лучшего партнера требуется чуть больше информации о Вас.')
        if self.age is None:
            while True:
                try:
                    self.age = int(input('\tВаш возраст '))
                    break
                except ValueError:
                    print('Возраст должен быть указан арабскими цифрами')

        if self.sex == 0:
            while True:
                sex = input('\tВаш пол (м/ж) ').lower()
                if self.sex == 'м' or self.sex == 'ж':
                    break
                else:
                    print('Введите "м" или "ж"')
            self.sex = 1 if sex == 'ж' else 2

        if self.city is None:
            while True:
                city = input('\tгород, в котором живёте ').capitalize()
                params = deepcopy(VKinder.params)
                params['country_id'] = 1
                params['q'] = city
                params['count'] = '1'
                try:
                    resp = VKinder.execute(self.vk_id, self.token, 'database.getCities', params)
                    self.city = resp.json()['response']['items'][0]['id']
                    break
                except:
                    print('\t\tУказанный город не найден. Пожалуйста, повторите ввод.')

        if self.status is None:
            print('Введите своё семейное положение (выберите из списка)')
            pprint(RELATION)
            while True:
                try:
                    status = int(input('\tсвоё семейное положение '))
                    if not 1 < status < 8:
                        raise ValueError
                    self.status = status
                    break
                except ValueError:
                    print('введите подходящую цифру')

    def get_photos(self):
        params = deepcopy(VKinder.params)
        params['owner_id'] = self.vk_id
        params['album_id'] = 'profile'
        params['extended'] = '1'
        params['photo_sizes'] = '1'

        try:
            resp = VKinder.execute(self.vk_id, self.token, 'photos.get', params)
        except Error as e:
            return -1
        photo_list = resp.json()['response']['items']

        if len(photo_list) < 3:
            return -1

        sorted_photos = sorted(photo_list, key=lambda k: k['likes']['count'] + k['comments']['count'])[:3]
        self.photos = [photo['sizes'][-1]['src'] for photo in sorted_photos]

    def get_dict(self):
        return dict(vk_user=str(self), photos=list(self.photos))

    def __str__(self):
        return f'https://vk.com/id{self.vk_id}'

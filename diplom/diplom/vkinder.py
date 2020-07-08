from copy import deepcopy
from requests.exceptions import ReadTimeout, ConnectTimeout
from urllib.parse import urlencode

import requests
import time
import re


class Error(Exception):
    pass


class VKinder:
    api_vk_url = 'https://api.vk.com/method/'
    vk_url = 'https://vk.com/'

    params = {
        'v': '5.61'
    }

    exec_params = {
        'v': '5.61',
        'code': ''
    }

    def __init__(self, main_user):
        self.user = main_user

    def search_partner(self, offset):
        params = deepcopy(VKinder.params)
        params['offset'] = offset
        params['count'] = '50'
        params['has_photo'] = '1'

        params['city'] = self.user.city
        params['sex'] = 2 if self.user.sex == 1 else 1
        params['age_from'] = self.user.age - 1
        params['age_to'] = self.user.age + 1
        params['status'] = self.user.status

        resp = VKinder.execute(self.user.vk_id, self.user.token, 'users.search', params)
        users_list = resp.json()['response']['items']

        return users_list


    @staticmethod
    def app_enter(api_id):
        try:
            user_id, token = VKinder.get_access_token(api_id)
        except Error as e:
            print(e)
            return

        return user_id, token

    @staticmethod
    def get_access_token(api_id):
            oauth_url = 'https://oauth.vk.com/authorize'
            oauth_params = {
                'client_id': api_id,
                'display': 'page',
                'scope': r'+'.join(['friend', 'groups', 'status', 'photos']),
                'response_type': 'token',
                'v': '5.52'
            }

            print('Для предоставления приложению доступа к вашим данным, пожалуйста, перейдите по ссылке:')
            print('?'.join((oauth_url, urlencode(oauth_params, safe='+'))))
            print('В открывшемся окне нажмите кнопку "Разрешить" '
                  'и скопируйте URL-адрес, на который Вы будете перенаправлены.')
            url = input('Вставьте скопированный URL: ')

            token_re = re.compile('access_token=[0-9a-zA-Z]*')
            try:
                token = token_re.search(url).group(0)[13:]
            except Exception:
                raise Error(f'Не удалось извлечь ключ доступа из предоставленного URL.')

            user_id_re = re.compile('user_id=[0-9]*')
            try:
                user_id = user_id_re.search(url).group(0)[8:]
            except Exception:
                raise Error(f'Не удалось извлечь ID пользователя из предоставленного URL.')
                return

            return user_id, token

    @staticmethod
    def execute(user_id, token, method, method_params):
        resp = VKinder.execute_with_timeout(token, method, method_params)

        if 'error' in resp.json():
            VKinder.check_errors(user_id, resp.json()['error']['error_code'], resp.json()['error']['error_msg'])

        return resp

    @staticmethod
    def execute_with_timeout(token, method, method_params):
        VKinder.exec_params['access_token'] = token
        VKinder.exec_params['code'] = f'return API.{method}({method_params});'
        read_timeout_flag = False

        while True:
            try:
                resp = requests.get(''.join((VKinder.api_vk_url, 'execute')), params=VKinder.exec_params)
            except (ReadTimeout, ConnectTimeout):
                if not read_timeout_flag:
                    print('Потеряна связь с сервером. Ожидание восстановления соединения.', end='')
                    read_timeout_flag = True
                else:
                    print('.', end='')

                time.sleep(1)
                continue

            if 'error' in resp.json() and resp.json()['error']['error_code'] == 6:
                time.sleep(0.1)
            else:
                return resp

        if read_timeout_flag:
            print(f'\r{" " * 100}', end='')

    @staticmethod
    def check_errors(user_id, error_code, description):
        if error_code == 18:
            raise Error(f'Пользователь {user_id} удален или заблокирован.')
        elif error_code == 15:
            raise Error(f'Страница пользователя {user_id} скрыта.')
        else:
            raise Error(description)

import unittest
import requests

URL = 'https://translate.yandex.net/api/v1.5/tr.json'
API_KEY = r'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'


class YandexTranslateTest(unittest.TestCase):

    @staticmethod
    def translate_it(text, from_lang, to_lang):
        params = {
            'key': API_KEY,
            'text': text,
            'lang': f'{from_lang}-{to_lang}',
        }
        response = requests.get('/'.join([URL, 'translate']), params=params)
        return response

    @staticmethod
    def detect_lang(text):
        params = {
            'key': API_KEY,
            'text': text,
        }
        response = requests.get('/'.join([URL, 'detect']), params=params)
        return response

    def test_check_response_code(self):
        response = self.translate_it('Работает ли этот API?', 'ru', 'en')
        self.assertEqual(response.status_code, 200)

    def test_detect_lang(self):
        response = self.detect_lang('Check language')
        self.assertEqual(response.json()['lang'], 'en')

    def test_neg_check_wrong_lang(self):
        response = self.translate_it('1234567890', 'rt', 'tr')
        self.assertIn('The specified translation direction is not supported', response.text)

    def test_neg_check_wrong_word(self):
        response = self.translate_it('0твет', 'ru', 'en')
        self.assertEqual(response.json()['text'][0], '0твет')


if __name__ == '__main__':
    unittest.main()

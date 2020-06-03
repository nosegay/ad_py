from selenium import webdriver
import unittest
import time


class YandexLoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.get('https://passport.yandex.ru/auth/')

    def test_right_page(self):
        xpath_login_label = '//*[@id="root"]/div/div/div[2]/div/div/div[3]' \
                            '/div[2]/div/div/div[1]/form/div[1]/div[1]/label'
        login_label = self.driver.find_element_by_xpath(xpath_login_label)
        self.assertEqual(login_label.text, 'Введите логин, почту или телефон')

    def neg_mail(self, email):
        xpath_login_field = '//*[@id="passp-field-login"]'
        login_field = self.driver.find_element_by_xpath(xpath_login_field)
        login_field.send_keys(email)

        xpath_login_button = '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/form/div[3]/button[1]'
        login_button = self.driver.find_element_by_xpath(xpath_login_button)
        login_button.click()

        time.sleep(1)

        xpath_neg_response = '//*[@id="root"]/div/div/div[2]/div/div/div[3]/div[2]/div/div/div[1]/form/div[1]/div[2]'
        neg_response = self.driver.find_element_by_xpath(xpath_neg_response)
        return neg_response

    def test_bad_email(self):
        neg_response = self.neg_mail('my_neg_test_mail@ya.ru')
        self.assertEqual(neg_response.text, 'Такой логин не подойдет')

    def test_not_exist_email_1(self):
        neg_response = self.neg_mail('io@ya.ru')
        self.assertEqual(neg_response.text, 'Логин введен некорректно или удален')

    def test_not_exist_email_2(self):
        neg_response = self.neg_mail('my-neg-test-mail@ya.ru')
        self.assertEqual(neg_response.text, 'Такого аккаунта нет')

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()

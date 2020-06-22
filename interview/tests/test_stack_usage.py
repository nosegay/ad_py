from .. import stack_usage
from unittest.mock import patch

import unittest


class StackUsageTester(unittest.TestCase):
    def test_1(self):
        self.assertEqual('Сбалансированно', stack_usage.main('(((([{}]))))'))

    def test_2(self):
        self.assertEqual('Сбалансированно', stack_usage.main('[([])((([[[]]])))]'))

    def test_3(self):
        self.assertEqual('Сбалансированно', stack_usage.main('{()}'))

    def test_4(self):
        self.assertEqual('Сбалансированно', stack_usage.main('{{[()]}}'))

    def test_5(self):
        self.assertEqual('Несбалансированно', stack_usage.main('}{}'))

    def test_6(self):
        self.assertEqual('Несбалансированно', stack_usage.main('{{[(])]}}'))

    def test_7(self):
        self.assertEqual('Несбалансированно', stack_usage.main('[[{())}]'))


if __name__ == '__main__':
    unittest.main()

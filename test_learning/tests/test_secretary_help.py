from .. import secretary_help
from unittest.mock import patch

import unittest
import io
import sys


class SecretaryHelpTester(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = secretary_help.SecretaryHelper()
        self.capturedOutput = io.StringIO()
        self.real_stdout = sys.stdout
        sys.stdout = self.capturedOutput

    def test_help(self):
        str_list = ['people', 'move', 'shelf', 'quit']
        self.helper.command_help()
        help_output = self.capturedOutput.getvalue()
        for x_str in str_list:
            self.assertTrue(x_str in help_output)

    def output_comparing(self, tested_func, input_value, pattern_str):
        with patch('test_learning.secretary_help.input', return_value=input_value):
            tested_func()
            self.assertEqual(pattern_str, self.capturedOutput.getvalue())

    def test_doc_owner(self):
        self.output_comparing(self.helper.get_doc_owner, '10006', '\tАристарх Павлов\n', )

    def test_doc_location(self):
        self.output_comparing(self.helper.get_doc_location, '10006', '\t2\n')

    def test_neg_doc_location(self):
        self.output_comparing(self.helper.get_doc_location, '124ed', '\tДокумента с таким номером не найдено!\n')

    def test_add_new_doc(self):
        new_doc = ['9876554', 'photo', 'Kate B.', '1']
        with patch('test_learning.secretary_help.input', side_effect=new_doc):
            self.helper.add_new_doc()

        self.assertDictEqual({"type": "photo", "number": "9876554", "name": "Kate B."}, self.helper.documents[-1])
        self.assertIn('9876554', self.helper.directories['1'])

        with patch('test_learning.secretary_help.input', return_value='9876554'):
            self.helper.delete_doc()

    def test_delete_doc(self):
        new_doc = ['9876554', 'photo', 'Kate B.', '1']
        with patch('test_learning.secretary_help.input', side_effect=new_doc):
            self.helper.add_new_doc()

        with patch('test_learning.secretary_help.input', return_value='9876554'):
            self.helper.delete_doc()

        self.assertIsNone(self.helper.get_doc_info('9876554'))
        self.assertNotIn('9876554', self.helper.directories['1'])

    def test_change_doc_location(self):
        input_info = ['5400 028765', '1']
        with patch('test_learning.secretary_help.input', side_effect=input_info):
            self.helper.change_doc_location()

        self.assertNotIn('5400 028765', self.helper.directories['2'])
        self.assertIn('5400 028765', self.helper.directories['1'])

    def test_shelf_adding(self):
        self.output_comparing(self.helper.add_shelf, '1', '\tПолка с таким номером уже существует!\n')

    def tearDown(self) -> None:
        sys.stdout = self.real_stdout


if __name__ == '__main__':
    unittest.main()

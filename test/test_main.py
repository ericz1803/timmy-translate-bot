import unittest

import sys
sys.path.append('../src')
from main import map_code_to_name, map_input_to_language_code

class TestMappingFunctions(unittest.TestCase):
    def test_code_to_name_correct(self):
        self.assertEqual(map_code_to_name('de'), 'German')

    def test_code_to_name_none(self):
        self.assertIsNone(map_code_to_name('German'))
        self.assertIsNone(map_code_to_name('dn'))

    def test_input_to_language_code_correct(self):
        self.assertEqual(map_input_to_language_code('de'), 'de')

    def test_input_to_language_code_conversion(self):
        self.assertEqual(map_input_to_language_code('German'), 'de')
        self.assertEqual(map_input_to_language_code('germaN'), 'de')

    def test_input_to_language_code_none(self):
        self.assertIsNone(map_input_to_language_code('dn'))
        self.assertIsNone(map_input_to_language_code('germen'))

if __name__ == '__main__':
    unittest.main()
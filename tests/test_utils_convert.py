import sys
import os
import unittest

sys.path.append(os.path.abspath('../r2api'))

import r2api.utilities.unit_conversion as uc

class KnownValues(unittest.TestCase):
    known_values_ing = (
        (('300', 'g'), (round(300 * .00220462, 2) * 16, 'oz')),
        (('2,7', 'kg'), (round(2.7 * 2.205, 2), 'lb')),
        (('1.5', 'litri'), (round(round(1.5 * 33.814, 2) / 32, 2), 'quart')),
        (('(5 o 6','n/a'), ('(5 o 6','n/a'))
    )
    known_values_name = (
        ('Farina 00 oppure 500 gr di farina senza glutine per dolci', 'Farina 00 oppure 1.1 lb di farina senza glutine per dolci'),
    )
    known_values_prep = (
        ('190°-200° C ', '374-392° F '),
        ('190-200° C ', '374-392° F '),
        ('300g', f"{round(300 * .00220462, 2)*16}oz"),
        ('1,5 litri', f"{round(round(1.5 * 33.814, 2) / 32, 2)} quart"),
        ('15,5-20,2 cm', f"{round(.3937 * 15.5, 2)}-{round(.3937 * 20.2, 2)} inches"),
    )
    known_values_simplify = (
        ((0.4, 'lb'), (0.4 * 16, 'oz')),
        ((10, 'fl oz'), (round(10/8, 2), 'cup')),
        ((50, 'fl oz'), (round(50/32, 2), 'quart')),
        ((20, 'inches'), (f"{20//12}'{20 % 12}''", 'feet and inches')),
        ((12, 'inches'), ("1'", 'feet'))
    )
    known_values_dot_zero = (
        (4.0, (True, bool)),
        (0.4, (False, bool)),
        ('yogurt', (False, bool)),
        (0, (False, bool)),
        ([], (False, bool))
    )

    def test_convert_ing_known_values(self):
        """convert_units_ing should give known results for known values"""
        for known_value, known_result in self.known_values_ing:
            result = uc.convert_units_ing(known_value[0], known_value[1])
            error_msg = f"{result[0]}, f{result[1]} not converted correctly to {known_value[0]}, {known_value[1]}"
            self.assertEqual(known_result, result, error_msg)
    
    def test_convert_name_known_values(self):
        """convert_units_name should give known results for known values"""
        for known_value, known_result in self.known_values_name:
            result = uc.convert_units_name(known_value)
            error_msg = f"{result[0]} not converted correctly to {known_value[1]}"
            self.assertEqual(known_result, result, error_msg)

    def test_convert_prep_known_values(self):
        """convert_units_prep should give known results for known values"""
        for known_value, known_result in self.known_values_prep:
            result = uc.convert_units_prep(known_value)
            error_msg = f"{result} not converted correctly to {known_value}"
            self.assertEqual(known_result, result)

    def test_simplify_units_known_values(self):
        """simplify_units should give known results for known values"""
        for known_value, known_result in self.known_values_simplify:
            result = uc.simplify_units(known_value[0], known_value[1])
            error_msg = f"{result[0]}, f{result[1]} not converted correctly to {known_value[0]}, {known_value[1]}"
            self.assertEqual(known_result, result, error_msg)    
    
    def test_float_dot_zero_known_values(self):
        """float_dot_zero should give known results for known values"""
        for known_value, known_result in self.known_values_dot_zero:
            result = uc.float_dot_zero(known_value)
            error_msg_equal = f"{result} not converted correctly to {known_result[0]}"
            error_msg_type = f"type of {result}, {type(result)}, not same as {known_result[1]}"
            self.assertEqual(known_result[0], result, error_msg_equal)
            self.assertIsInstance(result, known_result[1], error_msg_type)

class BadInputs(unittest.TestCase):
    def test_convert_prep_bad(self):
        """convert_unit_prep should raise a TypeError if parameter is not a string"""
        self.assertRaises(TypeError, uc.convert_units_prep, 5)

    def test_convert_ing_bad(self):
        """convert_unit_ing should raise a TypeError if parameter cannot be coerced into a string"""
        self.assertRaises(TypeError, uc.convert_units_ing, [])

    def test_convert_name_bad(self):
        """convert_unit_name should raise a TypeError if parameter is not a string"""
        self.assertRaises(TypeError, uc.convert_units_name, 5)

if __name__ == '__main__':
    unittest.main()
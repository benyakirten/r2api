import sys
import os
import json
import unittest
import bs4

sys.path.append(os.path.abspath('../r2api'))

import r2api.converter.giallo_zafferano as gz
from r2api.utilities.errors import ParsingError

file_path = os.path.abspath(os.path.dirname(__file__))
path_to_soup = os.path.join(file_path, "soups/GZSoup.html")
path_to_json = os.path.join(file_path, "recipes/GZRecipe.json")

path_to_wrong_soup = os.path.join(file_path, "soups/FCSoup.html")

# To not make requests, tests will read from a file
gzc = gz.GZConverter(path_to_soup, read_from_file = True)

with open(path_to_soup, 'r') as f:
    # Using a with/as statement will produce an inconsistent comprehension
    # of the soup if the html.parser is used
    soup = bs4.BeautifulSoup(f, 'lxml')

with open(path_to_json, 'r') as f:
    gz_json = json.load(f)

class KnownValues(unittest.TestCase):
    def test_ingredients_identification(self):
        """get_ingredients should give known results for known values"""
        parsed_ing = gzc.get_ingredients(soup)
        for idx in range(len(parsed_ing)):
            self.assertEqual(gz_json['ingredients'][idx], parsed_ing[idx])

    def test_preparation_identification(self):
        """get_preparation should give known results for known values"""
        parsed_prep = gzc.get_preparation(soup)
        for idx in range(len(parsed_prep)):
            self.assertEqual(gz_json['preparation'][idx], parsed_prep[idx])
    
    def test_private_parse_ingredients(self):
        """_parse_ingredients should give known results for known values"""
        soup_ingredients = soup.find_all("dd", {"class": "gz-ingredient"})
        for i in range(len(gz_json['ingredients'])):
            result_name, result_quantity, result_unit = gzc._parse_ingredients(soup_ingredients[i])
            known_json = gz_json['ingredients'][i]
            known_name, known_quantity, known_unit = known_json[0], known_json[1], known_json[2]
            self.assertEqual((result_name, result_quantity, result_unit), (known_name, known_quantity, known_unit))

class KnownQualities(unittest.TestCase):
    def test_recipe_qualities(self):
        """After instantiation, a recipe should have a name, image, ingredients and preparation"""
        self.assertIn('name', gzc.recipe, "recipe doesn't have a name")
        self.assertIn('image', gzc.recipe, "recipe doesn't have an image")
        self.assertIn('ingredients', gzc.recipe, "recipe doesn't have ingredients")
        self.assertIn('preparation', gzc.recipe, "recipe doesn't have preparation")

class IncorrectInput(unittest.TestCase):
    def test_bad_recipe(self):
        """The converter class should raise a a ParsingError if the recipe cannot be parsed"""
        self.assertRaises(ParsingError, gz.GZConverter, path_to_wrong_soup, read_from_file = True)
    
    def test_bad_type_ing(self):
        """The converter class method get_ingredients should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, gzc.get_ingredients, [])
    
    def test_bad_type_prep(self):
        """The converter class method get_preparation should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, gzc.get_preparation, [])
        

if __name__ == '__main__':
    unittest.main()
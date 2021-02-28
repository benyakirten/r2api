import sys
import os
import json
import unittest
import bs4
import re

sys.path.append(os.path.abspath('../r2api'))

import r2api.converter.molliche_di_zucchero as mz

file_path = os.path.abspath(os.path.dirname(__file__))
path_to_soup = os.path.join(file_path, "soups/MZSoup.html")
path_to_json = os.path.join(file_path, "recipes/MZRecipe.json")

path_to_wrong_soup = os.path.join(file_path, "soups/GZSoup.html")

# To not make requests, tests will read from a file
mz_converter = mz.MZConverter(path_to_soup, read_from_file = True)

with open(path_to_soup, 'r') as f:
    # Using a with/as statement will produce an inconsistent comprehension
    # of the soup if the html.parser is used
    soup = bs4.BeautifulSoup(f, 'html.parser')

with open(path_to_json, 'r') as f:
    mz_json = json.load(f)

class KnownValues(unittest.TestCase):
    def test_ingredients_identification(self):
        """get_ingredients should give known results for known values"""
        parsed_ing = mz_converter.get_ingredients(soup)
        for idx in range(len(parsed_ing)):
            self.assertEqual(mz_json['ingredients'][idx], parsed_ing[idx])

    def test_preparation_identification(self):
        """get_preparation should give known results for known values"""
        parsed_prep = mz_converter.get_preparation(soup)
        for idx in range(len(parsed_prep)):
            self.assertEqual(mz_json['preparation'][idx], parsed_prep[idx])

class KnownQualities(unittest.TestCase):
    def test_recipe_qualities(self):
        """After instantiation, a recipe should have a name, image, ingredients and preparation"""
        self.assertIn('name', mz_converter.recipe, "recipe doesn't have a name")
        self.assertIn('image', mz_converter.recipe, "recipe doesn't have an image")
        self.assertIn('ingredients', mz_converter.recipe, "recipe doesn't have ingredients")
        self.assertIn('preparation', mz_converter.recipe, "recipe doesn't have preparation")

class IncorrectInput(unittest.TestCase):
    def test_bad_recipe(self):
        """The converter class should raise a TypeError if the recipe cannot be parsed"""
        self.assertRaises(AttributeError, mz.MZConverter, path_to_wrong_soup, read_from_file = True)
    
    def test_bad_type_ing(self):
        """The converter class method get_ingredients should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, mz_converter.get_ingredients, [])
    
    def test_bad_type_prep(self):
        """The converter class method get_preparation should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, mz_converter.get_preparation, [])

class SimpleInstantiation(unittest.TestCase):
    sample_good_recipes = [
        "https://blog.giallozafferano.it/mollichedizucchero/torta-sofficissima/",
        "https://blog.giallozafferano.it/mollichedizucchero/pasta-al-forno-con-ragu-e-piselli/",
        "https://blog.giallozafferano.it/mollichedizucchero/pasta-con-pomodorini-e-tonno-ricetta-veloce/"
    ]

    sample_bad_recipes = [
        "https://ricette.giallozafferano.it/Strozzapreti-ai-frutti-di-mare.html",
        "https://www.fattoincasadabenedetta.it/ricetta/riso-al-latte-al-forno/",
        "https://www.fattoincasadabenedetta.it/ricetta/penne-arrabbiate-al-forno/"
    ]


    def test_requests_instantiation_good(self):
        """For recipes on the Molliche di Zucchero site, the converter successfully instantiates"""
        for recipe in self.sample_good_recipes:
            converter = mz.MZConverter(recipe)
            self.assertIsInstance(converter, mz.MZConverter)

    def test_instantiation_bad(self):
        """For recipes not on the Molliche di Zucchero site, the converter will throw in error"""
        for recipe in self.sample_bad_recipes:
            self.assertRaises(Exception, mz.MZConverter, recipe)

if __name__ == '__main__':
    unittest.main()
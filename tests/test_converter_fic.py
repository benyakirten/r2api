import sys
import os
import json
import unittest
import bs4
import re

sys.path.append(os.path.abspath('../'))

import r2api.converter.fatto_in_casa as fic

file_path = os.path.abspath(os.path.dirname(__file__))
path_to_soup = os.path.join(file_path, "soups/FCSoup.html")
path_to_json = os.path.join(file_path, "recipes/FCRecipe.json")

path_to_wrong_soup = os.path.join(file_path, "soups/GZSoup.html")

# To not make requests, tests will read from a file
fcc = fic.FCConverter(path_to_soup, read_from_file = True)

with open(path_to_soup, 'r') as f:
    # Using a with/as statement will produce an inconsistent comprehension
    # of the soup if the html.parser is used
    soup = bs4.BeautifulSoup(f, 'html.parser')

with open(path_to_json, 'r') as f:
    fic_json = json.load(f)

class KnownValues(unittest.TestCase):
    def test_image_identification(self):
        """get_image should give a known result for a known value"""
        parsed_image = fcc.get_image(soup)
        self.assertEqual(fic_json['image'], parsed_image)

    def test_ingredients_identification(self):
        """get_ingredients should give known results for known values"""
        parsed_ing = fcc.get_ingredients(soup)
        for idx in range(len(parsed_ing)):
            # This is a rather hack-y solution
            # But I can't figure out what's the problem
            # With the recipe - and, no, .strip() doesn't work for some reason
            if '\n' in parsed_ing[idx][0]:
                find_extra_chars = re.findall("\n\s*", parsed_ing[idx][0])
                for find in find_extra_chars:
                    parsed_ing[idx][0] = parsed_ing[idx][0].replace(find, '')
            self.assertEqual(fic_json['ingredients'][idx], parsed_ing[idx])

    def test_preparation_identification(self):
        """get_preparation should give known results for known values"""
        parsed_prep = fcc.get_preparation(soup)
        for idx in range(len(parsed_prep)):
            _prep = parsed_prep[idx].strip().replace("\n", "")
            _prep = re.sub(r'\s+', ' ', _prep)
            self.assertEqual(fic_json['preparation'][idx], _prep)

class KnownQualities(unittest.TestCase):
    def test_recipe_qualities(self):
        """After instantiation, a recipe should have a name, image, ingredients and preparation"""
        self.assertIn('name', fcc.recipe, "recipe doesn't have a name")
        self.assertIn('image', fcc.recipe, "recipe doesn't have an image")
        self.assertIn('ingredients', fcc.recipe, "recipe doesn't have ingredients")
        self.assertIn('preparation', fcc.recipe, "recipe doesn't have preparation")

class IncorrectInput(unittest.TestCase):
    def test_bad_recipe(self):
        """The converter class should raise an exception if the recipe cannot be parsed"""
        self.assertRaises(Exception, fic.FCConverter, path_to_wrong_soup, read_from_file = True)
    
    def test_bad_type_ing(self):
        """The converter class method get_ingredients should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, fcc.get_ingredients, [])
    
    def test_bad_type_prep(self):
        """The converter class method get_preparation should raise a TypeError if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(TypeError, fcc.get_preparation, [])

class SimpleInstantiation(unittest.TestCase):
    sample_good_recipes = [
        "https://www.fattoincasadabenedetta.it/ricetta/polentone-veloce/",
        "https://www.fattoincasadabenedetta.it/ricetta/riso-al-latte-al-forno/",
        "https://www.fattoincasadabenedetta.it/ricetta/penne-arrabbiate-al-forno/"
    ]

    sample_bad_recipes = [
        "https://ricette.giallozafferano.it/Strozzapreti-ai-frutti-di-mare.html",
        "https://ricette.giallozafferano.it/Bomboloni-al-forno.html",
        "https://ricette.giallozafferano.it/Polenta-concia.html"
    ]

    def test_requests_instantiation_good(self):
        """For recipes on the Fatto In Casa site, the converter successfully instantiates"""
        for recipe in self.sample_good_recipes:
            converter = fic.FCConverter(recipe)
            self.assertIsInstance(converter, fic.FCConverter)

    def test_instantiation_bad(self):
        """For recipes not on the Fatto In Casa site, the converter will throw in error"""
        for recipe in self.sample_bad_recipes:
            self.assertRaises(Exception, fic.FCConverter, recipe)

if __name__ == '__main__':
    unittest.main()
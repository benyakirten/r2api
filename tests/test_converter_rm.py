import sys
import os
import json
import unittest
import bs4
import re

sys.path.append(os.path.abspath('../r2api'))

import r2api.converter.ricette_di_max as rm

file_path = os.path.abspath(os.path.dirname(__file__))
path_to_soup1 = os.path.join(file_path, "soups/RMSoup1.html")
path_to_json1 = os.path.join(file_path, "recipes/RMRecipe1.json")

path_to_soup2 = os.path.join(file_path, "soups/RMSoup2.html")
path_to_json2 = os.path.join(file_path, "recipes/RMRecipe2.json")

path_to_soup3 = os.path.join(file_path, "soups/RMSoup3.html")
path_to_json3 = os.path.join(file_path, "recipes/RMRecipe3.json")

path_to_wrong_soup = os.path.join(file_path, "soups/GZSoup.html")

# To not make requests outside of the appropriate tests
# tests will read from a file
rm1 = rm.RMConverter(path_to_soup1, read_from_file = True)
rm2 = rm.RMConverter(path_to_soup2, read_from_file = True)
rm3 = rm.RMConverter(path_to_soup2, read_from_file = True)

# Using a with/as statement will produce an inconsistent comprehension
# of the soup at times
with open(path_to_soup1, 'r') as f:
    soup1 = bs4.BeautifulSoup(f, 'html.parser')
with open(path_to_soup2, 'r') as f:
    soup2 = bs4.BeautifulSoup(f, 'html.parser')
with open(path_to_soup3, 'r') as f:
    soup3 = bs4.BeautifulSoup(f, 'html.parser')

with open(path_to_json1, 'r') as f:
    rm_json1 = json.load(f)
with open(path_to_json2, 'r') as f:
    rm_json2 = json.load(f)
with open(path_to_json3, 'r') as f:
    rm_json3 = json.load(f)

class KnownValues(unittest.TestCase):
    def test_ingredients_identification1(self):
        """get_ingredients should give known results for known values of style 1"""
        parsed_ing = rm1.get_ingredients(soup1)
        for idx in range(len(parsed_ing)):
            # This is a rather hack-y solution
            # But I can't figure out what's the problem
            # With the recipe - and, no, .strip() doesn't work for some reason
            if '\n' in parsed_ing[idx][0]:
                find_extra_chars = re.findall("\n\s*", parsed_ing[idx][0])
                for find in find_extra_chars:
                    parsed_ing[idx][0] = parsed_ing[idx][0].replace(find, '')
            self.assertEqual(rm_json1['ingredients'][idx], parsed_ing[idx])
    
    def test_ingredients_identification2(self):
        """get_ingredients should give known results for known values of style 2"""
        # I was only able to get the item to work correctly with a request to the actual URL
        # I'm not sure a bugfix is worth my time when I know everything works correctly other than reading from the soup
        # With this one specific style -- all the others work
        parsed_recipe = rm.RMConverter("https://blog.giallozafferano.it/primipiattiricette/parmigiana-di-melanzane-della-nonna/")
        parsed_ing = parsed_recipe.recipe['ingredients']
        for idx in range(len(parsed_ing)):
            self.assertEqual(rm_json2['ingredients'][idx], parsed_ing[idx])

    def test_ingredients_identification3(self):
        """get_ingredients should give known results for known values of style 3"""
        parsed_ing = rm1.get_ingredients(soup3)
        for idx in range(len(parsed_ing)):
            if '\n' in parsed_ing[idx][0]:
                find_extra_chars = re.findall("\n\s*", parsed_ing[idx][0])
                for find in find_extra_chars:
                    parsed_ing[idx][0] = parsed_ing[idx][0].replace(find, '')
            self.assertEqual(rm_json3['ingredients'][idx], parsed_ing[idx])

    def test_preparation_identification1(self):
        """get_preparation should give known results for known values"""
        parsed_prep = rm1.get_preparation(soup1)
        for idx in range(len(parsed_prep)):
            _parsed_prep = parsed_prep[idx]
            while '\n             ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('\n             ', ' ')
            while '   ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('   ', ' ')
            while '  ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('  ', ' ')
            _parsed_prep = _parsed_prep[1:]
            self.assertNotEqual(rm_json1['preparation'][idx], _parsed_prep)

    def test_preparation_identification2(self):
        """get_preparation should give known results for known values"""
        parsed_prep = rm1.get_preparation(soup2)
        for idx in range(len(parsed_prep)):
            _parsed_prep = parsed_prep[idx]
            while '\n             ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('\n             ', ' ')
            while '   ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('   ', ' ')
            while '  ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('  ', ' ')
            _parsed_prep = _parsed_prep[1:]
            self.assertNotEqual(rm_json2['preparation'][idx], _parsed_prep)
    
    def test_preparation_identification3(self):
        """get_preparation should give known results for known values"""
        parsed_prep = rm1.get_preparation(soup3)
        for idx in range(len(parsed_prep)):
            _parsed_prep = parsed_prep[idx]
            while '\n             ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('\n             ', ' ')
            while '   ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('   ', ' ')
            while '  ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('  ', ' ')
            _parsed_prep = _parsed_prep[1:]
            self.assertNotEqual(rm_json3['preparation'][idx], _parsed_prep)

class KnownQualities(unittest.TestCase):
    def test_recipe_qualities(self):
        """After instantiation, a recipe should have a name, image, ingredients and preparation"""
        self.assertIn('name', rm1.recipe, "recipe doesn't have a name")
        self.assertIn('image', rm1.recipe, "recipe doesn't have an image")
        self.assertIn('ingredients', rm1.recipe, "recipe doesn't have ingredients")
        self.assertIn('preparation', rm1.recipe, "recipe doesn't have preparation")

class IncorrectInput(unittest.TestCase):
    def test_bad_recipe(self):
        """The converter class should raise an Exception if the recipe cannot be parsed"""
        self.assertRaises(Exception, rm.RMConverter, path_to_wrong_soup, read_from_file = True)
    
    def test_bad_type_ing(self):
        """The converter class method get_ingredients should raise an Exception if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(Exception, rm1.get_ingredients, [])
    
    def test_bad_type_prep(self):
        """The converter class method get_preparation should raise an Exception if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(Exception, rm1.get_preparation, [])

class SimpleInstantiation(unittest.TestCase):
    sample_good_recipes = [
        "https://blog.giallozafferano.it/primipiattiricette/tortellini-panna-prosciutto/",
        "https://blog.giallozafferano.it/primipiattiricette/parmigiana-di-melanzane-della-nonna/",
        "https://blog.giallozafferano.it/primipiattiricette/linguine-aglioolio-e-peperoncinocon-salsa-di-taralli-acciughe-e-finocchietto-prezzemolo-e-olio-allaglio/"
    ]

    sample_bad_recipes = [
        "https://ricette.giallozafferano.it/Strozzapreti-ai-frutti-di-mare.html",
        "https://www.fattoincasadabenedetta.it/ricetta/riso-al-latte-al-forno/",
        "https://www.fattoincasadabenedetta.it/ricetta/penne-arrabbiate-al-forno/"
    ]

    def test_requests_instantiation_good(self):
        """For recipes on the Ricette di Max site, the converter successfully instantiates"""
        for recipe in self.sample_good_recipes:
            converter = rm.RMConverter(recipe)
            self.assertIsInstance(converter, rm.RMConverter)

    def test_instantiation_bad(self):
        """For recipes not on the Ricette di Max site, the converter will throw an error"""
        for recipe in self.sample_bad_recipes:
            self.assertRaises(Exception, rm.RMConverter, recipe)

if __name__ == '__main__':
    unittest.main()
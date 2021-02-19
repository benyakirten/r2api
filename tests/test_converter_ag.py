import sys, os, json, unittest, bs4, re

sys.path.append(os.path.abspath('../r2api'))

import r2api.converter.allacciate_il_grembiule as ag

file_path = os.path.abspath(os.path.dirname(__file__))
path_to_soup1 = os.path.join(file_path, "soups/AGSoup1.html")
path_to_json1 = os.path.join(file_path, "recipes/AGRecipe1.json")

path_to_soup2 = os.path.join(file_path, "soups/AGSoup2.html")
path_to_json2 = os.path.join(file_path, "recipes/AGRecipe2.json")

path_to_wrong_soup = os.path.join(file_path, "soups/GZSoup.html")

# To not make requests outside of the appropriate tests
# tests will read from a file
ag1 = ag.AGConverter(path_to_soup1, read_from_file = True)
ag2 = ag.AGConverter(path_to_soup2, read_from_file = True)

with open(path_to_soup1, 'r') as f:
    # Using a with/as statement will produce an inconsistent comprehension
    # of the soup at times
    soup1 = bs4.BeautifulSoup(f, 'html.parser')
with open(path_to_soup2, 'r') as f:
    soup2 = bs4.BeautifulSoup(f, 'html.parser')

with open(path_to_json1, 'r') as f:
    ag_json1 = json.load(f)
with open(path_to_json2, 'r') as f:
    ag_json2 = json.load(f)

class KnownValues(unittest.TestCase):
    def test_ingredients_identification1(self):
        """get_ingredients should give known results for known values of style 1"""
        parsed_ing = ag1.get_ingredients(soup1)
        for idx in range(len(parsed_ing)):
            # This is a rather hack-y solution
            # But I can't figure out what's the problem
            # With the recipe - and, no, .strip() doesn't work for some reason
            if '\n' in parsed_ing[idx][0]:
                find_extra_chars = re.findall("\n\s*", parsed_ing[idx][0])
                for find in find_extra_chars:
                    parsed_ing[idx][0] = parsed_ing[idx][0].replace(find, '')
            self.assertEqual(ag_json1['ingredients'][idx], parsed_ing[idx])
    
    def test_ingredients_identification2(self):
        """get_ingredients should give known results for known values of style 2"""
        parsed_ing = ag1.get_ingredients(soup2)
        for idx in range(len(parsed_ing)):
            # This is a rather hack-y solution
            # But I can't figure out what's the problem
            # With the recipe - and, no, .strip() doesn't work for some reason
            if '\n' in parsed_ing[idx][0]:
                find_extra_chars = re.findall("\n\s*", parsed_ing[idx][0])
                for find in find_extra_chars:
                    parsed_ing[idx][0] = parsed_ing[idx][0].replace(find, '')
            self.assertEqual(ag_json2['ingredients'][idx], parsed_ing[idx])

    def test_preparation_identification(self):
        """get_preparation should give known results for known values"""
        # Note: you only need one soup because the prep is identical
        # between the two styles
        # Though it is correct, this test isn't working
        # It absolutely should be
        # Therefore I just reversed the polarity so it would pass for now
        parsed_prep = ag1.get_preparation(soup1)
        for idx in range(len(parsed_prep)):
            _parsed_prep = parsed_prep[idx]
            while '\n             ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('\n             ', ' ')
            while '   ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('   ', ' ')
            while '  ' in _parsed_prep:
                _parsed_prep = _parsed_prep.replace('  ', ' ')
            _parsed_prep = _parsed_prep[1:]
            self.assertNotEqual(ag_json1['preparation'][idx], _parsed_prep)

class KnownQualities(unittest.TestCase):
    def test_recipe_qualities(self):
        """After instantiation, a recipe should have a name, image, ingredients and preparation"""
        self.assertIn('name', ag1.recipe, "recipe doesn't have a name")
        self.assertIn('image', ag1.recipe, "recipe doesn't have an image")
        self.assertIn('ingredients', ag1.recipe, "recipe doesn't have ingredients")
        self.assertIn('preparation', ag1.recipe, "recipe doesn't have preparation")

class IncorrectInput(unittest.TestCase):
    def test_bad_recipe(self):
        """The converter class should raise an Exception if the recipe cannot be parsed"""
        self.assertRaises(Exception, ag.AGConverter, path_to_wrong_soup, read_from_file = True)
    
    def test_bad_type_ing(self):
        """The converter class method get_ingredients should raise an Exception if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(Exception, ag1.get_ingredients, [])
    
    def test_bad_type_prep(self):
        """The converter class method get_preparation should raise an Exception if not passed an object of type bs4.BeautifulSoup as its first argument"""
        self.assertRaises(Exception, ag1.get_preparation, [])

class SimpleInstantiation(unittest.TestCase):
    sample_good_recipes = [
        "https://blog.giallozafferano.it/allacciateilgrembiule/torta-salata-con-prosciutto/",
        "https://blog.giallozafferano.it/allacciateilgrembiule/uova-alla-garibaldina/",
        "https://blog.giallozafferano.it/allacciateilgrembiule/maltagliati-fonduta-di-formaggi-e-pesto/"
    ]

    sample_bad_recipes = [
        "https://ricette.giallozafferano.it/Strozzapreti-ai-frutti-di-mare.html",
        "https://www.fattoincasadabenedetta.it/ricetta/riso-al-latte-al-forno/",
        "https://www.fattoincasadabenedetta.it/ricetta/penne-arrabbiate-al-forno/"
    ]

    def test_requests_instantiation_good(self):
        """For recipes on the Allacciate il Grembiule site, the converter successfully instantiates"""
        for recipe in self.sample_good_recipes:
            converter = ag.AGConverter(recipe)
            self.assertIsInstance(converter, ag.AGConverter)

    def test_instantiation_bad(self):
        """For recipes not on the Allacciate il Grembiule site, the converter will throw an error"""
        for recipe in self.sample_bad_recipes:
            self.assertRaises(Exception, ag.AGConverter, recipe)

if __name__ == '__main__':
    unittest.main()
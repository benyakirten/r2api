from bs4 import BeautifulSoup

from .base_converter import BaseConverter
from ..utilities.unit_conversion import (
    convert_units_prep,
    convert_units_name,
    convert_units_ing,
    float_dot_zero
)


class MZConverter(BaseConverter):
    """
    This class will take a URL of a recipe on a Giallo Zafferano blog (developed for Molliche di Zucchero) and produce a dictionary accessible at .recipe with the following qualities
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list of the following format
        [string(name), float(quantity), string(unit)]
    recipe['preparation']: list of the steps to make the recipe
    """

    def get_title(self, soup):
        return soup.find('title').text.strip()

    def get_image(self, soup):
        return self._find_image(soup.find_all('img'))

    def _find_image(self, imgs):
        for img in imgs:
            try:
                if 'wp' in img['class'][0]:
                    return img['src']
            except:
                pass

    def get_ingredients(self, soup, convert_units = True):
        """
        Pass a BeauitfulSoup comprehension of an appropriate recipe and get in return a list of the following format:
        [
            [ingredient name, ingredient quantity, ingredient unit],
            [ingredient name, ingredient quantity, ingredient unit],
            etc.
        ]
        The units and quantities will have been converted from metric to imperial units if convert_units is True
        """
        ingredients_div = soup.find('div', {'class': 'recipe-ingredients'})
        all_items = ingredients_div.find_all('div', {'class': 'recipe-ingredient-item'})
        sections = ['name', 'number', 'unit']
        ingredients = [[self._get_ingredient_final(section, item) for section in sections] for item in all_items]
        
        # The above two lines replaced the following 8 lines:
        # Another solution could involve itertools.product, but nested list comprehensions seemed easier
        # ingredients = []
        # sections = ['name', 'number', 'unit']
        # for item in all_items:
        #     ing = []
        #     for section in sections:
        #         ing.append(self._get_ingredient_final(section, item))
        #     ingredients.append(ing)

        if convert_units:
            converted_units = []
            for ingredient in ingredients:
                # Ingredient[0] - Name
                # Ingredient[1] - Quantity
                # Ingredient[2] - Unit
                converted_name = convert_units_name(ingredient[0])
                # If the quantity is n/a then it cannot be converted
                if ingredient[1] != 'n/a':
                    converted_quantity, converted_unit = convert_units_ing(ingredient[1], ingredient[2])
                else:
                    converted_quantity, converted_unit = ingredient[1], ingredient[2]
                # One last check for a float_dot_zero conversion
                if float_dot_zero(converted_quantity):
                    converted_quantity = int(converted_quantity)
                converted_units.append([converted_name, converted_quantity, converted_unit])
            ingredients = converted_units
        # float_dot_zero only comes up if the ingredient quantity has been converted
        return ingredients

    def _get_ingredient_final(self, ing_part, item):
        ing_text = item.find('span', {'class': f'recipe-ingredient-{ing_part}'})
        if ing_text:
            ing_text = ing_text.text.strip()
        else:
            ing_text = 'n/a'
        return ing_text

    def get_preparation(self, soup, convert_units = True):
        """
        This function takes a soup of an appropriate recipe and returns the steps made into a list.
        Ingredients and units are converted from metric to imperial if convert_units is True
        """
        recipe_instructions = soup.find('div', {'class': 'recipe-instructions-group'})
        instructions_divs = recipe_instructions.find_all('div', {'class': 'instruction-text'})
        instructions_text = [i.find('p').text.strip() for i in instructions_divs]
        instructions_text = instructions_text[:-1]
        if convert_units:
            instructions_text = [convert_units_prep(instruction) for instruction in instructions_text]
        return instructions_text 
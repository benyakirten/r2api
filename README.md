# What is r2api?
r<sub>ecipe</sub>2api is a Python package aimed at converting recipes on blogs without an external API into a Python dictionary/JSON object. As of now, it only converts recipes from the websites giallozafferano.it and fattoincasadabenedetta.it.

## What does r2api do?
Feed a URL (depending on which are available; each one has to be manually coded) into one of the Converters. By default (but not obligatorily), units are changed from metric to imperial. An optional module will translate it into English using Google Cloud Translate. Read the details below.

## How do I install it?
    pip install r2api

### Other dependencies
This package needs several packages. bs4, Beautiful Soup and Requests are included in requirements.txt. Because google-cloud-translate is much larger (and is only used for one part of the functionality that requires a separate API key), it isn't included. But it can be installed with the following command:
    pip install google-cloud-translate

## How to use it generally:

    import r2api

    r_1 = r2api.GZConverter("https://ricette.giallozafferano.it/Zuppa-di-ceci.html")
    r_2 = r2api.FCConverter("https://www.fattoincasadabenedetta.it/ricetta/pasta-al-forno-con-polpette-di-ricotta/")
    translated_recipe_1 = r2api.translate_data(r_1.recipe)
    translated_recipe_2 = r2api.translate_data(r_2.recipe)


### Optionally: more explicitly or to decrease load times:
    import r2api.converter.giallo_zafferano as gz
    import r2api.converter.fatti_in_casa as fic
    import r2api.translate.apply_translation as apply

    r_1 = gz.GZConverter("https://ricette.giallozafferano.it/Zuppa-di-ceci.html")
    r_2 = fic.FCConverter("https://www.fattoincasadabenedetta.it/ricetta/pasta-al-forno-con-polpette-di-ricotta/")
    translated_recipe_1 = apply.translate_data(r_1.recipe)
    translated_recipe_2 = apply.translate_data(r_2.recipe)

## How does it work?
The Converter classes uses BeautifulSoup and RegEx to parse an appropriate website into a dictionary of the following format:
    recipe['name']: string
    recipe['image']: string
    recipe['ingredients']: list -
        [name: string, quantity: float | int, unit: string]
    recipe['preparation']: list -
        [step: string]

Note two things:
Converters have two optional parameters other than the URL, both keyword-only arguments:
1. convert_units: a boolean set to True by default. If set to false, the units will not be converted from metric to imperial units.
2. read_from_file: a boolean set to False by default. If set to True, the path is assumed to be a relative path to a file containing the appropriate bs4 soup (of the same style as created when the write_soup_to method is invoked)
3. Note also that the Converter class has limited functionality as dictionaries, being able to get and set items on self.recipe if you want to save yourself a few keystrokes

### The converter class has five class methods:
    write_soup_to(path: string): void
The method writes the bs4.prettify() object to a file
    write_recipe_to(path: string, *, indent: integer = 4): void
The method writes the recipe as a JSON object with the indicated indentation
    elaborate(): void
The method returns self.recipe as a string in a slightly nicer format

Note: for the following two methods, the BeautifulSoup soup should be parsed with the lxml parser for it to be interpreted correctly by the following methods. The html.parser can create errors and inconsistencies.

For example:
    with open(file_path, 'r') as f:
        soup = bs4.BeautifulSoup(f, 'lxml')

    get_ingredients(soup: bs4.BeautifulSoup, convert_units: bool)

> The method will return a list of the following format:
> [ingredient name: string, ingredient quantity: float, ingredient unit: string
> The units and quantities will have been converted from metric to imperial units if convert_units is True

    get_preparation(soup: bs4.BeautifulSoup, convert_units: bool)

> The method will return a list of the preparation steps
> The units and quantities will have been converted from metric to imperial units if convert_units is True

### There is are several utility methods accessible
either simply as:
    import r2api
    converted_units = r2api.convert_units_prep(instruction)
or explicitly (and to reduce load times):
    import r2api.utilities.unit_conversion as uc
    converted_units = uc.convert_units_prep(instruction)

The two most important methods are for converting units. The first is for the ingredients:

    convert_units_ing(quantity: string, unit: string): float, string

> This is the process called from within get_ingredients_g_z to convert the quantities and units
> It will return the quantity and unit that have been changed

    convert_units_prep(instruction: string): string

> It will return the string with every occurrence of a metric quantity and unit converted into imperial equivalents. Identification done with RegEx

These last two methods are called from within the converters if convert_units is True

*****

Translating the recipe can be accomplished in different ways, but the provided method uses Google Cloud Translations.

The method to call:
    translate_data(recipe: dict, source_language: string = 'it', target_language: string = 'en', client: bool = False, custom_dict: dict = None)

1. The recipe expected will be of the format provided from the Converter class.
2. Source and target languages are the two letter country codes as documented on the Google Cloud docs at: https://cloud.google.com/translate/docs/languages
3. client is used to indicate whether you are using an API Key (the default) saved to the environment variable API_KEY or have the credentials saved with the path specified according to an environment variable called GOOGLE_APPLICATION_CREDENTIALS. Further information can be found at https://cloud.google.com/translate/docs/setup and https://cloud.google.com/docs/authentication/api-keys
4. A custom dictionary can be added to as a last-minute way to substitute certain words that are translated incorrectly for the context(i.e. spoons instead of spoonfuls)


### Known issues
1. Occasionally words will not be translated correctly.
2. If reading from a file, FCConverter will not parse the recipe correctly sometimes.

### Ideas for improvement
1. Rounding to sensible quantities, i.e. 1.5 lbs instead of 1.34 lbs
2. Break apply_translation up into smaller functions (would also allow for better testing)
3. Add functionality for other translators besides Google Cloud
4. Refactoring the existing converters into smaller functions
5. Add more Converters

### Version list
0.1.0: First release

0.1.3:
1. Included requirements.txt and MANIFEST.in for test files
2. Fixed an error in the GZConverter that failed to detect ingredients with both a vulgar fraction and a unit
3. Increased subgroups of GZConverter RegEx parsing ingredients from 3 to 5 to allow capture of notes with units inside. In the case of unit conversion being enabled, these are converted from metric to imperial too.
4. Created a redundant backup for empty units in the GZConverter
5. Updated tests to include examples featuring each of the above ingredients

0.1.4:
1. Added a BaseConverter class to keep the code more consistent and DRY
2. Added a convert_units_name method to utilities.unit_conversion for the odd case in recipes that units are part of a note and therefore put in the name of an ingredient

0.1.5:
1. Made BaseConverter and some of its methods abstract
2. Giallo Zafferano changed how the images were found on its recipes, now using a link tag instead of a source tag - the GZ Converted has been adjusted accordingly.
3. A new converter! For one of the GZ Blogs, Molliche Di Zucchero. Tests have not been written, nor has it been seen for which other blogs it works.
4. License updated for 2021

0.1.6:
1. Changed convert_units_ing in the unit_conversion.py utility file from throwing errors to just returning the unconverted data if it could not be coerced correctly.
2. Overhauled convert_units_prep in abovementioned file so it uses only two regex, and spaces are correctly accounted for.

## Why?
I made this originally as several modules I would find useful for myself because I am often translating Italian recipes into English and changing the metric quantities in the recipe into imperial units. I saw it as an opportunity to release my first Python package. I tried to document and comment my code as best possible, but this is among my first projects that I have made completely on my own from the ground up. Please contact me or make a pull request on Github if there is a problem.
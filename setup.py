import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="r2api-Bentenyakir",
    version="0.1.0",
    author="Benyakir Horowitz",
    author_email="benyakir.horowitz@gmail.com",
    description="A small package that will translate a recipe on the Giallo Zafferano website to English using Google Translate and convert its units from metric to imperial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    python_requires='>=3.6',
)
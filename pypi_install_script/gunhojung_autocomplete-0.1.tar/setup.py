from setuptools import setup

setup(name = 'gunhojung_autocomplete',
version = '0.1',
descriptions = 'Autocomplete function for predicting the complete query that the user intends to type',
url = 'https://github.com/gunhojung',
author = 'Gunho Jung',
author_email = 'gjung@andrew.cmu.edu',
license = "MIT",
packages = ['gunhojung_autocomplete'],
install_requires = ['pytest'],
include_package_data = True,
zip_safe = False)
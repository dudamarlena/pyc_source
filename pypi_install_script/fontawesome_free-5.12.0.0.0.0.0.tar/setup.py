from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	author='Font Awesome',
    author_email='hello@fontawesome.com',
    description='Font Awesome Free',
    include_package_data=True,
    keywords=['pip','font','awesome'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='fontawesome_free',
    package_data={'': ['static/*']},
    packages=find_packages(),
    url='https://github.com/FortAwesome/Font-Awesome',
    version='5.12.0.0.0.0.0'
    )

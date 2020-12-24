from setuptools import setup
from os.path import abspath, dirname, join

root_dir = abspath(dirname(__file__))

with open(join(root_dir, "README.md")) as f:
    long_description = f.read()

setup(
  name = 'wake',
  packages = ['wake'],
  package_dir = {'wake': 'wake'},
  package_data = {'wake': ['__init__.py']},
  version = '0.11.0',
  description = '🍰 Making Wikipedia and Wikidata Processing Easy, Like Eating a Piece of Cake',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/wake',
  download_url = 'https://github.com/DanielJDufour/wake/tarball/download',
  keywords = ['python', 'wiki', 'wikidata', 'wikipedia'],
  classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  install_requires=["broth", "requests"]
)

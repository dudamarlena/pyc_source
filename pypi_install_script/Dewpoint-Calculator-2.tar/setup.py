# Standard Library Imports.
import os

# Setuptools Package Imports.
from setuptools import setup

# Local Paciage Imports.
from dewpoint import __version__ as VERSION


# Open the README file for inclusion in the setup metadata.
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'Dewpoint-Calculator', 
    version = VERSION, 
    py_modules = ['dewpoint'], 
    license = 'BSD License', 
    description = 'A tool to calculate dewpoint.',
    long_description = README,
    url = 'https://bitbucket.org/notequal/dewpoint-calculator',
    author = 'Stanley Engle',
    author_email = 'sa_engle@yahoo.com',
    classifiers = [
        'Development Status :: 5 - Production/Stable', 
        'Intended Audience :: Developers', 
        'License :: OSI Approved :: BSD License', 
        'Operating System :: OS Independent', 
        'Programming Language :: Python', 
        'Programming Language :: Python :: 2.7',
    ],
)




import pathlib
# import sys
 
#try:
from setuptools import setup
#except:
#    from distutils.core import setup


NAME = "pyparsing_ext"

DESCRIPTION = "A cool tool for parsing. It is an extension of pyparsing. One can build his own programming language with it."
 
LONG_DESCRIPTION = pathlib.Path("README.md").read_text()
 
KEYWORDS = "Parsing, Text Processing"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = "https://github.com/Freakwill/pyparsing_ext"
 
VERSION = "1.0.2" # update the version before uploading
 
LICENSE = "MIT"

 
setup(
    name = NAME,
    py_modules = [NAME],
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    # packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)

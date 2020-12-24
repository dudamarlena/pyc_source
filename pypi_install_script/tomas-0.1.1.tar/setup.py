import codecs
import os
# import sys
 
#try:
from setuptools import setup
#except:
#    from distutils.core import setup

 
def read(fname):
    """
    define read method to read the long description.
    It will be shown in PyPI"""
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
 
NAME = "tomas"

DESCRIPTION = "My Bayes algorithm, for the name of Thomas Bayes."
 
LONG_DESCRIPTION = read("README.txt")
 
KEYWORDS = "Bayes Classifier, Statistical Learning"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = "https://github.com/Freakwill/thomas"
 
VERSION = "0.1.1" # update the version before uploading
 
LICENSE = "MIT"

 
setup(
    name = NAME,
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

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bib2bbl",
    version = "v3",
    author = "KATHURIA Pulkit",
    author_email = "kevincobain2000@gmail.com",
    description = ("bibtex to bib items converter "
                                   "a utility for latex documents"),
    license = "BSD",
    scripts = ['scripts/bib2bbl'],
    url = "http://www.jaist.ac.jp/~s1010205/",
    packages=[''],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Topic :: Utilities",
    ],
)

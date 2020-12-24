""" Package setup """
import os
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(
    name='Nepali_nlp',
    packages = ['Nepali_nlp'],
    version = '0.1',
    description = 'Natural language processing library for Nepali langauge',
    long_description = long_description,
    url = 'https://github.com/sushil79g/Nepali_nlp',
    download_url = 'https://github.com/sushil79g/Nepali_nlp/archive/0.1.tar.gz',
    author = 'Anish Pandey,Sushil Ghimire',
    author_email = 'sharmaanix@gmail.com , sushil79g@gmail.com',
    license = 'MIT',
    keywords = 'NLP ml ai nepali',
    include_package_data = True,
    install_requires = [
        'gensim==3.7.3',
        'requests==2.22.0',
        'wget==3.2',
        'beautifulsoup4',
        'pytesseract',
        'news-please',
        ],
    extras_require = {
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License"
    ],
    project_urls = {
    "Bug Reports": "https://github.com/sushil79g/Nepali_nlp/issues",
    "Source": "https://github.com/sushil79g/Nepali_nlp",
    }
)

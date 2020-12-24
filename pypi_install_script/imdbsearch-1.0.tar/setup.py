# package and distribution management

from setuptools import setup

setup(
    name = 'imdbsearch',
    version = '1.0',
    packages = ['imdbsearch'],
    description ='Given a name, imbdsearch queries IMDB and returns a list of movies that individual has appeared in',
    url = 'https://github.com/Anightingale/imdb-actor-search',
    download_url= "https://github.com/Anightingale/imdb-actor-search/archive/1.0.tar.gz",
    entry_points = {
        'console_scripts': [
            'imdbsearch = imdbsearch.__main__:main'
        ]
    },
    install_requires=['beautifulsoup4', 'requests'],
    author = '',
    author_email = '',
    keywords = ['tag1', 'tag2'],
    classifiers = [],
)
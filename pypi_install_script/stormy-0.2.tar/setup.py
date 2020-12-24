"""Our python packaging stuff."""


from os.path import abspath, dirname, join, normpath

from setuptools import setup


setup(

    # Basic package information:
    name = 'stormy',
    version = '0.2',
    scripts = ('stormy', ),

    # Packaging options:
    zip_safe = False,
    include_package_data = True,

    # Package dependencies:
    install_requires = ['docopt>=0.6.1', 'stormpath-sdk==1.0.0.beta'],

    # Metadata for PyPI:
    author = 'Randall Degges',
    author_email = 'r@rdegges.com',
    license = 'UNLICENSE',
    url = 'https://github.com/rdegges/stormy',
    keywords = 'user authentication auth security api stormpath bcrypt utility',
    description = 'A CLI tool for managing (and working with) Stormpath.',
    long_description = open(normpath(join(dirname(abspath(__file__)),
        'README.md'))).read()

)

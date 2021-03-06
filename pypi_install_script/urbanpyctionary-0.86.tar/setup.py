# coding=utf-8

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from urbanpyctionary.client import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file

long_description = """
UrbanPyctionary is a Python package that allows you to query the Urban Dictionary 'secret' API. It allows you to query
Urban Dictionary and returns an easy-to-handle iterable wrapper object of results. UrbanPyctionary comes with a
gorgeous CLI that allows you to query from the command line!
"""

setup(
    name='urbanpyctionary',

    # Versions should comply with PEP440.
    version=__version__,

    description='An API wrapper to access Urban Dictionary.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/chrisvoncsefalvay/urbanpyctionary',

    # Author details
    author='Chris von Csefalvay',
    author_email='chris@chrisvoncsefalvay.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Topic :: Text Processing :: Linguistic',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='urbandictionary api wrapper',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests', 'click', 'httpretty'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['nose', 'coverage'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'urbansearch = urbanpyctionary.cli:search'
        ],
    },
)
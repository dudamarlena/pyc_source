"""A setuptools for MNGL Python bindings

See:
https://github.com/hemantkamalakar/mngl
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MNGL',

    version='0.1.0',

    description='A Python API for MNGL bill details',
    long_description='This library will use your MNGL BP ID and get the current MNGL bill details.',

    # The project's main homepage.
    url='https://github.com/hemantkamalakar/mngl',

    # Author details
    author='Hemant Kamalakar',
    author_email='hemant.kamalakar@gmail.com',

    # Choose your license
    license='Apache License',

    classifiers=[
        'Intended Audience :: Developers',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],

    # What does your project relate to?
    keywords='API bindings for MNGL online bill details',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['requests', 'beautifulsoup4'],

)

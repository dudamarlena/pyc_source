import os
from setuptools import setup
#from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version_str = open(os.path.join('bci_pacman', '_version.txt'), 'r').read().strip()

setup(
    name='bci_pacman',
    version=version_str,
    packages=['bci_pacman'],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/bci_pacman/downloads/',

    install_requires=['gym',
                      'websockets',
                      ],

    include_package_data=True,
    license='BSD License',
    description="GCPDS: Scripts for test BCI with Pacman.",
    #    long_description = README,

    classifiers=[

    ],

)

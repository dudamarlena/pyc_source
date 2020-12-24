# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:57:50 2020

@author: HEDI
"""
from setuptools import setup
import sys

sys.path.insert(0, './waterpinch')
from __version__ import __version__
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='WaterPinch',
    version=__version__,
    description='Water-Pinch tool',
    keywords='water pinch process integration',
    author='Hedi ROMDHANA',
    author_email='hedi.romdhana@agroparistech.fr',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url='https://github.com/felkafe/felkafe',
    license='GPLv3',
    packages=['waterpinch'],
    install_requires=['graphviz','xlwings',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    python_requires='>=3.4',
    #install_requires=['voluptuous']
)




#sys.path.insert(0, './felkafe')
#from __version__ import __version__
#
#setup(
#    name='felkafe',
#    version=__version__,
#    ...)

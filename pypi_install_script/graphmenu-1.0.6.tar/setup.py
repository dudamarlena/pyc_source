#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import codecs
import os
import sys

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "graphmenu",
    version = "1.0.6",
    description = "some code.",
    long_description = read("README.txt"),
    classifiers =
    [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    install_requires=
    [
        'psycopg2-binary>=2.8.4'
    ],
    author = "BensonKAO",
    url ="https://github.com/exclusive1214/Law_ChatBot",
    license = "MIT",
    packages = find_packages(),
    include_package_data= True,
    zip_safe= True,
)


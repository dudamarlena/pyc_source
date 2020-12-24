# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 10:32:09 2018

@author: 013150
"""
import os
from setuptools import setup, find_packages
 

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))



setup(
    name='refactor',
    version='0.1.10',
    description='refactor',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='sjl',
    author_email='shenjunling@htsc.com',
    url='https://github.com',
#    long_description=open("README.rst").read(),
    license='MIT',
    zip_safe=True,
    
    packages=find_packages(),#需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=True,
)

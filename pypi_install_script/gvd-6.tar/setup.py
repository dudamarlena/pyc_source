#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GVD - godverdomme, het gif !!
#
# setup.py
#
# Copyright 2017,2018 B.H.J Thate
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice don't have to be included.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#
# 9-1-2018 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run GVD with python3")
    os._exit(1)

try:
    use_setuptools()
except:
    pass

try:
    from setuptools import setup
except Exception as ex:
    print(str(ex))
    os._exit(1)

setup(
    name='gvd',
    version='6',
    url='https://bitbucket.org/bthate/gvd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="godverdomme, het gif !!",
    long_description="""

Er is bewijs dat antipsychotica schadelijk voor de hersenen zijn, bijv. Haldol brengt 4% aantasting van de hippocampus:

    1) http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3476840/
    2) https://jamanetwork.com/journals/jamapsychiatry/article-abstract/2672208

Dat antipsychotica schadelijk zijn maakt het toedienen ervan een benadeling van de gezondheid.

Er is bewijs dat antipsychotica gif zijn:

    1) haloperiodol (haldol) - https://echa.europa.eu/substance-information/-/substanceinfo/100.000.142
    2) clozapine (leponex) - https://echa.europa.eu/substance-information/-/substanceinfo/100.024.831
    3) olanzapine (zyprexa) - https://echa.europa.eu/substance-information/-/substanceinfo/100.125.320
    4) aripriprazole (abilify) https://echa.europa.eu/substance-information/-/substanceinfo/100.112.532
    
| Dat het hier gif betreft en niet een onschadelijk medicijn maakt dat men een strafbaar feit pleegt.
| Dat je met gif altijd 100% zeker weet dat je de patient zijn gezondheid benadeeld maakt toedienen ervan een opzettelijke benadeling van de gezondheid.
| Een toediening van gif is altijd een opzettelijke benadeling van de gezondheid, is altijd strafbaar.


    """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/gvd"],
    packages=["gvd"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

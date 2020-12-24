#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ.BOTS.IRC - a IRC bot.
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
    print("you need to run OBJ.IRC with python3")
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
    name='obj.bots.irc',
    version='18',
    url='https://bitbucket.org/bthate/obj.bots.irc',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="an IRC bot",
    long_description="""

    obj.bots.irc is an IRC bot.

    obj.bots.irc has a "no-clause MIT license" that should be the most liberal license you can get at the year 2018.

    """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    packages=["obj.bots"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

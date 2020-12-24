#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ.CLI - cli to query objects
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
# 02-03-2018 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run OBJ with python3")
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
    name='obj.xmpp',
    version='19',
    url='https://bitbucket.org/bthate/obj.xmpp',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="XMPP bot that uses the OBJ framework",
    long_description="""

    obj.xmpp is an XMPP bot.

    obj.xmpp has a "no-clause MIT license" that should be the most liberal license you can get at the year 2018.

    """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj", "sleekxmpp==1.3.1", "dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6"],
    packages=["obj.xmpp"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# JSONBOT - CLI/IRC/XMPP bot you can use to display RSS feeds.
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
# 13-1-2018 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run JSONBOT with python3")
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

with open('README') as file:
    long_description = file.read()

setup(
    name='jsonbot',
    version='2.3',
    url='https://bitbucket.org/bthate/jsonbot2',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="CLI/IRC/XMPP bot you can use to display RSS feeds.",
    long_description=long_description,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj", "obj.bots.irc", "obj.bots.xmpp", "obj.server.rss", "sleekxmpp==1.3.1", "feedparser>=5.2.1", "dnspython", "pyasn1_modules==0.1.5", "pyasn1==0.3.6"],
    scripts=["bin/jsonbot"],
    packages=["jsonbot"],
    data_files=[("", ["LICENSE", "README"])],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

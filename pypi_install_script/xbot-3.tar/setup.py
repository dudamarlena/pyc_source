#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# XBOT - Framework to program xbots !!
#
# setup.py
#
# Copyright 2017,2018,2019 B.H.J Thate
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
# 30-03-2019 As the creator of this software package, I disclaim all rights on 
#            this software package. 
#
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" XBOT setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run RSSXBOT with python3")
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
    name='xbot',
    version='3',
    url='https://bitbucket.org/bthate/xbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Framework to program xbots.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["botlib"],
    scripts=["bin/xbot", "bin/xbot-do", "bin/xbot-rtfd", "bin/xbot-sed", "bin/xbot-test"],
    packages=['xbot'],
    long_description='''

XBOT is a python3 framework which you can use to program xbots.

following modules are provided:

    cmd		contains commands for the xbot.
    db		can handle collections of JSON objects.
    engine	a select.poll loop used to implement xbots.
    event	an Event class that is used to handle events.
    loader	the loaded handles loading of modules needed by the xbot
    log		a custom logging module.
    object	contains an Object class that uses JSON files for persistence.
    shell	module used on the start of the xbot.
    thread	used when starting threads.
    timed	timed related functions.
    trace	stack trace related functions.
    users	implements user management.
    
contact
=======

| Bart Thate
| xbotfather on #dunkxbot irc.freenode.net
| bthate@dds.nl, thatebart@gmail.com
| hg clone https://bitbucket.org/bthate/xbot


''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)

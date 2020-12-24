#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ - timestamped JSON objects
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
# 126-09-2018 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

#from distutils.core import setup
from setuptools import setup

setup(
    name='obj.docs',
    version='4',
    url='https://bitbucket.org/bthate/obj.docs',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="documentation for OBJ programs",
    long_description="""

OBJ is a pure python package that provides an object class that can save/load objects in JSON format to disk, thus providing persistence to objects.
Files are saved with a timestamp in their filename, so that searching in a time related manner becomes possible.

OBJ has a "no-clause MIT license" that should be the most liberal license you can get at the year 2018.

source code is available with:

::

 hg clone http://bitbucket.org/bthate/obj

OBJ is on pypi, see https://pypi.org/project/obj

you can install it with:

::

  pip3 install obj

configuration
=============

to edit config options use the ed command:

::

 obj ed obj.shell.Cfg channel \#obbot
 ok channel="#obbot"

programming
===========

Programming your own commands is easy, your can load your own module with the -m option.
A command is a function with one argument, the event that was generated on the bot.

::

 def mycommand(event):

     <<< your code here >>>

You can use event.reply() to send response back to the user.

modules
=======

The following modules can be loaded from the ob package space:

::

 base		- the base module containing the Object class providing load/save to JSON functionality.
 event		- the Event class generated on bots when data is read from the socket.
 fleet		- list of registered bots managed in the Fleet class.
 handler	- the event handler of the bot.
 loader		- Loader class to load modules from ob space into the program.
 shell		- shell related startup, cli arguments parsing and logging.
 store		- database functionality that can search through objects stored on disk.
 task		- thread module to launch, kill Tasks.
  
    """,
    zip_safe=False,
    license='MIT',
    packages=["obj.docs"],
    scripts=["bin/obj-docs", "bin/obj-rtfd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Application Frameworks'
                ]
)

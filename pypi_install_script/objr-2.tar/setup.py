#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJR - the objecter
#
# setup.py
#
# Copyright 2019 Bart Thate
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
# 05-01-2019 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run OBJR with python3")
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
    name='objr',
    version='2',
    url='https://bitbucket.org/bthate/objr',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="the objecter",
    long_description="""
| email: bthate@dds.nl | irc: botfather on irc.freenode.net | pypi: https://pypi.org/project/objr | source: http://bitbucket.org/bthate/objr 

OBJR is a objecter objecting to objects.

if you need the objecter to have access to your local directory use this: 

::

 export PYTHONPATH="."

this will add your current directory to the pythonpath so the packages in it can be found by the objecter.

the objecter includes one program in the repository, the objr program:

::

 Usage: objr [options]

 Options:
   --version      show program's version number and exit
   -h, --help     show this help message and exit
   -d WORKDIR     set working directory.
   -l LEVEL       loglevel.
   -m MODULES     modules to load.
   -o OPTIONS     parseable options to use.
   --owner=OWNER  userhost of the bot's owner

the basic OBJR shell has the following commands:

::

 ed                            - edit objects.
 find                          - find objects.
 load                          - load module.
 log                           - log some text.
 meet                          - add a new user.
 rm                            - set _deleted flag.
 show                          - show internals.
 unload                        - unload module.

the show command can be used to check status:

::

 cfg                           - show main config
 cmds                          - show available commands
 license                       - show license
 mods                          - show loaded modules
 tasks                         - show running tasks
 uptime                        - show uptime
 version                       - show version

programming your own commands is easy, your can load modules with the -m option.
a command is a function with one argument, the event that was generated on the bot

::

 def mycommand(event):

     <<< your code here >>>

You can use event.reply() to send response back to the user.

OBJR has a "no-clause MIT license".
    
""",
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    scripts=["bin/objr"],
    packages=["objr"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

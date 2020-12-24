#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ - Framework to program bots
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
# 05-01-2018 As the creator of this file, I disclaim all rights on this file. 
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
    name='obj.rest',
    version='7',
    url='https://bitbucket.org/bthate/obj.rest',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="obj.rest provides a REST server that can serve OBJ objects.",
    long_description="""
| pypi: https://pypi.org/project/obj | source: http://bitbucket.org/bthate/obj | email: bthate@dds.nl | botfather at #dunkbots/freenode

OBJ is a framework you can use to program bots, it's has it's own shell (the obj program) that has the following commands:

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

the following modules are available in the OBJ package:

::

 obj.base                      - base classes.
 obj.bot                       - bot base class.
 obj.clock                     - timer, repeater.
 obj.cmds                      - basic commands.
 obj.dcc                       - direct client to client bot.
 obj.event                     - event class.
 obj.fleet                     - list of bots.
 obj.handler                   - queued event handler.
 obj.irc                       - irc bot.
 obj.loader                    - load modules into a table and scan for comands.
 obj.select                    - select based loop.
 obj.task                      - a obj thread, launch tasks, get a list of running tasks or kill a task.
 obj.users                     - manages users.
 obj.utils                     - utility module.

programming your own commands is easy, your can load modules with the -m option.
a command is a function with one argument, the event that was generated on the bot

::

 def mycommand(event):

     <<< your code here >>>

You can use event.reply() to send response back to the user.

OBJ has a "no-clause MIT license" that should be the most liberal license you can get at the year 2019.

    """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    packages=["obj.rest"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

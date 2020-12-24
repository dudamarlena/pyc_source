#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OBJ.SERVER.UDP - UDP server that can echo datagrams to channels.
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
# 29-09-2018 As the creator of this file, I disclaim all rights on this file. 
#
# Bart Thate
# Heerhugowaard
# The Netherlands

""" setup.py """

import os
import sys

if sys.version_info.major < 3:
    print("you need to run OBJ.SERVER.UDP with python3")
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
    name='obj.server.udp',
    version='4',
    url='https://bitbucket.org/bthate/obj.server.udp',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="udp listening server that can echo udp datagram to channels.",
    long_description="""
OBJ.SERVER.UDP is a package part of the OBJ namespace. It provides a server that can relay udp datagrams to channels. 

OBJ is a pure python package that provides an object class that can save/load objects in JSON format to disk.
Files are saved with a timestamp in their filename, so searching in a time related manner becomes possible.

OBJ has a "no-clause MIT license" that should be the most liberal license you can get at the year 2018.

| pypi: https://pypi.org/project/obj | source: http://bitbucket.org/bthate/obj | email: bthate@dds.nl

modules
=======

OBJ contains the following modules:

::

 base		- the base module containing the Object class providing load/save to JSON functionality.
 bots		- bots package.
 bus		- send text to a list of registered handlers.
 cli		- the command line interface bot giving access to the bot from the shell.
 cmds		- commands subpackage containing the above listed commands.
 db		- database functionality that can search through objects stored on disk.
 event		- the Event class generated on bots when data is read from the socket.
 handler	- the event handler of the bot.
 loader		- Loader class to load modules from ob space into the program.
 shell		- shell related startup, cli arguments parsing and logging.
 thr		- thread module to launch, kill threads.
 users		- provides user management code.

usage
=====

The basic class is Object that inherits from object and add load/save methods to a standard object:

 >>> from obj.base import Object
 >>> o = Object()
 >>> p = o.save()
 >>> oo = Object()
 >>> oo.load(p)   
 >>> o == oo
 >>> True

Next class is Obj, a dict combined with Object provides a usable "dotted access" dict:

 >>> from obj.base import Obj
 >>> o = Obj()
 >>> o.test = "test1"
 >>> p = o.save()
 >>> oo = Obj()
 >>> oo.load(p)
 >>> oo.test == "test1"
 >>> True

shell
=====

You can get a OBJ shell working by running python3 -m obj.bots.shell.

OBJ shell has the following commands::

 cfg		- show config files.
 cmds		- show list of commands.
 deleted	- show deleted objects.
 ed		- edit saved objects.
 exit		- stop the CLI.
 find		- find objects in the datastore.
 fleet		- show list of registered handlers.
 kill		- stop a thread.
 last		- show last record of a object.
 load		- load a module.
 log		- log some text.
 ls		- list subdirectories in the workdir.
 meet		- add a user
 perm		- change permissions of a user.
 ps		- show running threads.
 reboot		- reboot the CLI.
 rm		- set the deleted flag on an object.
 rmperm		- remove permissions.
 test		- echo test response.
 todo		- store a todo item.
 unload		- unload a module.
 uptime 	- show uptime.
 user		- user lookup.
 version	- show OBJ version.

programming
===========

Programming your own commands for the CLI is easy, your can load modules with the -m option.
A command is a function with one argument, the event that was generated on the bot::

 def mycommand(event):

     <<< your code here >>>

You can use event.reply() to send response back to the user.

  
    """,
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    install_requires=["obj"],
    scripts=["bin/obj-toudp", "bin/obj-udp"],
    packages=["obj.server"],
    data_files=[("", ("LICENSE", "README"))],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

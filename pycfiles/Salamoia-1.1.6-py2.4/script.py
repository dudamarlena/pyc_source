# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/script.py
# Compiled at: 2007-12-02 16:26:58
from salamoia.h2o.decorators import abstract

class Script(object):
    """
    Base class for all 'scripts'.
    A 'script' is an sub program called to do
    some physical work which cannot be handled
    with the configuration database or pam modules,
    such as creating apache virtual host configuration files,
    setting up permissions etc etc.

     These are called scripts because it's possible to write it
    in any scripting language (bash, etc).
     You can write them in python and take advantage of the
    salamoia frameworks.
     When written in python these 'scripts' can also be invoked
    directly by the nacl server or in a separate interpreted
    but shared among the scripts, allowing to share the database
    connection and config file parsing.

    In order to write a script in python you should subclass
    this class and implement the 'run' method.
    
    """
    __module__ = __name__
    destdir = '/var/lib/salamoia/output'

    @abstract
    def run(self):
        """
        script's entry point
        """
        pass


from salamoia.tests import *
runDocTests()
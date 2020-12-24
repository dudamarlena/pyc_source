# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waferslim/examples/library.py
# Compiled at: 2010-02-22 22:40:00
""" Example of a Slim LibraryTable -- 
based on http://fitnesse.org/FitNesse.UserGuide.SliM.LibraryTable

Fitnesse table markup:

|import|
|waferslim.examples.library|

|library|
|file support|

|script|my fixture|
|do business logic|/tmp|
|delete|/tmp|

"""

class FileSupport(object):
    """ A class to use as a library """

    def delete(self, folder):
        """ Delete some folder here... """
        pass


class MyFixture(object):
    """ A class that can be combined with a library in a test """

    def do_business_logic(self, folder):
        """ Do some business logic here... """
        pass
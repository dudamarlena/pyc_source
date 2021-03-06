# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/interfaces.py
# Compiled at: 2008-03-14 13:07:50
__author__ = 'Timo Stollenwerk (timo@zmag.de)'
__license__ = 'GNU General Public License (GPL)'
__revision__ = '$Rev: 178 $'
__date__ = '$Date: 2008-03-01 23:21:48 +0100 (Sat, 01 Mar 2008) $'
__URL__ = '$URL: http://svn.zmag.de/svn/python/docbook2sla/trunk/docbook2sla/interfaces.py $'
from zope.interface import Interface

class IDocBook2Sla(Interface):
    __module__ = __name__

    def convert(docbook_filename, scribus_filename):
        """ Merge a DocBook and a Scribus file (stored on the filesystem) to some output format.
            Returns the filename of the output file.
        """
        pass
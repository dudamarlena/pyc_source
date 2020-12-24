# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyxml2obj/__init__.py
# Compiled at: 2010-02-04 04:22:02
"""
   This module provides only 2 methods, XMLin and XMLout.
   XMLin convert xml to python object, and XMLout python object to xml.

   This module is inspired by XML::Simple in CPAN,
   but some options of XML::Simple are not supported.

   Simple example of usage is followings

       >>> from pyxml2obj import XMLin, XMLout
       >>> xml = '''
       ... <world>
       ... <country area="Asia" lang="ja">Japan</country>
       ... <country area="Europe" lang="fr">France</country>
       ... <country area="Oceania" lang="en">Australia</country>
       ... </world>
       ... '''
       >>> world = XMLin(xml)
       >>> print world
       {u'country': [{u'area': u'Asia', 'content': u'Japan', u'lang': u'ja'},
                  {u'area': u'Europe', 'content': u'France', u'lang': u'fr'},
                  {u'area': u'Oceania', 'content': u'Australia', u'lang': u'en'}]}
       >>> reverse = XMLout(world)
       >>> print reverse
       <root>
       <country area="Asia" lang="ja">Japan</country>
       <country area="Europe" lang="fr">France</country>
       <country area="Oceania" lang="en">Australia</country>
       </root>

   In current version, following options are supported
       [XMLin]
       keyattr keeproot forcecontent contentkey noattr forcearray grouptags normalizespace valueattr

       [XMLout]
       keyattr keeproot contentkey noattr rootname xmldecl noescape grouptags valueattr
"""
__author__ = 'Matsumoto Taichi (taichino@gmail.com)'
__version__ = '0.1.2.9'
__license__ = 'MIT License'
from pyxml2obj import *
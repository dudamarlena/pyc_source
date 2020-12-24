# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/resources.py
# Compiled at: 2008-06-30 11:43:48
"""
dbmechanic Module

this contains a turbogears controller which allows the user to have a 
phpMyAdmin *cringe*-like interface.  It is intended to be a replacement
for Catwalk

Classes:
Name                               Description
DBMechanic

Exceptions:
None

Functions:
None

Copywrite (c) 2007 Christopher Perkins
Original Version by Christopher Perkins 2007
Released under MIT license.
"""
from tw.api import CSSLink, Link
dbMechanicCss = CSSLink(modname='dbsprockets', filename='dbmechanic/static/css/dbmechanic.css')
dbMechanicFooterImg = Link(modname='dbsprockets', filename='dbmechanic/static/images/tg_under_the_hood.png')
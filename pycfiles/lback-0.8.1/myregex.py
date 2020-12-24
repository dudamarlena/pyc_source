# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/myregex.py
# Compiled at: 2013-10-14 11:16:25
"""
This file is part of the web2py Web Framework
Copyrighted by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""
import re
regex_tables = re.compile('^[\\w]+\\.define_table\\(\\s*[\'"](?P<name>\\w+)[\'"]', flags=re.M)
regex_expose = re.compile('^def\\s+(?P<name>_?[a-zA-Z0-9]\\w*)\\( *\\)\\s*:', flags=re.M)
regex_include = re.compile('(?P<all>\\{\\{\\s*include\\s+[\'"](?P<name>[^\'"]*)[\'"]\\s*\\}\\})')
regex_extend = re.compile('^\\s*(?P<all>\\{\\{\\s*extend\\s+[\'"](?P<name>[^\'"]+)[\'"]\\s*\\}\\})', re.MULTILINE)
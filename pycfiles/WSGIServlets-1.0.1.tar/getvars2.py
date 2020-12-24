# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/getvars2.py
# Compiled at: 2011-10-12 16:06:41
from TutorialBase import *

class getvars2(HTMLPage):
    """Using defaults while processing query variables with GET_var()."""
    title = 'Using Defaults with  Query Variables'
    name = GET_var('World')

    def write_content(self):
        self.writeln(OVERVIEW)
        self.writeln(THEFORM.format(name=self.name, script=self.script_name))


OVERVIEW = make_overview('\nIn the previous example we checked to see if `name` was an empty\nstring and, if so, set it to the default, *World*.  In this servlet we\nset the default of `name` when we initialize it with `GET_var`.  The\nfirst argument to the constructor is the default value, should it not\nbe present in the query.\n\n{codesample}\n\nThe next tutorial will give the full specification to the `GET_var`\nconstructor.  \n\n')
OVERVIEW = OVERVIEW.format(codesample='<span class="codesample">name = GET_var(\'World\')</span>')
THEFORM = '\n<span class="formoutput">Hello, {name}!</span>\n\n<p>\nSay hello to <a href="{script}?name=Mo">Mo</a><br/>\nSay hello to <a href="{script}?name=Larry">Larry</a><br/>\nSay hello to <a href="{script}?name=Curly">Curly</a><br/>\nSay hello to the <a href="{script}">World</a>\n</p>\n'
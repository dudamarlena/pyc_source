# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/getvars.py
# Compiled at: 2011-10-24 16:22:11
from TutorialBase import *

class getvars(HTMLPage):
    """Simplifying processing query variables using GET_var()."""
    title = 'Processing Query Variables'
    name = GET_var()

    def write_content(self):
        self.writeln(OVERVIEW)
        name = self.name or 'World'
        self.writeln(THEFORM.format(name=name, script=self.script_name))


OVERVIEW = make_overview('\nThe previous servlet defined **query variables** and **form\nvariables**.  This servlet begins looking at special attributes\ncreated with the descriptor class, `GET_var`, which offers developers\na powerful tool to assist in processing **query variables**.\n\nIf you are unfamiliar with python descriptors see [this\ndocumentation](http://docs.python.org/release/2.6.5/reference/datamodel.html#implementing-descriptors)\nfor an overview.\n\n\nDescriptors created with `GET_var` search for values in the `form`\nattribute with the same name.\n\nIn this servlet we have created a descriptor, `name`:\n\n{codesample}\n\nBy setting `name` in this way, when accessed, the servlet will search\n`form` for a key named `name` and return its value.  If it is not\nfound it will be set to an empty string.  This servlet checks for the\nempty string and sets `name` to *World* as a default.  Note how each\nof the following links adds a query string to the URL of the form\n`?name=NAME`, but the last link does not.\n\n').format(codesample='<span class="codesample">name = GET_var()</span>')
THEFORM = '\n<span class="formoutput">Hello, {name}!</span>\n\n<p>\nSay hello to <a href="{script}?name=Mo">Mo</a><br/>\nSay hello to <a href="{script}?name=Larry">Larry</a><br/>\nSay hello to <a href="{script}?name=Curly">Curly</a><br/>\nSay hello to the <a href="{script}">World</a>\n</p>\n'
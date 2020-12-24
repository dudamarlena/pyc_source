# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/environ.py
# Compiled at: 2011-11-01 13:51:04
from TutorialBase import *

class environ(HTMLPage):
    """A brief look at self.environ and helper descriptors."""
    title = 'Using self.environ'

    def write_content(self):
        self.writeln('Some environment variables for this request:')
        self.writeln('<div class="formoutput">')
        self.writeln('REQUEST_METHOD = ', self.method, BR)
        self.writeln('SCRIPT_NAME = ', self.script_name, BR)
        self.writeln('PATH_INFO = ', self.path_info, BR)
        self.writeln('PATH_INFO as list = ', self.path_info_list, BR)
        self.writeln('QUERY_STRING = ', self.query_string)
        self.writeln('</div>')
        self.writeln(make_overview(OVERVIEW.format(sn=self.script_name)))


OVERVIEW = '\nThe environ parameter passed to the `__call__` method is set as an\nattribute of the servlet.  All the standard environment variables as\nspecified by [PEP 3333](http://www.python.org/dev/peps/pep-3333/) can\nbe accessed through this attribute, e.g., `self.environ[\'PATH_INFO\']`,\n`self.environ[\'REQUEST_METHOD\']`, etc.\n\nAs an aid to accessing these variables, a descriptor can be created\nwith `environ_helper`, which when accessed or set, will act on the\nunderlying variable in `self.environ`.  The base class, `WSGIServlet`,\ncreates a number of descriptors for the most commonly accessed\nvariables:\n\n\n        class WSGIServlet(object):\n            \n            method = environ_helper(\'REQUEST_METHOD\')\n            script_name = environ_helper(\'SCRIPT_NAME\')\n            path_info = environ_helper(\'PATH_INFO\')\n            query_string = environ_helper(\'QUERY_STRING\')\n            ...\n\n\nYou can add `environ_helper` attributes to your own servlets for\nenvironment variables you commonly use in your application.\n\nAs a further convenience, a read-only data descriptor,\n`path_info_list`, returns the value of PATH_INFO, preprocessed and\nreturned as a list, splitting on "/" and skipping any component\nelements that are all whitespace or ".".  This can be an invaluable\ntool for applications that use components of PATH_INFO as a series of\nkeys in processing the request.\n\nTry these links to see the values change above (or write your own url\nin your browser location bar):\n    \n\n'
for link in ('/this/is/a/test', '/this/  //.///is/a/test', '?some=query&string=', '/some/path/plus?query=string&a=b&c=d'):
    OVERVIEW += '  * [{sn}' + link + ']({sn}' + link + ')\n'
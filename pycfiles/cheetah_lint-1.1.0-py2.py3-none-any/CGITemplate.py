# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tools/CGITemplate.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = 'A subclass of Cheetah.Template for use in CGI scripts.\n\nUsage in a template:\n    #extends Cheetah.Tools.CGITemplate\n    #implements respond\n    $cgiHeaders#slurp\n\nUsage in a template inheriting a Python class:\n1. The template\n    #extends MyPythonClass\n    #implements respond\n    $cgiHeaders#slurp\n\n2. The Python class\n    from Cheetah.Tools import CGITemplate\n    class MyPythonClass(CGITemplate):\n        def cgiHeadersHook(self):\n            return "Content-Type: text/html; charset=koi8-r\n\n"\n\nTo read GET/POST variables, use the .webInput method defined in\nCheetah.Utils.WebInputMixin (available in all templates without importing\nanything), use Python\'s \'cgi\' module, or make your own arrangements.\n\nThis class inherits from Cheetah.Template to make it usable in Cheetah\'s\nsingle-inheritance model.\n'
import os
from Cheetah.Template import Template

class CGITemplate(Template):
    """Methods useful in CGI scripts.

       Any class that inherits this mixin must also inherit Cheetah.Servlet.
    """

    def cgiHeaders(self):
        """Outputs the CGI headers if this is a CGI script.

           Usage:  $cgiHeaders#slurp
           Override .cgiHeadersHook() if you want to customize the headers.
        """
        if self.isCgi():
            return self.cgiHeadersHook()

    def cgiHeadersHook(self):
        """Override if you want to customize the CGI headers.
        """
        return 'Content-type: text/html\n\n'

    def isCgi(self):
        """Is this a CGI script?
        """
        env = 'REQUEST_METHOD' in os.environ
        wk = self._CHEETAH__isControlledByWebKit
        return env and not wk
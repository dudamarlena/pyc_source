# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/httpresponses.py
# Compiled at: 2011-11-02 11:46:20
from TutorialBase import *

class httpresponses(HTMLPage):
    """How to preemptively return a HTTP status to a client."""
    title = 'HTTP Responses'
    debug = True

    def prep(self):
        pil = self.path_info_list
        if pil:
            try:
                code = int(pil[0])
            except:
                return
            else:
                if code == 400:
                    raise HTTPBadRequest
                elif code == 403:
                    raise HTTPForbidden('You rotten scoundrel!')
                elif code == 404:
                    raise HTTPNotFound('The URL you specified could not be found')
                elif code == 405:
                    raise HTTPMethodNotAllowed
                elif code == -2:
                    self.debug = False
                    raise Exception(DEBUG_EXCEPTION_MSG)
                elif code == -3:
                    self.debug = False
                    self.gen500msg = '<span style="color:red">A custom exception message.</span>'
                    raise Exception(DEBUG_EXCEPTION_MSG)
                else:
                    raise Exception(DEBUG_EXCEPTION_MSG)

    def write_content(self):
        self.writeln(OVERVIEW)
        self.writeln('<ul>')
        for code in (400, 403, 404, 405):
            r = http_responses_map[code]
            self.writeln('<li>', LINK.format(code=code, title=r.title))

        self.writeln('</ul>')


OVERVIEW = make_overview('\n`WSGIServlet` instances use instances of `HTTPResponse` for building\nthe response to be sent back to the client.  `HTTPResponse` instances\nencapsulate the outgoing content as well as the outgoing HTTP headers.\n\nEvery incoming request creates an attribute, `response`, which is an\ninstance of `HTTPOK`, a subclass of `HTTPResponse`.\n\nCalls to `WSGIServlet.write` and `WSGIServlet.writeln` which send\noutput to the client are actually appending the output to `response`,\nwhich caches all output until it is eventually delivered to the\nclient.  Likewise, when manipulating outgoing headers (e.g., by\nsetting cookies, or creating a session), a container for outgoing\nheaders inside `response` is manipulated.\n\nIf your code runs without exception, the content accumulated in\n`response` (and all the set headers) will be sent to the client.\n\nIf an exception occurs, `repsonse` will be discarded and a new\nresponse will be created, `HTTPInternalServerError`, and returned to\nthe client.  If the `debug` attribute of the servlet is set to `True`\n(it is for this servlet), then the exception stack trace along with\nthe environment will be sent to the client.  If `debug` is set to\n`False` (the default value for servlets unless overridden) then a\nterse message controlled by the `gen500msg` attribute will be sent to\nthe client.\n\n**NOTE: when you click on links in the following examples you will\nwill raise exceptions which produce error pages.  You will need to use\nyour browser back button to return to the tutorial!**\n\nThis link [will simulate an internal exception](/httpresponses/-1).   \nThis link [will simulate an internal exception with debug set\nto False](/httpresponses/-2).    \nThis link [will simulate an internal exception with debug set\nto False and a custom gen500msg](/httpresponses/-3).\n\nSo, how do you return a page to the client other than a HTTP OK\n(status 200) or HTTP Internal Server Error (status 500)?  What if you\nwant to send back a 404 (Not Found), or a 403 (Forbidden) response?\n`HTTPResponse` is a subclass of `Exception`, so the answer is simple:\nraise an exception with a subclass of `HTTPResponse`.  WSGIServlets\ndefines a subclass for each status defined in the HTTP 1.1\nspecification.  See the WSGIServlets reference documentation for a\ncomplete list, but here are examples of a few of the most common (note\nhow any text you specify in the constructor becomes part of the detail\nsent to the client):\n\n')
LINK = '<A href=/httpresponses/{code}>{title}</A>'
DEBUG_EXCEPTION_MSG = "\nWe're simulating some arbitrary python code exception with the debug\nattribute set to True.  When debug is True a stack trace and the\ncontents of the environment are returned to the client.  When debug is\nFalse, a stark error message is returned (the contents of the\ngen500msg attribute).  Setting debug to True while developing your\nservlets will prove an invaluable tool.  You'll want to set it to\nFalse for production environments so you don't broadcast your code to\nthe WWW.\n"
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/auth2.py
# Compiled at: 2011-11-02 16:41:03
from TutorialBase import *
users = {'wsgi': 'servlets'}

class auth2(HTMLPage):
    """Basic HTTP authentication, Part II."""
    title = 'Basic HTTP Authentication (2 of 2)'
    auth_realm = 'WSGI Servlet Auth Tutorial'

    def prep(self):
        self.auth_with_mapping(users)

    def write_content(self):
        self.writeln(OVERVIEW)


OVERVIEW = make_overview("\nWSGIServlets provides three methods and a data attribute for\nimplementing [Basic HTTP\nAuthentication](http://www.ietf.org/rfc/rfc2617.txt):\n\n  * `WSGIServlet.get_basic_auth()`\n\n    Searches the incoming HTTP headers for the `Authorization` header\n    and if found, returns a tuple: (*username*, *password*).  If the\n    header is found but the username and password cannot be decoded,\n    the method does not return and a HTTP Bad Request is sent to the\n    client.  If the header is not found, `unauthorized` is called.\n   \n\n    \n  * `WSGIServlet.unauthorized()`\n\n    Creates a HTTP Unauthorized response, setting the HTTP header\n    `WWW-Authenticate` to the contents of the `auth_realm` attribute.\n    The response is sent directly to the client and the method does\n    not return to the caller.\n\n  * `WSGIServlet.auth_realm`\n\n    A string used by `unauthorized()` to specify the realm for the\n    authentication and will be presented to users by browsers when\n    prompting for a username and password.  This servlet sets\n    `auth_realm` to **WSGI Servlet Auth Tutorial**.\n\n  * `WSGIServlet.auth_with_mapping()`\n\n    A helper method that calls `get_basic_auth` and checks if the\n    returned username and password are non-empty and exist in the\n    mapping passed in to the call.  The mapping's keys are usernames\n    and values are their associated passwords.  Any mapping\n    implementing the standard `dict.get` method can be used.  This\n    servlet uses this method and passes in a mapping: `{'wsgi' :\n    'servlets'}`.\n\n\nSomething to note in the code of this servlet: the call to\n`auth_with_mapping` is made in the `prep` method which is called by\n`_lifecycle` before `write_html`.  This demonstrates placing certain\nkinds of logic outside of content generation.  Also consider we could\nhave placed this call inside an abstract base class:\n\n                WSGIServlet\n                  |\n                  |--HTMLPage\n                       |\n                       |--SitePage\n                            |\n                            |--AuthorizedSitePage\n\n\nWith `AuthorizedSitePage` implemented, in its entirety, as follows:\n\n\n                class AuthorizedSitePage(SitePage):\n\n                      def prep(self):\n\n                            self.auth_with_mapping(SOME_MAPPING)\n                            SitePage.prep(self)\n\n\nIf `SitePage` is an abstract base class implementing the basic layout\nof your site, then all servlets inherititing from `SitePage` will\nrequire no authentication while servlets inheriting from\n`AuthorizedSitePage` will require authentication.\n")
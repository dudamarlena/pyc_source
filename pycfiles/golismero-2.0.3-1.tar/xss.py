# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/injection/xss.py
# Compiled at: 2014-02-05 05:48:48
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Jekkay Hu | jekkay<@>gmail.com\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from . import HTTPInjection

class XSS(HTTPInjection):
    """
    Cross-Site Scripting.

    Cross-site scripting vulnerabilities, also known as XSS, allow an attacker
    to inject arbitrary HTML content into a web page. Typically an attacker
    would inject JavaScript code in order to control the web application on
    behalf of the user, or redirect the user to a malicious site.

    There are several libraries and methods of filtering user input to prevent
    XSS vulnerabilities. Use whichever is provided for your current programming
    language and platform or, if none is available or feasible, try using
    third party products. As a last resort, try developing your own XSS filter
    using the guidelines provided by OWASP.
    """
    DEFAULTS = HTTPInjection.DEFAULTS.copy()
    DEFAULTS['cwe'] = ('CWE-79', 'CWE-80')
    DEFAULTS['cvss_base'] = '6.8'
    DEFAULTS['references'] = ('https://www.owasp.org/index.php/Cross_Site_Scripting_Flaw',
                              'https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)',
                              'https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet',
                              'https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet')
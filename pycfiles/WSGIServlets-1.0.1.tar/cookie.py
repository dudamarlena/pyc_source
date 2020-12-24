# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/cookie.py
# Compiled at: 2011-10-14 15:50:08
from TutorialBase import *
TIMEOUT = 30
COLORS = ['red', 'blue', 'green', 'orange', 'brown']
FILL_COOKIE = 'fill-pref'
DEF_FILL = 'grey'

class cookie(HTMLPage):
    """How to manage cookies."""
    title = 'State Management, Part 1: Cookies'
    fillpref = GET_var()

    def prep(self):
        HTMLPage.prep(self)
        self.fill = fill = None
        if self.method == 'POST':
            fill = self.fillpref
            if not fill or fill not in COLORS:
                self.del_cookie(FILL_COOKIE)
                fill = DEF_FILL
            else:
                self.set_cookie(FILL_COOKIE, fill, expires=TIMEOUT)
                self.fill = fill
        if not fill:
            fill = self.cookies.get(FILL_COOKIE)
            if fill:
                fill = fill.value
                if fill not in COLORS:
                    self.del_cookie(FILL_COOKIE)
                    fill = DEF_FILL
                else:
                    self.fill = fill
            else:
                fill = DEF_FILL
        self.css = self.csstmpl.format(fillpref=fill)
        return

    def write_content(self):
        self.writeln(DEMO.format(fillpref=self.fill))
        self.writeln(OVERVIEW)

    csstmpl = '\n    #floatbox {{\n    float: right;\n    margin: 20px 50px;\n    }}\n    #demobox {{\n    margin-top: 10px;\n    border: 3px solid black;\n    background-color: {fillpref};\n    width: 100px;\n    height: 100px;\n    }}\n    '


OVERVIEW = make_overview("\n\nCookies are easily managed with WSGIServlets.  Servlets have an\nattrbiute, `cookies`, which is a container for incoming cookies and\nis, by default, an instance of `Cookie.SimpleCookie`, a class defined\nin the standard python `Cookie` module.  Any subclass of\n`Cookie.BaseCookie` can be used for incoming cookies.  Which class is\nused is determined by the servlet attribute `cookieclass`.\n\nIf you are unfamiliar with the `Cookie` module you should review the\nstandard python documentation.\n\nIt is recommended you use the standard `Cookie.SimpleCookie` for\nunsigned cookies and `SignedCookie` for cookies where end-user\nmanipulation can present a security risk (e.g., session IDs).  Note,\n`SignedCookie` is *not* part of the standard `Cookie` module and is a\nclass defined in wsgiservlets.\n\nTo set a cookie, use the set_cookie method:\n\n        servlet.set_cookie('default_border', 'red')\n\nTo delete a cookie, use the del_cookie method:\n\n        servlet.del_cookie('default_border')\n\nIn the box in the upper right is a colored box. By submitting the form\nbelow you can set your preference for the fill color.  Then navigate\naway from this page and back and you will see your preference has been\nremembered: it was stored in a cookie, `fill-pref`.  The cookie is set\nto timeout in {timeout} seconds so you can see how the box returns to its\ndefault grey after the cookie expires.\n\n\n")
FORM = '\n<hr>\n<div style="margin-left: 30px;">\n<form method="POST">\n<table>\n<tr>\n<td>\nFill Preference:&nbsp;&nbsp;<select name="fillpref">\n<option selected>Delete Pref</option>\n<option>red</option>\n<option>blue</option>\n<option>green</option>\n<option>orange</option>\n<option>brown</option>\n</select)\n</td>\n<td>\n<input type="submit" value="Set Preferences">\n</td>\n</tr>\n</table>\n</form>\n</div>\n'
OVERVIEW = OVERVIEW.format(timeout=TIMEOUT) + FORM
DEMO = '\n<div id="floatbox">\nDefault&nbsp;fill:&nbsp;grey<br>\nYour&nbsp;fill&nbsp;pref:&nbsp;{fillpref}\n<div id="demobox"></div>\n</div>\n'
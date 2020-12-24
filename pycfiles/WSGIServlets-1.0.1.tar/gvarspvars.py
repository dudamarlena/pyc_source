# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/gvarspvars.py
# Compiled at: 2011-10-12 16:06:46
from TutorialBase import *
GVAR_DEFAULT = 'Gvar default'
PVAR_DEFAULT = 'Pvar default'

class gvarspvars(HTMLPage):
    """Query variables vs form variables and the introduction of POST_var()."""
    title = 'Query Variables vs. Form Variables'
    Gvar = GET_var(GVAR_DEFAULT)
    Pvar = POST_var(PVAR_DEFAULT)

    def write_content(self):
        self.writeln(OVERVIEW)
        if self.Gvar != GVAR_DEFAULT or self.Pvar != PVAR_DEFAULT:
            self.writeln(FORMRESULTS.format(Gvar=self.Gvar, Pvar=self.Pvar))
        self.writeln(THEFORM)


OVERVIEW = make_overview('\nIn a [previous servlet](formdata), both **query variables** and **form\nvariables** were defined.  Since then, we have only used `GET_var` to\ndemonstrate processing URL and form data.  Now we will look at\n`POST_var`.\n\n`POST_var` is identical to `GET_var` except for one detail: while a\n`GET_var` is processed for all requests, any `POST_var` is only\nprocessed for **POST** requests.  For **GET** requests, `POST_var`s\nare set to their default values, whether or not they are in the URL or\nform data.  You may be wondering why this distinction is made and why\nthis functionality exists.  Here are two examples:\n\n  1. There may be applications where you do not want users to submit\n     sensitive data with an URL (like usernames and passwords), but\n     only through your form submissions.\n\n  2. Imagine a list of options a user can choose from (checkboxes,\n     multiple selects), but you want to offer a default selection.\n     With only `GET_vars` there is no way to distinguish between a\n     user deselecting all options from a user viewing a page for the\n     first time.  Using `POST_vars` solves this problem: first time\n     viewing is by GET, so defaults will always be used, but when the\n     form is POSTed, the value will be retrieved with `form.getlist`,\n     which may return an empty list, if all are deselected.\n\nBelow are three ways of setting two variables, `Gvar` and `Pvar`, both\nto the value `1`: setting variables with a URL (via GET) and setting\nthe variables with forms (one via GET, one via POST).  You will notice\nthat `Gvar` is set each time, but `Pvar` is only set with a POST:')
FORMRESULTS = make_formresults('\nValue of **Gvar**: {Gvar}  \nValue of **Pvar**: {Pvar}\n')
THEFORM = '\n<DIV align="center">\n  <TABLE class="formdisplay">\n    <TR>\n      <TD><A href="?Gvar=1&Pvar=1">Set Gvar and Pvar to "1"</A></TD>\n      <TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>\n      <TD><FORM method="GET">\n              <INPUT type="hidden" name="Gvar" value="1">\n              <INPUT type="hidden" name="Pvar" value="1">\n              <INPUT type="submit" value="GET submit">\n          </FORM></TD>\n      <TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>\n      <TD><FORM method="POST">\n              <INPUT type="hidden" name="Gvar" value="1">\n              <INPUT type="hidden" name="Pvar" value="1">\n              <INPUT type="submit" value="POST submit">\n          </FORM></TD>\n    </TR>\n  </TABLE>\n</DIV>\n'
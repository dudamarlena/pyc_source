# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/dicts.py
# Compiled at: 2011-10-14 15:46:31
from TutorialBase import *

class dicts(HTMLPage):
    """Converting form data to python dicts"""
    title = 'Converting URL/Form Data to Python Dicts'
    fields = [
     'name', 'address', 'city', 'state', 'zip', 'email']
    userinfo = GET_var(dict([ (f, '') for f in fields ]))

    def write_content(self):
        self.writeln(OVERVIEW)
        if self.method == 'POST':
            self.writeln(self.process_form())
        self.writeln(self.theform())

    def process_form(self):
        userinfo = self.userinfo.copy()
        for field in self.fields:
            if not userinfo[field]:
                userinfo[field] = '?'

        return FORMRESULTS.format(**userinfo)

    def theform(self):
        return THEFORM.format(**self.userinfo)


OVERVIEW = make_overview('\nThis servlet demonstrates how you can use standard python dicts in\nprocessing forms.  If the `default` parameter to the `GET_var`\nconstructor is a dict, as in:\n\n{codesample}\n\nthen for each request, the servlet will search `form` for names of the\nform *userinfo[KEY]*.  For every such occurrence a new key will\nbe inserted into `userinfo`.\n\nThe dict specified as `default` does not have to be empty.  If\nnon-empty then the keys must be strings and their values must be\nstrings or lists.  If the value is a string then it will be retrieved\nwith `form.getfirst`, if a list, it will be retrieved with\n`form.getlist`.  Note: `default`s that are strings or lists are\n*replaced* when found in `form`, however, with dicts, when keys are\nfound in `form` that are not found in the default, they are *merged*\nwith default dict.\n\nThe benefits of collecting form data under the umbrella of one dict\nare considerable: fewer attributes to manage, resulting in fewer lines\nof cleaner code.  If you create a class that subclasses dict you can\nuse an instance of that class as `default` which will completely\nencapsulate your form in an object!\n\n### Example\n\nIn the form below we name each text INPUT element with the special\nsyntax:\n\n        <input type="text" name="userinfo[name]">\n        <input type="text" name="userinfo[address]">\n        <input type="text" name="userinfo[city]">\n        <input type="text" name="userinfo[state]">\n        <input type="text" name="userinfo[zip]">\n        <input type="text" name="userinfo[email]">\n\nWhen the servlet processes the incoming form it will create one dict\nwith six elements.\n')
OVERVIEW = OVERVIEW.format(codesample='<span class="codesample">userinfo = GET_var({})</span>')
FORMRESULTS = make_formresults('\nname: {name}    \naddress: {address}    \ncity: {city}    \nstate: {state}    \nzip: {zip}    \nemail: {email}    \n')
THEFORM = '\n<FORM method="POST">\n  <DIV align="center">\n    <TABLE class="formdisplay">\n      <TR>\n        <TD>name: </TD>\n        <TD><INPUT type="text" name="userinfo[name]" value="{name}"></TD>\n      </TR>\n      <TR>\n        <TD>address: </TD>\n        <TD><INPUT type="text" name="userinfo[address]" value="{address}"></TD>\n      </TR>\n      <TR>\n        <TD>city: </TD>\n\n        <TD><INPUT type="text" name="userinfo[city]" value="{city}"></TD>\n      </TR>\n      <TR>\n        <TD>state: </TD>\n        <TD><INPUT type="text" name="userinfo[state]" value="{state}"></TD>\n      </TR>\n      <TR>\n        <TD>zip: </TD>\n        <TD><INPUT type="text" name="userinfo[zip]" value="{zip}"></TD>\n      </TR>\n      <TR>\n        <TD>email: </TD>\n        <TD><INPUT type="text" name="userinfo[email]" value="{email}"></TD>\n      </TR>\n      <TR>\n        <TD colspan="2" align="center"><INPUT type="submit"></TD>\n      </TR>\n    </TABLE>\n  </DIV>\n</FORM>\n'
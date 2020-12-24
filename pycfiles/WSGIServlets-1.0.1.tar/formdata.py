# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/formdata.py
# Compiled at: 2011-10-14 15:34:36
from TutorialBase import *

class formdata(HTMLPage):
    """Introduction to processing URL and FORM data using the form attribute."""
    title = 'Processing URL and FORM Data'

    def write_content(self):
        self.writeln(OVERVIEW)
        if self.method == 'POST':
            firstname = self.form.getfirst('firstname')
            age = self.form.getfirst('age')
            self.writeln(FORMRESULTS.format(firstname=firstname, age=age))
        self.writeln(THEFORM)


OVERVIEW = make_overview('\n### Nomenclature\n\n[RFC 2396](http://www.ietf.org/rfc/rfc2396.txt)\nrefers to the part of a URI to the right of a \'?\' as the\nquery, as in:\n\n        <scheme>://<authority><path>?<query>\n\nAn example of an HTTP URL with a query:\n    \n        http://somehost/somepath?firstname=Bob&age=42\n\nHere we say that *firstname* and *age* are **query variables** and\nthat *Bob* and *42* are their **values**.\n\nIn HTML FORM elements, as in:\n\n        <INPUT type="text" name="firstname">\n        <INPUT type="text" name="age">\n\nwe say *firstname* and *age* are **form variables**, *if and only if*\nthe form is submitted with method POST.  If the form is submitted with\nmethod GET, the data will be placed in the URL and so will become\n**query variables**.\n\nWhy we make this distinction between **query variables** and\n**form variables** will be made clear in the next few\nservlets.\n\n### Retrieving Data\n\nFor each request processed by a servlet an attribute is created,\n`form`, and is an instance of `cgi.FieldStorage` (refer to the python\nstandard library documentation for details).  Here we will briefly\nshow how you can use the `form` attribute to retrieve data.\n            \n')
FORMRESULTS = make_formresults('\nFirst Name: {firstname}      \nAge: {age}\n')
THEFORM = '\n<div align="center">\n<form method="POST">\n\n<table class="formdisplay">\n<tr>\n<td>First Name:</td>\n<td><input name="firstname"></td>\n</tr>\n<tr>\n<td>Age:</td>\n<td><input name="age" size="4"></td>\n</tr>\n<tr>\n<td colspan="2" align="center"><input type="submit" value="Try Me"></td>\n</tr>\n</table>\n\n</form>                     \n</div>\n'
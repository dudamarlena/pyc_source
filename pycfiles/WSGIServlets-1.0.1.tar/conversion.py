# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/conversion.py
# Compiled at: 2011-10-28 11:32:03
from TutorialBase import *

def _age(age):
    """Converts age (a string) to an int.  All values < 1 return as -1"""
    try:
        a = int(age)
    except:
        return -1

    if a < 1:
        return -1
    return a


class conversion(HTMLPage):
    """Converting query variables to arbitrary python types."""
    title = 'Converting Query Variables to Arbitrary Types'
    firstname = GET_var()
    age = GET_var('-1', _age)

    def write_content(self):
        self.writeln(OVERVIEW)
        if self.method == 'POST':
            self.writeln(self.process_form())
        self.writeln(THEFORM.format(firstname=self.firstname, age=self.age if self.age != -1 else ''))

    def process_form(self):
        if self.firstname and self.age != -1:
            return FORMRESULTS.format(firstname=self.firstname, age=self.age, msg='')
        else:
            f = self.firstname if self.firstname else 'First name is required'
            a = self.age if self.age != -1 else 'A proper age is required'
            return FORMRESULTS.format(firstname=f, age=a, msg='There was a problem!')


OVERVIEW = make_overview("\nBy default, all data returned via an URL or the posting of a form are\nstrings. This can make for tedious programming having to manually\nconvert the incoming strings to other python types.  Using `GET_var`\neliminates much of this tedium by allowing the developer to specify\nexactly what types each attribute should be by specifying a default\nvalue and/or providing a conversion function.\n\nThis servlet will demonstrate how to convert strings to arbitrary\ntypes by specifying a conversion function. The next servlets will\ndemonstrate special treatment for python lists and dicts.\n\nThe constructor for `GET_var` is:\n\n{codesample}      \n\nThe first argument, `default`, specifies the default value for the\nattribute if it is not found in `form`.  The value of default must be\na string, list or dict.\n\nThe second argument, `conv`, specifies the conversion function and\nmust be None (the default, which does no conversion) or be a callable\nthat accepts a single argument and returns the converted value. If the\nconversion function raises an exception the attribute will be set to\nits default value.\n\nThis servlet creates two such variables with the following\ndeclarations:\n\n        firstname = GET_var()\n        age = GET_var('-1', _age)\n\n\n`firstname` specifies no default (so the default value will be the\nempty string) and no conversion (so the result will be type `str`).\n`age` will be an `int`, the incoming string from the request will be\npassed through the conversion function, `_age` (view the source to see\nhow it is implemented).  If the value passed in through the form is\nillegal, the value stored in age will be -1, which can act as a flag\nin the code for an unspecified or illegal value.\n")
OVERVIEW = OVERVIEW.format(codesample='<span class="codesample">def __init__(self, default=\'\', conv=None)</span>')
FORMRESULTS = make_formresults('\n{span}\n\nFirst Name: {{firstname}}  \nAge: {{age}}\n').format(span='<span style="color:red">{msg}</span>')
THEFORM = '\n<div align="center">\n<form method="POST">\n\n<table class="formdisplay">\n<tr>\n<td>First Name:</td>\n<td><input name="firstname" value="{firstname}"></td>\n</tr>\n<tr>\n<td>Age:</td>\n<td><input name="age" value="{age}" size="4"></td>\n</tr>\n<tr>\n<td colspan="2" align="center"><input type="submit" value="Try Me"></td>\n</tr>\n</table>\n\n</form>                     \n</div>\n'
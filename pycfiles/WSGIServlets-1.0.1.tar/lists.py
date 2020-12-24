# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/lists.py
# Compiled at: 2011-10-12 16:07:08
from TutorialBase import *

class lists(HTMLPage):
    """Converting form data to python lists"""
    title = 'Converting URL/Form Data to Python Lists'
    all_colors = ['red', 'blue', 'green', 'violet', 'cyan', 'amber']
    all_animals = ['dog', 'cat', 'African Sparrow', 'hippopotamus', 'grub',
     'python']
    colors = GET_var([])
    animals = GET_var([])

    def write_content(self):
        self.writeln(OVERVIEW)
        if self.method == 'POST':
            self.writeln(self.process_form())
        self.writeln(self.theform())

    def process_form(self):
        nofav = '<span style="color:red">You don\'t have any favorite %s!</span>'
        colors = (', ').join(self.colors) if self.colors else nofav % 'colors'
        animals = (', ').join(self.animals) if self.animals else nofav % 'animals'
        return FORMRESULTS.format(colors=colors, animals=animals)

    def theform(self):
        colors = []
        for color in self.all_colors:
            colors.append(INPUT.format(color=color, checked='checked' if color in self.colors else ''))

        animals = []
        for animal in self.all_animals:
            animals.append(OPTION.format(animal=animal, selected='selected' if animal in self.animals else ''))

        return THEFORM.format(colors=('<BR>\n').join(colors), animals=('\n').join(animals))


OVERVIEW = make_overview('\nI said in the previous servlet that the `default` parameter to\n`GET_var` had to be a string, list or dict.  The data type of\n`default` determines how the data is extracted from `form`.  If\n`default` is a string, the value will be retrieved with a call to\n`form.getfirst()`. If `default` is a list, the value will be retrieved\nwith a call to `form.getlist()`. If `default` is a dict, form will be\nsearched for variables with names of the form *NAME[KEY]*.\n\nIf you are not familiar with the `getfirst` and `getlist` methods, you\nshould review the python standard library documentation; see\n`cgi.FieldStorage`.\n\nThis servlet will demonstrate lists. The next will demonstrate dicts.\n\nWhen `default` specifies a list, it can be empty or have elements, but\nif it has elements they must be strings.  You may also specify a\nconverstion object, in which case it should be a callable that expects\na list as its only argument; it may return any arbitrary object, but\ntypically you will want it to return a list with its elements\nconverted to some arbitrary type, e.g., convert a list of strings into\na list of ints.\n\nWhen do you want to use lists? They are particularly handy when\nprocessing `INPUT` elements with the `type` attribute set to\n*checkbox* and `SELECT` elements with the `multiple` attribute set.\nHere is an example of each:\n')
FORMRESULTS = make_formresults('\nYour favorite colors are: {colors}    \nYour favorite animals are: {animals}\n')
THEFORM = '\n<FORM method="POST">\n  <DIV align="center">\n    <TABLE class="formdisplay">\n      <TR valign="top">\n        <TD>Favorite Colors:</TD>\n        <TD>{colors}</TD>\n        <TD>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</TD>\n        <TD>Favorite Animals:</TD>\n        <TD><SELECT multiple name="animals" size="6">{animals}</SELECT></TD></TR>\n      <TR>\n        <TD colspan="5" align="center"><INPUT type="submit" value="Submit Favorites"></TD></TR></TABLE></DIV></FORM>\n\n'
INPUT = '<INPUT type="checkbox" {checked} name="colors" value="{color}"> {color}'
OPTION = '<OPTION {selected}>{animal}</OPTION>'
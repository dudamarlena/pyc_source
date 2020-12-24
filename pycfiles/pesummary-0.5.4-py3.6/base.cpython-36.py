# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/core/webpage/base.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 3528 bytes
import numpy as np

class Base(object):
    __doc__ = 'Meta class containing helper functions for generating webpages\n    '

    def close(self):
        """Close the opened html file.
        """
        self.html_file.close()

    def _check_content(self, content):
        """Make sure that the content has new line in string

        Parameters
        ----------
        content: str
            string that you want to check
        """
        if content[(-1)] != '\n':
            content += '\n'
        return content

    def add_content(self, content, indent=0):
        """Add content to the html page

        Parameters
        ----------
        content: str/list, optional
            either a single string or a list of string that you want to add to
            your html page
        indent: int, optional
            the indent of the line
        """
        if type(content) == list:
            for i in np.arange(len(content)):
                content[i] == self._check_content(content[i])
                self.html_file.write(' ' * indent + content)

        else:
            content = self._check_content(content)
            self.html_file.write(' ' * indent + content)

    def make_div(self, indent=0, _class=None, _style=None, _id=None):
        """Make a div of your choice

        indent: int, optional
            the indent of the line
        _class: str, optional
            the class name of your div
        _style: str, optional
            the style of your div
        _id: str, optional
            the id of your div
        """
        string = '<div'
        if _class:
            string += " class='%s'" % _class
        if _style:
            string += " style='%s'" % _style
        if _id:
            string += " id='%s'" % _id
        string += '>\n'
        self.add_content(string, indent=indent)

    def end_div(self, indent=0):
        """End a div of your choice

        Parameters
        ----------
        indent: int, optional
            the indent of the new line
        """
        self.add_content('</div>', indent)

    def make_container(self, style=None, indent=0):
        """Make a container for your webpage

        Parameters
        ----------
        indent: int, optional
            the indent of the new line
        """
        if not style:
            style = 'margin-top:3em; margin-bottom:5em; background-color:#FFFFFF; box-shadow: 0 0 5px grey; max-width: 1400px'
        self.make_div(indent, _class='container', _style=style)

    def end_container(self, indent=0):
        """End a container

         Parameters
         ----------
         indent: int, optional
             the indent of the new line
         """
        self.end_div(indent)
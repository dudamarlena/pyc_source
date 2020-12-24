# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/html_multipage_navigator/web_browser.py
# Compiled at: 2011-09-28 13:50:09
import mechanize

class AbstractWebBrowser:
    """An abstract functionality of a web browser"""

    def open(self, address):
        """Open a web page with a given address"""
        raise NotImplementedError

    def response(self):
        """
                Return a copy of the currently opened web page

                @rtype: file-like object
                """
        raise NotImplementedError

    def back(self, steps=1):
        """Go back C{steps} steps in history"""
        raise NotImplementedError


class AbstractWebBrowserCreator:
    """The 'Creator' class from the Factory Method design pattern"""

    def create(self):
        """
                Create a browser. This method has to be thread-safe since it is 
                called as the method of the same object in different threads.
                
                @rtype: L{AbstractWebBrowser}
                """
        raise NotImplementedError


class MechanizeBrowser(AbstractWebBrowser):
    """The default browser. It uses C{mechanize} library"""

    def __init__(self):
        self.__br = mechanize.Browser()

    def open(self, address):
        self.__br.open(address)

    def response(self):
        return self.__br.response()

    def back(self, steps=1):
        self.__br.back(steps)


class MechanizeBrowserCreator(AbstractWebBrowserCreator):

    def create(self):
        return MechanizeBrowser()
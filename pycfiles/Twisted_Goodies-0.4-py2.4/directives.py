# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted_goodies/simpleserver/http/rest/directives.py
# Compiled at: 2007-07-25 20:52:30
"""
Module for reStructuredText Directives

"""
import sre
from docutils import nodes
from docutils.parsers.rst import directives
import nevow.tags as T

class Manager:
    """
    I register reStructuredText directives (as d_* methods of a Directives()
    object) and provide lock/unlock methods for setting them up for per-page
    use
    """
    __module__ = __name__

    def __init__(self):
        """
        Constructs a separate button object for each instance and (just the
        first time) registers all of my d_* methods as rEST directive(s)
        """
        button = Button(page.parentResource, bgColor='#FFFFFF')
        if not self.__class__.buttonDict:
            myDirectives = Directives(self)
            self.directiveNames = [ x.replace('d_', '') for x in myDirectives.__class__.__dict__.keys() if str(x).startswith('d_') ]
            for name in self.directiveNames:
                object = getattr(myDirectives, 'd_' + name)
                directives.register_directive(name, object)

        self.__class__.buttonDict[id(page)] = (page.config, button)

    def get(self, objectName):
        """
        Returns the named object, used by directives because their attributes
        are frozen when registered

        """
        pageID = self.__class__.pageID
        (self.config, self.button) = self.__class__.buttonDict[pageID]
        print 'DEBUG dir: %s' % dir(self)
        return getattr(self, objectName)

    def lock(self, page):
        """
        Locks all instances of me to the supplied parent resource
        
        THREADS BEWARE
        """
        self.__class__.pageID = id(page)

    def unlock(self):
        """
        Unlocks (really just a feel-good placeholder for now)

        """
        self.__class__.pageID = None
        return


class Directives:
    """
    I house custom reStructuredText directives as d_* methods.
    """
    __module__ = __name__
    rePatentNumber = sre.compile('[0-9],?[0-9]{3},?[0-9]{3}')

    def error(self, textProto, textTuple, *arg):
        """
        Generates a suitable error message from the supplied text
        
        """
        text = textProto % textTuple
        error = arg[8].reporter.error(text, nodes.literal_block(arg[6], arg[6]), line=arg[4])
        return [error]

    def parse(self, *arg):
        """
        Parses the args for a rEST directive function, returning a tuple with the
        first (only?) argument and the options dictionary
        
        """
        return (
         arg[1][0], arg[2])

    def d_patent(self, *arg):
        """
        Returns a link to full text of a patent whose number is supplied
        
        """
        (pn, opts) = self.parse(*arg)
        if not self.rePatentNumber.match(pn):
            return self.error('"%s" is not a valid patent number', pn, *arg)
        url = 'http://patft.uspto.gov/netacgi/nph-Parser?patentnumber=%s' % pn.replace(',', '')
        html = '<a href="%s">%s</a>' % (url, pn)
        return [nodes.raw('', html, format='html')]

    d_patent.arguments = (1, 0, 0)
    d_patent.options = {}
    d_patent.content = False
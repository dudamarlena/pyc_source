# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\pypp\trunk\pypp\preprocessor.py
# Compiled at: 2009-03-07 07:08:56
""" Preprocessor class
    project: pypp
    
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: preprocessor.py 12 2009-03-05 06:17:28Z jeanlou.dupont $'
__all__ = [
 'Tpl']
import os, sys
try:
    from mako.template import Template
    from mako.lookup import TemplateLookup
except:
    print 'pypp: Mako template package not found. Please install'
    sys.exit(1)

def stripLeadingHash(text):
    """ Strips the leading # from open & close Mako tags
        i.e. #<%    #</%
    """
    return text.replace('#<%', '<%').replace('#</%', '</%')


def stripLeadingHashFromVar(text):
    """ Strips the leading # from variable references
        i.e.  #${ 
    """
    return text.replace('#${', '${')


class Tpl(object):
    """ Template based on the Mako engine
    """

    def __init__(self, input, dirs=None):
        """ The directory path of the input file
            serves as configuration for the template
            directory by default. If *dirs* is specified,
            it takes precedence.
            
            @param input: the input file (complete file path)
            @param dirs: the template directory list   
        """
        self.input = input
        self.dirs = dirs

    def render(self, **params):
        """ Performs the preprocessing.
            @param params: the input parameters
            @return: rendered text            
        """
        lookup = TemplateLookup(directories=self.dirs) if self.dirs else None
        tpl = Template(text=self.input, lookup=lookup, cache_enabled=False, preprocessor=[stripLeadingHash, stripLeadingHashFromVar])
        return tpl.render(**params)
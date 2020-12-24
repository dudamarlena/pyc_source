# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyfo.py
# Compiled at: 2007-06-12 14:53:48
__doc__ = 'pyfo - Generate XML using native python data structures.\n\nCreated and maintained by Luke Arno <luke.arno@gmail.com>\n\nSee documentation of pyfo method in this module for details.\n\nCopyright (C) 2006-2007  Central Piedmont Community College\n\nThis library is free software; you can redistribute it and/or\nmodify it under the terms of the GNU Lesser General Public\nLicense as published by the Free Software Foundation; either\nversion 2.1 of the License, or (at your option) any later version.\n\nThis library is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\nLesser General Public License for more details.\n\nYou should have received a copy of the GNU Lesser General Public\nLicense along with this library; if not, write to \nthe Free Software Foundation, Inc., 51 Franklin Street, \nFifth Floor, Boston, MA  02110-1301  USA\n\nCentral Piedmont Community College\n1325 East 7th St.\nCharlotte, NC 28204, USA\n\nLuke Arno can be found at http://lukearno.com/\n\n'
import re
from xml.sax.saxutils import escape

def isiterable(it):
    """return True if 'it' is iterable else return False."""
    try:
        iter(it)
    except:
        return False
    else:
        return True


def make_attributes(dct):
    """Turn a dict into string of XML attributes."""
    return ('').join((' %s="%s"' % (x, escape(unicode(y))) for (x, y) in dct.iteritems()))


def pyfo(node, prolog=False, pretty=False, indent_size=2, encoding='utf-8', collapse=True):
    """Generate XML using native python data structures.
   
    node structure like (name, contents) or (name, contents, attribs)
    accepts stings, callables, or another node structure.
   
    pyfo should be called with a tuple of two or three items like so:
    (element, contents, attributes) or a string.

    for a tuple:
    
        the first item:
            is the element name.
  
        the second item:
            if it is callable, it is called 
            and its return value .
    
            if it is a list, pyfo is called on all its members 
            and the results are concatenated to become the contents.

            otherwise it is run through 'unicode' and 'escape'.
    
        optional third item: 
            should be a dictionary used as xml attributes
    
    for a string:
        
        just return it as unicode.
    """
    if callable(node):
        node = node()
    if not node:
        return ''
    if pretty and pretty >= 0:
        if pretty is True:
            pretty = 1
        indent = '\n' + ' ' * indent_size * pretty
        unindent = '\n' + ' ' * indent_size * (pretty - 1)
        pretty += 1
    else:
        unindent = indent = ''
    if isinstance(node, basestring):
        return unicode(node)
    elif len(node) == 2:
        (name, contents) = node
        dct = {}
    else:
        (name, contents, dct) = node
    leaf = False
    if callable(contents):
        contents = contents()
    if isinstance(contents, dict):
        contents = contents.items()
    if isinstance(contents, tuple):
        contents = pyfo(contents, pretty=pretty, indent_size=indent_size, collapse=collapse)
    elif not isinstance(contents, basestring) and isiterable(contents):
        cgen = (pyfo(c, pretty=pretty, indent_size=indent_size, collapse=collapse) for c in contents)
        contents = indent.join((c for c in cgen if c))
    elif contents not in [None, '']:
        contents = escape(unicode(contents))
        leaf = True
    if leaf:
        indent = unindent = ''
    if prolog:
        prolog = '<?xml version="1.0" encoding="%s"?>\n' % encoding
    else:
        prolog = ''
    if contents or not collapse:
        return '%s<%s%s>%s%s%s</%s>' % (prolog, name, make_attributes(dct), indent, contents or '', unindent, name)
    else:
        return '%s<%s%s/>' % (prolog, name, make_attributes(dct))
    return
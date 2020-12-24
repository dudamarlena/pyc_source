# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/renderers/Python.py
# Compiled at: 2011-09-28 02:31:46
__doc__ = '$id$'
import Globals, Products, os, pydoc, inspect, sys, re, keyword, logging
from pydoc import classname, HTMLDoc, getdoc, allmethods, isdata, ispackage
from string import expandtabs, find, join, lower, split, strip, rfind, rstrip, replace
from OFS.ObjectManager import ObjectManager
from OFS.PropertyManager import PropertyManager
from OFS.DTMLMethod import DTMLMethod
from OFS.SimpleItem import SimpleItem
from PyDoc import PyDoc
from Products.Zpydoc.inspectors.PythonInfo import PackageInfo
from Products.PageTemplates.ZopePageTemplate import ZopePageTemplate
from AccessControl.Permissions import view
LOG = logging.getLogger('ZpyDoc.renderers.Python')
keyword_re = re.compile('(\\W)(%s)(\\W)' % join(keyword.kwlist, '|'))
class_re = re.compile('^class ')
space_re = re.compile(' ')

class Python(ObjectManager, PropertyManager, PyDoc):
    """
    Render a standard pydoc page using ZPT's
    """
    meta_type = 'PythonRenderer'
    __ac_permissions__ = ObjectManager.__ac_permissions__ + ((view, ('read', 'format')),) + PropertyManager.__ac_permissions__
    id = 'Python'
    title = 'Customisable Python (ZPT)'

    def __init__(self):
        thisdir = os.path.dirname(__file__)
        self._setObject('index', ZopePageTemplate('index', open(os.path.join(thisdir, 'zpt', 'p_index.zpt')).read()))
        self._setObject('document', ZopePageTemplate('document', open(os.path.join(thisdir, 'zpt', 'p_document.zpt')).read()))
        self._setObject('standard_template.pt', ZopePageTemplate('standard_template.pt', open(os.path.join(thisdir, 'zpt', 'standard_template.zpt')).read()))
        self._setObject('stylesheet.css', DTMLMethod(open(os.path.join(thisdir, 'zpt', 'stylesheet.css')).read(), __name__='stylesheet.css'))

    manage_options = ObjectManager.manage_options + PropertyManager.manage_options + SimpleItem.manage_options

    def __getattr__(self, name):
        """
        we seem to be returning a function that ObjectManager confuses with an object ...
        """
        obj = Python.inheritedAttribute('_getattr__')(self, name)
        if obj and hasattr(obj, 'meta_type'):
            return obj
        else:
            return

    def __call__(self, object, name):
        """ render page using our Python info object """
        return self.document(self, self.REQUEST, PackageInfo(object, name))

    def read(self, filename):
        """
        return the contents of a file

        this just returns raw contents so that you can plug in your own parser ...
        """
        return open(filename, 'r').read()

    def format(self, filename):
        """
        return a basic html rendering of a python source file - this is a *very*
        unsophisticated parser ...
        """
        content = []
        for line in open(filename, 'r').readlines():
            if line.find('#') != -1:
                (line, comment) = line.split('#', 1)
                comment = '<span class="comment">#%s</span>' % comment
            else:
                comment = ''
            i = 0
            while len(line) > i and line[i] == ' ':
                i += 1

            if i:
                line = re.sub(space_re, '&nbsp;', line, i)
            line = re.sub(keyword_re, '\\1<span class="keyword">\\2</span>\\3', line)
            line = re.sub(class_re, '<span class="keyword">class</span>&nbsp;', line)
            content.append('%s%s' % (line, comment))

        content = join(content, '<br>')
        return content


Globals.InitializeClass(Python)

def manage_addPythonRenderer(self, REQUEST=None):
    """ """
    try:
        self._setObject('Python', Python())
    except:
        pass

    if REQUEST:
        return self.manage_main(self, REQUEST)
    return self.Python
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/zcml.py
# Compiled at: 2009-05-04 14:30:04
import os.path
from zope.schema import TextLine
from zope.interface import Interface, classImplements
from zope.component.zcml import adapter
from zope.configuration.fields import Tokens, Path
from zope.configuration.exceptions import ConfigurationError
from interfaces import ITemplate, ITemplates

class ITemplateDirective(Interface):
    """Persistent Cheetah template directive."""
    __module__ = __name__
    name = TextLine(title='Unique name')
    title = TextLine(title='Title')
    storage = TextLine(title='Local name of the storage')
    variables = Tokens(title='Variables names', value_type=TextLine(), default=[], required=False)
    source = Path(title='Source template file, using Cheetah syntax.', default=None, required=False)


def read_src(path):
    f = open(path)
    src = f.read()
    f.close()
    return src


def templateDirective(_context, name, title, storage, variables=[], source=None):
    path = os.path.abspath(str(_context.path(source)))
    if not os.path.isfile(path):
        raise ConfigurationError('No such file', path)

    def __init__(self, context):
        self.context = context

    cdict = {'__init__': __init__, 'title': title, 'storage': storage, 'variables': variables, 'source': read_src(path)}
    klass = type('Template', (), cdict)
    classImplements(klass, ITemplate)
    adapter(_context, (klass,), provides=ITemplate, for_=(ITemplates,), name=name)
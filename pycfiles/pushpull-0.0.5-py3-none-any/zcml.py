# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/zcml.py
# Compiled at: 2006-09-22 15:28:54
import os
from zope.interface import Interface
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Path
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import TextLine
from zope.security.checker import CheckerPublic
from zope.security.checker import Checker
from zope.app.component.fields import LayerField
from zope.app.component.interface import provideInterface
from zope.app.component.metaconfigure import handler
from zope.app.security.fields import Permission
try:
    import Zope2
except ImportError:
    from pushpage.browser import PushPageFactory
else:
    from pushpage.z2 import Z2PushPageFactory as PushPageFactory

class IPushPageViewDirective(Interface):
    """ Create a view using a push page template.

    Example:

     <configure xmlns="http://namespaces.zope.org/zope"
                xmlns:pushpage="http://namespaces.zope.org/pushpage">

      <pushpage:view
        for=".interfaces.ISomeContentInterface"
        name="somepage.html"
        permission="zope.Public"
        template="templates/sometemplate.pt"
        mapping=".somemodule,somefunction"
        layer="mylayer"
        />

     </configure>
    """
    __module__ = __name__
    for_ = GlobalInterface(title='Target Interface', description="The interface for which this view is registered.\n            \n            '*' maps to None, which registers the view for *all* objects.", required=True)
    name = TextLine(title='The name of the page (view)', description="The name shows up in URLs/paths.\n        \n            For example, 'page.html'.", required=True)
    permission = Permission(title='Permission', description='The permission needed to use the view.', required=True)
    template = Path(title='', description='The name of a template that implements the page.\n\n            Path to a file containing a page template.', required=True)
    mapping = GlobalObject(title='Value Mapping', description='Dotted name of a callable providing values to the page.', required=True)
    layer = LayerField(title='Skin Layer', description='The layer the page should be found in.\n\n        For information on layers, see the documentation for the browser:skin\n        directive.\n        \n        Defaults to IDefaultBrowserLayer.', required=False)


def pushpageViewDirective(_context, for_, name, permission, template, mapping, layer=IDefaultBrowserLayer):
    """ Create and register factory for pushpage-driven views.
    """
    if for_ is not None:
        _context.action(discriminator=None, callable=provideInterface, args=('', for_))
    if permission == 'zope.Public':
        permission = CheckerPublic
    template = os.path.abspath(str(_context.path(template)))
    if not os.path.isfile(template):
        raise ConfigurationError('No such file', template)
    required = {'__call__': permission, '__getitem__': permission, 'browserDefault': permission, 'publishTraverse': permission}
    checker = Checker(required)
    factory = PushPageFactory(open(template, 'r'), mapping, checker)
    _context.action(discriminator=('view', for_, name, IBrowserRequest, layer), callable=handler, args=('provideAdapter', (for_, layer), Interface, name, factory, _context.info))
    return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/paypal.py
# Compiled at: 2013-03-02 05:42:46
__docformat__ = 'restructuredtext'
from z3c.json.interfaces import IJSONWriter
from zope.traversing.interfaces import TraversalError
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.gallery.interfaces import IGalleryManagerPaypalInfo, IGalleryImage, IGalleryImagePaypalInfo, IGalleryImageExtension
from ztfy.skin.interfaces import IDialogEditFormButtons
from ztfy.skin.layer import IZTFYBackLayer
from z3c.form import field, button
from z3c.formjs import ajax, jsaction
from z3c.template.template import getLayoutTemplate
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from zope.traversing import api as traversing_api
from zope.traversing import namespace
from ztfy.gallery.skin.menu import GallerySkinDialogMenuItem
from ztfy.skin.form import DialogEditForm
from ztfy.utils.traversing import getParent
from ztfy.gallery import _

class SiteManagerPaypalNamespaceTraverser(namespace.view):
    """++paypal++ namespace"""

    def traverse(self, name, ignored):
        result = getParent(self.context, ISiteManager)
        if result is not None:
            return IGalleryManagerPaypalInfo(result)
        else:
            raise TraversalError('++paypal++')
            return


class SiteManagerPaypalEditForm(DialogEditForm):
    """Site manager Paypal edit form"""
    legend = _('Edit Paypal properties')
    fields = field.Fields(IGalleryManagerPaypalInfo)
    layout = getLayoutTemplate()
    parent_interface = ISiteManager

    def getContent(self):
        return IGalleryManagerPaypalInfo(self.context)


class SiteManagerPaypalMenuItem(GallerySkinDialogMenuItem):
    """Paypal properties menu item"""
    title = _(':: Paypal account...')
    target = SiteManagerPaypalEditForm


class GalleryImagePaypalNamespaceTraverser(namespace.view):
    """++paypal++ namespace for images"""

    def traverse(self, name, ignored):
        result = IGalleryImagePaypalInfo(self.context, None)
        if result is not None:
            return result
        else:
            raise TraversalError('++paypal++')
            return


class GalleryImagePaypalExtension(object):
    """Gallery image Paypal extension"""
    adapts(IGalleryImage, IZTFYBackLayer)
    implements(IGalleryImageExtension)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.paypal = IGalleryImagePaypalInfo(self.context)

    title = _('Enable or disable Paypal')

    @property
    def icon(self):
        if self.paypal.paypal_enabled:
            name = 'enabled'
        else:
            name = 'disabled'
        return '/--static--/ztfy.gallery.back/img/paypal-%s.png' % name

    @property
    def klass(self):
        if self.paypal.paypal_enabled:
            return 'paypal enabled'
        else:
            return 'paypal disabled'

    @property
    def url(self):
        return "javascript:$.ZBlog.gallery.paypal_switch('%s');" % traversing_api.getName(self.context)

    weight = 50


class GalleryImagePaypalEditForm(DialogEditForm):
    """Gallery image Paypal edit form"""
    buttons = button.Buttons(IDialogEditFormButtons)
    fields = field.Fields(IGalleryImagePaypalInfo)

    def __call__(self):
        info = IGalleryImagePaypalInfo(self.context)
        if info.paypal_enabled:
            return super(GalleryImagePaypalEditForm, self).__call__()
        else:
            info.paypal_enabled = True
            writer = getUtility(IJSONWriter)
            return writer.write({'output': 'OK'})

    @jsaction.handler(buttons['dialog_submit'])
    def submit_handler(self, event, selector):
        return '$.ZBlog.gallery.paypal_edit(this.form);'

    @jsaction.handler(buttons['dialog_cancel'])
    def cancel_handler(self, event, selector):
        return '$.ZTFY.dialog.close();'

    @ajax.handler
    def ajaxEdit(self):
        writer = getUtility(IJSONWriter)
        self.updateWidgets()
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            self.update()
            return writer.write({'output': self.layout()})
        else:
            if self.applyChanges(data):
                parent = getParent(self.context, self.parent_interface)
                notify(ObjectModifiedEvent(parent))
                return writer.write({'output': 'OK', 'enabled': IGalleryImagePaypalInfo(self.context).paypal_enabled})
            return writer.write({'output': 'NONE'})
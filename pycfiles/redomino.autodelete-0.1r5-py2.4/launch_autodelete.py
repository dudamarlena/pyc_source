# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/browser/launch_autodelete.py
# Compiled at: 2008-09-16 09:17:13
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
from zope.interface import implements
from zope.component import queryUtility
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from redomino.autodelete import autodeleteMessageFactory as _
from redomino.autodelete.interfaces import IAutodeleteControlPanel
from redomino.autodelete.utils.interfaces import IAutoDelete

class AutodeleteControlPanel(BrowserView):
    """ AutodeleteControlPanel view """
    __module__ = __name__
    implements(IAutodeleteControlPanel)
    label = _('Autodelete control panel')
    description = _('You can run manually the autodelete task for element expired.')
    __call__ = ViewPageTemplateFile('templates/control-panel.pt')

    def delete(self):
        """ Delete task """
        response = self.request.response
        response.setHeader('Content-type', 'text/html')
        try:
            auto_delete = queryUtility(IAutoDelete)
            if auto_delete:
                for item in auto_delete.run_autodelete():
                    if isinstance(item, unicode):
                        response.write(item.encode() + '<br />')
                    else:
                        response.write(item + '<br />')

            response.write('Done')
        except Exception, e:
            response.write('An error was occurred: ' + str(e))
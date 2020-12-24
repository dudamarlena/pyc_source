# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimageschema/imagedisplay.py
# Compiled at: 2008-12-23 17:55:58
"""SmartImageDisplayWidget class for the Zope 3 based ks.widget package

$Id: imagedisplay.py 35340 2008-06-13 19:34:06Z anatoly $
"""
__author__ = 'Anatoly Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 35340 $'
__date__ = '$Date: 2008-06-13 22:34:06 +0300 (Fri, 13 Jun 2008) $'
__credits__ = 'Based heavily on Anatoly Bubenkov sources'
from zope.interface import Interface
from zope.app.zapi import absoluteURL
from zope.app.form.browser.widget import DisplayWidget, renderElement
from ks.smartimage.smartimageadapter.interfaces import ISmartImageContainer
from ks.smartimage.smartimagecache.interfaces import ISmartImageProp
from zope.component import ComponentLookupError, getUtility, getMultiAdapter
from logging import getLogger
logger = getLogger('ks.smartimage')

class ImageDisplay(object):
    __module__ = __name__
    cssClass = ''
    extra = ''

    def imagedisplay(self, value):
        res = []
        if value.title:
            res.append(renderElement('p', contents=value.title))
        if value.data is not None and value.data:
            src = self.imageurl(value)
            if value.title is None:
                alt = ''
            else:
                alt = value.title
            res.append(renderElement('img', src=src, alt=alt, cssClass=self.cssClass, extra=self.extra))
        return ('\n').join(res)

    def imageurl(self, value):
        try:
            cache = getUtility(ISmartImageProp)
        except ComponentLookupError, msg:
            logger.warning('Getting image cache fault, widgets will be used without cache', exc_info=False)
            src = absoluteURL(self.context.context, self.request) + '/++attribute++' + self.context.__name__
        else:
            img = ISmartImageContainer(value)[(self.context.scale or getUtility(ISmartImageProp).scale)]
            if cache.use_basepath:
                src = ''
                if cache.basepath:
                    src = cache.basepath + '/'
                src = src + '@@smartimagebyid/' + str(img.uniqid) + '/' + img.__name__ + '/get'
            else:
                src = absoluteURL(self.context.context, self.request) + '/++attribute++' + self.context.__name__ + '/' + '@@smartimagecontainer/' + img.__name__ + '/get'

        return src
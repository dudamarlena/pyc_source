# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/red5/protectedvod/utils.py
# Compiled at: 2009-08-19 12:31:49
from zope.interface import implements
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.PythonScripts.standard import url_quote_plus
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from plone.memoize.view import memoize
from interfaces import IRed5ProtectedVodTool
import logging, hmac
logger = logging.getLogger('unimr.red5.protectedvod')

class Red5ProtectedVodTool(BrowserView):
    """A view that implements a hmac algorithm for url signatures
       in interaction with a red5 streaming server
    """
    __module__ = __name__
    implements(IRed5ProtectedVodTool)

    def netConnectionUrl(self, fieldname='file'):
        """ returns the netConnectionUrl including path, signature and expire date"""
        data = self._signature_data(fieldname=fieldname)
        return '%(server_url)s/%(path)s/%(signature)s/%(expires)s' % data

    def clip(self, fieldname='file'):
        """ return clip's name """
        data = self._signature_data(fieldname=fieldname)
        return '%(filename)s' % data

    @memoize
    def _signature_data(self, fieldname='file'):
        context = aq_inner(self.context)
        request = self.request
        properties_tool = getToolByName(context, 'portal_properties')
        hmac_properties = getattr(properties_tool, 'red5_protectedvod_properties', None)
        red5_server_url = hmac_properties.getProperty('red5_server_url')
        red5_server_url = red5_server_url.rstrip('/')
        secret_phrase = hmac_properties.getProperty('secret')
        try:
            ttl = int(hmac_properties.getProperty('ttl'))
        except ValueError:
            ttl = 60

        clientip = request.get('HTTP_X_FORWARDED_FOR', None)
        if not clientip:
            clientip = request.get('REMOTE_ADDR', None)
        expires = '%08x' % (DateTime().timeTime() + ttl)
        (path, filename) = self._fss_info(fieldname)
        sign_path = '/%s/' % (path,)
        signature = hmac_hexdigest(secret_phrase, [sign_path, filename, clientip, expires])
        data = {'server_url': red5_server_url, 'sign_path': sign_path, 'path': path, 'filename': filename, 'expires': expires, 'clientip': clientip, 'signature': url_quote_plus(signature)}
        logger.debug(data)
        return data

    def _fss_info(self, fieldname='file'):
        context = aq_inner(self.context)
        field = context.getField(fieldname)
        storage = field.storage
        try:
            info = storage.getFSSInfo(fieldname, context)
            strategy = storage.getStorageStrategy(fieldname, context)
            props = storage.getStorageStrategyProperties(fieldname, context, info)
        except AttributeError:
            logger.error('cannot retrieve fss properties. fss installed?')
            return

        valueDirectoryPath = strategy.getValueDirectoryPath(**props)
        valueFilename = strategy.getValueFilename(**props)
        length = len(strategy.storage_path.split('/'))
        path = ('/').join(valueDirectoryPath.split('/')[length - 1:]).strip('/')
        return (
         path, valueFilename)


def hmac_hexdigest(secret, update_list):
    """ returns a hex encoded digest of signature """
    mac = hmac.new(secret)
    for s in update_list:
        mac.update(s)

    return mac.hexdigest()
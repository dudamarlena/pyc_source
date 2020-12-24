# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\api\mindmeister_response.py
# Compiled at: 2008-12-12 20:05:34
""" MindMeister WEB Service API
    Change List:
     - Added 'public' attribute to the getlist method
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mindmeister_response.py 728 2008-12-11 16:47:54Z jeanlou.dupont $'
import jld.api as api
from xml.dom import minidom

class MM_ResponseBase(object):
    """ Base class response
    """
    MM_ErrorCodes = {'20': (
            'Object not found', api.ErrorObject), 
       '21': (
            'Collaborators and Viewers empty', api.ErrorValidation), 
       '22': (
            'Invalid email', api.ErrorValidation), 
       '24': (
            'Parameter x_pos and/or y_pos', api.ErrorValidation), 
       '25': (
            'Not privileged: the API key is not authorized for the action', api.ErrorAccess), 
       '26': (
            'User login already taken', api.ErrorValidation), 
       '27': (
            'Email already taken', api.ErrorValidation), 
       '28': (
            'Password and confirmation do not match', api.ErrorValidation), 
       '29': (
            'Password or email too short', api.ErrorValidation), 
       '30': (
            'Subsharing not activated for map', api.ErrorProperty), 
       '31': (
            'No default map defined', api.ErrorProperty), 
       '32': (
            'No write access on map', api.ErrorAccess), 
       '95': (
            'Not premium: user must have a premium account', api.ErrorAccess), 
       '96': (
            'Invalid signature', api.ErrorAuth), 
       '97': (
            'Missing signature', api.ErrorAuth), 
       '98': (
            'Login failed', api.ErrorAuth), 
       '99': (
            'The method requires authentication', api.ErrorAuth), 
       '100': (
             'Invalid API key', api.ErrorAuth), 
       '112': (
             'Method not found', api.ErrorMethod)}

    def __init__(self, raw):
        self.code = None
        self.error = None
        self._extractErrorCode(raw)
        return

    def _extractErrorCode(self, raw):
        """ Extract the <err code="" ..> section
            and raises and appropriate exception if need be
        """
        try:
            e = minidom.parseString(raw).documentElement
            err = e.getElementsByTagName('err')[0]
            self.code = err.getAttribute('code')
            msg = err.getAttribute('msg')
        except Exception, e:
            return

        self._codeToException(self.code, msg)

    def _codeToException(self, code, msg):
        """ Raises a correlated exception
        """
        if not self.MM_ErrorCodes.has_key(code):
            raise Exception('Found an undocumented Exception Code [%s] [%s]' % (code, msg))
        raise self.MM_ErrorCodes[code][1](msg)


class MM_ResponseBasic(MM_ResponseBase):
    """ Basic response
        Used for testing purpose only
    """

    def __init__(self, raw=None):
        MM_ResponseBase.__init__(self, raw)


class MM_Response_getFrob(MM_ResponseBase):
    """ In response to mm.auth.getFrob
    """

    def __init__(self, raw):
        MM_ResponseBase.__init__(self, raw)
        self.frob = None
        try:
            e = minidom.parseString(raw).documentElement
            self.frob = e.getElementsByTagName('frob')[0].childNodes[0].nodeValue
        except Exception, e:
            raise api.ErrorProtocol('expecting parameter "frob"')

        return


class MM_Response_getAuthToken(MM_ResponseBase):
    """ In response to mm.auth.getToken
    """

    def __init__(self, raw):
        MM_ResponseBase.__init__(self, raw)
        self.auth_token = None
        try:
            e = minidom.parseString(raw).documentElement
            self.auth_token = e.getElementsByTagName('token')[0].childNodes[0].nodeValue
        except Exception, e:
            raise api.ErrorProtocol('expecting parameter "token"')

        return


class MM_Response_getList(MM_ResponseBase):
    """ In response to mm.maps.getList
    """
    _attribs = ('id', 'title', 'created', 'modified', 'tags', 'public')
    _remap = {'id': 'mapid'}

    def __init__(self, raw):
        MM_ResponseBase.__init__(self, raw)
        self.raw = raw
        self.pages = 0
        self.total = None
        self.maps = []
        self.count = 0
        self.error = False
        self.error_msg = None
        try:
            self.tree = minidom.parseString(raw).documentElement
        except:
            raise api.ErrorProtocol('no XML response found')

        self._extractTotal()
        self._extractMaps()
        return

    def _extractTotal(self):
        try:
            self.total = self.tree.getElementsByTagName('maps')[0].getAttribute('total')
            self.pages = self.tree.getElementsByTagName('maps')[0].getAttribute('pages')
        except Exception, e:
            raise api.ErrorProtocol('expecting parameter "maps"')

    def _extractMaps(self):
        """ Returns a list of dict
        """
        try:
            all_maps = self.tree.getElementsByTagName('map')
            for map in all_maps:
                this = {}
                for attr in self._attribs:
                    value = map.getAttribute(attr)
                    if attr in self._remap:
                        attr = self._remap[attr]
                    this[attr] = value

                self.maps.append(this)

            self.count = len(self.maps)
        except Exception, e:
            raise api.ErrorProtocol('expecting parameter "map"')


class MM_Response_getMapExport(MM_ResponseBase):
    """ In response to mm.maps.export
        exports[image] = url
    """

    def __init__(self, raw):
        MM_ResponseBase.__init__(self, raw)
        self.exports = []
        try:
            entry = {}
            e = minidom.parseString(raw).documentElement
            images = e.getElementsByTagName('image')
            for image in images:
                mimetype = image.getAttribute('mimetype')
                entry[mimetype] = image.childNodes[0].nodeValue

            params = ['pdf', 'rtf', 'freemind', 'mindmeister']
            for param in params:
                i = e.getElementsByTagName(param)[0]
                entry[param] = i.childNodes[0].nodeValue

            self.exports.append(entry)
        except Exception, e:
            raise api.ErrorProtocol('expecting %s' % param, {'param': param})


if __name__ == '__main__':
    rGetList = '\n<rsp stat="ok">\n<maps page="1" pages="1" perpage="100" total="2">\n<map id="2490" title="Copy of Freemind map" owner="3" description=""\n    created="2007-06-20 06:40:04" modified="2007-06-20 06:40:04" sharedwith=""\n    tags="" public="0" viewonly="0" default="0"/>\n<map id="2480" title="Freemind map" owner="3" description=""\n    created="2007-06-20 06:40:03" modified="2007-06-20 06:40:03" sharedwith=""\n    tags="" public="0" viewonly="0" default="0"/>\n</maps>\n</rsp>\n'
    r = MM_Response_getList(rGetList)
    print r.total
    print r.maps
    err = '\n<rsp stat="fail"> \n<err code="97" msg="The call required signing but no signature was sent."/> \n</rsp>    \n'
    r2 = MM_ResponseBasic(err)
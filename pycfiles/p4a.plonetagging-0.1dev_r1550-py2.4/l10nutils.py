# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/l10nutils.py
# Compiled at: 2007-10-12 18:11:48
import datetime, DateTime, pytz, pytz.zoneinfo.GMT, time, zope.component, zope.i18n.interfaces, zope.i18n.locales, zope.interface, zope.interface.common.idatetime

class ServerTZInfo(pytz.UTC.__class__):
    """Default tzinfo adapter that will add the current server tzinfo
    during a normalize call.

      >>> from datetime import datetime
      >>> tzinfo = ServerTZInfo()
      >>> normalized = tzinfo.normalize(datetime.now())
    """
    __module__ = __name__
    zope.interface.implements(zope.interface.common.idatetime.ITZInfo)
    zope.component.adapts(zope.interface.Interface)

    def __init__(self, context=None):
        pass

    def normalize(self, dt):
        tzinfo = dt.tzinfo
        if tzinfo == None:
            tzstr = DateTime.DateTime(str(dt)).timezone()
            if tzstr.startswith('GMT'):
                offset = int(tzstr[3:])
                tzinfo = pytz.zoneinfo.GMT.GMT.__class__()
                tzinfo.zone = 'GMT' + str(offset)
                tzinfo._utcoffset = datetime.timedelta(hours=offset)
                tzinfo._tzname = tzinfo.zone
            else:
                tzinfo = pytz.timezone(tzstr)
        return dt.replace(tzinfo=tzinfo)


def derive_locale(request):
    envadapter = zope.i18n.interfaces.IUserPreferredLanguages(request)
    langs = envadapter.getPreferredLanguages()
    for httplang in langs:
        parts = (httplang.split('-') + [None, None])[:3]
        try:
            return zope.i18n.locales.locales.getLocale(*parts)
        except zope.i18n.locales.LoadLocaleError:
            pass

    else:
        return zope.i18n.locales.locales.getLocale(None, None, None)

    return
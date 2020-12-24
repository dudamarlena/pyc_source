# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/kenkisi.py
# Compiled at: 2009-03-11 11:00:08
import logging
from frla.lib.base import *
import pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
log = logging.getLogger(__name__)

class KenkisiController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        set_lang(g.lang)
        kisi = "SELECT DISTINCT AcctStartTime from radacct where Username='" + request.params['isim'] + "' and nasipaddress='" + request.params['ken'] + "'"
        bilgiler = db.query(kisi)
        bilgiler = bilgiler.getresult()
        baglanmasayisi = db.query("SELECT COUNT(DISTINCT AcctStartTime) FROM radacct WHERE Username='" + request.params['isim'] + "' and nasipaddress='" + request.params['ken'] + "'")
        baglanmasayisi = baglanmasayisi.getresult()
        c.sonuc = [
         _('bilgikisi') + request.params['isim'] + _('kenkisi') + request.params['ken'] + _('kenbilgisi2') + ungettext('%(num)d time', '%(num)d times', int(baglanmasayisi[0][0])) % {'num': int(baglanmasayisi[0][0])}]
        tarih = 0
        for i in bilgiler:
            if tarih == i[0][:i[0].find(' ')]:
                c.sonuc[(len(c.sonuc)):] = [
                 g.bqac + _('saat') + i[0][i[0].find(' '):] + g.bqkapa]
            else:
                c.sonuc[(len(c.sonuc)):] = [
                 _('tarih') + '</b>' + i[0][:i[0].find(' ')] + g.bqac + _('saat') + i[0][i[0].find(' '):] + g.bqkapa]
            tarih = i[0][:i[0].find(' ')]

        return render('/sonuc2.mako')
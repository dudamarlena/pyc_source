# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/bilgikisi.py
# Compiled at: 2009-03-11 10:59:06
import logging, pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
from frla.lib.base import *
log = logging.getLogger(__name__)

class BilgikisiController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        set_lang(g.lang)
        ip = "SELECT NASIPAddress,AcctStartTime from radacct where UserName='" + request.params['ad'] + "' ORDER BY NASIPAddress"
        bilgiler = db.query(ip)
        sayi = "SELECT COUNT(UserName) from radacct where UserName='" + request.params['ad'] + "'"
        baglanmasayisi = db.query(sayi)
        baglanmasayisi = baglanmasayisi.getresult()
        bilgiler = bilgiler.getresult()
        ken_adres = 0
        c.sonuc = [
         _('bilgikisi') + request.params['ad'] + _('bilgikisi2') + ungettext('%(num)d time', '%(num)d times', int(baglanmasayisi[0][0])) % {'num': int(baglanmasayisi[0][0])}]
        for i in bilgiler:
            if ken_adres == i[0]:
                c.sonuc[(len(c.sonuc)):] = [
                 g.bqac + _('tarih') + i[1][:i[1].find(' ')] + _('saat') + i[1][i[1].find(' '):] + g.bqkapa]
                continue
            ken_ad = "SELECT ad FROM kenn WHERE adres='" + i[0] + "'"
            ken_ad = db.query(ken_ad)
            ken_ad = ken_ad.getresult()
            if len(ken_ad) == 0:
                ken_ad = [
                 (
                  _('isimverme1') + i[0] + _('isimverme2'),)]
            c.sonuc[(len(c.sonuc)):] = [
             '<br>' + _('kenadres') + i[0] + _('ad') + ken_ad[0][0] + g.bqac + _('tarih') + i[1][:i[1].find(' ')] + _('saat') + i[1][i[1].find(' '):] + g.bqkapa]
            ken_adres = i[0]

        return render('/sonuc2.mako')
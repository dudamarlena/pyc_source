# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/tarihbilgisi.py
# Compiled at: 2009-03-11 11:05:22
import logging
from frla.lib.base import *
import pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
log = logging.getLogger(__name__)

class TarihbilgisiController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        set_lang(g.lang)
        kisi = "SELECT DISTINCT UserName FROM radacct WHERE date_trunc('day',AcctStartTime)='" + request.params['tarih'] + "' and UserName!='anonymous@comu.edu.tr'"
        bilgiler = db.query(kisi)
        bilgiler = bilgiler.getresult()
        sayi = "SELECT COUNT(DISTINCT Username) from radacct where date_trunc('day',AcctStartTime)='" + request.params['tarih'] + "'and UserName!='anonymous@comu.edu.tr'"
        kisisayisi = db.query(sayi)
        kisisayisi = kisisayisi.getresult()
        c.sonuc = [
         _('tarihbilgi') + request.params['tarih'] + _('tarihbilgi2') + ungettext('%(num)d user', '%(num)d users', int(kisisayisi[0][0])) % {'num': int(kisisayisi[0][0])}]
        for i in bilgiler:
            c.sonuc[(len(c.sonuc)):] = [
             '<a href="/tarihkisi?isim=' + i[0] + '&amp;tarih=' + request.params['tarih'] + '">' + i[0][:i[0].find('@')] + '</a><br>']

        return render('/sonuc.mako')
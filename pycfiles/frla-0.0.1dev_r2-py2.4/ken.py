# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/ken.py
# Compiled at: 2009-03-11 11:00:25
import logging, pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
from frla.lib.base import *
log = logging.getLogger(__name__)

class KenController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        kenler = db.query('SELECT DISTINCT nasipaddress from radacct')
        kenler = kenler.getresult()
        g.lang = request.params['dil']
        set_lang(g.lang)
        c.sonuc = [
         _('kenler')]
        c.sonuc[(len(c.sonuc)):] = ['<table>']
        for i in kenler:
            ken_ad = "SELECT ad FROM kenn WHERE adres='" + i[0] + "'"
            ken_ad = db.query(ken_ad)
            ken_ad = ken_ad.getresult()
            if len(ken_ad) == 0:
                ken_ad = [
                 (
                  _('isimverme1') + i[0] + _('isimverme2'),)]
            c.sonuc[(len(c.sonuc)):] = [
             '<tr><td><a href="/kenbilgisi?ken=' + i[0] + '">' + i[0] + '</a></td><td>' + ken_ad[0][0] + '<br></td></tr>']

        c.sonuc[(len(c.sonuc)):] = [
         '</table>']
        return render('/sonuc.mako')
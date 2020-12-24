# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/tarih.py
# Compiled at: 2009-03-11 11:06:08
import logging, pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
from frla.lib.base import *
log = logging.getLogger(__name__)

class TarihController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        tarihler = db.query('SELECT DISTINCT AcctStartTime from radacct')
        tarihler = tarihler.getresult()
        tarihler.reverse()
        g.lang = request.params['dil']
        set_lang(g.lang)
        c.sonuc = [
         _('tarih1')]
        tarihler[0] = tarihler[0][0][:tarihler[0][0].find(' ')]
        c.sonuc[(len(c.sonuc)):] = ['<a href="/tarihbilgisi?tarih=' + tarihler[0] + '">' + tarihler[0] + '</a><br>']
        for i in range(1, len(tarihler) - 1):
            tarihler[i] = tarihler[i][0][:tarihler[i][0].find(' ')]
            if tarihler[i] == tarihler[(i - 1)]:
                continue
            c.sonuc[(len(c.sonuc)):] = [
             '<a href="/tarihbilgisi?tarih=' + tarihler[i] + '">' + tarihler[i] + '</a><br>']

        return render('/sonuc.mako')
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/ad.py
# Compiled at: 2009-03-23 05:20:18
import logging, pg
from frla.lib import baglan
from pylons.i18n import get_lang, set_lang
from frla.lib.base import *
log = logging.getLogger(__name__)

class AdController(BaseController):
    __module__ = __name__

    def index(self):
        db = baglan.baglan()
        adlar = db.query('SELECT DISTINCT UserName from radacct')
        adlar = adlar.getresult()
        adlar.sort()
        g.lang = request.params['dil']
        set_lang(g.lang)
        c.sonuc = [_('ad1')]
        for i in adlar:
            if i[0] == 'anonymous@comu.edu.tr':
                continue
            c.sonuc[(len(c.sonuc)):] = [
             '<a href="/bilgikisi?ad=' + i[0] + '">' + i[0][:i[0].find('@')] + '</a><br>']

        return render('/sonuc.mako')
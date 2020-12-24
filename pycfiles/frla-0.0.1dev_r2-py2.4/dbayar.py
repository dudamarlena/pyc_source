# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/controllers/dbayar.py
# Compiled at: 2009-03-25 08:03:55
import logging
from pylons.i18n import get_lang, set_lang
from frla.lib.base import *
log = logging.getLogger(__name__)

class DbayarController(BaseController):
    __module__ = __name__

    def form(self):
        return render('/form.mako')

    def form2(self):
        return render('/form2.mako')

    def ayarla(self):
        set_lang(request.params['dil'])
        vtisim = request.params['vtisim']
        host = request.params['host']
        kullanici = request.params['kullanici']
        parola = request.params['parola']
        if vtisim.strip() == '' or host.strip() == '' or kullanici.strip() == '':
            c.sonuc = [
             _('dbayar2')]
        else:
            baglan = open('./frla/lib/baglan.py', 'w')
            baglan.write('#!/usr/bin/python\n# -*- coding: utf-8 -*-\nimport pg\ndef baglan():\n\t')
            ayar = "db=pg.connect(dbname='" + vtisim + "',host='" + host + "',user='" + kullanici + "',passwd='" + parola + "')\n\t"
            baglan.write(ayar)
            baglan.write('return db')
            baglan.close()
            c.sonuc = [_('dbayar')]
        return render('/sonuc2.mako')
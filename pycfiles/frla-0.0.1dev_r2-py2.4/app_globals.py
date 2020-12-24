# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/lib/app_globals.py
# Compiled at: 2009-03-25 08:03:24
"""The application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """
    __module__ = __name__

    def __init__(self):
        self.lang = 'tr'
        self.anasayfalink = '<a href="index.html">Anasayfa</a><br>'
        self.anasayfalink2 = '<b><a href="/index.html">Anasayfa</a><br></b>'
        self.anasayfa = ''
        self.bqac = '<blockquote>'
        self.bqkapa = '</blockquote>'
        self.nasconf = '<h3><font color="ff0000">Kablosuz Erişim Noktalarının İsimlerini Yapılandırma</font></h3><br>'
        self.dbconf = '<h3><font color="ff0000">Veritabanı Bağlantı Ayarları</font></h3><br>'
        self.homepage = '<b><a href="/indexeng.html">Home</a><br></b>'
        self.nasconfeng = '<h3><font color="ff0000">Configuration of Network Attached Storage Name</font></h3><br>'
        self.dbconfeng = '<h3><font color="ff0000">Database Connection</font></h3><br>'
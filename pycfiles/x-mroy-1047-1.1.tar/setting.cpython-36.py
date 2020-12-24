# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/vps-manager/web/setting.py
# Compiled at: 2019-05-30 05:08:49
# Size of source mod 2**32: 2336 bytes
import os
from os import path
from qlib.file import ensure_path
from Qtornado.log import LogControl
from Qtornado.db import *
from web.controller import *
from qlib.data import Cache
import web.ui as ui, sys, geoip2.database
from .test_route import DB_PATH
db_connect_cmd = 'database="' + DB_PATH + '"'
db_engine = Cache(DB_PATH, check_same_thread=False)
rdir_path = os.path.dirname(__file__)
static_path = os.path.join(rdir_path, 'static')
files_path = os.path.join(static_path, 'files')
geo_path = os.path.join(static_path, 'res/geo')
D = os.path.dirname(DB_PATH)
shadowsocks_path = os.path.join(D, 'shadowsocks')
ss_saved = '/tmp/ss-random'
ss_proxy = '/tmp/ss-proxy.conf'
ensure_path(static_path)
ensure_path(files_path)
ensure_path(shadowsocks_path)
ensure_path(ss_saved)

def get_ip(ip):
    reader = geoip2.database.Reader(os.path.join(geo_path, 'GeoLite2-City.mmdb'))
    res = reader.city(ip)
    return (str(res.location.longitude), str(res.location.latitude))


LogControl.LOG_LEVEL |= LogControl.OK
LogControl.LOG_LEVEL |= LogControl.INFO
Settings = {'db':db_engine, 
 'L':LogControl, 
 'debug':True, 
 'geo':get_ip, 
 'geo_db':geoip2.database.Reader(os.path.join(geo_path, 'GeoLite2-City.mmdb')), 
 'ui_modules':ui, 
 'ss-saved':ss_saved, 
 'proxy-config-file.conf':ss_proxy, 
 'autoreload':True, 
 'cookie_secret':'This string can be any thing you want', 
 'static_path':static_path}
appication = (tornado.web.Application)(
 [
  (
   '/', IndexHandler),
  (
   '/map', MapHandler),
  (
   '/get_ip', Get_ipHandler),
  (
   '/getstatus', GetStatusHandler),
  (
   '/remoteapi', RemoteapiHandler),
  (
   '/asyncremoteapi', AsyncremoteapiHandler),
  (
   '/create', CreateHandler),
  (
   '/out', AuthLogoutHandler),
  (
   '/whatthefuckcanyoubrut3memanwhatthefuckcanyoubrutememan', LoginHandler),
  (
   '/reg', RegHandler)], **Settings)
port = 8080
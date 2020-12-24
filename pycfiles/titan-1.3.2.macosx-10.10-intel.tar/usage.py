# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/usage.py
# Compiled at: 2014-10-16 21:41:50
from __future__ import unicode_literals

def _(text):
    return text.strip(b'\n')


HELP = _(b'\n  -h, --help         show help message\n  -v, --version      show version\n  --verbose          show script while running\n  --dry-run          show script without running\n\ncommands:\n  run                invoke the scanner\n  manager            manage device\n  monitor            manage monitors\n  report             display report\n\n')
USAGE = _(b"\n\n           NxW     NK0xllllox0W      OlN\n          0. k  Nd,            .;xW  l .0\n         O   .0d.   .,        .   .dO.   0\n        K          'dk:      ;:,.        .N\n       W,    ;.  ,okkkk,    '::::,   ..   :W\n       x    :kx, 'xkkkkd   .:::::;  '::.   x\n      X.   ckdlxl.'dkkkk.  '::::,..;:;::.  .N\n      l  .okkx'.:xo:lxkk;  ;::;'';;. ':cc'  o\n      ;   ,dkko   'lxdkkc  :::::'.   :c:;.  ;\n      Nx.   :kkc    ..:kl .::..     ;c;.  'xN\n        Wx.  .ok:      od .:'      ;:'  .O\n          Wx.  ckxxx.  ,x.':.  .::::. .xW\n            o   okk:   .k.,;    ,::'  k\n           W,   ,ko    .k;;:    .::   ;W\n          Nc    'k,    ckl::.    ,; .  'X    KKKXN\n        Wk'  .c.:k;    .,,..     ;:.;;   cdd:   'O\n     Wx,.   ckkcxkxc.          .,::;,:,.      ;OW\n      WO,  cOkxxkkkkc          ::::::::;.   ;0\n        Wk, :kkkkkkkc         .:::::::,   ;0\n          WO,.:dkkkkl         .:::::;.  ,0\n            Wx, 'okkx.        ':::'.  :0\n               O' .lk;        ::'   ,K\n                Wd' 'l.      .'   :0\n                  Wk, .         ;K\n                    Wx.       :K\n                      Wx.   ;0\n                        N, k\n\nUsage: titanosx [--config=CONFIG] command\n\n%s" % HELP)
MONITOR_USAGE = _(b'\nUsage: titanosx monitor [ install | list | upgrade | remove ]\n\ncommands:\n  list               show all installed monitors\n  install            installs specified monitor\n  upgrade            upgrades specified monitor\n  remove             removes specified monitor\n')
MANAGER_USAGE = _(b'\nUsage: titanosx manager [ status | register | unregister ]\n\ncommands:\n  status             return status of remote server\n  register           register this device with a remote server\n  unregister         unregister this device with a remote server\n')
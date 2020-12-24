# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/run.py
# Compiled at: 2020-01-04 07:05:35
# Size of source mod 2**32: 96 bytes
from protonvpn_gtk.ui.app import MyApp

def main():
    app = MyApp('ProtonVPN')
    app.run()
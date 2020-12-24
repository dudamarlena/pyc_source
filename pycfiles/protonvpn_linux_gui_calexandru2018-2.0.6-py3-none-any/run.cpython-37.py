# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/run.py
# Compiled at: 2020-01-04 07:05:35
# Size of source mod 2**32: 96 bytes
from protonvpn_gtk.ui.app import MyApp

def main():
    app = MyApp('ProtonVPN')
    app.run()
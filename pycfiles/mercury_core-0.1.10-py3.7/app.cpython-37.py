# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/boot/app.py
# Compiled at: 2018-02-08 17:03:50
# Size of source mod 2**32: 1074 bytes
from flask import Flask
from mercury.boot.configuration import get_boot_configuration
from mercury.boot.urls import boot_urls
app = Flask(__name__)
for url, view_func in boot_urls:
    app.add_url_rule(url, view_func=view_func, strict_slashes=False)

if __name__ == '__main__':
    configuration = get_boot_configuration()
    app.run(host=(configuration.host), port=(configuration.port), debug=True)
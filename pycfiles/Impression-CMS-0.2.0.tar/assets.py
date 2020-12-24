# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scottblevins/git/old impression/impression/assets.py
# Compiled at: 2016-07-20 14:22:29
from flask_assets import Bundle
common_css = Bundle('css/vendor/bootstrap.min.css', 'css/vendor/helper.css', 'css/main.css', filters='cssmin', output='public/css/common.css')
common_js = Bundle('js/vendor/jquery.min.js', 'js/vendor/knockout-3.4.0.js', 'js/vendor/bootstrap.min.js', Bundle('js/main.js', filters='jsmin'), output='public/js/common.js')
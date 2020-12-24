# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/boot/urls.py
# Compiled at: 2018-03-12 13:33:25
# Size of source mod 2**32: 937 bytes
from mercury.boot.views import BootView, DiscoverView
boot_view = BootView.as_view('boot')
discover_view = DiscoverView.as_view('discover')
boot_urls = [
 (
  '/boot', boot_view),
 (
  '/boot/discover/<mac_address>', discover_view)]
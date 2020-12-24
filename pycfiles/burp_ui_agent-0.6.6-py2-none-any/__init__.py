# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ziirish/workspace/burp-ui/pkgs/burp-ui-agent/burpui_agent/__init__.py
# Compiled at: 2019-04-05 05:50:52
"""
Burp-UI is a web-ui for burp backup written in python with Flask and
jQuery/Bootstrap

.. module:: burpui_agent
    :platform: Unix
    :synopsis: Burp-UI agent module.

.. moduleauthor:: Ziirish <hi+burpui@ziirish.me>
"""
import sys
__title__ = 'burp-ui-agent'
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
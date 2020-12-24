# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ziirish/workspace/burp-ui/pkgs/burp-ui-agent/burpui_agent/desc.py
# Compiled at: 2019-04-05 05:50:52
__doc__ = '\nBurp-UI is a web-ui for burp backup written in python with Flask and\njQuery/Bootstrap\n\n.. module:: burpui.desc\n    :platform: Unix\n    :synopsis: Burp-UI desc module.\n\n.. moduleauthor:: Ziirish <hi+burpui@ziirish.me>\n'
import os
__title__ = 'burp-ui'
__author__ = 'Benjamin SANS (Ziirish)'
__author_email__ = 'hi+burpui@ziirish.me'
__url__ = 'https://git.ziirish.me/ziirish/burp-ui'
__doc__ = 'https://burp-ui.readthedocs.io/en/latest/'
__description__ = 'Burp-UI is a web-ui for burp backup written in python with Flask and jQuery/Bootstrap'
__license__ = 'BSD 3-clause'
__version__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().rstrip()
try:
    __release__ = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RELEASE')).read().rstrip()
except:
    __release__ = 'unknown'
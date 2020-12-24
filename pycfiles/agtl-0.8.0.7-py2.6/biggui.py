# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/biggui.py
# Compiled at: 2011-04-23 08:43:29
import simplegui

class BigGui(simplegui.SimpleGui):
    USES = [
     'gpsprovider']
    XMLFILE = 'freerunner.glade'
    TOO_MUCH_POINTS = 100
    CACHES_ZOOM_LOWER_BOUND = 3
    MAX_NUM_RESULTS = 500
    MAX_NUM_RESULTS_SHOW = 500
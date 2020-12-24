# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
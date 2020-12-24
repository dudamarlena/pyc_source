# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/eagle_automation/default.py
# Compiled at: 2015-08-24 04:20:23
# Size of source mod 2**32: 2589 bytes
import sys, glob
if 'darwin' == sys.platform:
    eagle_bin = glob.glob('/Applications/EAGLE*/EAGLE.app/Contents/MacOS/EAGLE')[(-1)]
    open_bin = '/usr/bin/open'
else:
    if 'linux' == sys.platform:
        eagle_bin = glob.glob('/usr/local/eagle*/bin/eagle')[(-1)]
        open_bin = '/usr/bin/xdg-open'
    elif 'win32' == sys.platform:
        eagle_bin = 'c:/program files/EAGLE*/eagle.exe'
        open_bin = 'start'

class Config:
    LAYERS = {'topassembly': {'layers': [
                                'tPlace', 'tNames', 'tDocu'], 
                     'pp_id': 1}, 
     'topsilk': {'layers': [
                            'tPlace', 'tNames']}, 
     'toppaste': {'layers': [
                             'tCream']}, 
     'topmask': {'layers': [
                            'tStop']}, 
     'topcopper': {'layers': [
                              'Top', 'Pads', 'Vias']}, 
     'bottomcopper': {'layers': [
                                 'Bottom', 'Pads', 'Vias'], 
                      'mirror': True}, 
     'bottommask': {'layers': [
                               'bStop'], 
                    'mirror': True}, 
     'bottompaste': {'layers': [
                                'bCream'], 
                     'mirror': True}, 
     'bottomsilk': {'layers': [
                               'bPlace', 'bNames'], 
                    'mirror': True}, 
     'bottomassembly': {'layers': [
                                   'bPlace', 'bNames', 'bDocu'], 
                        'mirror': True, 
                        'pp_id': 16}, 
     'outline': {'layers': [
                            'Milling']}, 
     'measures': {'layers': [
                             'DrillLegend', 'Measures']}, 
     'drills': {'layers': [
                           'Drills', 'Holes']}}
    DOCUMENT_LAYERS = [
     'Dimension', 'Document']
    EAGLE = eagle_bin
    DPI = 400
    OPEN = open_bin
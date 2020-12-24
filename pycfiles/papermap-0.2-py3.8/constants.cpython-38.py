# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\papermap\constants.py
# Compiled at: 2019-12-17 15:05:06
# Size of source mod 2**32: 782 bytes
NAME = 'papermap'
DESCRIPTION = 'A python package and CLI for creating paper maps'
VERSION = '0.2'
HEADERS = {'User-Agent':f"{NAME}v{VERSION}",  'Accept':'image/png,image/*;q=0.9,*/*;q=0.8'}
TILE_SIZE = 256
GRID_SIZE = 1000000
SERVERS = ['a', 'b', 'c']
R = 6378137
C = 40075017
X0 = 155000
Y0 = 463000
LAT0 = 52.1551744
LON0 = 5.38720621
K0 = 0.9996
E = 0.00669438
E_ = E / (1.0 - E)
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/util/trackers.py
# Compiled at: 2017-11-04 01:43:23
# Size of source mod 2**32: 914 bytes
TRACKERS_URL_LIST = [
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_udp.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_http.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_https.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best_ip.txt',
 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all_ip.txt']

def get_trackers_url(index=0):
    return TRACKERS_URL_LIST[index]
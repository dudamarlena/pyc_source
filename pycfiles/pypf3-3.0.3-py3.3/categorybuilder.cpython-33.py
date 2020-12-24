# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/categorybuilder.py
# Compiled at: 2014-04-04 12:16:37
# Size of source mod 2**32: 856 bytes
"""
Created on Sep 27, 2013

@author: "Colin Manning"
"""
import requests, os
dropbox_root = '/home/colin/Dropbox/printflow/SAB'
url = 'http://dis.printflow2.com/search/sab/category?path=$Categories'

def ensureDirectoryExists(path):
    if not os.path.exists(path):
        os.makedirs(path, mode=493)


def process_subcategory(parent, cat):
    path = os.path.join(parent, cat['name'])
    ensureDirectoryExists(path)
    if 'subcategories' in cat:
        subcats = cat['subcategories']
        for i in range(len(subcats)):
            process_subcategory(path, subcats[i])


response = requests.post(url)
if response.status_code == 200:
    r = response.json()
    subcategories = r['subcategories']
    for i in range(len(subcategories)):
        process_subcategory(dropbox_root, subcategories[i])
# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/categorybuilder.py
# Compiled at: 2014-04-04 12:16:37
# Size of source mod 2**32: 856 bytes
__doc__ = '\nCreated on Sep 27, 2013\n\n@author: "Colin Manning"\n'
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
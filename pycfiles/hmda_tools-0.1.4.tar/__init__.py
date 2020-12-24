# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/crnixon/Projects/hmda-tools/hmda_tools/__init__.py
# Compiled at: 2013-02-19 20:03:20
import os, tempfile, pkgutil, requests

def get_resource(file):
    return pkgutil.get_data(__name__, file)


def download_file(uri):
    r = requests.get(uri)
    if r.status_code == 200:
        fh, filename = tempfile.mkstemp()
        with os.fdopen(fh, 'wb') as (f):
            for chunk in r.iter_content():
                f.write(chunk)

        return filename
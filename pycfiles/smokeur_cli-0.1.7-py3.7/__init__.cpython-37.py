# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smokeur/__init__.py
# Compiled at: 2019-05-16 18:06:33
# Size of source mod 2**32: 1282 bytes
"""
Smokeur CLI
"""
import os, sys, pyperclip, requests
VERSION = '0.1.7'
try:
    SMOKEUR_SERVER = os.environ['SMOKEUR_SERVER']
except KeyError:
    print('Please set "SMOKEUR_SERVER" environment variable before using this tool.')
    sys.exit(1)

def upload_file():
    """Upload a file to Smokeur"""
    try:
        file_name = sys.argv[1]
    except IndexError:
        print('You have to give the file path to upload; e.g.:\n$ smokeur somefile.jpg\nor\n$ smokeur /path/to/somefile.png')
        sys.exit(1)

    smokeur_headers = {'User-Agent': 'Smokeur CLI/{version}'.format(version=VERSION)}
    with open(file_name, 'rb') as (file):
        data = {'file': file}
        response = requests.post(url=SMOKEUR_SERVER,
          files=data,
          headers=smokeur_headers)
    if response.status_code == 200:
        result_url = response.json().get('result')
        pyperclip.copy(result_url)
        print(f"Your file is available on: {result_url}")
        print('It has been copied to the clipboard too.')
    else:
        print(response.reason)


if __name__ == '__main__':
    upload_file()
# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pteste.py
# Compiled at: 2017-12-28 10:35:24
# Size of source mod 2**32: 125 bytes
import requests
response = requests.get('https://httpbin.org/ip')
print('Seu ip é {0}'.format(response.json()['origin']))
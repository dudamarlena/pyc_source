# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wojak\__init__.py
# Compiled at: 2018-07-15 15:11:21
# Size of source mod 2**32: 530 bytes
import random
from random import randint
import requests, json

def get(num=None):
    if num == None:
        req = requests.get('https://yakz.cf/wojaks/wojak.json').json()
        rdmn = randint(0, len(req) - 1)
        req = req[rdmn]
        return [
         req, rdmn]
    else:
        argInt = int(num)
        req = requests.get('https://yakz.cf/wojaks/wojak.json').json()
        if argInt < 1 or argInt > len(req):
            return
        req = req[(argInt - 1)]
        return [req, argInt]


def grayon():
    req = requests.get('https://yakz.cf/wojaks/wojak.json').json()
    return [req[46], 47]
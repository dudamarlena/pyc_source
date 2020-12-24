# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\pytesser3\code.py
# Compiled at: 2016-09-22 22:09:01
# Size of source mod 2**32: 1387 bytes
"""
-------------------------------------------------------------------------------
Function:   test your pytesser3
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 
 
-------------------------------------------------------------------------------
"""
from pytesser3 import image_to_string
from PIL import Image
import requests

def get_code():
    url = 'http://www.rongtudai.com/validimg.html'
    f = requests.get(url)
    print(f)
    with open('code.jpg', 'wb') as (code):
        code.write(f.content)
    img = Image.open('code.jpg')
    img = img.convert('RGBA')
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[(x, y)][0] < 90:
                pixdata[(x, y)] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[(x, y)][1] < 136:
                pixdata[(x, y)] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[(x, y)][2] > 0:
                pixdata[(x, y)] = (255, 255, 255, 255)

    img.save('newcode.jpg')
    img = Image.open('newcode.jpg')
    vcode = image_to_string(img)
    return vcode


print(get_code())
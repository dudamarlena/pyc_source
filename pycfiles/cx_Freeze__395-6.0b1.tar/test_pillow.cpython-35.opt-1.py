# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\pillow\test_pillow.py
# Compiled at: 2020-01-04 18:05:46
# Size of source mod 2**32: 374 bytes
from io import BytesIO
from urllib.request import urlopen
from PIL import Image
print('Opening image with PIL')
filename = 'https://avatars3.githubusercontent.com/u/12752334?s=400&u=3ba7ed4b03221b76af248ff57b5f619d77b6021f&v=4'
fp = BytesIO(urlopen(filename).read())
with Image.open(fp) as (im):
    with open('test_pillow.pdf', 'w+b') as (fp2):
        im.save(fp2, format='PDF')
print('OK')
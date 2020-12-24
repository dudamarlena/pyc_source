# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
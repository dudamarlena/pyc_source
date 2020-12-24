# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/frames.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 1151 bytes
from color_matcher import ColorMatcher
from color_matcher.io_handler import load_img_file
from color_matcher.normalizer import Normalizer
import os, numpy as np, imageio
try:
    from PIL import Image, ImageSequence
except:
    raise Exception('Please install pillow')
else:
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
    fn_img1 = 'wave.gif'
    if fn_img1.endswith('gif'):
        im = Image.open(os.path.join(dir_path, fn_img1))
    duration = 40
    img2 = load_img_file(os.path.join(dir_path, 'sunrise_mvgd.png'))
    sequence = []
    method = 'mvgd'
    for frame in ImageSequence.Iterator(im):
        img1 = np.asarray(frame.convert('RGB'), np.uint8)
        match = ColorMatcher(img1, img2, method=method).main()
        sequence.append(Image.fromarray(Normalizer(match).uint8_norm()))
    else:
        output_fn = os.path.join(dir_path, os.path.splitext(fn_img1)[0] + '_' + method + '.gif')
        imageio.mimwrite(output_fn, sequence, duration=(1 / duration), palettesize=256)
# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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

    output_fn = os.path.join(dir_path, os.path.splitext(fn_img1)[0] + '_' + method + '.gif')
    imageio.mimwrite(output_fn, sequence, duration=(1 / duration), palettesize=256)
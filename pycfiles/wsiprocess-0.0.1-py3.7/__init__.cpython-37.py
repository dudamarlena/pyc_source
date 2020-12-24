# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/__init__.py
# Compiled at: 2019-11-28 08:31:06
# Size of source mod 2**32: 781 bytes
from .slide import Slide
from .patcher import Patcher
from .annotation import Annotation
from .inclusion import Inclusion

def slide(path):
    return Slide(path)


def annotation(path):
    return Annotation(path)


def inclusion(path):
    return Inclusion(path)


def patcher(slide, method, annotation=False, save_to='.', patch_width=256, patch_height=256, overlap_width=1, overlap_height=1, on_foreground=0.8, on_annotation=1.0, start_sample=True, finished_sample=True, extract_patches=True):
    return Patcher(slide, method, annotation, save_to, patch_width, patch_height, overlap_width, overlap_height, on_foreground, on_annotation, start_sample, finished_sample, extract_patches)
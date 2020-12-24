# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/verify.py
# Compiled at: 2019-11-21 06:51:45
# Size of source mod 2**32: 1206 bytes
from pathlib import Path

class Verify:

    def __init__(self, save_to, filestem, method, start_sample, finished_sample, extract_patches):
        self.save_to = save_to
        self.filestem = filestem
        self.method = method
        self.start_sample = start_sample
        self.finished_sample = finished_sample
        self.extract_patches = extract_patches

    def verify_dirs(self):
        base_dir = Path(self.save_to) / self.filestem
        self.verify_dir(base_dir)
        if self.method == 'segmentation':
            self.verify_dir(base_dir / 'masks')
        if self.start_sample:
            self.verify_dir(base_dir / 'start_sample')
        if self.finished_sample:
            self.verify_dir(base_dir / 'finished_sample')
        if self.extract_patches:
            self.verify_dir(base_dir / 'patches')

    @staticmethod
    def verify_dir(path):
        if not Path(path).exists():
            Path(path).mkdir(parents=True)

    def verify_magnification(self, slide, magnification):
        basemsg = 'Magnification for this slide has to be smaller than'
        msg = '{} {}'.format(basemsg, slide.slide.magnification)
        assert slide.slide.magnification < magnification, msg
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/patcher.py
# Compiled at: 2019-11-28 08:31:06
# Size of source mod 2**32: 11113 bytes
import random
from itertools import product
import json
from joblib import Parallel, delayed
import numpy as np, cv2
from pathlib import Path
from .verify import Verify

class Patcher:

    def __init__(self, slide, method, annotation=False, save_to='.', patch_width=256, patch_height=256, overlap_width=1, overlap_height=1, on_foreground=0.8, on_annotation=1.0, start_sample=True, finished_sample=True, extract_patches=True):
        self.slide = slide
        self.filepath = slide.filename
        self.filestem = slide.filestem
        self.method = method
        self.wsi_width = slide.wsi_width
        self.wsi_height = slide.wsi_height
        self.p_width = patch_width
        self.p_height = patch_height
        self.p_area = patch_width * patch_height
        self.o_width = overlap_width
        self.o_height = overlap_height
        self.x_lefttop = [i for i in range(0, self.wsi_width, patch_width - overlap_width)][:-1]
        self.y_lefttop = [i for i in range(0, self.wsi_height, patch_height - overlap_height)][:-1]
        self.iterator = product(self.x_lefttop, self.y_lefttop)
        self.last_x = self.slide.width - patch_width
        self.last_y = self.slide.height - patch_height
        self.start_sample = start_sample
        self.finished_sample = finished_sample
        self.extract_patches = extract_patches
        if annotation:
            self.annotation = annotation
            self.masks = annotation.masks
            self.classes = annotation.classes
            self.on_foreground = on_foreground
            self.on_annotation = on_annotation
        else:
            self.annotation = False
            self.masks = False
            self.classes = False
            self.on_foreground = False
            self.on_annotation = False
        self.save_to = save_to
        self.result = {'result': []}
        self.verify = Verify(save_to, self.filestem, method, start_sample, finished_sample, extract_patches)
        self.verify.verify_dirs()

    def save_patch_result(self, x, y, cls):
        if self.method == 'none':
            self.result['result'].append({'x':x,  'y':y, 
             'w':self.p_width, 
             'h':self.p_height})
        else:
            if self.method == 'classification':
                self.result['result'].append({'x':x,  'y':y, 
                 'w':self.p_width, 
                 'h':self.p_height, 
                 'class':cls})
            else:
                if self.method == 'detection':
                    bbs = []
                    for cls in self.classes:
                        for bb in self.find_bbs(x, y, cls):
                            bbs.append({'x':bb['x'],  'y':bb['y'], 
                             'w':bb['w'], 
                             'h':bb['h'], 
                             'class':bb['class']})

                    self.result['result'].append({'x':x,  'y':y, 
                     'w':self.p_width, 
                     'h':self.p_height, 
                     'bbs':bbs})
                else:
                    if self.method == 'segmentation':
                        masks = []
                        for cls in self.classes:
                            for mask in self.find_masks(x, y, cls):
                                masks.append({'coords':mask['coords'],  'class':mask['class']})

                        self.result['result'].append({'x':x,  'y':y, 
                         'w':self.p_width, 
                         'h':self.p_height, 
                         'masks':masks})
                    else:
                        raise NotImplementedError

    def find_bbs(self, x, y, cls):
        if not self.patch_on_annotation(cls, x, y):
            return []
        if cls == 'foreground':
            return []
        coords = self.annotation.mask_coords[cls]
        coords = np.array(coords)
        bblefts = np.min(coords, axis=1)[:, 0]
        bbtops = np.min(coords, axis=1)[:, 1]
        bbrights = np.max(coords, axis=1)[:, 0]
        bbbottoms = np.max(coords, axis=1)[:, 1]
        patch_left = x
        patch_right = x + self.p_width
        patch_top = y
        patch_bottom = y + self.p_height
        bbleft_right_of_patch_left = set(np.where(bblefts >= patch_left)[0])
        bbleft_left_of_patch_right = set(np.where(bblefts <= patch_right)[0])
        bbright_right_of_patch_left = set(np.where(bbrights >= patch_left)[0])
        bbright_left_of_patch_right = set(np.where(bbrights <= patch_right)[0])
        bbtop_below_patch_top = set(np.where(bbtops >= patch_top)[0])
        bbtop_above_patch_bottom = set(np.where(bbtops <= patch_bottom)[0])
        bbbottom_below_patch_top = set(np.where(bbbottoms >= patch_top)[0])
        bbbottom_above_patch_bottom = set(np.where(bbbottoms <= patch_bottom)[0])
        bbleft_on_patch = bbleft_right_of_patch_left & bbleft_left_of_patch_right
        bbright_on_patch = bbright_right_of_patch_left & bbright_left_of_patch_right
        bbtop_on_patch = bbtop_above_patch_bottom & bbtop_below_patch_top
        bbbottom_on_patch = bbbottom_above_patch_bottom & bbbottom_below_patch_top
        bb_lefttop_on_patch = bbleft_on_patch & bbtop_on_patch
        bb_leftbottom_on_patch = bbleft_on_patch & bbbottom_on_patch
        bb_righttop_on_patch = bbright_on_patch & bbtop_on_patch
        bb_rightbottom_on_patch = bbright_on_patch & bbbottom_on_patch
        idx_of_bb_on_patch = bb_lefttop_on_patch | bb_leftbottom_on_patch | bb_righttop_on_patch | bb_rightbottom_on_patch
        bbs_raw = coords[list(idx_of_bb_on_patch)]
        bbs = []
        for bb_raw in bbs_raw:
            x1 = bb_raw[:, 0].min()
            y1 = bb_raw[:, 1].min()
            x2 = bb_raw[:, 0].max()
            y2 = bb_raw[:, 1].max()
            bbx1 = int(max(x1 - x, 0))
            bby1 = int(max(y1 - y, 0))
            bbx2 = int(min(x2 - x1 + bbx1, self.p_width)) - bbx1
            bby2 = int(min(y2 - y1 + bby1, self.p_height)) - bby1
            bb = {'x':bbx1,  'y':bby1, 
             'w':bbx2, 
             'h':bby2, 
             'class':cls}
            bbs.append(bb)

        return bbs

    def find_masks(self, x, y, cls):
        if not self.patch_on_annotation(cls, x, y):
            return []
        patch_mask = self.masks[cls][y:y + self.p_height, x:x + self.p_width]
        mask_png_path = '{}/{}/masks/{}/{:06}_{:06}.png'.format(self.save_to, self.filestem, cls, x, y)
        cv2.imwrite(mask_png_path, patch_mask, (cv2.IMWRITE_PXM_BINARY, 1))
        masks = []
        mask = {'coords':mask_png_path, 
         'class':cls}
        masks.append(mask)
        return masks

    def save_results(self):
        self.result['slide'] = self.filepath
        self.result['method'] = self.method
        self.result['wsi_width'] = self.wsi_width
        self.result['wsi_height'] = self.wsi_height
        self.result['patch_width'] = self.p_width
        self.result['patch_height'] = self.p_height
        self.result['overlap_width'] = self.o_width
        self.result['overlap_hegiht'] = self.o_height
        self.result['start_sample'] = self.start_sample
        self.result['finished_sample'] = self.finished_sample
        self.result['extract_patches'] = self.extract_patches
        self.result['on_foreground'] = self.on_foreground
        self.result['on_annotation'] = self.on_annotation
        self.result['save_to'] = str(Path(self.save_to).absolute())
        self.result['classes'] = self.classes
        with open('{}/{}/results.json'.format(self.save_to, self.filestem), 'w') as (f):
            json.dump((self.result), f, indent=4)

    def get_patch(self, x, y, cls=False):
        if self.on_foreground:
            if not self.patch_on_foreground(x, y):
                return
        if self.on_annotation:
            if not self.patch_on_annotation(cls, x, y):
                return
        if self.extract_patches:
            patch = self.slide.slide.crop(x, y, self.p_width, self.p_height)
            patch.pngsave('{}/{}/patches/{}/{:06}_{:06}.png'.format(self.save_to, self.filestem, cls, x, y))
        self.save_patch_result(x, y, cls)

    def get_patch_parallel(self, cls=False, cores=-1):
        if self.extract_patches:
            self.verify.verify_dir('{}/{}/patches/{}'.format(self.save_to, self.filestem, cls))
        if self.method == 'segmentation':
            self.verify.verify_dir('{}/{}/masks/{}'.format(self.save_to, self.filestem, cls))
        if self.start_sample:
            self.get_random_sample('start', 3)
        parallel = Parallel(n_jobs=cores, backend='threading', verbose=1)
        parallel([delayed(self.get_patch)(x, y, cls) for x, y in self.iterator])
        parallel([delayed(self.get_patch)(x, self.last_y, cls) for x in self.x_lefttop])
        parallel([delayed(self.get_patch)(self.last_x, y, cls) for y in self.y_lefttop])
        self.get_patch(self.last_x, self.last_y, cls)
        self.save_results()
        if self.finished_sample:
            self.get_random_sample('finished', 3)

    def patch_on_foreground(self, x, y):
        patch_mask = self.masks['foreground'][y:y + self.p_height, x:x + self.p_width]
        return patch_mask.sum() / self.p_area >= self.on_foreground

    def patch_on_annotation(self, cls, x, y):
        patch_mask = self.masks[cls][y:y + self.p_height, x:x + self.p_width]
        return patch_mask.sum() / self.p_area >= self.on_annotation

    def get_random_sample(self, phase, sample_count=1):
        for i in range(sample_count):
            x = random.choice(self.x_lefttop)
            y = random.choice(self.y_lefttop)
            patch = self.slide.slide.crop(x, y, self.p_width, self.p_height)
            patch.pngsave('{}/{}/{}_sample/{:06}_{:06}.png'.format(self.save_to, self.filestem, phase, x, y))
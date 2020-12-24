# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matraszek/PycharmProjects/img2unicode/build/lib/img2unicode/dual.py
# Compiled at: 2020-04-30 15:17:01
# Size of source mod 2**32: 8283 bytes
"""Optimizers that use both foreground and background."""
from abc import ABC, abstractmethod, abstractproperty
import numpy as np, skimage, skimage.transform
from img2unicode.templates import get_16x8_flat
from img2unicode.utils import cubify

class BaseDualOptimizer(ABC):

    @abstractproperty
    def n_chars(self):
        pass

    def optimize_char(self, char):
        return self.optimize_chunk(char)

    def optimize_chunk(self, img):
        pieces = cubify(img, (16, 8) if len(img.shape) == 2 else (16, 8, 3))
        if hasattr(self, 'optimize_image'):
            return self.optimize_image(pieces)
        chars, fgs, bgs = zip(*[self.optimize_char(c) for c in pieces])
        return (np.array(chars), np.array(fgs), np.array(bgs))


class HalfBlockDualOptimizer(BaseDualOptimizer):
    __doc__ = 'This is very simple, since we use the block is predefined.\n\n        We use the average color of the top 8x8 block for foreground and bottom 8x8 for background.\n    '

    def __init__(self, *args):
        pass

    @property
    def n_chars(self):
        return 1

    def optimize_char(self, piece):
        s = piece.reshape(-1, 3)
        char = ord('▀')
        fc = s[:8].mean(axis=0)
        bg = s[8:].mean(axis=0)
        return (char, fc, bg)

    def optimize_chunk(self, img):
        min_img = skimage.transform.downscale_local_mean(img, (8, 8, 1))
        chars = np.ones_like((min_img[::2, :, 0]), dtype='int') * ord('▀')
        return (chars, min_img[::2], min_img[1::2])


class SpaceDualOptimizer(BaseDualOptimizer):
    __doc__ = 'This is very simple, since we use only background color – the average color of 16x8 block.'

    def __init__(self, *args):
        pass

    @property
    def n_chars(self):
        return 1

    def optimize_char(self, piece):
        s = piece.reshape(-1, 3)
        char = ord(' ')
        fc = s.mean(axis=0)
        return (char, fc, fc)

    def optimize_chunk(self, img):
        min_img = skimage.transform.downscale_local_mean(img, (16, 8, 1))
        chars = np.ones_like((min_img[:, :, 0]), dtype='int') * ord(' ')
        return (chars, min_img, min_img)


class FastQuadDualOptimizer(BaseDualOptimizer):
    __doc__ = 'Here we use the same trick as in FastGenericDualOptimizer.\n\n    The only difference is that we have homogenous pixels and each template is\n    in reality 2x2 matrix. Therefore we reduce the input piece size to 2x2 by subsampling first.\n    '
    QUADS = np.array([ord(c) for c in '▀▌▖▗▘▝▚'])

    def __init__(self, _charmask=None, _templates=None):
        masks = np.array([[1.0, 1.0, 0.0, 0.0],
         [
          1.0, 0.0, 1.0, 0.0],
         [
          0.0, 0.0, 1.0, 0.0],
         [
          0.0, 0.0, 0.0, 1.0],
         [
          1.0, 0.0, 0.0, 0.0],
         [
          0.0, 1.0, 0.0, 0.0],
         [
          1.0, 0.0, 0.0, 1.0]])
        self.masks = masks
        self.db1 = np.nan_to_num(masks / np.sqrt(np.sum(masks, axis=1))[:, np.newaxis])
        self.db2 = np.nan_to_num((1 - masks) / np.sqrt(np.sum((1 - masks), axis=1))[:, np.newaxis])

    @property
    def n_chars(self):
        return len(self.QUADS)

    def optimize_chunk(self, img):
        img = skimage.transform.downscale_local_mean(img, (8, 4, 1))
        imgc = cubify(img, (2, 2, 3)).reshape(-1, 4, 3)
        masks = self.masks
        best_char = np.argmax(((self.db1 @ imgc) ** 2 + (self.db2 @ imgc) ** 2).sum(axis=2), 1)
        best_masks = masks[best_char][:, :, np.newaxis]
        fg = np.sum((best_masks * imgc), axis=1) / best_masks.sum(axis=1)
        bg = np.sum(((1 - best_masks) * imgc), axis=1) / (1 - best_masks).sum(axis=1)
        return (
         self.QUADS[best_char], fg, bg)


class ExactGenericDualOptimizer(BaseDualOptimizer):
    __doc__ = 'Here we optimize the following function:\n\n    cs - chars template (Nx16*8)\n    x - image chunk to match (16*8, 3)\n    $$argmin_i \\sum_p (cs_{i,p} * fg_i + (1-cs_{i,p}) * bg_i - s_p)^2$$\n    where fg and bg are, respectively, computed average foreground color and background color as follows:\n\n    $$ fg_i = \x0crac{\\sum_p (cs_{i,p} * s_p)}{\\sum_p cs_{i,p}} == \x0crac{cs_i \\cdot s}{|cs_i|}$$\n    $$ bg_i = \x0crac{\\sum_p ( (1-cs_{i,p}) * s_p)}{\\sum_p 1-cs_{i,p}} == \x0crac{(1-cs_i) \\cdot s}{|1-cs_i|} $$\n    with the assumption, that 0/0 is 0.\n\n    '

    def __init__(self, charmask=None, templates=None):
        cs, indexer = get_16x8_flat(templates, charmask)
        self.cs = cs
        self.indexer = indexer

    @property
    def n_chars(self):
        return len(self.cs)

    def optimize_char(self, piece):
        cs = self.cs
        s = piece.reshape(-1, 3)
        with np.errstate(divide='ignore', invalid='ignore'):
            fc = np.nan_to_num(np.clip(cs @ s / cs.sum(axis=1)[:, np.newaxis], 0, 1))
            bg = np.nan_to_num(np.clip((1 - cs) @ s / (1 - cs).sum(axis=1)[:, np.newaxis], 0, 1))
        props = cs[:, :, np.newaxis] * fc[:, np.newaxis, :] + (1 - cs)[:, :,
         np.newaxis] * bg[:, np.newaxis, :]
        arr = np.abs(props - s) ** 2
        summ = np.sum(arr, axis=1).sum(axis=1)
        res = np.argsort(summ)
        idx = self.indexer[res[0]]
        return (idx, fc[res[0]], bg[res[0]])


class FastGenericDualOptimizer(BaseDualOptimizer):
    __doc__ = "\n        Here we optimize the following function:\n\n        cs - chars templatse (N,16*8)\n        x - image chunk to match (16*8,3)\n        $$argmin_i \\sum_p (cs_{i,p} * fg_i - s_p)^2 + \\sum _p ((1-cs_{i,p}) * bg_i - s_p)^2$$\n\n        where fg and bg are, respectively, computed average foreground color and background color as follows:\n        fg_i = \x0crac{\\sum_p (cs_{i,p} * s_p)}{\\sum_p cs_{i,p}}\n        bg_i = \x0crac{\\sum_p ( (1-cs_{i,p}) * s_p)}{\\sum_p 1-cs_{i,p}}\n        with the assumption, that 0/0 is 0.\n\n        In the special case that cs_{i,p} is binary (either 0 or 1), this is equivalent the the ExactGenericDualOptimizer.\n        But in this version, we may convert the initial optimization problem into just:\n        $$argmax_i (\\sum_p cs_{i,p}/\\sqrt{\\sum_p cs_{i,p}}  * s_p)^2 + (\\sum_p (1-cs_{i,p})/\\sqrt{\\sum_p 1-cs_{i,p}}  * s_p)^2$$\n        Where we may precompute the $cs_{i,p}/\\sqrt{\\sum_p cs_{i,p}}$ part as [C]{i,p} matrix, (same C' for $1-cs$).\n        And now we have just scalar products:\n\n        $$ argmax_i (C_i * s)^2 + (C'_i * s)^2 $$\n        Which can be further simplified to tensor multiplication if we have several s-es (S : (batch, 16*8, 3)):\n\n        $$ char(j, S) = argmax_i ((C_i*S)^2+(C'_i*S)^2)_{i,j}$$\n\n    "

    def __init__(self, charmask=None, templates=None):
        cs, indexer = get_16x8_flat(templates, charmask)
        self.cs = cs
        self.indexer = indexer
        with np.errstate(divide='ignore', invalid='ignore'):
            self.cs1 = np.nan_to_num(cs / np.sqrt(np.sum(cs, axis=1))[:, np.newaxis])
            self.cs2 = np.nan_to_num((1 - cs) / np.sqrt(np.sum((1 - cs), axis=1))[:, np.newaxis])

    @property
    def n_chars(self):
        return len(self.cs)

    def optimize_image(self, img):
        Q = img.reshape(-1, 128, 3)
        best_char = np.argmax(((self.cs1 @ Q) ** 2 + (self.cs2 @ Q) ** 2).sum(axis=2), 1)
        best_masks = self.cs[best_char][:, :, np.newaxis]
        with np.errstate(divide='ignore', invalid='ignore'):
            fg = np.nan_to_num(np.clip(np.sum((best_masks * Q), axis=1) / best_masks.sum(axis=1), 0, 1))
            bg = np.nan_to_num(np.clip(np.sum(((1 - best_masks) * Q), axis=1) / (1 - best_masks).sum(axis=1), 0, 1))
        return (self.indexer[best_char], fg, bg)
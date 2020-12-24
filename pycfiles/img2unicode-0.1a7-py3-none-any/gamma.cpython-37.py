# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matraszek/PycharmProjects/img2unicode/build/lib/img2unicode/gamma.py
# Compiled at: 2020-04-30 19:04:16
# Size of source mod 2**32: 5996 bytes
import numpy as np, skimage.transform
from n2 import HnswIndex
from sklearn.neighbors import NearestNeighbors
from img2unicode.templates import get_16x16, DEFAULT_TEMPLATES, normalize_mask

class BasicGammaOptimizer:
    __doc__ = 'Here we optimize the euclidean distance of chunk and template and their edges:\n\n    cs - chars template (Nx16*8)\n    cse - chars edges (Nx8*4)\n    x - image chunk to match (16*8)\n    xe - image chunk edges to match (8*4)\n    alpha - weight of edges distance\n\n    $$argmin_i \\sum_p (cs_{i,p} - s_p)^2 + \\sum_p (cse_{i,p} - se_p)^2$$\n\n    Foreground color is achieved by first normalizing the example, matching,\n    and then applying color.\n    '

    def __init__(self, use_color=True, charmask=None, templates=DEFAULT_TEMPLATES):
        self.use_color = use_color
        bigs = templates.raw_16x16
        self.bigs = bigs
        self.bigs2 = templates.base_16x16
        wide_mask = np.tile(np.repeat([0, 1], 8), (16, 1))
        almost_thin_mask = wide_mask.copy()
        almost_thin_mask[:, 8:10] = 0
        self.wide_mask = wide_mask
        self.almost_thin_mask = almost_thin_mask
        self.almost_thin_mask_half = skimage.transform.downscale_local_mean(almost_thin_mask, (2,
                                                                                               2))
        self.iswide = (bigs * wide_mask).sum(axis=1).sum(axis=1) > 0.1
        self.isalmostthin = (bigs * almost_thin_mask).sum(axis=1).sum(axis=1) < 0.1
        charmask = normalize_mask(charmask, np.ones((len(bigs)), dtype='bool'), templates)
        athin_idx_m = charmask & (self.iswide & self.isalmostthin)
        if athin_idx_m.sum() == 0:
            athin_idx_m[32] = 1
        thin_idx_m = charmask & ~self.iswide
        if thin_idx_m.sum() == 0:
            thin_idx_m[32] = 1
        self.athin_bigs2, self.athin_bigse, self.athin_idx = get_16x16(templates, athin_idx_m, return_edges=True)
        self.thin_bigs2, self.thin_bigse, self.thin_idx = get_16x16(templates, thin_idx_m, return_edges=True)

    @property
    def n_chars(self):
        return len(self.athin_idx) + len(self.thin_idx)

    def search(self, t, te, bigs2, bigse):
        c = (np.abs(bigs2 - t) ** 2).sum(axis=1).sum(axis=1) + np.abs(bigse - te).sum(axis=1).sum(axis=1) / 10
        chr = np.argmin(c)
        res = (chr, c[chr])
        return res

    def _optimize_char(self, t, te):
        thin_masked = t - t * self.wide_mask
        athin_masked = t - t * self.almost_thin_mask
        te_athin_masked = te - te * self.almost_thin_mask_half
        arc, ars = self.search(athin_masked, te_athin_masked, self.athin_bigs2, self.athin_bigse)
        rc, rs = self.search(thin_masked, te_athin_masked, self.thin_bigs2, self.thin_bigse)
        res_c = self.thin_idx[rc] if rs <= ars else self.athin_idx[arc]
        return res_c

    def _optimize_chunk(self, img_gray, img_edges, imgc=None):
        for x in range(img_gray.shape[0] // 16):
            for y in range(img_gray.shape[1] // 8 - 1):
                piece_gray = img_gray[x * 16:(x + 1) * 16, y * 8:(y + 2) * 8]
                if self.use_color:
                    piece_gray /= piece_gray.max() + 1e-05
                else:
                    piece_edges = img_edges[x * 8:(x + 1) * 8, y * 4:(y + 2) * 4]
                    res = self._optimize_char(piece_gray, piece_edges)
                    if self.use_color:
                        piece_color = imgc[x * 16:(x + 1) * 16, y * 8:(y + 2) * 8]
                        with np.errstate(divide='ignore', invalid='ignore'):
                            color = np.nan_to_num(((piece_color * self.bigs2[res][:, :, np.newaxis]).sum(axis=0).sum(axis=0) / self.bigs2[res].sum()).clip(0.0, 1.0))
                        background = np.array([0.0, 0.0, 0.0])
                    else:
                        color = None
                    background = None
                yield (
                 res, color, background)

    def optimize_chunk(self, img_gray, img_edges, imgc=None):
        chars, fgs, bgs = zip(*list(self._optimize_chunk(img_gray, img_edges, imgc)))
        fgs = np.array(fgs)
        if fgs.ravel()[0] is None:
            fgs = None
        bgs = np.array(bgs)
        if bgs.ravel()[0] is None:
            bgs = None
        return (
         np.array(chars), fgs, bgs)


class ExactGammaOptimizer(BasicGammaOptimizer):
    __doc__ = "Since we optimize euclidean distance, we may use NearestNeighbours algorithm to find the matching template.\n\n\n    The only change is that instead of separate `cs` and `cse`, we have:\n    $$cs' = [cs, cse/10]$$\n    $$s' = [s, se/10]$$\n    And we optimize:\n    $$argmin_i (cs' - s')^2$$\n\n    That can be solved for instance using kd_tree.\n    "

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.athin_bigs2 = self.build_nn(self.athin_bigs2, self.athin_bigse)
        self.thin_bigs2 = self.build_nn(self.thin_bigs2, self.thin_bigse)

    def build_nn(self, bigs2, bigse):
        Dataset = np.concatenate([
         bigs2.reshape(bigs2.shape[0], -1), bigse.reshape(bigse.shape[0], -1) / 10],
          axis=1)
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='kd_tree', n_jobs=1, leaf_size=10).fit(Dataset)
        return nbrs

    def search(self, t, te, nbrs, _bigse):
        Q = np.array([np.concatenate([t.ravel(), te.ravel() / 10])])
        distances, indices = nbrs.kneighbors(Q)
        res = (indices[0][0], distances[0][0] ** 2)
        return res


class FastGammaOptimizer(ExactGammaOptimizer):
    __doc__ = 'This has the same principle as ExactGammaOptmizer, but an approximate nearest neighbour algorithm is used.'

    def build_nn(self, bigs2, bigse):
        Dataset = np.concatenate([
         bigs2.reshape(bigs2.shape[0], -1), bigse.reshape(bigse.shape[0], -1) / 10],
          axis=1)
        index = HnswIndex(320, 'euclidean')
        for i in Dataset:
            index.add_data(i)

        index.build(m=5)
        return index

    def search(self, t, te, nbrs, _bigse):
        Q = np.array(np.concatenate([t.ravel(), te.ravel() / 10]))
        res = nbrs.search_by_vector(Q, 1, include_distances=True)[0]
        return res
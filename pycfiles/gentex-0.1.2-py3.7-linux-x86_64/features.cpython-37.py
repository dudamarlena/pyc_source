# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gentex/features.py
# Compiled at: 2019-10-04 13:17:54
# Size of source mod 2**32: 11267 bytes
import numpy as np

class Features:
    __doc__ = "\n    Class features for generating and manipulating feature spaces\n\n    Class Methods\n    --------------\n\n    __init__(images,mask,template)\n\n    \n    clusfs(method,numclus,clusmax)\n\n    Class Variables\n    ----------------\n\n    Class variables required by constructor:\n\n    images:   array of 1-4 dimensional ndarrays (images) used to build\n              feature space\n\n    mask:     1-4 dimensional mask used to determines which\n              voxels to use for building feature space\n\n    template: set of points relative to an anchor point\n              used to build feature space\n\n    Internal class variables:\n\n    fs:       P x F ndarray constituing feature space. P is the number\n              of points in the image(s) such that the template fell\n              within the mask and hence generated a feature space\n              point. F is the number of features (i.e. number of template\n              points times number of images)\n\n    fsc:      P X D ndarray constituing array of coordinates associated with\n              the points in feature space where as for fs, P is the number\n              of points in the image(s) such that the template fell\n              within the mask, and D is the underlying dimension of the\n              image space.\n\n    fsmask    Image mask with 1's where the template coordinates were\n              inside the image and mask (i.e. image coordinates for which\n              the feature space points were obtained)\n              \n    clusim    clustered feature space image - currently uses kmeans\n              to cluster the image using the feature space values\n\n    numclus - int\n              Number of clusters used to generate segmented image\n\n    clusmax - int\n              if numclus is passed to the clusfs() function with a value\n              less than 2 then clusf() will try to determine the optimal\n              number of clusters (if the default 'Kmeans' method is being\n              used) and clusmax specifies the maximum number of clusters\n              to try\n\n              default = 20\n              \n\n    cluscrit - string\n               penalty method to use with k-means to determine\n               number of epsilon machine states when estimating\n               epsilon machine from the cooccurence matrix.\n               One of:\n               'AIC' - Akaike's information criterion [Akaike, 1974]\n               'BIC' - Bayesian information criterion [Schwartz, 1978]\n               'ICL' - Integrated completed likelihood [Biernacki, 2000]\n               \n               default = 'BIC'\n    \n    "

    def __init__(self, images, mask, template):
        self.images = images
        self.mask = mask
        self.template = template
        self.fs = np.array([], dtype=(np.float32))
        self.fsc = np.array([], dtype=(np.int16))
        self.fsmask = np.zeros((self.images[0].shape), dtype=(np.int16))
        self.foundfeat = 0
        self.clusim = np.zeros((self.images[0].shape), dtype=(np.int16))
        self.numclus = 3
        self.cluscrit = 'BIC'
        self.clusmax = 20
        self.dims = images[0].shape
        assert len(self.dims) == len(self.mask.shape)
        assert len(self.dims) == len(template[0])
        self.numfeats = len(template) * len(images)
        maxs = np.max((np.array(self.template)), axis=0)
        mins = np.min((np.array(self.template)), axis=0)
        uplim = self.dims - maxs
        lowlim = np.where(np.greater(-mins, 0), -mins, 0)
        ind = np.indices(uplim - lowlim)
        self.fsc = np.array([np.ravel(ind[i] + lowlim[i]) for i in range(len(lowlim))], dtype=(np.int16))
        imcount = 0
        colcount = 0
        for im in images:
            for temp in template:
                upl = uplim + temp
                downl = lowlim + temp
                thiscol = np.ravel(np.where(self.mask == 1, im, np.inf)[tuple([slice(down, up) for down, up in zip(downl, upl)])])
                if colcount == 0:
                    badelts = np.array(np.where(thiscol == np.inf)[0])
                    self.fs = np.array((np.delete(thiscol, badelts, 0)), dtype=(np.float32))
                else:
                    badnew = np.array(np.where(thiscol == np.inf)[0])
                    newstack = np.array((np.delete(thiscol, badelts, 0)), dtype=(np.float32))
                    shortnew = np.where(newstack == np.inf)[0]
                    badelts = np.array(np.unique(np.append(badelts, badnew)))
                    if colcount == 1:
                        if newstack.size != 0:
                            self.fs = np.vstack((np.delete(self.fs, shortnew, 0), np.delete(newstack, shortnew, 0)))
                    elif newstack.size != 0:
                        self.fs = np.vstack((np.delete(self.fs, shortnew, 1), np.delete(newstack, shortnew, 0)))
                    colcount += 1

            del im
            imcount += 1

        self.fs = np.transpose(self.fs)
        self.fsc = np.array((np.delete(self.fsc, badelts, 1)), dtype=(np.int16))
        self.fsc = tuple(self.fsc)
        self.fsmask[self.fsc] = 1

    def clusfs(self, method='Kmeans', numclus=3, clusmax=20, cluscrit='BIC'):
        """
        method clusfs - clusters feature space

        With no arguments clusfs uses Kmeans (only clustering method
        currently implemented) to cluster the feature space points
        into 3 clusters. The user can specify a set of arguments that
        either specify a set number of clusters to use or asks clusfs
        to try and find the best number of clusters using a Gaussian
        likelihood and a penalty term the form of which can be specified
        by the user (currently AIC or BIC are the only choices available)

        optional arguments:

        method - clustering method, currently Kmeans is the only method
                 implemented

                 default = 'Kmeans'

        numclus - number of clusters to try; if this number is less than 2
                  clusfs will try to find the best number of clusters,
                  trying up to clusmax.

                  default = 3

        clusmax - the largest number of clusters that clusfs will try

                  default = 20

        cluscrit - the 'overfitting' criteria used as a penalty term in
                   conjuction with a Gaussian likelihood term that estimates
                   the fidelity of the clustering. See, e.g.
                   
                   Goutte C, Hansen LK, Liptrot MG, Rostrup E.
                   Feature-space clustering for fMRI meta-analysis.
                   Hum Brain Mapp. 2001 Jul;13(3):165-83.
        
        """
        self.numclus = numclus
        self.clusmax = clusmax
        self.cluscrit = cluscrit
        if method == 'Kmeans':
            import scipy.cluster as sc
            opto = []
            b = sc.vq.whiten(self.fs)
            if self.cluscrit == 'ICL':
                print("Haven't implemented ICL yet, using BIC...")
            if numclus < 2:
                for i in range(2, min([self.clusmax + 1, self.fs.shape[0] + 1])):
                    z = sc.vq.kmeans(b, i)
                    t = sc.vq.kmeans2(b, z[0])
                    if i == self.fs.shape[0]:
                        lh = 1.0
                    else:
                        sig = 1.0 / b.shape[0] * np.sum(np.abs(t[0][t[1]] - b) ** 2)
                        lh = np.sum(np.log2(1.0 / np.sqrt(2.0 * np.pi * sig * sig)) * np.exp(-(1.0 / (2.0 * sig * sig) * np.sum(((t[0][t[1]] - b) ** 2), axis=1))))
                        if self.cluscrit == 'AIC':
                            opto.append(lh - (i * self.fs.shape[1] + 1))
                        elif self.cluscrit == 'ICL':
                            print('Warning: ICL not quite ready, using BIC')
                            opto.append(lh - (i * self.fs.shape[1] + 1) / 2.0 * np.log2(self.fs.shape[1]))
                        else:
                            opto.append(lh - (i * self.fs.shape[1] + 1) / 2.0 * np.log2(self.fs.shape[1]))

                self.numclus = np.array(opto).argmax() + 2
                z = sc.vq.kmeans(sc.vq.whiten(self.fs), self.numclus)
                t = sc.vq.kmeans2(sc.vq.whiten(self.fs), z[0])
                self.clusim[self.fsc] = t[1]
                print('Using', self.numclus, 'clusters for feature space')
            else:
                z = sc.vq.kmeans(sc.vq.whiten(self.fs), self.numclus)
                t = sc.vq.kmeans2(sc.vq.whiten(self.fs), z[0])
                self.clusim[self.fsc] = t[1]
        else:
            print('Sorry Kmeans only clustering method currently supported')
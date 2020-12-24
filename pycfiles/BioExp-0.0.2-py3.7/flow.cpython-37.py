# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioExp/spatial/flow.py
# Compiled at: 2019-11-15 02:16:49
# Size of source mod 2**32: 2025 bytes
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cv2
from keras import activations
from ..helpers.utils import *
import vis
from vis.visualization import visualize_cam
import vis.utils as utils

def cam(model, img, gt, nclasses=2, save_path=None, layer_idx=-1, threshol=0.5, modifier='guided'):
    """
        """
    model.layers[layer_idx].activation = activations.linear
    num_layers = sum([model.layers[layer].name.__contains__('conv') for layer in range(1, len(model.layers))])
    layer_dice = np.zeros((num_layers, nclasses))
    counter = 0
    for layer in range(1, len(model.layers)):
        if 'conv' not in model.layers[layer].name:
            continue
        if save_path:
            plt.figure(figsize=(30, 10))
            gs = gridspec.GridSpec(1, 3)
            gs.update(wspace=0.025, hspace=0.05)
        for class_ in range(nclasses):
            grads_ = visualize_cam(model, layer_idx, filter_indices=class_, penultimate_layer_idx=layer, seed_input=(img[(None,
                                                                                                                          Ellipsis)]),
              backprop_modifier=modifier)
            if save_path:
                ax = plt.subplot(gs[(class_ - 1)])
                im = ax.imshow(grads_, cmap=(plt.cm.RdBu))
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                ax.set_aspect('equal')
                ax.tick_params(bottom='off', top='off', labelbottom='off')
                if class_ == nclasses:
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes('right', size='5%', pad=0.2)
                    cb = plt.colorbar(im, ax=ax, cax=cax)
            thresh_image = grads_ > threshold
            gt_mask = gt == class_
            score = np.sum(thresh_image * gt_mask) * 2.0 / (np.sum(gt_mask * 1.0 + thresh_image * 1.0) + 0.001)
            layer_dice[counter][(class_ - 1)] += score

        counter += 1
        if save_path:
            os.makedirs(os.path.join(save_path, 'gradientflow'))
            plt.savefig((os.path.join(os.path.join(save_path, 'gradientflow'), model.layers[layer].name.replace('/', '_') + '.png')), bbox_inches='tight')
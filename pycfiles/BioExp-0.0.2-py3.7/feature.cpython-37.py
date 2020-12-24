# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BioExp/concept/feature.py
# Compiled at: 2019-11-16 00:17:00
# Size of source mod 2**32: 8027 bytes
import matplotlib
matplotlib.use('Agg')
import lucid.optvis.param as param
import lucid.optvis.render as render
from lucid.misc.io.showing import _image_url, _display_html
from lucid.modelzoo.vision_base import Model
import tensorflow as tf
import lucid.optvis.transform as transform
from lucid.optvis import objectives
from lucid.misc.io import show
from lucid.optvis.objectives_util import _dot, _dot_cossim, _extract_act_pos, _make_arg_str, _T_force_NHWC, _T_handle_batch
from lucid.optvis.objectives import Objective
import matplotlib.pyplot as plt
import cv2, numpy as np
from pprint import pprint
import matplotlib.gridspec as gridspec
from decorator import decorator
from lucid.optvis.param.color import to_valid_rgb
from lucid.optvis.param.spatial import pixel_image, fft_image
import os

class Feature_Visualizer:
    __doc__ = '\n  A class for generating Feature Visualizations of internal filters from a .pb model file (based on Lucid)\n\n  Inputs: model_loader: A function that loads an instance of the Lucid Model class (see examples)\n          layer: The layer to visualize\n          channel(optional): The index of the filter to visualize; defaults to 0.\n          savepath(optional): Path to save visualized features\n          n_channels(optional): Number of channels in model input; defaults to 4\n          regularizer_params(optional): A dictionary of regularizer parameters for the optimizer. Parameters which are not given will default to below values.\n\n  Outputs: Visualized Feature saved at savepath\n  '

    def __init__(self, model_loader, savepath='./', n_channels=4, regularizer_params=dict.fromkeys(['jitter', 'rotate', 'scale', 'TV', 'blur', 'decorrelate', 'L1'])):
        default_dict = dict.fromkeys(['jitter', 'rotate', 'scale', 'TV', 'blur', 'decorrelate', 'L1'])
        for key in regularizer_params.keys():
            default_dict[key] = regularizer_params[key]

        regularizer_dict = default_dict
        print('Regularizer Paramaters: ', regularizer_dict)
        self.loader = model_loader
        self.jitter = regularizer_dict['jitter'] if regularizer_dict['jitter'] is not None else 8
        self.rotate = regularizer_dict['rotate'] if regularizer_dict['rotate'] is not None else 4
        self.scale = regularizer_dict['scale'] if regularizer_dict['scale'] is not None else 1.2
        self.TV = regularizer_dict['TV'] if regularizer_dict['TV'] is not None else 0
        self.blur = regularizer_dict['blur'] if regularizer_dict['blur'] is not None else 0
        self.decorrelate = regularizer_dict['decorrelate'] if regularizer_dict['decorrelate'] is not None else True
        self.L1 = regularizer_dict['L1'] if regularizer_dict['L1'] is not None else 1e-05
        self.savepath = savepath
        self.n_channels = n_channels
        print('jitter: {}, rotate: {}'.format(self.jitter, self.rotate))
        self.model = self.loader()
        self.model.load_graphdef()

    def show_images(self, images):
        html = ''
        for image in images:
            data_url = _image_url(image)
            html += '<img width="100" style="margin: 10px" src="' + data_url + '">'

        _display_html(html)

    def wrap_objective(require_format=None, handle_batch=False):
        """Decorator for creating Objective factories.

    Changes f from the closure: (args) => () => TF Tensor
    into an Obejective factory: (args) => Objective

    while perserving function name, arg info, docs... for interactive python.
    """

        @decorator
        def inner(f, *args, **kwds):
            objective_func = f(*args, **kwds)
            objective_name = f.__name__
            args_str = ' [' + ', '.join([_make_arg_str(arg) for arg in args]) + ']'
            description = objective_name.title() + args_str

            def process_T(T):
                if require_format == 'NHWC':
                    T = _T_force_NHWC(T)
                return T

            return Objective(lambda T: objective_func(process_T(T)), objective_name, description)

        return inner

    @wrap_objective(require_format='NHWC')
    def _channel(self, layer, n_channel, gram=None):
        """Visualize a single channel"""

        def inner(T):
            if gram is not None:
                kernel = lambda x, y: tf.reduce_mean(tf.exp(-0.125 * tf.abs(x - y) ** 2))
                var = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)[0]
                var_vec = tf.reshape(var, [-1, 4])
                gram_vec = tf.reshape(gram, [-1, 4])
                kernel_loss = 0
                for i in range(4):
                    for j in range(4):
                        kernel_loss += kernel(var_vec[:, i], var_vec[:, j]) + kernel(gram_vec[:, i], gram_vec[:, j]) - 2 * kernel(var_vec[:, i], gram_vec[:, j])

                return tf.reduce_mean(T(layer)[(..., n_channel)]) - 0.01 * kernel_loss - self.L1 * tf.norm(var)
            var = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)[0]
            return tf.reduce_mean(T(layer)[(..., n_channel)])

        return inner

    def image(self, w, h=None, batch=None, sd=None, decorrelate=True, fft=True, alpha=False, channels=None):
        h = h or w
        batch = batch or 1
        ch = channels or (4 if alpha else 3)
        shape = [batch, h, w, ch]
        param_f = fft_image if fft else pixel_image
        t = param_f(shape, sd=sd)
        if channels:
            output = tf.nn.sigmoid(t)
        else:
            output = to_valid_rgb((t[..., :3]), decorrelate=decorrelate, sigmoid=True)
            if alpha:
                a = tf.nn.sigmoid(t[..., 3:])
                output = tf.concat([output, a], -1)
        return output

    def run(self, layer, class_, channel=None, style_template=None, transforms=False, opt_steps=1000):
        """
    layer         : layer_name to visualize
    class_        : class to consider
    style_template: template for comparision of generated activation maximization map
    transforms    : transforms required
    opt_steps     : number of optimization steps
    """
        self.layer = layer
        self.channel = channel if channel is not None else 0
        with tf.Graph().as_default() as (graph):
            with tf.Session() as (sess):
                if style_template is not None:
                    gram_template = tf.constant((np.load(style_template)), dtype=(tf.float32))
                else:
                    obj = self._channel((self.layer + '/convolution'), (self.channel), gram=style_template)
                    obj += -self.L1 * objectives.L1(constant=0.5)
                    obj += self.TV * objectives.total_variation()
                    obj += self.blur * objectives.blur_input_each_step()
                    if transforms == True:
                        transforms = [transform.pad(2 * self.jitter),
                         transform.jitter(self.jitter),
                         transform.random_scale([self.scale ** (n / 10.0) for n in range(-10, 11)]),
                         transform.random_rotate(range(-self.rotate, self.rotate + 1))]
                    else:
                        transforms = []
                T = render.make_vis_T((self.model), obj, param_f=(lambda : self.image(240, channels=(self.n_channels), fft=(self.decorrelate), decorrelate=(self.decorrelate))),
                  optimizer=None,
                  transforms=transforms,
                  relu_gradient_override=False)
                tf.initialize_all_variables().run()
                for i in range(opt_steps):
                    T('vis_op').run()

                plt.figure(figsize=(10, 10))
                texture_images = []
                for i in range(1, self.n_channels + 1):
                    plt.subplot(1, self.n_channels, i)
                    image = T('input').eval()[:, :, :, i - 1].reshape((240, 240))
                    print('channel: ', i, image.min(), image.max())
                    plt.imshow(image, cmap='gray', interpolation='bilinear',
                      vmin=0.0,
                      vmax=1.0)
                    plt.xticks([])
                    plt.yticks([])
                    texture_images.append(image)

        os.makedirs((os.path.join(self.savepath, class_)), exist_ok=True)
        plt.savefig((os.path.join(self.savepath, class_, self.layer + '_' + str(self.channel) + '.png')), bbox_inches='tight')
        return np.array(texture_images).transpose(1, 2, 0)
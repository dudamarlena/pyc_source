# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flopth/model_viewer.py
# Compiled at: 2019-02-21 08:48:56
# Size of source mod 2**32: 4129 bytes
""" Main file to calculate infomation of a pytorch model. """
import numpy as np
from tabulate import tabulate
import torch
from flopth.helper import compute_flops

class ModelViewer:

    def __init__(self, model, x, param_dict, dtype='float32', *args):
        self._model = model
        self.args = args
        self.leaf_modules, self.leaf_module_names = self.obtain_leaf_modules()
        self.register_parameter(param_dict)
        self.apply_forward_hook()
        self._model.eval()
        if torch.cuda.is_available():
            x = x.cuda()
            self._model = self._model.cuda()
        self._model(x, *args)

    def obtain_leaf_modules(self):
        """ Get modules which have no children. """
        leaf_modules = []
        leaf_module_names = []
        for n, m in self._model.named_modules():
            if len(list(m.children())) == 0:
                if not isinstance(m, torch.nn.Module):
                    print('Module {} is not supported at now.', 'All info about it will be ignored.'.format(n))
                    continue
                    leaf_modules.append(m)
                    leaf_module_names.append(n)

        return (
         leaf_modules, leaf_module_names)

    def register_parameter(self, param_dict):
        """ Register Parameters to leaf nn.Module instance in the model.

        Args:
            param_dict: see `param_dict` in `settings.py` for details.
        """
        assert 'flops' in param_dict.keys(), 'The key "flops" must be in params'
        for m in self.leaf_modules:
            for k in param_dict.keys():
                m.register_buffer(k, getattr(torch.zeros(param_dict[k]['size']), param_dict[k]['type'])())

    def apply_forward_hook(self):

        def forward_with_hook(module, *args, **kwargs):
            output = self.forward_funcs[module.__class__](module, *args, **kwargs)
            module.flops = torch.from_numpy(np.array(compute_flops(module, *[args, output]), dtype=np.int64))
            return output

        self.forward_funcs = {}
        for m in self.leaf_modules:
            if m.__class__ not in self.forward_funcs.keys():
                self.forward_funcs[m.__class__] = m.__class__.__call__
                m.__class__.__call__ = forward_with_hook

    def divide_by_unit(self, value):
        if value > 1000000000.0:
            return '{:.6} GFlops'.format(value / 1000000000.0)
        if value > 1000000.0:
            return '{:.6} MFlops'.format(value / 1000000.0)
        if value > 1000.0:
            return '{:.6} KFlops'.format(value / 1000.0)
        return '{:.6} Flops'.format(value / 1.0)

    def show_info(self, show_detail=True):
        sum_flops = torch.zeros(1, dtype=torch.int64)
        if torch.cuda.is_available():
            sum_flops = sum_flops.cuda()
        for m, n in zip(self.leaf_modules, self.leaf_module_names):
            if torch.cuda.is_available():
                sum_flops += m.flops.cuda()
            else:
                sum_flops += m.flops

        sum_flops = sum_flops.detach().cpu().numpy()[0] if sum_flops.is_cuda else sum_flops.detach().numpy()[0]
        if show_detail:
            info = []
            for m, n in zip(self.leaf_modules, self.leaf_module_names):
                flops = m.flops.detach().cpu().numpy() if m.flops.is_cuda else m.flops.detach().numpy()
                if flops.ndim > 0:
                    flops = flops[0]
                info.append([n, self.divide_by_unit(flops), '{:.6}%'.format(flops / sum_flops * 100), '#' * int(flops / sum_flops * 100)])

            print(tabulate(info, headers=('module', 'flops', 'percent', 'percent-vis')))
            print('\n')
        return sum_flops

    def get_info(self, for_human=True):
        flops = self.show_info(show_detail=False)
        if for_human:
            flops = self.divide_by_unit(flops)
        return flops
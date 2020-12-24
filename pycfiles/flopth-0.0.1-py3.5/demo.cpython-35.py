# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flopth/demo.py
# Compiled at: 2019-02-21 08:08:21
# Size of source mod 2**32: 2464 bytes
import argparse, importlib, os, sys, torch, torchvision, torchvision.models as models
from info import ModelViewer
from settings import settings

def parse_parameters():
    parser = argparse.ArgumentParser('A program to calculate FLOPs for pytorch models')
    parser.add_argument('-p', '--module_path', default=None, help='Path to the .py file which contains model' + 'definition, e.g., ../lib/my_models.py')
    parser.add_argument('class_name', help='Name of the net to evaluate defined in ' + 'modeule_path, e.g., DeepLab')
    parser.add_argument('-d', '--dtype', default='float32', help='Type of input tensor of target net. default is ' + 'float32')
    parser.add_argument('-i', '--in_size', nargs='+', type=int, default=[3, 224, 224], help='Input size of target net, without batch_size ' + 'item, e.g., 3 224 224')
    parser.add_argument('-x', '--extra_params', nargs='+', type=int, help='Extra parameters for forward function.')
    return parser.parse_args()


def parse_net(module_path, class_name):
    torchvision_models = [m for m in torchvision.models.__dict__.keys() if '__' not in m]
    if class_name in torchvision_models:
        Model = getattr(torchvision.models, class_name)
    else:
        fail_msg = 'For the model not in torchvision.models, you have to ' + 'specify the python file where the model is defined.'
        assert module_path is not None, fail_msg
        module_dir = os.path.dirname(module_path)
        module_name = os.path.basename(module_path).split('.')[0]
        sys.path.insert(0, module_dir)
        custom_models = importlib.import_module(module_name)
        Model = getattr(custom_models, class_name)
    model = Model()
    return model


def main():
    args = parse_parameters()
    model = parse_net(args.module_path, args.class_name)
    dtype = getattr(torch, args.dtype)
    x = torch.rand([1, *args.in_size], dtype=dtype)
    print(x.shape, args.extra_params)
    if args.extra_params is not None:
        mv = ModelViewer(model, x, True, settings.param_dict, args.extra_params)
    else:
        mv = ModelViewer(model, x, True, settings.param_dict)
    f = mv.get_info()
    print(f)


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quadratum/transformer.py
# Compiled at: 2018-09-28 03:46:28
# Size of source mod 2**32: 1088 bytes
from . import transforms as qtrfm
from torchvision import transforms as vtrfm

class Transformer(object):
    __doc__ = 'Useful pre-defined transforms just for me.'

    def __init__(self, name):
        if name == 'resnet':
            self.transform = vtrfm.Compose([
             qtrfm.Whiten(),
             qtrfm.Dominofy(),
             qtrfm.Contain(256),
             vtrfm.ToPILImage(),
             vtrfm.CenterCrop(224),
             vtrfm.ToTensor(),
             vtrfm.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        else:
            if name == 'inception':
                self.transform = vtrfm.Compose([
                 qtrfm.Whiten(),
                 qtrfm.Dominofy(),
                 qtrfm.Contain(320),
                 vtrfm.ToPILImage(),
                 vtrfm.CenterCrop(299),
                 vtrfm.ToTensor(),
                 vtrfm.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
            else:
                raise NotImplementedError

    def __call__(self, image):
        return self.transform(image)
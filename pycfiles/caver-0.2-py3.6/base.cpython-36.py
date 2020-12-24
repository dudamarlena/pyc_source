# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caver/model/base.py
# Compiled at: 2018-12-25 00:59:13
# Size of source mod 2**32: 1858 bytes
import os, torch, dill as pickle

class BaseModule(torch.nn.Module):
    __doc__ = '\n    Base module for text classification.\n\n    Inherit this if you want to implement your own model.\n    '

    def __init__(self):
        super().__init__()
        self.labels = []
        self.vocab = {}

    def load(self, loaded_checkpoint, path):
        """ load model from file """
        self.update_args(loaded_checkpoint['model_args'])
        self.load_state_dict(loaded_checkpoint['model_state_dict'])
        self.labels = pickle.load(open(os.path.join(path, 'y_feature.p'), 'rb'))
        self.TEXT = pickle.load(open(os.path.join(path, 'TEXT.p'), 'rb'))
        self.vocab = self.TEXT.vocab.stoi

    def save(self, path):
        """ save model to file """
        folder, _ = os.path.split(path)
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print('Folder: {} is created.'.format(folder))
        torch.save(self.state_dict(), path)
        print('[+] Model saved.')

    def get_args(self):
        return vars(self)

    def update_args(self, args):
        for arg, value in args.items():
            vars(self)[arg] = value

    def predict_label(self, batch_top_k_index):
        """
        lookup all the labels basedon own labels and top K index
        """
        batch_top_k_index = batch_top_k_index.data.cpu().numpy()
        labels = []
        for pred in batch_top_k_index:
            labels.append([self.labels[idx] for idx in pred])

        return labels
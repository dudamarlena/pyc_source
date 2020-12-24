# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/naresh/Projects/embark/embark/tensorflow_classifier/mission_control.py
# Compiled at: 2020-02-03 18:42:05
# Size of source mod 2**32: 1806 bytes
import argparse

def str2bool(s):
    return s.lower() in ('true', '1', 'yes')


parser = argparse.ArgumentParser(description='Tensorflow Classification')
args = parser.add_argument_group('Dataset Parameters')
args.add_argument('--dataset_dir', type=str, default='./data', help='Directory containing data')
args = parser.add_argument_group('Training Parameters')
args.add_argument('--train', type=str2bool, default=True, help='Train or Test the model')
args.add_argument('--n_epochs', type=int, default=10, help='No. of iterations through the entire dataset')
args.add_argument('--save_model_iter', type=int, default=3, help='Saves model every nth epoch')
args.add_argument('--batch_size', type=int, default=8, help='No. of samples in each data batch')
args.add_argument('--init_lr', type=float, default=0.001, help='Initial learning rate used during training (this value might be decayed)')
args.add_argument('--train_patience', type=int, default=5, help='Number of epochs to wait before stopping train')
args.add_argument('--cuda_device', type=int, default=0, help='CUDA GPU to use')
args.add_argument('--model', type=str, choices=['resnet50', 'mobilenetv2'], default='mobilenetv2', help='Model to use')
args.add_argument('--n_classes', type=int, default=2, help='No. of classes')
args.add_argument('--model_checkpoint', type=str, default='', help='Load model checkpoints from this file')
args.add_argument('--results_dir', type=str, default='results', help='Directory in which to save model checkpoints')

def get_config():
    config, unparsed = parser.parse_known_args()
    return (config, unparsed)
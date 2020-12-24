# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/train_infer/train_infer_uncertainty.py
# Compiled at: 2020-04-15 21:24:26
# Size of source mod 2**32: 16625 bytes
from __future__ import print_function, division
import sys, time, scipy, torch, torchvision, torchvision.transforms as transforms, numpy as np, torch.nn as nn, torch.optim as optim, torch.nn.functional as F, matplotlib.pyplot as plt
from scipy import special
from datetime import datetime
from tensorboardX import SummaryWriter
from pymic.io.image_read_write import save_nd_array_as_image
from pymic.io.nifty_dataset import NiftyDataset
from pymic.io.transform3d import get_transform
from pymic.train_infer.net_factory import get_network
from pymic.train_infer.infer_func import volume_infer
from pymic.train_infer.train_infer import TrainInferAgent
from pymic.train_infer.loss import *
from pymic.train_infer.get_optimizer import get_optimiser
from pymic.util.image_process import convert_label
from pymic.util.parse_config import parse_config

class TrainInferAgentUncertainty(TrainInferAgent):

    def __init__(self, config, stage='train'):
        super(TrainInferAgentUncertainty, self).__init__(config, stage)

    def train(self):
        device = torch.device(self.config['training']['device_name'])
        self.net.to(device)
        summ_writer = SummaryWriter(self.config['training']['summary_dir'])
        multi_pred_weight = self.config['training']['multi_pred_weight']
        chpt_prefx = self.config['training']['checkpoint_prefix']
        loss_func = self.config['training']['loss_function']
        uncertain_reg_wht = self.config['training']['uncertain_reg_wht']
        iter_start = self.config['training']['iter_start']
        iter_max = self.config['training']['iter_max']
        iter_valid = self.config['training']['iter_valid']
        iter_save = self.config['training']['iter_save']
        class_num = self.config['network']['class_num']
        if iter_start > 0:
            checkpoint_file = '{0:}_{1:}.pt'.format(chpt_prefx, iter_start)
            self.checkpoint = torch.load(checkpoint_file)
            assert self.checkpoint['iteration'] == iter_start
            self.net.load_state_dict(self.checkpoint['model_state_dict'])
        else:
            self.checkpoint = None
        self.create_optimizer()
        train_loss = 0
        train_dice_list = []
        loss_obj = SegmentationLossCalculator(loss_func, multi_pred_weight)
        loss_obj.set_uncertainty_dice_loss_reg_weight(uncertain_reg_wht)
        trainIter = iter(self.train_loader)
        print('{0:} training start'.format(str(datetime.now())[:-7]))
        for it in range(iter_start, iter_max):
            try:
                data = next(trainIter)
            except StopIteration:
                trainIter = iter(self.train_loader)
                data = next(trainIter)

            inputs = self.convert_tensor_type(data['image'])
            labels_prob = self.convert_tensor_type(data['label_prob'])
            inputs, labels_prob = inputs.to(device), labels_prob.to(device)
            self.optimizer.zero_grad()
            self.schedule.step()
            outputs = self.net(inputs)
            loss_input_dict = {'prediction':outputs,  'ground_truth':labels_prob}
            gumb_list = []
            for n in range(4):
                gumb_n = np.random.gumbel(size=(list(labels_prob.shape)))
                gumb_n = torch.from_numpy(gumb_n).to(device)
                gumb_list.append(gumb_n)

            loss_input_dict['label_distance'] = gumb_list
            loss = loss_obj.get_loss(loss_input_dict)
            loss.backward()
            self.optimizer.step()
            if isinstance(outputs, tuple) or isinstance(outputs, list):
                outputs = outputs[0]
            outputs_argmax = torch.argmax(outputs, dim=1, keepdim=True)
            soft_out = get_soft_label(outputs_argmax, class_num)
            soft_out, labels_prob = reshape_prediction_and_ground_truth(soft_out, labels_prob)
            dice_list = get_classwise_dice(soft_out, labels_prob)
            train_dice_list.append(dice_list.cpu().numpy())
            train_loss = train_loss + loss.item()
            if it % iter_valid == iter_valid - 1:
                train_avg_loss = train_loss / iter_valid
                train_cls_dice = np.asarray(train_dice_list).mean(axis=0)
                train_avg_dice = train_cls_dice.mean()
                train_loss = 0.0
                train_dice_list = []
                valid_loss = 0.0
                valid_dice_list = []
                with torch.no_grad():
                    for data in self.valid_loader:
                        inputs = self.convert_tensor_type(data['image'])
                        labels_prob = self.convert_tensor_type(data['label_prob'])
                        inputs, labels_prob = inputs.to(device), labels_prob.to(device)
                        outputs = self.net(inputs)
                        loss_input_dict = {'prediction':outputs,  'ground_truth':labels_prob}
                        gumb_list = []
                        for n in range(4):
                            gumb_n = np.random.gumbel(size=(list(labels_prob.shape)))
                            gumb_n = torch.from_numpy(gumb_n).to(device)
                            gumb_list.append(gumb_n)

                        loss_input_dict['label_distance'] = gumb_list
                        loss = loss_obj.get_loss(loss_input_dict)
                        valid_loss = valid_loss + loss.item()
                        if isinstance(outputs, tuple) or isinstance(outputs, list):
                            outputs = outputs[0]
                        outputs_argmax = torch.argmax(outputs, dim=1, keepdim=True)
                        soft_out = get_soft_label(outputs_argmax, class_num)
                        soft_out, labels_prob = reshape_prediction_and_ground_truth(soft_out, labels_prob)
                        dice_list = get_classwise_dice(soft_out, labels_prob)
                        valid_dice_list.append(dice_list.cpu().numpy())

                valid_avg_loss = valid_loss / len(self.valid_loader)
                valid_cls_dice = np.asarray(valid_dice_list).mean(axis=0)
                valid_avg_dice = valid_cls_dice.mean()
                loss_scalers = {'train':train_avg_loss,  'valid':valid_avg_loss}
                summ_writer.add_scalars('loss', loss_scalers, it + 1)
                dice_scalers = {'train':train_avg_dice,  'valid':valid_avg_dice}
                summ_writer.add_scalars('class_avg_dice', dice_scalers, it + 1)
                print('train cls dice', train_cls_dice.shape, train_cls_dice)
                print('valid cls dice', valid_cls_dice.shape, valid_cls_dice)
                for c in range(class_num):
                    dice_scalars = {'train':train_cls_dice[c], 
                     'valid':valid_cls_dice[c]}
                    summ_writer.add_scalars('class_{0:}_dice'.format(c), dice_scalars, it + 1)

                print('{0:} it {1:}, loss {2:.4f}, {3:.4f}'.format(str(datetime.now())[:-7], it + 1, train_avg_loss, valid_avg_loss))
            if it % iter_save == iter_save - 1:
                save_dict = {'iteration':it + 1, 
                 'model_state_dict':self.net.state_dict(), 
                 'optimizer_state_dict':self.optimizer.state_dict()}
                save_name = '{0:}_{1:}.pt'.format(chpt_prefx, it + 1)
                torch.save(save_dict, save_name)

        summ_writer.close()

    def infer(self):
        device = torch.device(self.config['testing']['device_name'])
        self.net.to(device)
        self.checkpoint = torch.load((self.config['testing']['checkpoint_name']), map_location=device)
        self.net.load_state_dict(self.checkpoint['model_state_dict'])
        if self.config['testing']['evaluation_mode'] == True:
            self.net.eval()
            if self.config['testing']['test_time_dropout'] == True:

                def test_time_dropout(m):
                    if type(m) == nn.Dropout:
                        print('dropout layer')
                        m.train()

                self.net.apply(test_time_dropout)
        output_dir = self.config['testing']['output_dir']
        output_num = self.config['testing']['output_num']
        multi_pred_avg = self.config['testing']['multi_pred_avg']
        save_probability = self.config['testing']['save_probability']
        label_source = self.config['testing'].get('label_source', None)
        label_target = self.config['testing'].get('label_target', None)
        class_num = self.config['network']['class_num']
        mini_batch_size = self.config['testing']['mini_batch_size']
        mini_patch_inshape = self.config['testing']['mini_patch_input_shape']
        mini_patch_outshape = self.config['testing']['mini_patch_output_shape']
        mini_patch_stride = self.config['testing']['mini_patch_stride']
        filename_replace_source = self.config['testing']['filename_replace_source']
        filename_replace_target = self.config['testing']['filename_replace_target']
        infer_time_list = []
        with torch.no_grad():
            for data in self.test_loder:
                images = self.convert_tensor_type(data['image'])
                names = data['names']
                print(names[0])
                start_time = time.time()
                data['predict'] = volume_infer(images, self.net, device, class_num, mini_batch_size, mini_patch_inshape, mini_patch_outshape, mini_patch_stride, output_num)
                for i in reversed(range(len(self.transform_list))):
                    if self.transform_list[i].inverse:
                        data = self.transform_list[i].inverse_transform_for_prediction(data)

                predict_list = [
                 data['predict']]
                if isinstance(data['predict'], tuple) or isinstance(data['predict'], list):
                    predict_list = data['predict']
                pred_n = len(predict_list)
                print('predict number', pred_n)
                uncertain_list = []
                output_list = []
                for n in range(pred_n):
                    predict = predict_list[n][0]
                    print('predict shape', predict.shape)
                    alpha = np.exp(predict)
                    av0 = np.sum(alpha, axis=0)
                    alpha_sq = np.square(alpha)
                    avq = np.sum(alpha_sq, axis=0)
                    uncertain = (av0 * av0 - avq) / (av0 * av0 * (1.0 + av0))
                    uncertain_list.append(uncertain)
                    output_list.append(predict_list[n][0])

                if multi_pred_avg:
                    uncertain = np.asarray(uncertain_list)
                    uncertain = np.mean(uncertain, axis=0)
                    output = np.asarray(output_list)
                    output = np.mean(output, axis=0)
                    output = np.asarray(np.argmax(output, axis=0), np.uint8)
                    prob_list = [scipy.special.softmax(item, axis=0)[1] for item in output_list]
                    prob_list = np.asarray(prob_list)
                    uncertain_esb = np.var(prob_list, axis=0)
                else:
                    uncertain = uncertain_list[0]
                    output = np.argmax((output_list[0]), axis=0)
                    print('output shape', output.shape)
                infer_time = time.time() - start_time
                infer_time_list.append(infer_time)
                if label_source is not None:
                    if label_target is not None:
                        output = convert_label(output, label_source, label_target)
                    root_dir = self.config['dataset']['root_dir']
                    save_name = names[0].split('/')[(-1)]
                    if filename_replace_source is not None:
                        if filename_replace_target is not None:
                            save_name = save_name.replace(filename_replace_source, filename_replace_target)
                    save_full_name = '{0:}/{1:}'.format(output_dir, save_name)
                    save_nd_array_as_image(output, save_full_name, root_dir + '/' + names[0])
                    if save_probability:
                        save_name_split = save_name.split('.')
                        if '.nii.gz' in save_name:
                            save_prefix = '.'.join(save_name_split[:-2])
                            save_format = 'nii.gz'
                        else:
                            save_prefix = '.'.join(save_name_split[:-1])
                            save_format = save_name_split[(-1)]
                        save_full_name = '{0:}_uncertain/{1:}'.format(output_dir, save_name)
                        save_nd_array_as_image(uncertain, save_full_name, root_dir + '/' + names[0])
                        if multi_pred_avg:
                            save_full_name = '{0:}_uncertain_esb/{1:}'.format(output_dir, save_name)
                            save_nd_array_as_image(uncertain_esb, save_full_name, root_dir + '/' + names[0])

        infer_time_list = np.asarray(infer_time_list)
        time_avg = infer_time_list.mean()
        time_std = infer_time_list.std()
        print('testing time {0:} +/- {1:}'.format(time_avg, time_std))

    def run(self):
        self.create_dataset()
        self.create_network()
        if self.stage == 'train':
            self.train()
        else:
            self.infer()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Number of arguments should be 3. e.g.')
        print('    python train_infer.py train config.cfg')
        exit()
    stage = str(sys.argv[1])
    cfg_file = str(sys.argv[2])
    config = parse_config(cfg_file)
    agent = TrainInferAgentUncertainty(config, stage)
    agent.run()
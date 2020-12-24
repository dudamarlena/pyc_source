# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\segmentation_api\evaluator.py
# Compiled at: 2019-04-03 09:00:19
# Size of source mod 2**32: 11425 bytes
"""
Module responsible for evaluating model
calculation seweral parameters
recall

"""
import glob, itertools, json, os
from collections import Counter
import numpy as np, pandas as pd, PIL.Image as Image
from sklearn.metrics import accuracy_score, auc, confusion_matrix, precision_score, recall_score, roc_curve
from tqdm import tqdm, trange
import cv2
from segmentation_module.segmentation_tools.eval_tools import _read_imgs_to_numpy, check_for_missing_class, check_for_missing_class2d, convert_dict_key, extract_both_masks, extract_classes, extract_masks, prepare_column_list
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir

class Evaluator(object):

    def __init__(self, config, logger):
        self.config_eval = config
        self.logger = logger
        self.logger.log_message('EVALUATION STARTED')

    def load_data(self, predictions_folder_path, labels_folder_path):
        self.pred_img = _read_imgs_to_numpy(get_photos_from_dir(predictions_folder_path))
        self.labels_img = _read_imgs_to_numpy(get_photos_from_dir(labels_folder_path))

    def _prepare_data(self):
        """Prepare prediction and label data to evaluate
        Prepares dataframe to write
        
        :return: [description]
        :rtype: [np.array flatten labels and predictions]
        """
        label_list = self.config_eval['label_list']
        if len(self.pred_img) == len(self.labels_img):
            labels_img = self.labels_img.copy()
            pred_img = self.pred_img.copy()
            self.labels_flatten = labels_img.reshape(labels_img.shape[0], -1).T
            self.pred_flatten = pred_img.reshape(pred_img.shape[0], -1).T
            self.evaluate_table = pd.DataFrame(data={}, index=label_list)
            return (
             self.labels_flatten, self.pred_flatten, labels_img, pred_img)
        print("Labels number don't match predictions")

    def _calculate_metrics(self, label, predict, metrics_type='recall'):
        label_list = self.config_eval['label_list']
        n_classes = len(label_list)
        if metrics_type == 'precision':
            single_precision = precision_score(label, predict, average=None)
            single_precision = check_for_missing_class(single_precision, n_classes)
            single_precision = single_precision.reshape((n_classes, 1))
            return single_precision
        if metrics_type == 'recall':
            single_recall = recall_score(label, predict, average=None)
            single_recall = check_for_missing_class(single_recall, n_classes)
            single_recall = single_recall.reshape((n_classes, 1))
            return single_recall

    def calculate_mean_precision_recall(self):
        label_list = self.config_eval['label_list']
        n_classes = len(label_list)
        labels_flatten = self.labels_flatten.copy()
        pred_flatten = self.pred_flatten.copy()
        m = labels_flatten.shape[1]
        preci_sum = np.zeros((n_classes, 1))
        recall_sum = np.zeros((n_classes, 1))
        curr_prec = np.zeros((n_classes, 1))
        curr_recal = np.zeros((n_classes, 1))
        for i in range(m):
            curr_prec = self._calculate_metrics(labels_flatten[:, i], pred_flatten[:, i], 'precision')
            preci_sum += curr_prec
            curr_recal = self._calculate_metrics(labels_flatten[:, i], pred_flatten[:, i], 'recall')
            recall_sum += curr_recal

        mean_preci = np.divide(preci_sum, m).reshape(n_classes)
        mean_recall = np.divide(recall_sum, m).reshape(n_classes)
        mean_F1_score = 2 * np.divide(np.multiply(mean_preci, mean_recall), np.add(mean_preci, mean_recall))
        self.evaluate_table['mean_recall'] = pd.Series(data=(mean_recall.tolist()), index=label_list)
        self.evaluate_table['mean_precision'] = pd.Series(data=(mean_preci.tolist()), index=label_list)
        self.evaluate_table['mean_F1_score'] = pd.Series(data=(mean_F1_score.tolist()), index=label_list)

    def _class_pixel_accuracy(self, predict_img, label_img):
        """
        number of pixels classyfied as class i (sum_n_ii) /  total number of pixels of class i (sum_t_i)
        """
        classes, n_classes = extract_classes(label_img)
        predict_mask, label_mask = extract_both_masks(predict_img, label_img, classes, n_classes)
        sum_n_ii = 0
        sum_t_i = 0
        pixel_accuracy_ = {}
        for i, c in tqdm(enumerate(classes)):
            curr_pred_mask = predict_mask[:, :, i]
            curr_label_mask = label_mask[:, :, i]
            sum_n_ii += np.sum(np.logical_and(curr_pred_mask, curr_label_mask))
            sum_t_i += np.sum(curr_label_mask)
            if sum_t_i == 0:
                pixel_accuracy_[c] = 0
            else:
                pixel_accuracy_[c] = sum_n_ii / sum_t_i

        return pixel_accuracy_

    def get_mean_values(self, class_sum, n_img):
        clase_mean = {}
        for key, value in class_sum.items():
            clase_mean[key] = value / n_img

        return clase_mean

    def calculate_mean_pixel_accuracy(self):
        """number of pixels classyfied as class i (sum_n_ii) /  total number of pixels of class i (sum_t_i)
        
        :param filename: [description]
        :type filename: [type]
        """
        label_list = self.config_eval['label_list']
        classes = dict([(a, 0) for a in range(len(self.config_eval['label_list']))])
        labels_imgs = self.labels_img.copy()
        pred_imgs = self.pred_img.copy()
        pixel_acc_summ = Counter(classes)
        m = labels_imgs.shape[0]
        mean_pixel_acc = {}
        for lab, pred in tqdm(zip(labels_imgs, pred_imgs)):
            temp_acc = self._class_pixel_accuracy(pred, lab)
            temp_counter = Counter(temp_acc)
            pixel_acc_summ += temp_counter
            mean_pixel_acc = self.get_mean_values(dict(pixel_acc_summ), m)

        self.evaluate_table['mean_pixel_accuracy'] = pd.Series(data=(list(mean_pixel_acc.values())), index=label_list)
        return mean_pixel_acc

    def iou_for_classes(self, label_img, predict_img):
        classes, n_classes = extract_classes(label_img)
        predict_mask, label_mask = extract_both_masks(predict_img, label_img, classes, n_classes)
        iou_score = {}
        for i, c in tqdm(enumerate(classes)):
            curr_pred_mask = predict_mask[:, :, i]
            curr_label_mask = label_mask[:, :, i]
            intersection = np.logical_and(curr_label_mask, curr_pred_mask)
            union = np.logical_or(curr_label_mask, curr_pred_mask)
            iou_score[c] = np.sum(intersection) / np.sum(union)

        return iou_score

    def calculate_mean_iou(self):
        label_list = self.config_eval['label_list']
        classes = dict([(a, 0) for a in range(len(self.config_eval['label_list']))])
        iou_summ = Counter(classes)
        labels_imgs = self.labels_img.copy()
        pred_imgs = self.pred_img.copy()
        m = labels_imgs.shape[0]
        for lab, pred in tqdm(zip(labels_imgs, pred_imgs)):
            temp_iou = Counter(self.iou_for_classes(lab, pred))
            iou_summ += temp_iou

        iou_mean = self.get_mean_values(iou_summ, m)
        self.evaluate_table['mean_iou'] = pd.Series(data=(list(iou_mean.values())), index=label_list)
        return iou_mean

    def calculate_confusion_matrix(self):
        label_list = self.config_eval['label_list']
        n_classes = len(label_list)
        labels_flatten = self.labels_flatten.copy()
        pred_flatten = self.pred_flatten.copy()
        columns_list = prepare_column_list(label_list)
        m = labels_flatten.shape[1]
        conf_sum = np.zeros((n_classes, n_classes))
        curr_matrix = np.zeros((n_classes, n_classes))
        for i in range(0, m):
            curr_matrix = check_for_missing_class2d(confusion_matrix(labels_flatten[:, i], pred_flatten[:, i]), n_classes)
            conf_sum += curr_matrix

        mean_matrix = np.divide(conf_sum, m)
        df_con_mat = pd.DataFrame(mean_matrix, index=label_list, columns=columns_list)
        self.mistake_matrix = self.calculate_prediction_mistake(df_con_mat)
        return self.mistake_matrix

    def calculate_mean_metrics(self):
        mean_metrics = self.evaluate_table.mean(axis=0)
        self.evaluate_table.loc['Mean'] = mean_metrics

    def calculate_prediction_mistake(self, conf_matrix):
        class_prediction_sum = conf_matrix.sum(axis=0)
        mistake_matrix_prec_class = conf_matrix.div(class_prediction_sum, axis='columns')
        return mistake_matrix_prec_class

    def calculate_evaluation_metrics(self):
        self._prepare_data()
        self.calculate_mean_precision_recall()
        self.calculate_mean_pixel_accuracy()
        self.calculate_mean_iou()
        self.calculate_confusion_matrix()
        self.calculate_mean_metrics()

    def save_evaluation_table(self):
        save_path = self.config_eval['eval_result_save_path']
        self.evaluate_table.to_csv((os.path.join(save_path, 'evaluation_result.csv')), float_format='%.3f', sep=',')
        self.mistake_matrix.to_csv((os.path.join(save_path, 'mistake_matrix.csv')), float_format='%.3f', sep=',')
        self.logger.log_message('Evaluation files saved successfully.')
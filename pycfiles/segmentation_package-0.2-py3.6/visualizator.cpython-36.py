# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\segmentation_api\visualizator.py
# Compiled at: 2019-03-20 06:50:54
# Size of source mod 2**32: 6361 bytes
import json, os, matplotlib.pyplot as plt, numpy as np
from PIL import Image
from tqdm import tqdm
import cv2
from segmentation_module.segmentation_api.api_object import APIObject
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir, prepare_folder_in_directory
from segmentation_module.segmentation_tools.segmentation_tools import save_any_img, raw_2_blob

class Visualizator(APIObject):

    def __init__(self, config_path, logger):
        super().__init__(config_path)
        self.logger = logger
        self.logger.log_message('VISULIZATION STARTED')

    def save_visualizations(self, filenames, visualizations, output_folder, model_name):
        vis_output_path = os.path.join(output_folder, 'visualizations')
        if not os.path.exists(vis_output_path):
            os.makedirs(vis_output_path)
        for filename, visualization in zip(filenames, visualizations):
            new_img_name = os.path.splitext(os.path.basename(filename))[0] + '_' + model_name + '_vis.jpg'
            new_path = os.path.join(vis_output_path, new_img_name)
            save_any_img(visualization, new_path)

    def visualize(self, images, predictions, transparent_ratio=0.4):
        output_visualizations = []
        for image, pred in tqdm(zip(images, predictions)):
            out_vis = self._visualize_image(image, pred, transparent_ratio)
            output_visualizations.append(out_vis)

        return np.asarray(output_visualizations)

    def visualize_folder(self, original_img_path, prediction_path, output_vis_path, only_to_memory, transparent_ratio=0.6):
        """
        Visualize predictions

        :transparent_ratio:  weight of label color on top of original image 
        """
        output_path = prepare_folder_in_directory(output_vis_path, 'predictions_vis')
        org_images = get_photos_from_dir(original_img_path)
        pred_labels = get_photos_from_dir(prediction_path)
        for img_path, pred_img_path in tqdm(zip(org_images, pred_labels)):
            org_img = np.asarray(Image.open(img_path))
            pred_img = np.asarray(Image.open(pred_img_path))
            out_vis = self._visualize_image(org_img, pred_img, transparent_ratio)
            vis_image_path = os.path.join(output_path, 'vis_' + os.path.basename(img_path))
            save_any_img(out_vis, vis_image_path)

    def visualize_single_image(self, img_path, pred_img_path, output_vis_path, only_to_memory, transparent_ratio):
        org_img = np.asarray(Image.open(img_path))
        pred_img = pred_img_path
        vis_result = self._visualize_image(org_img, pred_img, transparent_ratio)
        return vis_result

    def visualize_image_loaded(self, org_img, pred_img, transparent_ratio, mode):
        vis_result = self._visualize_image(org_img, pred_img, transparent_ratio)
        return vis_result

    def _visualize_image(self, org_img, pred_img, transparent_ratio):
        output_height, output_width = org_img.shape[0], org_img.shape[1]
        org_img = cv2.resize(org_img, (512, 512))
        out_vis = self._draw_labels(org_img, pred_img, transparent_ratio, False)
        return out_vis

    def _draw_labels(self, img, labels, transparent_ratio=0.8, convert=False):
        """
        Draw the labels on top of the input image for wisualisation
        :param img:          the image being classified
        :param labels:       the output of the neural network
        :param label_colors: the label color list
        :param convert:      should the output be converted to RGB
        """
        if self.config_parameters['prediction_methood'] == 'raw':
            labels = raw_2_blob(labels, self.config_colors)
        labels_colored = cv2.resize(labels, (img.shape[1], img.shape[0]))
        img = np.asarray(img, np.uint8)
        labels_colored = np.asarray(labels_colored, np.uint8)
        img = cv2.addWeighted(img, 1, labels_colored, transparent_ratio, 0)
        return img
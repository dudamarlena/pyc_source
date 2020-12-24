# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_binary_classification_data.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 10538 bytes
import json, os
from collections import OrderedDict
import numpy as np, rasterio
from rasterio import features
from iobjectspy import Rectangle, clip
from iobjectspy.ml.toolkit._create_training_data_util import get_tile_start_index, _get_input_feature, _save_img
from iobjectspy.ml.toolkit._toolkit import save_pattle_png, save_config_to_yaml

class CreateBinaryClassificationData(object):

    def __init__(self, input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False):
        self.input_data = input_data
        self.input_label = input_label
        self.label_class_field = label_class_field
        self.output_path = output_path
        self.output_name = output_name
        self.training_data_format = training_data_format
        self.tile_format = tile_format
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.tile_offset_x = tile_offset_x
        self.tile_offset_y = tile_offset_y
        self.tile_start_index = tile_start_index
        self.save_nolabel_tiles = save_nolabel_tiles

    def create_binary_classification(self):
        out_binary_sda = os.path.join(self.output_path, self.output_name, self.output_name + '.sda')
        output_path_images = os.path.join(self.output_path, self.output_name, 'Images')
        output_path_masks = os.path.join(self.output_path, self.output_name, 'Masks')
        if not os.path.exists(output_path_images):
            os.makedirs(output_path_images)
        else:
            if not os.path.exists(output_path_masks):
                os.makedirs(output_path_masks)
            temp_tile_index = get_tile_start_index(self.tile_start_index, out_binary_sda)
            temp_input_label = _get_input_feature(self.input_label)
            bounds = self.input_label.bounds
            categorys = [
             'background']
            if self.label_class_field == None:
                categorys.append('unspecified')
            else:
                for dlmc in temp_input_label:
                    category = dlmc.get_value(self.label_class_field)
                    if category not in categorys:
                        categorys.append(category)

        for category in categorys:
            if category != 'background':
                positive_e_category = category

        categorys_dict = {}
        categorys_dict[positive_e_category] = 0
        categorys_count = {}
        categorys_count['background'] = 0
        categorys_count[positive_e_category] = 0
        with rasterio.open(self.input_data) as (ds):
            transf = ds.transform
            ymin, xmax = rasterio.transform.rowcol(transf, bounds.right, bounds.top)
            ymax, xmin = rasterio.transform.rowcol(transf, bounds.left, bounds.bottom)
            x_pixel_res = (bounds.right - bounds.left) / (xmax - xmin)
            y_pixel_res = (bounds.top - bounds.bottom) / (ymax - ymin)
            geo_tile_size_x = self.tile_size_x * x_pixel_res
            geo_tile_size_y = self.tile_size_y * y_pixel_res
            if ds.bounds.right > bounds.right:
                bounds_right = bounds.right
            else:
                bounds_right = ds.bounds.right
            if ds.bounds.left > bounds.left:
                bounds_left = ds.bounds.left
            else:
                bounds_left = bounds.left
            if ds.bounds.top > bounds.top:
                bounds_top = bounds.top
            else:
                bounds_top = ds.bounds.top
            if ds.bounds.bottom > bounds.bottom:
                bounds_bottom = ds.bounds.bottom
            else:
                bounds_bottom = bounds.bottom
            geo_width_size = bounds_right - bounds_left
            get_height_size = bounds_top - bounds_bottom
            geo_width_block_num = int(geo_width_size / geo_tile_size_x)
            geo_height_block_num = int(get_height_size / geo_tile_size_y)
            for i in range(geo_height_block_num):
                for j in range(geo_width_block_num):
                    geo_block_left = bounds_left + j * geo_tile_size_x
                    geo_block_top = bounds_top - i * geo_tile_size_y
                    block_ymin, block_xmin = rasterio.transform.rowcol(transf, geo_block_left, geo_block_top)
                    tile_box = Rectangle(geo_block_left, geo_block_top, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                    recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                    if recordset.get_geometry() != None:
                        transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                        feature_list = []
                        for feature in recordset.get_features():
                            clip_geometry = clip(feature.geometry, tile_box)
                            if clip_geometry != None:
                                feature_geojson = json.loads(clip_geometry.to_geojson())
                                feature_list.append((feature_geojson, 1))

                        if len(feature_list) > 0:
                            temp_tile_index, positive_e_pixel_count, negative_e_pixel_count = self._save_images_labels(ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index, output_path_images, output_path_masks)
                            categorys_count['background'] = categorys_count['background'] + negative_e_pixel_count
                            categorys_count[positive_e_category] = categorys_count[positive_e_category] + positive_e_pixel_count

            list = []
            negative_e_count = int(categorys_count['background'])
            positive_e_count = int(categorys_count[positive_e_category])
            positive_e_dict = OrderedDict({'class_name':'background',  'class_value':0, 
             'pixel_count':negative_e_count,  'class_color':(0, 0, 0)})
            negative_e_dict = OrderedDict({'class_name':positive_e_category,  'class_value':1, 
             'pixel_count':positive_e_count,  'class_color':(255, 0, 0)})
            list.append(positive_e_dict)
            list.append(negative_e_dict)
            if self.tile_format == 'jpg':
                x_ext = self.tile_format
            else:
                if self.tile_format == 'png':
                    x_ext = self.tile_format
                else:
                    if self.tile_format == 'tif':
                        x_ext = self.tile_format
                    else:
                        if self.tile_format == 'origin':
                            x_ext = os.path.splitext(self.input_data)[(-1)][1:]
                        dic_binary_sda = OrderedDict({'dataset': OrderedDict({'name':'example_bc',  'data_type':'binary_classifition', 
                                     'x_bandnum':ds.count, 
                                     'x_ext':x_ext,  'x_type':ds.dtypes[0], 
                                     'y_bandnum':1,  'y_ext':'png',  'y_type':rasterio.uint8, 
                                     'tile_size':self.tile_size_x,  'image_mean':[
                                      115.6545965, 117.62014299, 106.01483799], 
                                     'image_std':[
                                      56.82521775, 53.46318049, 56.07113724], 
                                     'image_count':temp_tile_index, 
                                     'class_type':list})})
                        save_config_to_yaml(dic_binary_sda, out_binary_sda)

    def _save_images_labels(self, ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index, output_path_images, output_path_masks):
        start_index_string = str(temp_tile_index).zfill(8)
        _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_images, start_index_string), transf_tile, self.input_data)
        positive_e_pixel_count, negative_e_pixel_count = self._save_masks(feature_list, transf_tile, os.path.join(output_path_masks, start_index_string) + '.' + 'png')
        temp_tile_index = temp_tile_index + 1
        return (
         temp_tile_index, positive_e_pixel_count, negative_e_pixel_count)

    def _save_masks(self, feature_list, transf_tile, output_path_masks):
        image = features.rasterize(((g, 1) for g, v in feature_list), out_shape=(self.tile_size_y, self.tile_size_x), transform=transf_tile)
        positive_e_pixel_count = np.sum(image == 1)
        negative_e_pixel_count = np.sum(image == 0)
        color_codes = {(0, 0, 0):0, 
         (255, 0, 0):1}
        save_pattle_png(image, color_codes, output_path_masks)
        return (
         positive_e_pixel_count, negative_e_pixel_count)
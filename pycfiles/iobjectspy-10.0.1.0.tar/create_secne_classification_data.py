# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_secne_classification_data.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 9659 bytes
import csv, os
from collections import OrderedDict
import rasterio
from iobjectspy import Rectangle, clip
from iobjectspy.ml.toolkit._create_training_data_util import get_tile_start_index, _get_input_feature, _save_img
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml

class CreateSceneClassificationData(object):

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

    def create_scene_classification(self):
        out_secne_sda = os.path.join(self.output_path, self.output_name, self.output_name + '.sda')
        out_scene_csv = os.path.join(self.output_path, self.output_name, 'scene_classification.csv')
        temp_tile_index = get_tile_start_index(self.tile_start_index, out_secne_sda)
        temp_input_label = _get_input_feature(self.input_label)
        dom_bounds = self.input_label.bounds
        categorys = []
        for dlmc in temp_input_label:
            category = dlmc.get_value(self.label_class_field)
            if category not in categorys:
                categorys.append(category)

        categorys_dict = {}
        id_category = 0
        for category in categorys:
            categorys_dict[category] = id_category
            id_category = id_category + 1

        categorys_count = {}
        for category in categorys:
            categorys_count[category] = 0

        for category in categorys:
            output_path = os.path.join(self.output_path, self.output_name, str(categorys_dict[category]))
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        with rasterio.open(self.input_data) as (ds):
            transf = ds.transform
            ymin, xmax = rasterio.transform.rowcol(transf, dom_bounds.right, dom_bounds.top)
            ymax, xmin = rasterio.transform.rowcol(transf, dom_bounds.left, dom_bounds.bottom)
            x_pixel_res = (dom_bounds.right - dom_bounds.left) / (xmax - xmin)
            y_pixel_res = (dom_bounds.top - dom_bounds.bottom) / (ymax - ymin)
            geo_tile_size_x = self.tile_size_x * x_pixel_res
            geo_tile_size_y = self.tile_size_y * y_pixel_res
            with open(out_scene_csv, 'w', newline='', encoding='utf8') as (f):
                geo_width_block_num = int((self.input_label.bounds.right - self.input_label.bounds.left) / geo_tile_size_x) + 1
                geo_height_block_num = int((self.input_label.bounds.top - self.input_label.bounds.bottom) / geo_tile_size_y) + 1
                for i in range(geo_height_block_num):
                    for j in range(geo_width_block_num):
                        geo_block_left = self.input_label.bounds.left + j * geo_tile_size_x
                        geo_block_top = self.input_label.bounds.top - i * geo_tile_size_y
                        tile_box = Rectangle(geo_block_left, geo_block_top, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            dict_categorys = {'category': 0}
                            for feature in recordset.get_features():
                                if clip(feature.geometry, tile_box) != None:
                                    category = feature.get_value(self.label_class_field)
                                    try:
                                        dict_categorys[category] = dict_categorys[category] + clip(tile_box, feature.geometry).area
                                    except:
                                        dict_categorys.update({category: clip(tile_box, feature.geometry).area})

                            del dict_categorys['category']
                            for dict_category in dict_categorys:
                                if dict_categorys[dict_category] > 0.5 * (tile_box.height * tile_box.width):
                                    block_ymin, block_xmin = rasterio.transform.rowcol(transf, geo_block_left, geo_block_top)
                                    category = dict_category
                                    start_index_string = str(temp_tile_index).zfill(8)
                                    temp_tile_index = temp_tile_index + 1
                                    output_path = os.path.join(self.output_path, self.output_name, str(categorys_dict[category]), start_index_string)
                                    transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                                    _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, output_path, transf_tile, self.input_data)
                                    categorys_count[category] = categorys_count[category] + 1
                                    id_category = id_category + 1
                                    if self.tile_format == 'origin':
                                        relative_output_path = './' + str(categorys_dict[category]) + '/' + start_index_string + os.path.splitext(self.input_data)[(-1)]
                                    else:
                                        relative_output_path = './' + str(categorys_dict[category]) + '/' + start_index_string + '.' + self.tile_format
                                    list = []
                                    list.append(relative_output_path)
                                    list.append(category)
                                    list.append(categorys_dict[category])
                                    f_csv = csv.writer(f)
                                    f_csv.writerow(list)

            list = []
            for key in categorys_count:
                list.append({'class_name':key,  'class_id':categorys_dict[key], 
                 'image_count':categorys_count[key]})

            dic_scene_sda = OrderedDict({'dataset': OrderedDict({'name':'example_scene',  'data_type':'scene_classification', 
                         'x_bandnum':ds.count, 
                         'x_ext':self.input_data.split('.')[-1],  'x_type':ds.dtypes[0], 
                         'tile_size':self.tile_size_y,  'image_mean':[
                          115.6545965, 117.62014299, 106.01483799], 
                         'image_std':[
                          56.82521775, 53.46318049, 56.07113724], 
                         'image_list':'scene_classification.csv', 
                         'class_type':list})})
            save_config_to_yaml(dic_scene_sda, out_secne_sda)
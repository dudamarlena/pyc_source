# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_multi_classification_data.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 16008 bytes
import colorsys, json, os
from collections import OrderedDict
import numpy as np, rasterio
from rasterio import features
from iobjectspy import Rectangle, clip
from iobjectspy.ml.toolkit._create_training_data_util import get_tile_start_index, _get_input_feature, _save_img, _rgb, get_key
from iobjectspy.ml.toolkit._toolkit import save_pattle_png, save_config_to_yaml, get_config_from_yaml

class CreateMultiClassificationData(object):

    def __init__(self, input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False, **kwargs):
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
        self.kwargs = kwargs

    def create_multi_classification(self):
        out_multi_sda = os.path.join(self.output_path, self.output_name, self.output_name + '.sda')
        output_path_images = os.path.join(self.output_path, self.output_name, 'Images')
        output_path_masks = os.path.join(self.output_path, self.output_name, 'Masks')
        if not os.path.exists(output_path_images):
            os.makedirs(output_path_images)
        if not os.path.exists(output_path_masks):
            os.makedirs(output_path_masks)
        temp_tile_index = get_tile_start_index(self.tile_start_index, out_multi_sda)
        temp_input_label = _get_input_feature(self.input_label)
        bounds = self.input_label.bounds
        categorys = []
        try:
            config = get_config_from_yaml(out_multi_sda)
            for temp_class_type in config.get('dataset').get('class_type'):
                categorys.append(temp_class_type.get('class_name'))

        except:
            categorys.append('background')

        for dlmc in temp_input_label:
            category = dlmc.get_value(self.label_class_field)
            if category not in categorys:
                categorys.append(category)

        categorys_dict = {}
        color_codes_list = self._get_continuous_codes_list(254)
        color_codes = {}
        categorys_count = {}
        try:
            config = get_config_from_yaml(out_multi_sda)
            id_category = 0
            for temp_class_type in config.get('dataset').get('class_type'):
                categorys_dict[temp_class_type.get('class_name')] = temp_class_type.get('class_value')
                color_codes[tuple(temp_class_type.get('class_color'))] = temp_class_type.get('class_value')
                categorys_count[temp_class_type.get('class_value')] = int(temp_class_type.get('pixel_count'))
                id_category = id_category + 1

            for category in categorys:
                if category not in categorys_dict.keys():
                    categorys_dict[category] = id_category
                    color_codes[color_codes_list[id_category]] = categorys_dict[category]
                    categorys_count[categorys_dict[category]] = 0
                    id_category = id_category + 1

        except:
            categorys_dict['background'] = 0
            color_codes[(0, 0, 0)] = 0
            categorys_count[0] = 0
            id_category = 1
            for category in categorys:
                if category != 'background':
                    categorys_dict[category] = id_category
                    color_codes[color_codes_list[id_category]] = categorys_dict[category]
                    categorys_count[categorys_dict[category]] = 0
                    id_category = id_category + 1

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
                                feature_list.append((
                                 feature_geojson, categorys_dict[feature.get_value(self.label_class_field)]))

                        if len(feature_list) > 0:
                            temp_tile_index = self._save_images_labels(ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index, categorys_count, color_codes, output_path_images, output_path_masks)

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
                        list_class_type = []
                        for key in categorys:
                            list_class_type.append(OrderedDict({'class_name':key,  'class_value':categorys_dict[key], 
                             'pixel_count':int(categorys_count[categorys_dict[key]]), 
                             'class_color':get_key(color_codes, categorys_dict[key])[0]}))

                        dic_scene_sda = OrderedDict({'dataset': OrderedDict({'name':'example_mc',  'data_type':'multi_classification', 
                                     'x_bandnum':ds.count, 
                                     'x_ext':x_ext,  'x_type':ds.dtypes[0], 
                                     'y_bandnum':len(categorys_dict),  'y_ext':'png', 
                                     'y_type':rasterio.uint8, 
                                     'tile_size':self.tile_size_x,  'image_mean':[
                                      115.6545965, 117.62014299, 106.01483799], 
                                     'image_std':[
                                      56.82521775, 53.46318049, 56.07113724], 
                                     'image_count':temp_tile_index, 
                                     'class_type':list_class_type})})
                        save_config_to_yaml(dic_scene_sda, out_multi_sda)

    def _save_images_labels(self, ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index, categorys_count, color_codes, output_path_images, output_path_masks):
        start_index_string = str(temp_tile_index).zfill(8)
        _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_images, start_index_string), transf_tile, self.input_data)
        self._save_masks(feature_list, transf_tile, categorys_count, color_codes, os.path.join(output_path_masks, start_index_string) + '.' + 'png')
        temp_tile_index = temp_tile_index + 1
        return temp_tile_index

    def _save_masks(self, feature_list, transf_tile, categorys_count, color_codes, output_path_masks):
        image = features.rasterize(((g, v) for g, v in feature_list), out_shape=(self.tile_size_y, self.tile_size_x), transform=transf_tile)
        sum_count = sum(categorys_count.values())
        for feature in feature_list:
            categorys_count[feature[1]] = categorys_count[feature[1]] + np.sum(image == feature[1])

        categorys_count[0] = categorys_count[0] + np.sum(image == 0)
        save_pattle_png(image, color_codes, output_path_masks)

    def _get_continuous_codes_list(self, num_color=256):
        """
        从 dcf 文件中加载数据库连接信息，返回一个新的数据库连接信息对象。

        :param int num_color: 颜色表数量
        :return: color_continuous_codes_list 颜色表列表
        :type: list[tuple]

        """
        r, g, b = [v / 255 for v in _rgb('#ffffff')]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        color_continuous_codes_list = []
        for i in range(num_color):
            ns = 1 / num_color * (i + 1)
            color_continuous_codes_list.append(tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, ns, v)]))

        return list(set(color_continuous_codes_list))
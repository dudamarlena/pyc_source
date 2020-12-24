# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_object_detection_data.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 25682 bytes
import os
from collections import OrderedDict
import rasterio
from iobjectspy import Rectangle
from iobjectspy.ml.toolkit._create_training_data_util import _save_img, get_tile_start_index, _get_input_feature
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml

class CreateObjectDetectionData(object):

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

    def create_voc(self):
        output_path_img = os.path.join(self.output_path, self.output_name, 'Images')
        output_path_label = os.path.join(self.output_path, self.output_name, 'Annotations')
        output_path_main = os.path.join(self.output_path, self.output_name, 'ImageSets', 'Main')
        output_voc_sda = os.path.join(self.output_path, self.output_name, self.output_name + '.sda')
        if not os.path.exists(output_path_img):
            os.makedirs(output_path_img)
        if not os.path.exists(output_path_label):
            os.makedirs(output_path_label)
        if not os.path.exists(output_path_main):
            os.makedirs(output_path_main)
        temp_tile_index = get_tile_start_index(self.tile_start_index, output_voc_sda)
        with rasterio.open(self.input_data) as (ds):
            transf = ds.transform
            height = ds.height
            ymin, xmax = rasterio.transform.rowcol(transf, self.input_label.bounds.right, self.input_label.bounds.top)
            ymax, xmin = rasterio.transform.rowcol(transf, self.input_label.bounds.left, self.input_label.bounds.bottom)
            x_pixel_res = (self.input_label.bounds.right - self.input_label.bounds.left) / (xmax - xmin)
            y_pixel_res = (self.input_label.bounds.top - self.input_label.bounds.bottom) / (ymax - ymin)
            geo_tile_size_x = self.tile_size_x * x_pixel_res
            geo_tile_size_y = self.tile_size_y * y_pixel_res
            geo_tile_offset_x = self.tile_offset_x * x_pixel_res
            geo_tile_offset_y = self.tile_offset_y * y_pixel_res
            rectangle = Rectangle(self.input_label.bounds.right, self.input_label.bounds.top, self.input_label.bounds.left, self.input_label.bounds.bottom)
            geo_width_block_num = int((rectangle.right - rectangle.left) // geo_tile_size_x)
            geo_height_block_num = int((rectangle.top - rectangle.bottom) // geo_tile_size_y)
            for i in range(geo_height_block_num):
                for j in range(geo_width_block_num):
                    geo_block_left = rectangle.left + j * geo_tile_size_x
                    geo_block_top = rectangle.top - i * geo_tile_size_y
                    block_ymin, block_xmin = rasterio.transform.rowcol(transf, geo_block_left, geo_block_top)
                    tile_box = Rectangle(geo_block_left, geo_block_top, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                    recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                    if recordset.get_geometry() != None:
                        temp_input_label = recordset.get_features()
                        transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                        temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin, block_ymin, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)
                    if self.tile_offset_x != 0 and self.tile_offset_y != 0:
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top, geo_block_left + geo_tile_offset_x + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin + self.tile_offset_x, block_ymin, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)
                        tile_box = Rectangle(geo_block_left, geo_block_top - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin, block_ymin + self.tile_offset_y, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_offset_y, geo_block_left + geo_tile_offset_x + geo_tile_size_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin + self.tile_offset_x, block_ymin + self.tile_offset_y, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)
                    elif self.tile_offset_x != 0 and self.tile_offset_y == 0:
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top, geo_block_left + geo_tile_offset_x + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin + self.tile_offset_x, block_ymin, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)
                    elif self.tile_offset_x == 0 and self.tile_offset_y != 0:
                        tile_box = Rectangle(geo_block_left, geo_block_top + geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y + geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin, block_ymin + self.tile_offset_y, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label)

            temp_input_label = _get_input_feature(self.input_label)
            categorys = [
             '__background__']
            if self.label_class_field == None:
                categorys.append('unspecified')
            else:
                for i in temp_input_label:
                    category = i.get_value(self.label_class_field)
                    if category not in categorys:
                        categorys.append(category)

            dic_voc_yml = OrderedDict({'dataset': OrderedDict({'name':'example_voc',  'classes':categorys, 
                         'image_count':temp_tile_index, 
                         'data_type':'voc', 
                         'input_bandnum':ds.count, 
                         'input_ext':ds.dtypes[0],  'x_ext':self.input_data.split('.')[-1], 
                         'tile_size_x':self.tile_size_x, 
                         'tile_size_y':self.tile_size_y, 
                         'tile_offset_x':self.tile_offset_x, 
                         'tile_offset_y':self.tile_offset_y, 
                         'image_mean':[
                          115.6545965, 117.62014299, 106.01483799], 
                         'image_std':[
                          56.82521775, 53.46318049, 56.07113724]})})
            save_config_to_yaml(dic_voc_yml, output_voc_sda)
            self._save_index_file(output_path_main, output_path_img)
            print('train data saved to `{:s}`'.format(os.path.join(self.output_path, self.output_name)))

    def _get_features_box(self, temp_input_label, block_xmin, block_ymin, block_xmax, block_ymax, height, transf):
        features_box = []
        for feature_index in temp_input_label:
            if self.label_class_field == None:
                category = 'unspecified'
            else:
                category = feature_index.get_value(self.label_class_field)
            feature_xmin_geo = feature_index.geometry.bounds.left
            feature_xmax_geo = feature_index.geometry.bounds.right
            feature_ymin_geo = feature_index.geometry.bounds.bottom
            feature_ymax_geo = feature_index.geometry.bounds.top
            feature_ymax, feature_xmin = rasterio.transform.rowcol(transf, feature_xmin_geo, feature_ymin_geo)
            feature_ymin, feature_xmax = rasterio.transform.rowcol(transf, feature_xmax_geo, feature_ymax_geo)
            feature_half_length_x = abs(feature_xmax - feature_xmin) / 2
            feature_half_length_y = abs(feature_ymax - feature_ymin) / 2
            list_bbox = []
            if (feature_xmin >= block_xmin - feature_half_length_x) & (feature_xmax <= block_xmax + feature_half_length_x) & (feature_ymin >= block_ymin - feature_half_length_y) & (feature_ymax <= block_ymax + feature_half_length_y):
                if feature_xmin - block_xmin < 0:
                    xmin = 0
                else:
                    xmin = round(feature_xmin - block_xmin, 2)
                if feature_ymin - block_ymin < 0:
                    ymin = 0
                else:
                    ymin = round(feature_ymin - block_ymin, 2)
                if block_xmax - feature_xmax < 0:
                    xmax = block_xmax - block_xmin
                else:
                    xmax = round(feature_xmax - block_xmin, 2)
                if block_ymax - feature_ymax < 0:
                    ymax = block_ymax - block_ymin
                else:
                    ymax = round(feature_ymax - block_ymin, 2)
                if xmin < xmax - 2 and ymin < ymax - 2:
                    list_bbox.append(xmin)
                    list_bbox.append(ymin)
                    list_bbox.append(xmax)
                    list_bbox.append(ymax)
                    list_bbox.append(category)
                    list_bbox.append(0)
                    features_box.append(list_bbox)

        return features_box

    def _save_images_labels(self, temp_input_label, ds, block_xmin, block_ymin, height, transf, transf_tile, temp_tile_index, output_path_img, output_path_label):
        block_xmax = block_xmin + self.tile_size_x
        block_ymax = block_ymin + self.tile_size_y
        start_index_string = str(temp_tile_index).zfill(8)
        features_box = self._get_features_box(temp_input_label, block_xmin, block_ymin, block_xmax, block_ymax, height, transf)
        if self.save_nolabel_tiles == False:
            if features_box:
                _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_img, start_index_string), transf_tile, self.input_data)
                self._save_xml(output_path_label, features_box, self.tile_size_x, self.tile_size_y, start_index_string + '.' + self.tile_format, ds.count)
                temp_tile_index = temp_tile_index + 1
        else:
            _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_img, start_index_string), transf_tile, self.input_data)
            self._save_xml(output_path_label, features_box, self.tile_size_x, self.tile_size_y, start_index_string + '.' + self.tile_format, ds.count)
            temp_tile_index = temp_tile_index + 1
        return temp_tile_index

    def _save_xml(self, output_path_label, lists, width, height, pic_name, depth):
        """
            传入lists包含bbox，category，difficult信息，将其转换为xml格式

            :param output_path_label: 输入标签文件存储路径
            :type output_path_label: str
            :param lists: 包含bbox，category，difficult信息
            :type lists: list
            :param width: 图像宽度
            :type width: Long
            :param height: 图像高度
            :type height: Long
            :param pic_name: 对应标签文件的图片名称
            :type pic_name: str
            :param tile_format: 切片的图像格式:TIFF,PNG,JPG
            :type tile_format: str

            """
        if self.tile_format == 'jpg' or self.tile_format == 'png':
            depth = 3
        from lxml.etree import Element, SubElement, tostring
        node_root = Element('annotation')
        node_folder = SubElement(node_root, 'folder')
        node_folder.text = 'VOC'
        node_filename = SubElement(node_root, 'filename')
        node_filename.text = pic_name
        node_size = SubElement(node_root, 'size')
        node_width = SubElement(node_size, 'width')
        node_width.text = '%s' % width
        node_height = SubElement(node_size, 'height')
        node_height.text = '%s' % height
        node_depth = SubElement(node_size, 'depth')
        node_depth.text = '%s' % depth
        node_segmented = SubElement(node_root, 'segmented')
        node_segmented.text = '%s' % 0
        for list in lists:
            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = str(list[4])
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = str(list[5])
            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = '%s' % list[0]
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = '%s' % list[1]
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = '%s' % list[2]
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = '%s' % list[3]

        del lists[:]
        xml = tostring(node_root, pretty_print=True)
        save_xml = os.path.join(output_path_label, pic_name.replace(self.tile_format, 'xml'))
        with open(save_xml, 'wb') as (f):
            f.write(xml)

    def _save_index_file(self, output_path_main, output_path_img):
        pic_names = os.listdir(output_path_img)
        train_length = int(len(pic_names) / 5 * 4)
        val_length = int(len(pic_names) / 10)
        list_train = pic_names[0:train_length]
        list_val = pic_names[train_length:train_length + val_length]
        list_test = pic_names[train_length + val_length:]
        list_trainval = list_train + list_val
        train_txt = open(os.path.join(output_path_main, 'train.txt'), 'w')
        val_txt = open(os.path.join(output_path_main, 'val.txt'), 'w')
        test_txt = open(os.path.join(output_path_main, 'test.txt'), 'w')
        trainval_txt = open(os.path.join(output_path_main, 'trainval.txt'), 'w')
        for pic_name in list_train:
            label_name = pic_name.split('.')[0]
            train_txt.write(label_name + '\n')

        for pic_name in list_val:
            label_name = pic_name.split('.')[0]
            val_txt.write(label_name + '\n')

        for pic_name in list_test:
            label_name = pic_name.split('.')[0]
            test_txt.write(label_name + '\n')

        for pic_name in list_trainval:
            label_name = pic_name.split('.')[0]
            trainval_txt.write(label_name + '\n')

        train_txt.close()
        val_txt.close()
        test_txt.close()
        trainval_txt.close()
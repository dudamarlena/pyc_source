# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_object_detection_data_mask.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 37943 bytes
import colorsys, json, os
from collections import OrderedDict
import numpy as np, rasterio
from rasterio import features
from iobjectspy import Rectangle, clip
from iobjectspy.ml.toolkit._create_training_data_util import _save_img, get_tile_start_index, _get_input_feature, _rgb, get_key
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml, get_config_from_yaml, save_pattle_png

class CreateObjectDetectionDataMask(object):

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

    def create_voc_mask(self):
        output_path = os.path.join(self.output_path, self.output_name)
        output_path_img = os.path.join(output_path, 'Images')
        output_path_label = os.path.join(output_path, 'Annotations')
        output_path_main = os.path.join(output_path, 'ImageSets', 'Main')
        output_path_is_seg = os.path.join(output_path, 'ImageSets', 'Segmentation')
        output_path_segclass = os.path.join(output_path, 'SegmentationClass')
        output_path_segobject = os.path.join(output_path, 'SegmentationObject')
        output_voc_sda = os.path.join(output_path, self.output_name + '.sda')
        if not os.path.exists(output_path_img):
            os.makedirs(output_path_img)
        if not os.path.exists(output_path_label):
            os.makedirs(output_path_label)
        if not os.path.exists(output_path_main):
            os.makedirs(output_path_main)
        if not os.path.exists(output_path_is_seg):
            os.makedirs(output_path_is_seg)
        if not os.path.exists(output_path_segclass):
            os.makedirs(output_path_segclass)
        else:
            if not os.path.exists(output_path_segobject):
                os.makedirs(output_path_segobject)
            temp_tile_index = get_tile_start_index(self.tile_start_index, output_voc_sda)
            temp_input_label = _get_input_feature(self.input_label)
            categorys = [
             '__background__']
            if self.label_class_field == None:
                categorys.append('unspecified')
            else:
                try:
                    config = get_config_from_yaml(output_voc_sda)
                    for temp_class_type in config.get('dataset').get('class_type'):
                        categorys.append(temp_class_type.get('class_name'))

                except:
                    pass

                for i in temp_input_label:
                    category = i.get_value(self.label_class_field)
                    if category not in categorys:
                        categorys.append(category)

        categorys_dict = {}
        try:
            config = get_config_from_yaml(output_voc_sda)
            id_category = 0
            for temp_class_type in config.get('dataset').get('class_type'):
                categorys_dict[temp_class_type.get('class_name')] = temp_class_type.get('class_value')
                id_category = id_category + 1

            for category in categorys:
                if category not in categorys:
                    categorys_dict[category] = id_category
                    id_category = id_category + 1

        except:
            categorys_dict['__background__'] = 0
            id_category = 0
            for category in categorys:
                categorys_dict[category] = id_category
                id_category = id_category + 1

        color_codes_list = self._get_codes_list()
        color_codes = {}
        try:
            config = get_config_from_yaml(output_voc_sda)
            color_codes_id = 0
            for temp_class_type in config.get('dataset').get('class_type'):
                color_codes[tuple(temp_class_type.get('class_color'))] = temp_class_type.get('class_value')
                color_codes_id = color_codes_id + 1

            for category in categorys:
                if category not in categorys:
                    color_codes[color_codes_list[color_codes_id]] = categorys_dict[category]
                    color_codes_id = color_codes_id + 1

        except:
            color_codes[(0, 0, 0)] = 0
            color_codes_id = 0
            for category in categorys:
                if category is not '__background__':
                    color_codes[color_codes_list[color_codes_id]] = categorys_dict[category]
                    color_codes_id = color_codes_id + 1

        categorys_count = {}
        try:
            config = get_config_from_yaml(output_voc_sda)
            for temp_class_type in config.get('dataset').get('class_type'):
                categorys_count[temp_class_type.get('class_value')] = int(temp_class_type.get('pixel_count'))

            for category in categorys:
                if category not in categorys:
                    categorys_count[categorys_dict[category]] = 0

        except:
            categorys_count[0] = 0
            for category in categorys:
                categorys_count[categorys_dict[category]] = 0

        with rasterio.open(self.input_data) as (ds):
            transf = ds.transform
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
                        transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                        feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                        temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin, block_ymin, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)
                    if self.tile_offset_x != 0 and self.tile_offset_y != 0:
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top, geo_block_left + geo_tile_offset_x + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                            feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                            temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin + self.tile_offset_x, block_ymin, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)
                        tile_box = Rectangle(geo_block_left, geo_block_top - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                            temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin, block_ymin + self.tile_offset_y, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_offset_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                            temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin + self.tile_offset_x, block_ymin + self.tile_offset_y, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)
                    elif self.tile_offset_x != 0 and self.tile_offset_y == 0:
                        tile_box = Rectangle(geo_block_left + geo_tile_offset_x, geo_block_top, geo_block_left + geo_tile_offset_x + geo_tile_size_x, geo_block_top - geo_tile_size_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            transf_tile = rasterio.transform.from_bounds(geo_block_left + geo_tile_offset_x, geo_block_top - geo_tile_size_y, geo_block_left + geo_tile_size_x + geo_tile_offset_x, geo_block_top, self.tile_size_x, self.tile_size_y)
                            feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                            temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin + self.tile_offset_x, block_ymin, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)
                    elif self.tile_offset_x == 0 and self.tile_offset_y != 0:
                        tile_box = Rectangle(geo_block_left, geo_block_top - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_size_y - geo_tile_offset_y)
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type='STATIC')
                        if recordset.get_geometry() != None:
                            transf_tile = rasterio.transform.from_bounds(geo_block_left, geo_block_top - geo_tile_size_y - geo_tile_offset_y, geo_block_left + geo_tile_size_x, geo_block_top - geo_tile_offset_y, self.tile_size_x, self.tile_size_y)
                            feature_list_segobj, feature_list_segclass, feature_box = self._get_features_list(recordset, tile_box, categorys_dict, transf_tile)
                            temp_tile_index = self._save_images_labels_masks(ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin, block_ymin + self.tile_offset_y, transf_tile, temp_tile_index, categorys_count, color_codes, output_path)

            list_class_type = []
            for key in categorys:
                list_class_type.append(OrderedDict({'class_name':key,  'class_value':categorys_dict[key], 
                 'pixel_count':int(categorys_count[categorys_dict[key]]), 
                 'class_color':get_key(color_codes, categorys_dict[key])[0]}))

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
                          56.82521775, 53.46318049, 56.07113724], 
                         'class_type':list_class_type})})
            save_config_to_yaml(dic_voc_yml, output_voc_sda)
            self._save_index_file(output_path_main, output_path_is_seg, output_path_img)
            print('train data saved to `{:s}`'.format(output_path))

    def _get_features_list(self, recordset, tile_box, categorys_dict, transf):
        feature_list_segobj = []
        feature_list_segclass = []
        feature_box = []
        count_segobj = 0
        for feature in recordset.get_features():
            clip_geometry = clip(feature.geometry, tile_box)
            if (clip_geometry != None) & (feature.geometry.area != 0):
                list_bbox = []
                if clip_geometry.area / feature.geometry.area >= 0.5:
                    feature_geojson = json.loads(clip_geometry.to_geojson())
                    feature_ymax, feature_xmin = rasterio.transform.rowcol(transf, clip_geometry.bounds.left, clip_geometry.bounds.bottom)
                    feature_ymin, feature_xmax = rasterio.transform.rowcol(transf, clip_geometry.bounds.right, clip_geometry.bounds.top)
                    list_bbox.append(feature_xmin)
                    list_bbox.append(feature_ymin)
                    list_bbox.append(feature_xmax)
                    list_bbox.append(feature_ymax)
                    count_segobj = count_segobj + 1
                    if self.label_class_field == None:
                        feature_list_segclass.append((
                         feature_geojson, categorys_dict['unspecified']))
                        list_bbox.append('unspecified')
                        feature_list_segobj.append((
                         feature_geojson, count_segobj))
                    else:
                        feature_list_segclass.append((
                         feature_geojson,
                         categorys_dict[feature.get_value(self.label_class_field)]))
                        list_bbox.append(self.label_class_field)
                        feature_list_segobj.append((
                         feature_geojson, count_segobj))
                    list_bbox.append(0)
                    feature_box.append(list_bbox)

        return (
         feature_list_segobj, feature_list_segclass, feature_box)

    def _save_images_labels_masks(self, ds, feature_list_segobj, feature_list_segclass, feature_box, block_xmin, block_ymin, transf_tile, temp_tile_index, categorys_count, color_codes, output_path):
        start_index_string = str(temp_tile_index).zfill(8)
        output_path_img = os.path.join(output_path, 'Images')
        output_path_label = os.path.join(output_path, 'Annotations')
        output_path_segclass = os.path.join(output_path, 'SegmentationClass')
        output_path_segobject = os.path.join(output_path, 'SegmentationObject')
        if self.save_nolabel_tiles == False:
            if feature_box:
                _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_img, start_index_string), transf_tile, self.input_data)
                self._save_xml(output_path_label, feature_box, self.tile_size_x, self.tile_size_y, start_index_string + '.' + self.tile_format, ds.count)
                self._save_segclass(feature_list_segclass, transf_tile, categorys_count, color_codes, os.path.join(output_path_segclass, start_index_string) + '.' + 'png')
                self._save_segobject(feature_list_segobj, transf_tile, os.path.join(output_path_segobject, start_index_string) + '.' + 'png')
                temp_tile_index = temp_tile_index + 1
        else:
            _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, os.path.join(output_path_img, start_index_string), transf_tile, self.input_data)
            self._save_xml(output_path_label, feature_box, self.tile_size_x, self.tile_size_y, start_index_string + '.' + self.tile_format, ds.count)
            self._save_segclass(feature_list_segclass, transf_tile, categorys_count, color_codes, os.path.join(output_path_segclass, start_index_string) + '.' + 'png')
            self._save_segobject(feature_list_segobj, transf_tile, os.path.join(output_path_segobject, start_index_string) + '.' + 'png')
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
            node_name.text = list[4]
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

    def _save_index_file(self, output_path_main, output_path_is_seg, output_path_img):
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
        train_seg_txt = open(os.path.join(output_path_is_seg, 'train.txt'), 'w')
        val_seg_txt = open(os.path.join(output_path_is_seg, 'val.txt'), 'w')
        test_seg_txt = open(os.path.join(output_path_is_seg, 'test.txt'), 'w')
        trainval_seg_txt = open(os.path.join(output_path_is_seg, 'trainval.txt'), 'w')
        for pic_name in list_train:
            label_name = pic_name.split('.')[0]
            train_txt.write(label_name + '\n')
            train_seg_txt.write(label_name + '\n')

        for pic_name in list_val:
            label_name = pic_name.split('.')[0]
            val_txt.write(label_name + '\n')
            val_seg_txt.write(label_name + '\n')

        for pic_name in list_test:
            label_name = pic_name.split('.')[0]
            test_txt.write(label_name + '\n')
            test_seg_txt.write(label_name + '\n')

        for pic_name in list_trainval:
            label_name = pic_name.split('.')[0]
            trainval_txt.write(label_name + '\n')
            trainval_seg_txt.write(label_name + '\n')

        train_txt.close()
        val_txt.close()
        test_txt.close()
        trainval_txt.close()

    def _save_segclass(self, feature_list, transf_tile, categorys_count, color_codes, output_segclass):
        image = features.rasterize(((g, v) for g, v in feature_list), out_shape=(self.tile_size_y, self.tile_size_x), transform=transf_tile)
        for feature in feature_list:
            categorys_count[feature[1]] = categorys_count[feature[1]] + np.sum(image == feature[1])

        save_pattle_png(image, color_codes, output_segclass)

    def _save_segobject(self, feature_list, transf_tile, output_segobject):
        num_color_id = len(feature_list)
        color_continuous_codes_list = self._get_continuous_codes_list(num_color_id)
        color_codes_segobject = {}
        color_codes_segobject[(0, 0, 0)] = 0
        color_codes_id = 0
        for feature in feature_list:
            color_codes_segobject[color_continuous_codes_list[color_codes_id]] = color_codes_id
            color_codes_id = color_codes_id + 1

        image = features.rasterize(((g, v) for g, v in feature_list), out_shape=(
         self.tile_size_y, self.tile_size_x),
          transform=transf_tile)
        save_pattle_png(image, color_codes_segobject, output_segobject)

    def _get_codes_list(self):
        color_codes_list = []
        color_codes_list.append(_rgb('#f9886c'))
        color_codes_list.append(_rgb('#ed6498'))
        color_codes_list.append(_rgb('#eeeeee'))
        color_codes_list.append(_rgb('#f8f8f8'))
        color_codes_list.append(_rgb('#ffffff'))
        color_codes_list.append(_rgb('#3bb2d0'))
        color_codes_list.append(_rgb('#3887be'))
        color_codes_list.append(_rgb('#f1f075'))
        color_codes_list.append(_rgb('#fbb03b'))
        color_codes_list.append(_rgb('#404040'))
        color_codes_list.append(_rgb('#e55e5e'))
        color_codes_list.append(_rgb('#223b53'))
        color_codes_list.append(_rgb('#50667f'))
        color_codes_list.append(_rgb('#28353d'))
        color_codes_list.append(_rgb('#222b30'))
        color_codes_list.append(_rgb('#8a8acb'))
        color_codes_list.append(_rgb('#41afa5'))
        color_codes_list.append(_rgb('#56b881'))
        return color_codes_list

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
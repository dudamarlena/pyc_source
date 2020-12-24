# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_dataprepare_collector\binary_classification_training_data.py
# Compiled at: 2019-12-31 04:09:00
# Size of source mod 2**32: 1075 bytes
from _sample.create_binary_classification_data import CreateBinaryClassificationData

def create_binary_classification_data(input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False):
    create_td = CreateBinaryClassificationData(input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, tile_start_index, save_nolabel_tiles)
    create_td.create_binary_classification()
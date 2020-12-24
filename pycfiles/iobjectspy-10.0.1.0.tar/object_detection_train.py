# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_trainer_collector\object_detection_train.py
# Compiled at: 2019-12-31 04:09:04
# Size of source mod 2**32: 1508 bytes
from _models.faster_rcnn.model import faster_rcnn
from toolkit._toolkit import get_config_from_yaml

class ObjectDetection:

    def __init__(self, train_data_path, config, epoch, batch_size, lr, output_model_path, output_model_name, log_path, backbone_name, backbone_weight_path, reload_model, pretrained_model_path):
        self.train_data_path = train_data_path
        self.config = get_config_from_yaml(config)
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.log_path = log_path
        self.backbone_name = backbone_name
        self.backbone_weight_path = backbone_weight_path
        self.reload_model = reload_model
        self.pretrained_model_path = pretrained_model_path

    def train(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = 'self.' + self.config.model.name + '_' + self.config.framework.name
        eval(func_str)()

    def faster_rcnn_tensorflow(self):
        faster_rcnn.train(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.log_path, self.backbone_name, self.backbone_weight_path, self.output_model_path, self.output_model_name, self.pretrained_model_path)

    def ssd_pytorch(self):
        pass
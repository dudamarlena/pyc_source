# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\object_detection_infer.py
# Compiled at: 2019-12-31 04:09:00
# Size of source mod 2**32: 5950 bytes
import os, re, rasterio, yaml
from dotmap import DotMap
from iobjectspy import Dataset
from _models.faster_rcnn._detection import FasterRCNNEstimation
from toolkit._toolkit import get_config_from_yaml

class ObjectDetection:

    def __init__(self, input_data, model_path, category_name, out_data, out_dataset_name, nms_thresh, score_thresh):
        self.input_data = input_data
        self.config = model_path
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.category_name = category_name
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        self.nms_thresh = nms_thresh
        self.score_thresh = score_thresh

    def infer(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_config = get_config_from_yaml(self.config)
        func_str = 'self.' + func_config.model_architecture + '_' + func_config.framework
        return eval(func_str)()

    def faster_rcnn_tensorflow(self):
        if self.category_name is None:
            with open(self.config) as (f):
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            config = DotMap(config_dict)
            config.get('model').get('categorys').remove('__background__')
            category_name = config.get('model').get('categorys')
            category_name = [str(i) for i in category_name]
            self.category_name = category_name
        else:
            regex = ',|，'
            self.category_name = re.split(regex, self.category_name)
        if not isinstance(self.model_path, str):
            raise TypeError('model_path must be str ')
        if not os.path.exists(self.model_path):
            raise Exception('model_path does not exist ')
        if isinstance(self.out_data, str):
            pass
        if not isinstance(self.out_dataset_name, str):
            raise TypeError('out_dataset_name must be str ')
        if isinstance(self.input_data, Dataset):
            run_prediction = FasterRCNNEstimation(self.model_path, self.config)
            result = run_prediction.estimation_img(self.input_data, self.category_name, self.out_data, self.out_dataset_name, self.nms_thresh, self.score_thresh)
        else:
            if isinstance(self.input_data, str):
                try:
                    ds = rasterio.open(self.input_data)
                    height = ds.height
                    width = ds.width
                except Exception as e:
                    try:
                        print('input_data must be str')
                        os._exit(0)
                    finally:
                        e = None
                        del e

                with open(self.config) as (f):
                    config_dict = yaml.load(f, Loader=(yaml.FullLoader))
                config = DotMap(config_dict)
                blocksize = config.get('model').get('blocksize')
                if height > blocksize and width > blocksize:
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_large_img(self.input_data, self.category_name, self.out_data, self.out_dataset_name, self.nms_thresh, self.score_thresh)
                else:
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_img(self.input_data, self.category_name, self.out_data, self.out_dataset_name, self.nms_thresh, self.score_thresh)
            else:
                raise TypeError('input_data must be str or Dataset')
        return result

    def yolo_tensorflow(self):
        pass


class ObjectDetectionWithTile:

    def __init__(self, model_path):
        """
        使用numpy进行目标检测,输入为图像数组和输出为feature
        :param model_path: 模型路径
        :param config: 配置文件路径
        :param kwargs:
        """
        config = model_path
        self.config = get_config_from_yaml(model_path)
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.estimate = FasterRCNNEstimation(self.model_path, config)

    def load_model(self):
        func_str = 'self.' + self.config.model_architecture + '_' + self.config.framework + '_load_model'
        return eval(func_str)()

    def infer_tile(self, image_data, category_name, nms_thresh, score_thresh):
        func_str = 'self.' + self.config.model_architecture + '_' + self.config.framework + '_tile'
        return eval(func_str)(image_data, category_name, nms_thresh, score_thresh)

    def faster_rcnn_tensorflow_tile(self, image_data, category_name, nms_thresh, score_thresh):
        """使用numpy进行目标检测,输入图像数组，输出为特征数组
                :return:
                """
        return self.estimate.estimation_numpy(image_data, category_name, nms_thresh, score_thresh)

    def close_model(self):
        self.estimation.close_model()
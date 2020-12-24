# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference.py
# Compiled at: 2019-12-31 04:09:00
# Size of source mod 2**32: 5871 bytes
import os, tempfile
from iobjectspy import Dataset, conversion
from iobjectspy._jsuperpy._utils import check_lic
from ._inference_collector import ObjectDetection, BinaryClassification, MultiClassification, SceneClassification
from toolkit._toolkit import _is_image_file, del_dir, _get_dataset_readonly

class Inference:

    def __init__(self, input_data, model_path, out_data, out_dataset_name):
        """
        图像数据模型推理功能入口

        :param input_data: 待推理的数据
        :type  input_data: str or Dataset
        :param model_path: 模型存储路径
        :type  model_path: str
        :param out_data: 输出文件(或数据源)路径
        :type  out_data: str or Datasource or DatasourceConnectionInfo
        :param out_dataset_name: 输出文件(或数据集)名称
        :type  out_dataset_name: str
        """
        if _is_image_file(input_data):
            self.is_del_tmp_file = False
        else:
            self.is_del_tmp_file = True
            input_data = _get_dataset_readonly(input_data)
            temp_tif_path = os.path.join(tempfile.mkdtemp(), 'temp') + '.tif'
            conversion.export_to_tif(input_data, temp_tif_path)
            input_data = temp_tif_path
        self.input_data = input_data
        self.model_path = model_path
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        check_lic()

    def object_detect_infer(self, category_name, nms_thresh=0.3, score_thresh=0.5):
        """
        影像数据目标检测

        | 支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，检测结果为GeoJSON格式文件
        | 支持SuperMap SDX下的影像数据集，检测结果为矢量线数据集

        需要注意:
            - 当 input_data 为待检测文件时，out_data 为输出文件路径，out_dataset_name 为.json后缀的文件名
            - 当 input_data 为待检测数据集时，out_data 为输出数据源路径(或数据源对象)，out_dataset_name 为数据集名

        :param category_name: 目标检测类别，支持 'plane', 'ship', 'tennis-court', 'vehicle'
        :type  category_name: list[str] or str
        :param nms_thresh: nms的阈值
        :type  nms_thresh: float
        :param score_thresh: 类别分数的阈值
        :type  score_thresh: float
        :return: None
        """
        result = ObjectDetection(self.input_data, self.model_path, category_name, self.out_data, self.out_dataset_name, nms_thresh, score_thresh).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def binary_classify_infer(self, offset, result_type, **kwargs):
        """
        遥感影像数据二元分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为二值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        可添加关键字参数：'dsm_dataset' 输入与影像相匹配的DSM数据，实现基于DOM和DSM提取建筑物面。
        其中影像和DSM可以使用SuperMap iDesktop 桌面基于倾斜摄影数据提取：
            打开三维场景，使用 三维分析->生成DOM 三维分析->生成DSM，分辨率建议选择0.1m

        :param offset: 图像分块偏移，大幅图像需分块预测，其值为分块间重叠部分大小，以提高图像块边缘预测结果
        :type offset: int
        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = BinaryClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), offset, 
         result_type, **kwargs).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def scene_classify_infer(self, result_type, **kwargs):
        """
        遥感影像数据场景分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为二值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = SceneClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), 
         result_type, **kwargs).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def multi_classify_infer(self, offset, result_type, **kwargs):
        """
        遥感影像数据多分类，地物分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为多值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        :param offset: 图像分块偏移，大幅图像需分块预测，其值为分块间重叠部分大小，以提高图像块边缘预测结果
        :type offset: int
        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = MultiClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), offset, 
         result_type, **kwargs).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result
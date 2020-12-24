# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\API_test.py
# Compiled at: 2019-04-15 08:40:58
# Size of source mod 2**32: 1613 bytes
from segmentation_module.segmentation_api.API import API
config_path = 'configs\\config_model_KS.json'
config_path = 'configs\\config_stitch.json'
api = API()
config_path = 'C:\\Users\\PR\\OneDrive_Politechnika_Warszawska\\Repositories\\segmentation_module\\configs\\config_stitch.json'
img_path = 'C:\\Users\\PR\\GISS\\Stitch_dataset\\images\\val\\image_0002.png'
img_folder = 'D:\\segmentation_labels_15_04_2019\\images\\val'
img_path = 'F:\\GISS\\Gildia_kupiecka\\Google_Drive\\GISS\\Data\\2019-04-09_original_deg0_100m_fort_bema\\images\\raw_images\\DJI_0003.JPG'
outputo = 'F:\\GISS\\Gildia_kupiecka\\stitch'
config_path = 'C:\\Users\\PR\\Documents\\segmentation_training\\unet_2019-04-15-13-50-57\\config_model.json'
api.predict_and_visualize(config_path, img_path, 'example_preds4', with_blobs=True)
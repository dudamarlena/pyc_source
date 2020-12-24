# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\view\GUI_view.py
# Compiled at: 2020-04-03 09:00:04
# Size of source mod 2**32: 1119 bytes
"""
@File       :   GUI_view.py
@Author     :   jiaming
@Modify Time:   2020/1/16 18:54
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   展示生成的结果 - 展示传统二维码、延展后的柱面二维码的合图
"""
from PIL import Image
import matplotlib.pyplot as plt
from cqrcode.static._static_data import dataPath

def window(original_qrcode_path='', cqrcode_path=''):
    """
    呈现最终生成的结果
    :param original_qrcode_path: 传统二维码的路径
    :param cqrcode_path: 延展的柱面二维码的路径
    :return: 三张二维码的合图
    """
    plt.subplot(1, 2, 1)
    plt.imshow(Image.open(original_qrcode_path))
    plt.title('oridinary QRcode')
    plt.subplot(1, 2, 2)
    plt.imshow(Image.open(cqrcode_path))
    plt.title('cylindrical QRcode')
    fileName = dataPath + 'output' + '.png'
    plt.savefig(fileName, dpi=100, bbox_inchs='tight')
    plt.show()


if __name__ == '__main__':
    window(dataPath + '_blank.png', dataPath + '_blank.png')
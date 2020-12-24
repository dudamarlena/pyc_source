# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\view\GUI_view.py
# Compiled at: 2020-04-03 09:00:04
# Size of source mod 2**32: 1119 bytes
__doc__ = '\n@File       :   GUI_view.py\n@Author     :   jiaming\n@Modify Time:   2020/1/16 18:54\n@Contact    :   https://blog.csdn.net/weixin_39541632\n@Version    :   1.0\n@Desciption :   展示生成的结果 - 展示传统二维码、延展后的柱面二维码的合图\n'
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
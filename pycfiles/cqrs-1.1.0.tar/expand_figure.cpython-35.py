# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\make_qrcode\expand_figure.py
# Compiled at: 2020-04-03 08:25:02
# Size of source mod 2**32: 1467 bytes
__doc__ = '\n@File       :   expand_figure.py\n@Author     :   jiaming\n@Modify Time:   2020/4/3 14:59    \n@Contact    :   https://blog.csdn.net/weixin_39541632\n@Version    :   1.0\n@Desciption :   None\n'
import math
from PIL import Image
from cqrcode.static._static_data import dataPath

def expand_fig(multiplying_power=0.2, version=-1, filePath=''):
    """
    水平拉伸图片
    1 mm = 10 像素
    1 像素 = 0.1 mm
    :param multiplying_power:
    :return:
    """
    print('进行二维码拓展 %s...' % str(multiplying_power))
    INPUT_IMAGE = Image.open(filePath)
    w, h = INPUT_IMAGE.size
    width = w
    L = 350
    R = 0.1 * width / multiplying_power
    x = [0.1 * i for i in range(0, width // 2, 1)]
    y = []
    for i in x:
        y.append((math.asin((R + L) / R * math.sin(math.atan(i / L))) - math.atan(i / L)) * R * 10 - i * 10)

    y.reverse()
    OUT_IMAGE = INPUT_IMAGE.resize((2 * round(y[0]) + width, h), Image.ANTIALIAS)
    filePath = dataPath + '%s 扩展图片.png' % version
    OUT_IMAGE.save(filePath)
    print('扩展二维码成功 %s %s.' % (OUT_IMAGE, filePath))
    return filePath


if __name__ == '__main__':
    expand_fig(multiplying_power=1.5, version=1, filePath=dataPath + '1.png')
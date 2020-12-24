# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\make_qrcode\QRcode.py
# Compiled at: 2020-04-03 08:25:02
# Size of source mod 2**32: 2223 bytes
"""
@File       :   QRcode.py
@Author     :   jiaming
@Modify Time:   2020/1/13 19:55
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   生成传统二维码
                解析传统二维码
"""
import qrcode
from PIL import Image
from pyzbar import pyzbar
from cqrcode.static._static_data import dataPath, BOUNDARY, BOX

def create_QRcode(data=''):
    """
    创建二维码, 并保存到 static/ 下
    :return: 生成的二维码路径
    """
    print('生成传统二维码...')
    filePath = dataPath + '传统二维码' + '.png'
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=BOX, border=BOUNDARY)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(filePath, dpi=(254.0, 254.0))
    print('保存路径：', filePath)
    return filePath


def decode_QRcode(filePath=''):
    """
    :param filePath: 待识别二维码路径
    :return: 打印出识别的结果
    """
    decode_data = pyzbar.decode(Image.open(filePath), symbols=[
     pyzbar.ZBarSymbol.QRCODE])[0].data.decode('utf-8')
    return decode_data


if __name__ == '__main__':
    create_QRcode('xxx')
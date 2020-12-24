# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\make_qrcode\QRcode.py
# Compiled at: 2020-04-03 08:25:02
# Size of source mod 2**32: 2223 bytes
__doc__ = '\n@File       :   QRcode.py\n@Author     :   jiaming\n@Modify Time:   2020/1/13 19:55\n@Contact    :   https://blog.csdn.net/weixin_39541632\n@Version    :   1.0\n@Desciption :   生成传统二维码\n                解析传统二维码\n'
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
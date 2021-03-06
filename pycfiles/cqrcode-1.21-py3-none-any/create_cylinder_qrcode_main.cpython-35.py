# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\make_qrcode\create_cylinder_qrcode_main.py
# Compiled at: 2020-04-07 07:53:11
# Size of source mod 2**32: 5309 bytes
"""
@File       :   create_cylinder_qrcode_main.py
@Author     :   jiaming
@Modify Time:   2020/4/2 20:18
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
from cqrcode.static._static_data import CAPACITY, dataPath, alphanumeric_mode_table, data32, data64, BOX, version_bit_length
from cqrcode.app.make_qrcode.prepare_moudle import return_moudle_coordinate
from cqrcode.app.make_qrcode.alpha2bit import data_encode, random_bit
from cqrcode.app.make_qrcode.expand_figure import expand_fig
version_symbol = ''

def check(data='', version=None):
    """
    检查数据以及version是否正确
    :param data:
    :param version:
    :return:
    """
    data = data.upper()
    print('检查字符...', len(data), data)
    if data == '':
        print('数据为空！')
        return False
    for i in data.upper():
        if i not in alphanumeric_mode_table.keys():
            print('数据不合法！')
            return False

    if version is None:
        subdict = {}
        for i in CAPACITY:
            k, v = i
            subdict[k] = v - len(data)

        min = 99999
        key = -1
        for k, v in subdict.items():
            if v >= 0 and min > v:
                min = v
                key = k

        if key == -1:
            print('数据超长...')
            raise RuntimeError('数据超长！')
        else:
            version_bit = '0' * (version_bit_length - len(bin(key)[2:])) + bin(key)[2:]
            return (key, version_bit)
    elif version < 0 or version > len(CAPACITY):
        return False
    if CAPACITY[(version - 1)][1] < len(data):
        print('版本选择错误！')
        return False
    return (
     version,
     '0' * (version_bit_length - len(bin(version)[2:])) + bin(version)[2:])


def load_bits_to_moudle(version=-1, bits='', moudle_fig=None, coordinate=[]):
    """

    :param version:
    :param bits:
    :param moudle_fig:
    :param coordinate:
    :return:
    """
    index = 0
    for j in bits:
        x, y = coordinate[index]
        if j == '1':
            for k in range(0, BOX, 1):
                for z in range(0, BOX, 1):
                    moudle_fig.putpixel((x + k, y + z), (0, 0, 0))

        elif j == '0':
            for k in range(0, BOX, 1):
                for z in range(0, BOX, 1):
                    moudle_fig.putpixel((x + k, y + z), (255, 255, 255))

        index += 1

    fileName = dataPath + '%s 柱面二维码.png' % version
    moudle_fig.save(fileName)
    return fileName


def create_cqrcode(data=data64, version=None, rate=1.25):
    """

    :param data:
    :param version:
    :param expand:
    :param rate:
    :return:
    """
    if check(data, version) is False:
        raise RuntimeError('生成柱面二维码终止！')
    if version is None:
        version, version_bit = check(data, version)
    else:
        version, version_bit = check(data, version)
    data_bits = data_encode(alpha=data, version_bit=version_bit)
    data_bits += random_bit(length=(CAPACITY[(version - 1)][1] - len(data)) // 2 * 11)
    print('填充补齐：', data_bits)
    moudle_fig, coordinate_of_bit = return_moudle_coordinate(version=version)
    fileName = load_bits_to_moudle(version=version, bits=data_bits, moudle_fig=moudle_fig, coordinate=coordinate_of_bit)
    print('成功生成柱面二维码: ', fileName)
    expand_figure_fileName = expand_fig(multiplying_power=rate, version=version, filePath=fileName)
    return expand_figure_fileName


if __name__ == '__main__':
    l = ['4',
     'C',
     'J',
     'Z',
     '0',
     'm',
     'a',
     'W',
     'g',
     'O',
     '6',
     'b',
     '1',
     'c',
     'o',
     't',
     'T',
     'M',
     'd',
     'j',
     'U',
     '8',
     'u',
     '3',
     'Q',
     'p',
     'r',
     'V',
     'k',
     'P',
     'R',
     'Y',
     'l',
     'f',
     'z',
     'e',
     'S',
     'G',
     'X',
     'N',
     'y',
     'v',
     'n',
     'i',
     'H',
     '2',
     'B',
     'L',
     'F',
     '5',
     'x',
     'A',
     'E',
     'w',
     's',
     '7',
     '9',
     'D',
     'q',
     'h',
     'I',
     'K'] * 3
    for i in CAPACITY:
        import random
        random.shuffle(l)
        data = ''.join(l[:i[1]])
        create_cqrcode(data=data)
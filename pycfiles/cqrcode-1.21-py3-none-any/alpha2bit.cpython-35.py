# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\make_qrcode\alpha2bit.py
# Compiled at: 2020-04-07 07:47:23
# Size of source mod 2**32: 2606 bytes
"""
@File       :   alpha2bit.py
@Author     :   jiaming
@Modify Time:   2020/4/2 20:28
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   集合了字符编码解码函数调用
                只能对于 Alphanumeric_mode_table 中的字符进行编码
"""
from cqrcode.static._static_data import number_of_bits_in_character_count, alphanumeric_mode_table, version_bit_length
import random

def data_encode(alpha='', version_bit=''):
    """
    对传入原生字符串进行检查并编码为一份标准填充比特流。
    :param alpha: Alphanumeric_mode_table 表中的字符
    :return: 原生字符对应的填充比特流
    """
    if len(version_bit) > version_bit_length:
        raise RuntimeError('版本号比特长度错误！')
    alpha = alpha.upper()
    alpha_group = ''
    results = ''
    for i in range(0, len(alpha) - 1, 2):
        alpha_group += alpha[i] + alpha[(i + 1)] + ' '
        number = alphanumeric_mode_table[alpha[i]] * 45 + alphanumeric_mode_table[alpha[(i + 1)]]
        bits = ''.join(list(bin(number))[2:])
        if len(bits) < 11:
            bits = '0' * (11 - len(bits)) + bits
        results += bits + ' '

    if len(alpha) % 2 != 0:
        alpha_group += alpha[(-1)]
        number = alphanumeric_mode_table[alpha[(-1)]]
        bits = ''.join(list(bin(number))[2:])
        if len(bits) < 6:
            bits = '0' * (6 - len(bits)) + bits
        results += bits + ' '
    number_of_bits = ''.join(list(bin(len(alpha)))[2:])
    if len(number_of_bits) < number_of_bits_in_character_count:
        number_of_bits = '0' * (number_of_bits_in_character_count - len(number_of_bits)) + number_of_bits
    print('消除空格前编码后数据： ', version_bit + ' ' + number_of_bits + ' ' + results + '0000')
    data_bits = (version_bit + ' ' + number_of_bits + ' ' + results + '0000').replace(' ', '')
    print('消除空格后编码后数据: ', data_bits)
    return data_bits


def random_bit(length=-1):
    """
    返回 length 长度的比特流
    :param length:
    :return:
    """
    return ''.join([random.choice(['1', '0']) for i in range(length)])


if __name__ == '__main__':
    print(random_bit(10))
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/sniff_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 665 bytes
"""
@author = super_fazai
@File    : sniff_utils.py
@connect : superonesfazai@gmail.com
"""
from scapy.all import linehexdump
__all__ = [
 'get_hex_res_of_pkt']

def get_hex_res_of_pkt(pkt) -> (
 str, None):
    """
    scapy中得到数据包的16进制结果
    :param pkt: 数据包
    :return: None 表示失败
    """
    pkt_load = pkt.load
    line_hex = linehexdump(pkt_load, dump=True)
    try:
        hex_16_pkt_load = line_hex.split(' ')[0] if line_hex is not None else None
    except IndexError:
        return
    else:
        return hex_16_pkt_load
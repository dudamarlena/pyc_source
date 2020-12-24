# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyweights\coefficient_of_variation.py
# Compiled at: 2020-04-16 08:16:43
# Size of source mod 2**32: 3440 bytes
import numpy as np, pandas as pd

def coefficient_of_variation(data, target, pos_neg):
    v = np.nanstd(data, axis=0) / np.nanmean(data, axis=0)
    w = v / v.sum()
    pos = (pos_neg + 1) / 2
    neg = (1 - pos_neg) / 2
    g_pos = np.divide(data, target)
    g_pos = g_pos * pos
    g_neg = np.divide(target, data)
    g_neg = g_neg * neg
    g = g_pos + g_neg
    g = np.nan_to_num(g)
    rlt = (w * g).sum(axis=1)
    return rlt


if __name__ == '__main__':
    usedcolums = [
     '购买力平价法人均GNP', '农业占GDP比重(%)', '第三产业占GDP比重(%)',
     '非农业劳动力占总劳动力比重', '城市人口占总人口比重(%)',
     '平均预期寿命(岁)', '成人识字率(%)',
     '大学生入学率(%)', '千人拥有医生数(人)']
    a = pd.read_csv('C:\\Users\\FH\\Desktop\\cov_data.csv', encoding='utf-8')
    a = np.array(a[usedcolums][:37])
    target = np.array([22930, 2, 63, 0.958, 76, 77, 97.5, 58, 2.5], dtype='float')
    pos_neg = np.array([1, -1, 1, 1, 1, 1, 1, 1, 1], dtype='float')
    result = coefficient_of_variation(data=a, target=target, pos_neg=pos_neg)
    result = np.around(result, decimals=2)
    print(result)
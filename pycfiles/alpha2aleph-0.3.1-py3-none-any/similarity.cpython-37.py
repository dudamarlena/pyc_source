# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/alpha1p/dance/similarity.py
# Compiled at: 2020-04-14 08:04:08
# Size of source mod 2**32: 10137 bytes
__doc__ = '\nCreated on Sun March 15 12:35:24 2020\n\n@author: QQ\n'
import numpy as np
__all__ = [
 'handmade', 'mean', 'cos_dis', 'cheb_dis',
 'wenyao', 'batch_compare', 'diff',
 'dtw', 'pose_cosin']

def handmade(contrast_pose, stand_pose):
    """
    功能：以对比两个舞姿的相似度。相似度的计算思路为：先根据对各区域的分析，
    计算各区域的差异值，然后对各区域的值进行归一化，之后根据各区域的权重计算最终值。
    输入：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    返回：
    similarity：两个舞姿的相似度，格式为：numpy.float64
    """
    d = contrast_pose - stand_pose
    z = np.zeros([7])
    w_left = (abs(stand_pose[1] - 0.5) + abs(stand_pose[2] - 0.5) + 0.1) * 0.05
    w_right = (abs(stand_pose[1] - 0.5) + abs(stand_pose[2] - 0.5) + 0.1) * 0.05
    leg_weight = 0.2
    waist_weight = 0.4
    z[0] = abs(d[0]) * w_left
    z[1] = abs(d[3]) * w_right
    z[2] = abs(d[1] + d[2]) / 2 * (0.1 - w_left)
    z[3] = abs(d[4] + d[5]) / 2 * (0.1 - w_right)
    z[4] = abs(-d[7] + d[8] + d[9]) / 3 * leg_weight
    z[5] = abs(-d[12] + d[13] + d[14]) / 3 * leg_weight
    w = abs((d[6] + d[11]) / 2)
    t = abs(d[6] - d[11])
    f = abs(d[10] + d[6]) + abs(d[15] + d[11])
    z[6] = (w + t + f) / 5 * waist_weight
    similarity = 1 - z.sum()
    noise_mean = 0.917
    if similarity >= noise_mean:
        similarity = (similarity - noise_mean) / (2 * (1 - noise_mean)) + 0.5
    else:
        similarity = similarity / (2 * noise_mean)
    return similarity


def mean(contrast_pose, stand_pose):
    """
    功能：以各关节权重均等的方式对比两个舞姿的相似度。相似度的计算思路为：直接计算关节的差值，之后求均值。
    输入：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    返回：
    similarity：两个舞姿的相似度，格式为：numpy.float64
    """
    d = abs(contrast_pose - stand_pose)
    similarity = 1 - d.mean()
    noise_mean = 0.8675
    if similarity >= noise_mean:
        similarity = (similarity - noise_mean) / (2 * (1 - noise_mean)) + 0.5
    else:
        similarity = similarity / (2 * noise_mean)
    return similarity


def cos_dis(contrast_pose, stand_pose):
    """
    功能：以余弦相似度衡量两个舞姿的相似度。相似度的计算思路为：直接计算两个舞姿的余弦相似度。
    输入：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    返回：
    similarity：两个舞姿的Consin相似度，格式为：numpy.float64
    """
    a = contrast_pose
    b = stand_pose
    a_norm = np.sqrt(np.sum(np.square(a)))
    b_norm = np.sqrt(np.sum(np.square(b)))
    ab = np.sum(np.multiply(a, b))
    cosin_value = np.divide(ab, np.multiply(a_norm, b_norm))
    similarity = cosin_value.mean()
    noise_mean = 0.9523
    if similarity >= noise_mean:
        similarity = (similarity - noise_mean) / (2 * (1 - noise_mean)) + 0.5
    else:
        similarity = similarity / (2 * noise_mean)
    return similarity


def cheb_dis(contrast_pose, stand_pose):
    """
    功能：以切比雪夫距离衡量两个舞姿的相似度。相似度的计算思路为：直接计算两个舞姿的切比雪夫距离。
    输入：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    返回：
    similarity:两个舞姿的切比雪夫距离，格式为：numpy.float64
    """
    d = abs(contrast_pose - stand_pose)
    similarity = 1 - d.max()
    return similarity


def wenyao(contrast_pose, stand_pose):
    """
    功能：对文耀方法的改进，以便于与其他方法对比。相似度的计算思路为：对各关节赋予不同的权重，然后根据权重计算各关节的差异，之后都关节差异求和并进行归一化。
    参数解释：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    返回值：
    similarity：两个舞姿的相似度，格式为：numpy.float64
    """
    w = np.array([0.8, 1.2, 0.9, 0.8, 1.2, 0.9, 1.8, 1.2, 1.2, 1.2, 1.1, 1.8, 1.2, 1.2, 1.2, 1.1])
    d = abs(contrast_pose - stand_pose)
    diff = d * w
    diff = diff.sum() / w.sum()
    similarity = 1 - diff
    noise_mean = 0.8667
    if similarity >= noise_mean:
        similarity = (similarity - noise_mean) / (2 * (1 - noise_mean)) + 0.5
    else:
        similarity = similarity / (2 * noise_mean)
    return similarity


def batch_compare(batch_data, datasets, method=None):
    """
    功能：计算批量舞姿与数据集中舞姿的相似度。
    输入：
    batch_data:一个批量的舞姿数据，可以是一个也可以是多个舞姿
    datasets：要进行对比的舞姿数据集
    method:对比两个舞姿相似度的方法，可供选择的方法有：handmade, mean, wenyao, Chebyshev, Cosin

    返回：
    max_similar：返回批量舞姿中每个舞姿与数据集中所有舞姿的最大相似度，对象格式为：numpy.ndarray。
    """
    similar_function = {'handmade':handmade, 
     'mean':mean, 
     'wenyao':wenyao, 
     'Chebyshev':cheb_dis, 
     'cosin':cos_dis, 
     None:handmade}.get(method)
    if batch_data.ndim == 2 and datasets.ndim == 2:
        batch_len = batch_data.shape[0]
        datasets_len = datasets.shape[0]
        max_similar = np.zeros([batch_len], dtype='float64')
        for i in range(batch_len):
            similar_value = np.zeros([datasets_len], dtype='float64')
            for j in range(datasets_len):
                similar_value[j] = similar_function(batch_data[i], datasets[j])

            max_similar[i] = similar_value.max()

    elif batch_data.ndim == 2 and datasets.ndim == 1:
        batch_len = batch_data.shape[0]
        datasets_len = 1
        max_similar = np.zeros([batch_len], dtype='float64')
        for i in range(batch_len):
            max_similar[i] = similar_function(batch_data[i], datasets)

    elif batch_data.ndim == 1 and datasets.ndim == 2:
        batch_len = 1
        datasets_len = datasets.shape[0]
        similar_value = np.zeros([datasets_len], dtype='float64')
        max_similar = np.zeros([batch_len], dtype='float64')
        for i in range(datasets_len):
            similar_value[i] = similar_function(batch_data, datasets[i])

        max_similar[0] = similar_value.max()
    elif batch_data.ndim == 1 and datasets.ndim == 1:
        max_similar = np.zeros([1], dtype='float64')
        max_similar[0] = similar_function(batch_data, datasets)
    else:
        print('batch_data or dataset 的数据形状错误，请检查数据类型')
    return max_similar


def diff(contrast_pose, stand_pose, similar_function=handmade):
    """
    功能：用以对比两个舞姿的差异度。差异度为1减去二者的相似度。
    输入：
    contrast_pose:要对比的舞姿
    stand_pos: 基准舞姿
    similar_function:计算相似度时选用的相似度方法，可供选择的方法有：similar_calculation(), similar_mean(), 
                                                            similar_wenyao(), cheb_dis(), cos_dis()
    返回值：
    diff：两个舞姿的差异值，格式为：numpy.float64
    """
    similarity = similar_function(contrast_pose, stand_pose)
    diff = 1 - similarity
    return diff


def dtw(x, y, method=None):
    """
    功能：以Dynamic Time Warping (DTW)方法计算两个帧式表示舞蹈的相似度。
    输入：
    x：待对比的舞姿，数据格式为numpy.array。数据必须归一化
    y：参照舞姿，数据格式为numpy.array。数据必须归一化
    similar_method：计算相似度时选用的相似度方法，可供选择的方法有：
    handmade, mean, wenyao, Chebyshev, Cosin
    返回：
    similarity：两个帧式舞蹈的DTW相似度
    """
    similar_method = {'handmade':handmade, 
     'mean':mean, 
     'wenyao':wenyao, 
     'cheb':cheb_dis, 
     'cosin':cos_dis, 
     None:handmade}.get(method)
    r, c = len(x), len(y)
    D0 = np.zeros((r + 1, c + 1))
    D0[0, 1:] = np.inf
    D0[1:, 0] = np.inf
    D1 = D0[1:, 1:]
    for i in range(r):
        for j in range(c):
            D1[(i, j)] = diff((x[i]), (y[j]), similar_function=similar_method)

    C = D1.copy()
    for i in range(r):
        for j in range(c):
            D1[(i, j)] += min(D0[(i, j)], D0[(i, j + 1)], D0[(i + 1, j)])

    similarity = 1 - D1[(-1, -1)] / max(r, c)
    return similarity


def pose_cosin(outs, lables, batch_size=1):
    """
    功能：计算两个舞姿的cosin距离，此函数没有二次归一化结果。
    输入：
    outs：待对比舞姿，numpy.array格式，数据必须归一化。
    lables：参照舞姿，numpy.array格式，数据必须归一化。
    返回：
    cosin_valu：两个pose的cosin距离
    """
    a = np.reshape(outs, [batch_size, -1])
    b = np.reshape(lables, [batch_size, -1])
    a_norm = np.sqrt(np.sum((np.square(a)), axis=1, keepdims=True))
    b_norm = np.sqrt(np.sum((np.square(b)), axis=1, keepdims=True))
    ab = np.sum((np.multiply(a, b)), axis=1, keepdims=True)
    cosin_value = np.divide(ab, np.multiply(a_norm, b_norm))
    cosin_value = cosin_value.mean()
    return cosin_value
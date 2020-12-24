# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\at_algorithm\core_algorithm.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 19536 bytes
from collections import defaultdict
import numpy as np, pandas as pd, atquant.data.const_data as const_da, atquant.data.global_variable as GVAR
from atquant.data.const_data import GACV

def atMatrixUnfillComplete(Matrix, bars_start_offset, prebar_len, perbars_volume_offset=GACV.KMatrix_Volume):
    """
    Matrix 为二维的numpy.ndarray结构，根据成交量计算前向补齐的参数
    rule 1、[GACV.KMatrixPos_Begin,GACV.KMatrixPos_End] 之间为Matrix的head部分,其中 GACV.KMatrixPos_Begin = 0
    rule 2、[GACV.KMatrixPos_End+1,Matrix.shape[0]) 之间为N个target的bar部分
    rule 3、[GACV.KMatrix_Bar_Begin-GACV.KMatrix_Bar_End] 为bar结构,其中gacv.KMatrix_Bar_Begin = 0

    :param Matrix: numpy.ndarray,需要计算的矩阵
    :param bars_start_offset: 需要跳过的开始行，见rule1，一般为：GACV.KMatrixPos_End+1
    :param prebar_len: int, 见rule3，一般为：GACV.KMatrix_Bar_End - GACV.KMatrix_Bar_Begin + 1
    :param perbars_volume_offset: int，根据成交量计算填充因子，一般为：GACV.KMatrix_Volume
    :return: 
            unFillRefs, list(numpy.ndarray[timelinelen],...),存储的是unFillIdxs的索引
            unFillIdxs  list(numpy.ndarray[N],...),存储的是Matrix的volume大于0的索引
    """
    rowM, timeLen = Matrix.shape
    targetLen = (rowM - bars_start_offset + 2) // prebar_len
    unFillRefs = [np.arange(timeLen, dtype=np.float) for i in range(targetLen)]
    unFillIdxs = [np.arange(timeLen, dtype=np.float) for i in range(targetLen)]
    for targetPos in range(targetLen):
        vol = GVAR.atKMatixBarItemPos(perbars_volume_offset, targetPos, contain_head=True)
        vol_lteq0 = Matrix[vol] < 0.1
        if np.nonzero(vol_lteq0)[0].shape[0] == 0:
            pass
        else:
            vol_gt0 = np.logical_not(vol_lteq0)
            unFillIdxs[targetPos] = np.argwhere(vol_gt0).flatten()
            unFillRefs[targetPos][vol_gt0] = np.arange(vol_gt0.sum())
            fillIdx = np.argwhere(vol_lteq0)
            preitem = -100
            for item in fillIdx:
                item = int(item)
                if item == preitem + 1:
                    unFillRefs[targetPos][item] = unFillRefs[targetPos][preitem]
                else:
                    _r = np.argwhere(unFillIdxs[targetPos] < item).flatten()
                    if _r.size > 0:
                        unFillRefs[targetPos][item] = _r[(-1)]
                    else:
                        unFillRefs[targetPos][item] = np.nan
                preitem = item

    return (
     unFillRefs, unFillIdxs)


def atFillKMatrixFreshBar(kmatrix):
    FreshBarArray = []
    _index = GACV.KMatrixPos_TimeLine
    _fresh = GVAR.g_ATraderDataValueFresh
    TimeLen = kmatrix.shape[1]
    if _fresh.size > 0:
        if len(_fresh[_index]) == TimeLen:
            FreshBarArray = list(range(0, TimeLen))
    else:
        _len = len(_fresh[_index])
        FreshBarArray = [0] * _len
        for i in range(_len):
            if i > 0:
                FreshBarArray[i] = FreshBarArray[(i - 1)]
            while FreshBarArray[i] < TimeLen - 1 and kmatrix[(_index, FreshBarArray[i])] < _fresh[(_index, i)]:
                FreshBarArray[i] = FreshBarArray[i] + 1

    return FreshBarArray


def ismember(A, B):
    """
    matlab equivalent ismember function
    matlab [Lia,Locb] = ismember(A,B)
    Lia 1若A中元素在B中，反之为0
    Locb 若A中元素在B中，取B最小索引，否则为0
    """
    bool_ind = np.isin(A, B)
    common = A[bool_ind]
    common_unique, common_inv = np.unique(common, return_inverse=True)
    b_unique, b_ind = np.unique(B, return_index=True)
    common_ind = b_ind[np.isin(b_unique, common_unique, assume_unique=True)]
    locb = common_ind[common_inv]
    return (bool_ind, locb)


def atFillToTimeLine(TimeLine, OrgMatrixs, iKFreq):
    """
    如果现有行情数据时间标签有缺失，则进行相应的填充。思路为，如果时间戳缺失，则使用前一根bar的相应数据进行填充

    :param TimeLine: numpy.array, 时间线，包含具体时间点的matlab浮点型时间数值
    :param OrgMatrixs: list, 每一项为kdata基础词典数据
    :param iKFreq: 频率的数字形式
    :return: numpy.ndarry
    """
    perbarlen = GVAR.atBarItemsLen()
    TargetLen = len(OrgMatrixs)
    KMatrix = np.zeros([TargetLen * GVAR.atBarItemsLen(), len(TimeLine)])
    _timeline = np.array(TimeLine)
    if iKFreq >= GACV.KFreq_Day:
        _timeline = np.floor(TimeLine)
    for targetIndex in range(TargetLen):
        if iKFreq >= GACV.KFreq_Day:
            matrixTime = np.floor(OrgMatrixs[targetIndex]['Time'].flatten())
        else:
            matrixTime = OrgMatrixs[targetIndex]['Time'].flatten()
        _K_O = GVAR.atKMatixBarItemPos(GACV.KMatrix_Open, targetIndex, False)
        _K_H = GVAR.atKMatixBarItemPos(GACV.KMatrix_High, targetIndex, False)
        _K_L = GVAR.atKMatixBarItemPos(GACV.KMatrix_Low, targetIndex, False)
        _K_C = GVAR.atKMatixBarItemPos(GACV.KMatrix_Close, targetIndex, False)
        _K_V = GVAR.atKMatixBarItemPos(GACV.KMatrix_Volume, targetIndex, False)
        _K_T = GVAR.atKMatixBarItemPos(GACV.KMatrix_TurnOver, targetIndex, False)
        _K_I = GVAR.atKMatixBarItemPos(GACV.KMatrix_OpenInterest, targetIndex, False)
        curDict = OrgMatrixs[targetIndex]
        if iKFreq >= GACV.KFreq_Sec:
            tmflag, timePos = ismember(_timeline, matrixTime)
            LoopIdx = np.where(tmflag == False)[0]
            KMatrix[(_K_O, tmflag)] = curDict['Open'].flatten()[timePos]
            KMatrix[(_K_H, tmflag)] = curDict['High'].flatten()[timePos]
            KMatrix[(_K_L, tmflag)] = curDict['Low'].flatten()[timePos]
            KMatrix[(_K_C, tmflag)] = curDict['Close'].flatten()[timePos]
            KMatrix[(_K_V, tmflag)] = curDict['Volume'].flatten()[timePos]
            KMatrix[(_K_T, tmflag)] = curDict['TurnOver'].flatten()[timePos]
            KMatrix[(_K_I, tmflag)] = curDict['OpenInterest'].flatten()[timePos]
            if LoopIdx.size > 0 and LoopIdx[0] == 0:
                KMatrix[(_K_O, 0)] = float('nan')
                KMatrix[(_K_H, 0)] = float('nan')
                KMatrix[(_K_L, 0)] = float('nan')
                KMatrix[(_K_C, 0)] = float('nan')
                KMatrix[(_K_I, 0)] = float('nan')
                KMatrix[(_K_V, 0)] = 0
                KMatrix[(_K_T, 0)] = 0
                LoopIdx = LoopIdx[1:]
            for k in LoopIdx:
                KMatrix[(_K_O, k)] = KMatrix[(_K_C, k - 1)]
                KMatrix[(_K_H, k)] = KMatrix[(_K_C, k - 1)]
                KMatrix[(_K_L, k)] = KMatrix[(_K_C, k - 1)]
                KMatrix[(_K_C, k)] = KMatrix[(_K_C, k - 1)]
                KMatrix[(_K_I, k)] = KMatrix[(_K_I, k - 1)]
                KMatrix[(_K_V, k)] = 0
                KMatrix[(_K_T, k)] = 0

        else:
            KMatrix[(_K_O, 0)] = float('nan')
            KMatrix[(_K_H, 0)] = float('nan')
            KMatrix[(_K_L, 0)] = float('nan')
            KMatrix[(_K_C, 0)] = float('nan')
            KMatrix[(_K_I, 0)] = float('nan')
            KMatrix[(_K_V, 0)] = 0
            KMatrix[(_K_T, 0)] = 0
            j = 0
            for i in range(len(TimeLine)):
                if i > 0:
                    KMatrix[(_K_O, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_H, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_L, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_C, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_I, i)] = KMatrix[(_K_I, i - 1)]
                    KMatrix[(_K_V, i)] = KMatrix[(_K_V, i - 1)]
                    KMatrix[(_K_T, i)] = KMatrix[(_K_T, i - 1)]
                if j < len(matrixTime):
                    while j < len(matrixTime) and matrixTime[j] <= TimeLine[i]:
                        KMatrix[(_K_O, i)] = curDict['Open'][j]
                        KMatrix[(_K_H, i)] = curDict['High'][j]
                        KMatrix[(_K_L, i)] = curDict['Low'][j]
                        KMatrix[(_K_C, i)] = curDict['Close'][j]
                        KMatrix[(_K_I, i)] = curDict['OpenInterest'][j]
                        KMatrix[(_K_V, i)] = curDict['Volume'][j]
                        KMatrix[(_K_T, i)] = curDict['TurnOver'][j]
                        j += 1

                elif i > 0:
                    KMatrix[(_K_O, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_H, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_L, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_C, i)] = KMatrix[(_K_C, i - 1)]
                    KMatrix[(_K_I, i)] = KMatrix[(_K_I, i - 1)]
                    KMatrix[(_K_V, i)] = 0
                    KMatrix[(_K_T, i)] = 0

    return KMatrix


def atCalculateTimeLineAndDayPos(StructDataArray):
    """
    回测频率为tick级别时，取所有标的的时间轴的并集作为全局刷新矩阵的时间轴，并将每天的开始用时间轴最长的那个标的的Beginbar进行匹配

    :param StructDataArray: 
    :return: 
    """
    if len(StructDataArray) < 1:
        raise ValueError(const_da.Enum_Const.ERROR_DATA_TICK_MISS.value)
    TimeLine = np.array([])
    maxArrayLen = 0
    dayBeginTarget = 0
    for i in range(len(StructDataArray)):
        TimeLine = np.union1d(TimeLine, StructDataArray[i]['Time'])
        if maxArrayLen < len(StructDataArray[i]['Time']):
            maxArrayLen = len(StructDataArray[i]['Time'])
            dayBeginTarget = i

    orgBeginBarPos, = np.where(StructDataArray[dayBeginTarget]['BeginBar'] == 1)
    beginbar = np.zeros(len(TimeLine))
    beginbarPos = np.zeros(len(orgBeginBarPos))
    DayPos = np.zeros(len(TimeLine))
    for i in range(len(orgBeginBarPos)):
        newPos = np.where(TimeLine == StructDataArray[dayBeginTarget]['Time'][orgBeginBarPos[i]])[0][0]
        beginbarPos[i] = newPos

    beginbarPos = beginbarPos.astype(np.int)
    beginbar[beginbarPos] = 1
    lastBegin = 0
    for i in range(len(TimeLine)):
        if beginbar[i] == 1:
            lastBegin = i
        DayPos[i] = i - lastBegin + 1

    return (TimeLine, DayPos)


def atCalculateReshIdxArray(BaseKDataMatrix, KFreNum):
    tmLen = BaseKDataMatrix.shape[1]
    idxFreshArray = np.zeros((tmLen,), dtype=np.bool)
    if GVAR.g_ATraderStraInputInfo.KFrequencyI <= GACV.KFreq_Min:
        dayPArray = np.where(BaseKDataMatrix[GACV.KMatrixPos_DayPos] == 1)[0]
        for i in range(tmLen):
            P = np.where(dayPArray <= i)[0]
            P_last = P[(-1)]
            if np.mod(i - dayPArray[P_last] + 1, KFreNum):
                idxFreshArray[i] = False
            else:
                idxFreshArray[i] = True

        dayFinishPos = dayPArray
        dayFinishPos = dayFinishPos[(dayFinishPos > 0)] - 1
        dayFinishPos = np.insert(dayFinishPos, len(dayFinishPos), tmLen - 1)
        idxFreshArray[dayFinishPos] = True
    else:
        idxFreshArray[:] = np.mod(np.arange(1, tmLen + 1), KFreNum) == 0
    return idxFreshArray


def accumarray(subs, val, shape, func):
    """
    模仿matlab之accumarray函数

    :param subs: 分组下标 
    :param val: 计算的值
    :param shape: tuple or None, 若shape不为None，则返回shape的numpy.ndarry，否则返回原始的numpy.ndarray形状
    :param func: 支持计算传入numpy.ndarry的函数，若为None，则默认使用 numpy.sum
    :return: numpy.ndarry
    :Example: 分组计算和
     .. code-block:: python
        :linenos:

        import atquant.at_algorithm.core_algorithm as CORE_ALGO
        subs = np.array([1,2,4,2,4])
        val=np.arange(4)
        CORE_ALGO.accumarray(subs, val, None, np.sum)
    ..
    """
    if not isinstance(val, np.ndarray):
        raise ValueError('val expect type numpy.ndarry got type %s' % type(val))
    if not isinstance(subs, np.ndarray):
        raise ValueError('subs expect type numpy.ndarry got type %s' % type(subs))
    if func is None:
        func = np.sum
    subs = subs.reshape(-1, 1).astype(np.int)
    val = val.ravel()
    if subs.shape[0] != val.shape[0]:
        raise ValueError('accumarray subs and val param need same count of row')
    d = defaultdict(list)
    df = pd.DataFrame(subs).fillna(-1).astype(np.int64)
    for i in range(subs.shape[0]):
        d[df.iloc[(i, 0)]].append(val[i])

    d.pop(-1, -1)
    del df
    result = np.array([np.nan] * (int(np.max(subs[:, 0])) + 1))
    for k, v in d.items():
        result[k] = func(v)

    if shape is not None:
        result = result.reshape(shape)
    return result


def atCalcBeginEndPos(ref_matrix_index, start_calc_pos=0):
    """
    历史矩阵列表词典存储的beginPos,endPos选项记录的是在ref_matrix中的索引位置

    :param ref_matrix_index: 表示某注册矩阵所依赖计算的矩阵在 GVAR.g_ATraderKDatas中的索引位置。
    :param start_calc_pos: 从beginPos开始计算的位置
    :return: beginPos，endPos
    """
    base0_matrix_tl = GVAR.g_ATraderKDatas[0].Matrix[GACV.KMatrixPos_TimeLine]
    ref_matrix_tl = GVAR.g_ATraderKDatas[ref_matrix_index].Matrix[GACV.KMatrixPos_TimeLine]
    CombinedLen = len(ref_matrix_tl)
    baseTimeLineLen = base0_matrix_tl.size
    targetTMPos = np.zeros((baseTimeLineLen,), dtype=np.int)
    beginPos = np.arange(baseTimeLineLen).astype(np.int)
    endPos = np.arange(baseTimeLineLen)
    for i in range(start_calc_pos, baseTimeLineLen):
        freshTM = base0_matrix_tl[i]
        if i > 0:
            targetTMPos[i] = targetTMPos[(i - 1)]
        while targetTMPos[i] < CombinedLen - 1 and ref_matrix_tl[targetTMPos[i]] < freshTM:
            targetTMPos[i] = targetTMPos[i] + 1

        while beginPos[i] > 0 and targetTMPos[(beginPos[i] - 1)] == targetTMPos[i]:
            beginPos[i] = beginPos[i] - 1

    return (
     beginPos, endPos)


def atCalcCombineMatrix1toN(bP, eP, ind_d, perbarLen, combinedMatrix, beginPos=0):
    np_fmax = np.fmax
    np_fmin = np.fmin
    matrix_cache = np.zeros((combinedMatrix.shape[0], 1))
    _O = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Open)]
    _H = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_High)]
    _L = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Low)]
    _C = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Close)]
    _V = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Volume)]
    _T = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_TurnOver)]
    _I = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_OpenInterest)]
    matrix_cache[:, 0] = combinedMatrix[:, 0]
    for i in range(beginPos, combinedMatrix.shape[1]):
        if bP[i] == eP[i]:
            matrix_cache[_H::perbarLen, 0] = combinedMatrix[_H::perbarLen, bP[i]]
            matrix_cache[_L::perbarLen, 0] = combinedMatrix[_L::perbarLen, bP[i]]
            matrix_cache[_V::perbarLen, 0] = combinedMatrix[_V::perbarLen, bP[i]]
            matrix_cache[_T::perbarLen, 0] = combinedMatrix[_T::perbarLen, bP[i]]
        else:
            combinedMatrix[_H::perbarLen, i] = np_fmax(matrix_cache[_H::perbarLen, 0], combinedMatrix[_H::perbarLen, eP[i]])
            combinedMatrix[_L::perbarLen, i] = np_fmin(matrix_cache[_L::perbarLen, 0], combinedMatrix[_L::perbarLen, eP[i]])
            combinedMatrix[_V::perbarLen, i] = matrix_cache[_V::perbarLen, 0] + combinedMatrix[_V::perbarLen, eP[i]]
            combinedMatrix[_T::perbarLen, i] = matrix_cache[_T::perbarLen, 0] + combinedMatrix[_T::perbarLen, eP[i]]
            matrix_cache[_H::perbarLen, 0] = combinedMatrix[_H::perbarLen, i]
            matrix_cache[_L::perbarLen, 0] = combinedMatrix[_L::perbarLen, i]
            matrix_cache[_V::perbarLen, 0] = combinedMatrix[_V::perbarLen, i]
            matrix_cache[_T::perbarLen, 0] = combinedMatrix[_T::perbarLen, i]

    combinedMatrix[_O::perbarLen, :] = combinedMatrix[_O::perbarLen, bP]
    combinedMatrix[_C::perbarLen, :] = combinedMatrix[_C::perbarLen, eP]
    combinedMatrix[_I::perbarLen, :] = combinedMatrix[_I::perbarLen, eP]
    return combinedMatrix[:, beginPos:]


def atCalcCombineMatrixHtoL(bP, eP, ind_d, perbarLen, combinedMatrix, base_matrix, beginPos=0):
    np_fmax = np.fmax
    np_fmin = np.fmin
    _O = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Open)]
    _H = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_High)]
    _L = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Low)]
    _C = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Close)]
    _V = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_Volume)]
    _T = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_TurnOver)]
    _I = ind_d[(GACV.KMatrixPos_End + 1 + GACV.KMatrix_OpenInterest)]
    matrix_cache = np.zeros((combinedMatrix.shape[0], 1))
    for i in range(beginPos, combinedMatrix.shape[1]):
        if bP[i] == eP[i]:
            matrix_cache[_H::perbarLen, 0] = base_matrix[_H::perbarLen, bP[i]]
            matrix_cache[_L::perbarLen, 0] = base_matrix[_L::perbarLen, bP[i]]
            matrix_cache[_V::perbarLen, 0] = base_matrix[_V::perbarLen, bP[i]]
            matrix_cache[_T::perbarLen, 0] = base_matrix[_T::perbarLen, bP[i]]
            combinedMatrix[_H::perbarLen, bP[i]] = matrix_cache[_H::perbarLen, 0]
            combinedMatrix[_L::perbarLen, bP[i]] = matrix_cache[_L::perbarLen, 0]
            combinedMatrix[_V::perbarLen, bP[i]] = matrix_cache[_V::perbarLen, 0]
            combinedMatrix[_T::perbarLen, bP[i]] = matrix_cache[_T::perbarLen, 0]
        else:
            combinedMatrix[_H::perbarLen, i] = np_fmax(matrix_cache[_H::perbarLen, 0], base_matrix[_H::perbarLen, eP[i]])
            combinedMatrix[_L::perbarLen, i] = np_fmin(matrix_cache[_L::perbarLen, 0], base_matrix[_L::perbarLen, eP[i]])
            combinedMatrix[_V::perbarLen, i] = matrix_cache[_V::perbarLen, 0] + base_matrix[_V::perbarLen, eP[i]]
            combinedMatrix[_T::perbarLen, i] = matrix_cache[_T::perbarLen, 0] + base_matrix[_T::perbarLen, eP[i]]
            matrix_cache[_H::perbarLen, 0] = combinedMatrix[_H::perbarLen, i]
            matrix_cache[_L::perbarLen, 0] = combinedMatrix[_L::perbarLen, i]
            matrix_cache[_V::perbarLen, 0] = combinedMatrix[_V::perbarLen, i]
            matrix_cache[_T::perbarLen, 0] = combinedMatrix[_T::perbarLen, i]

    combinedMatrix[_O::perbarLen, :] = base_matrix[_O::perbarLen, bP]
    combinedMatrix[_C::perbarLen, :] = base_matrix[_C::perbarLen, eP]
    combinedMatrix[_I::perbarLen, :] = base_matrix[_I::perbarLen, eP]
    return combinedMatrix[:, beginPos:]
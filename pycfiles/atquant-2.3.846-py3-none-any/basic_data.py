# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\data\basic_data.py
# Compiled at: 2018-08-27 20:45:25
# Size of source mod 2**32: 5289 bytes
import tempfile
from functools import lru_cache
from atquant.socket_ctrl.tool_box_command import *
from .const_data import atStringToConst

@lru_cache(None)
def root_sub_dir(sub=''):
    """
    获取数据文件夹路径
    :param sub: '','record','mat','test' 
    :return: 当为''时，返回文件夹目录的根目录，否则返回rootdir/sub
    """
    __root_dir = os.path.normpath(os.path.join(tempfile.gettempdir(), 'Bitpower'))
    sub = sub if sub in ('', 'record', 'mat', 'test') else 'test'
    return os.path.normpath(os.path.join(__root_dir, sub))


def GetCurrentFreshBar(targetIdx):
    Idx = GACV.KMatrixPos_End + targetIdx * GVAR.atBarItemsLen()
    _dict = GVAR.g_ATraderKDatas[GVAR.g_ATraderStraInputInfo.FreshMatrixIdx]
    freshBar = _dict.CurrentBar[GVAR.g_ATraderSimCurBarFresh]
    open_price = _dict.Matrix[(Idx + GACV.KMatrix_Open, freshBar)]
    high_price = _dict.Matrix[(Idx + GACV.KMatrix_High, freshBar)]
    low_price = _dict.Matrix[(Idx + GACV.KMatrix_Low, freshBar)]
    close_price = _dict.Matrix[(Idx + GACV.KMatrix_Close, freshBar)]
    volume = _dict.Matrix[(Idx + GACV.KMatrix_Volume, freshBar)]
    return (open_price, high_price, low_price, close_price, volume)


def GetFreshBarByOffset(targetIdx, offset):
    """
    获取 g_ATraderStraInputInfo['FreshMatrixIdx'] 所在  g_ATraderKDatas 中 Matrix 中标的的 open, high, low, close, volume, 返回变量类型为 pandas.Series
    :param targetIdx: numpy.array, 在 Matrix 中标的开始索引计算的位置
    :param offset: int, 相对于当前 g_ATraderSimCurBarFresh 的偏移量
    :return: [open, high, low, close, volume]
    """
    if isinstance(targetIdx, np.ndarray):
        Idx = (GVAR.atBarHeadLen() + targetIdx * GVAR.atBarItemsLen()).astype(np.int)
    else:
        Idx = int(GVAR.atBarHeadLen() + targetIdx * GVAR.atBarItemsLen())
    freshmatrixidx = GVAR.g_ATraderStraInputInfo.FreshMatrixIdx
    currentbar = GVAR.g_ATraderKDatas[freshmatrixidx]['CurrentBar']
    freshBar = np.array([currentbar[(GVAR.g_ATraderSimCurBarFresh + offset)]])
    open = GVAR.g_ATraderKDatas[freshmatrixidx].Matrix[(Idx + GACV.KMatrix_Open, freshBar)]
    high = GVAR.g_ATraderKDatas[freshmatrixidx].Matrix[(Idx + GACV.KMatrix_High, freshBar)]
    low = GVAR.g_ATraderKDatas[freshmatrixidx].Matrix[(Idx + GACV.KMatrix_Low, freshBar)]
    close = GVAR.g_ATraderKDatas[freshmatrixidx].Matrix[(Idx + GACV.KMatrix_Close, freshBar)]
    volume = GVAR.g_ATraderKDatas[freshmatrixidx].Matrix[(Idx + GACV.KMatrix_Volume, freshBar)]
    return [
     open, high, low, close, volume]


def base_matrix_index(freq, freqnum):
    """
    freq = atStringToConst('KBaseFreq', KFrequency)
    KFrequency包含:'tick', 'day', 'sec', 'min' 
    :param freq: int 或者 str ,若为int类型，则返回值是atStringToConst('KBaseFreq', KFrequency)的返回值.若为str类型，则为KFrequency代表的值
    :param freqnum: int, 频数。比如
    :return: 目标所在矩阵链的索引,若不存在，返回None
    eg:
        base_matrix_index('min',1)
        base_matrix_index(2,1)
    """
    if isinstance(freq, str):
        freq = atStringToConst('KBaseFreq', freq)
    else:
        freq = int(freq)
    for i, kdata in enumerate(GVAR.g_ATraderKDatas):
        if kdata['iFreq'] == freq and kdata['FreqNum'] == freqnum:
            return i


def generate_base_dataframe(ntarget, timelinelen):
    """
    创建一个基础DataFrame结构，可以容纳n个标的信息
    :param ntarget: int,标的数据
    :param timelinelen: int,时间线长度
    :return: DataFrame
    """
    kmatrixpos_end = GACV.KMatrixPos_End
    kmatrix_bar_begin = GACV.KMatrix_Bar_Begin
    kmatrix_bar_end = GACV.KMatrix_Bar_End
    kmatrixpos_timeline = GACV.KMatrixPos_TimeLine
    kmatrixpos_freshidx = GACV.KMatrixPos_FreshIdx
    kmatrixpos_daypos = GACV.KMatrixPos_DayPos
    index = [kmatrixpos_timeline, kmatrixpos_freshidx, kmatrixpos_daypos]
    begin = kmatrixpos_end + kmatrix_bar_begin
    end = begin + ntarget * (kmatrix_bar_end - kmatrix_bar_begin + 1)
    index.extend(range(begin, end, 1))
    df = pd.DataFrame(np.zeros((kmatrixpos_end + ntarget * kmatrix_bar_end, timelinelen)), index=index)
    return df
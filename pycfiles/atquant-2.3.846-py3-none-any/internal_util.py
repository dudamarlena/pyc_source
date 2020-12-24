# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\internal_util.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 13921 bytes
import datetime, errno, hashlib, os, shutil, uuid
from functools import wraps, partial
import numpy as np, scipy.io as sio, atquant
from atquant.utils.logger import logger, write_syslog

def hashmd5_to_int(src, slice=8):
    """
    将字符串经过MD5编码的16进制切片后转为10进制数据
    :param src: 原始字符串,可以是bytes或者str类型 
    :param slice: 返回16进制列表切片的长度，即[:slice]
    :return: 转为int型的值
    """
    hash_obj = hashlib.md5()
    if isinstance(src, bytes):
        hash_obj.update(src)
    else:
        hash_obj.update(src.encode('utf-8'))
    value = hash_obj.hexdigest()
    if len(value) < abs(slice) or slice == 0:
        raise ValueError('slice param between %d and %d' % (1, len(value)))
    int_value = int(hash_obj.hexdigest()[:slice], 16)
    return int_value


def random_file_name(prefix='', suffix=''):
    """
    产生文件名称
    :param prefix: 文件名的前缀,字符串类型 
    :param suffix: 文件名的后缀，字符串类型
    :return: 合成的文件名称
    """
    prefix = prefix if isinstance(prefix, str) else ''
    suffix = prefix if isinstance(suffix, str) else ''
    middle = hashmd5_to_int(str(uuid.uuid4()), 8)
    return '%s%s%s' % (prefix, middle, suffix)


def remove_and_makedirs(dir):
    """
    如果存在dir路径，则先删除该路径，并重新创建目录
    :param dir: 本地路径,str类型
    :return: 当路径非法时,将会raise FileNotFoundError/AttributeError
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)


def load_mat(matFile, error='raise'):
    """
     加载mat文件,并raise指定错误
     
    :param matFile: mat文件路径
    :param error: 'ignore' or 'raise'
    :return: dict or raise Error
    """
    result = {}
    try:
        if isinstance(matFile, str) and os.path.exists(matFile):
            result = sio.loadmat(matFile)
            return result
    except Exception as e:
        if error == 'raise':
            raise OSError("can't open file: {!r}".format(matFile))

    return result


def save_mat(matFile, data, **kwargs):
    """
    保存文件为matlab的mat文件
    
    :param matFile: 文件路径
    :param data: dict 或者 list of dict
    ::
    
        若为列表词典时，kwargs 必须包含可能关键字为scipy.io.savemat 
        另外包含 'struct_name',表示结构体名称，默认为'KArray'
    ..
    """
    if isinstance(data, dict):
        sio.savemat(matFile, data, **kwargs)
    else:
        if isinstance(data, list) and len(data) > 0:
            KEY = 'struct_name'
            struct_name = kwargs.get(KEY, 'KArray')
            if KEY in kwargs:
                kwargs.pop(KEY)
            dtype = np.dtype([(str(key), 'O') for key in data[0]])
            datas = []
            for item in data:
                t = [v for _, v in item.items()]
                datas.append(tuple(t))

            _data = {'KArray': np.array(datas, dtype=dtype)}
            sio.savemat(matFile, _data, **kwargs)
        else:
            raise Exception('Not support data format')


def run_ignore_exception(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        write_syslog(str(e), level='warn')


def nppd_empty_test(data):
    """
    测试numpy 或者pandas 数据结构是否为空
    若data = 5，此时会出现异常
    
    :return 为空返回True，否则返回False 
    """
    if not isinstance(data, type(None)):
        if hasattr(data, 'size') and data.size > 0:
            return False
        if hasattr(data, 'empty') and not data.empty:
            return False
        if hasattr(data, '__len__'):
            if len(data) > 0:
                return False
            return True
        return not data
    return True


def nppd_nonempty_test(data):
    return not nppd_empty_test(data)


class SimpleTimer:
    __doc__ = "\n    简单时间计时器最高精度为毫秒(ms)\n    eg:\n    t = SimpleTimer('your tips',unit='ms')    \n    print(t)\n    "
    _unit_maps = {'year': ['年', 31536000000], 
     'mon': ['月', 2592000000], 
     'day': ['日', 86400000], 
     'hour': ['时', 3600000], 
     'min': ['分', 60000], 
     'sec': ['秒', 1000], 
     'ms': ['毫秒', 1]}

    def __init__(self, prompt='', unit='sec', start=True):
        """
        :param prompt: 提示信息,str类型  
        :param unit: 'year','mon','day','hour','min','sec','ms' 
        """
        self.start_time = None
        self.reset(prompt, unit)
        if start:
            self.start()

    def __str__(self):
        if self.running:
            format_elapsed_time = self.total()
        else:
            format_elapsed_time = self.elapsed
        return self.prompt + ' %d %s' % (format_elapsed_time, self.chs_unit)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def total(self):
        self._raise_not_start()
        end_time = datetime.datetime.now()
        elapsed_time = end_time - self.start_time
        divisor = SimpleTimer._unit_maps.get('sec')[0]
        if self.unit in SimpleTimer._unit_maps:
            divisor = SimpleTimer._unit_maps.get(self.unit, ['秒', 1000])[1]
        total_milliseconds = elapsed_time.days * 86400000 + elapsed_time.seconds * 1000 + elapsed_time.microseconds / 1000
        format_elapsed_time = total_milliseconds / divisor
        return format_elapsed_time

    def start(self):
        self._raise_started()
        self.start_time = datetime.datetime.now()

    def stop(self):
        self._raise_not_start()
        self.elapsed += self.total()
        self.start_time = None

    def reset(self, prompt=None, unit=None):
        if prompt is not None:
            self.prompt = prompt
        if unit is not None:
            self.unit = unit
        if self.unit not in SimpleTimer._unit_maps:
            self.unit = 'sec'
        self.elapsed = 0

    def restart(self, prompt=None, unit=None):
        self.reset(prompt=prompt, unit=unit)
        if self.running:
            self.stop()
        self.start()

    def _raise_not_start(self):
        if not self.running:
            raise RuntimeError('Not started')

    def _raise_started(self):
        if self.running:
            raise RuntimeError('Already started')

    @property
    def chs_unit(self):
        unit = SimpleTimer._unit_maps.get(self.unit, '秒')[0]
        return unit

    @property
    def running(self):
        return self.start_time is not None


def trace_time(func=None, *, unit='ms', debug=False, prompt=None, output=logger.info):
    if func is None:
        return partial(trace_time, unit=unit, debug=debug, prompt=prompt, output=output)
    if prompt is None:
        prompt = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        if atquant.TRACE_DEBUG or debug:
            t = SimpleTimer(func.__name__, unit)
            output('Begin Function ' + prompt)
            result = func(*args, **kwargs)
            output(t)
            output('End Function ' + prompt)
            del t
            return result
        else:
            return func(*args, **kwargs)

    return wrapper


def trace_cmd(func=None, *, debug=False, prompt=None, output=logger.info):
    """
    记录给AT发送命令的logger。

    若自动记录cmd命令，需要在被装饰函数内部第一条语句定义:  cmd = 'ATraderCloseOperation' 类似的语句
    """
    if func is None:
        return partial(trace_cmd, debug=debug, prompt=prompt, output=output)
    if prompt is None:
        var_name = 'cmd'
        if var_name in func.__code__.co_varnames:
            index = func.__code__.co_varnames.index(var_name) - func.__code__.co_argcount + 1
        if 0 < index < len(func.__code__.co_consts):
            prompt = func.__code__.co_consts[index]
    else:
        prompt = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        if atquant.TRACE_DEBUG or debug:
            output('Begin Cmd %s' % prompt)
            result = func(*args, **kwargs)
            output('End Cmd %s' % prompt)
            return result
        else:
            return func(*args, **kwargs)

    return wrapper


def error_param(funcname, paramname, detail):
    """
    返回形如: "funcname 参数 value 值需要大于10的整数" 
    :param funcname: str,函数名称
    :param paramname: str,参数名称
    :param detail: str,错误详情
    :return: 合成的字符串
    """
    return '%s 参数 %s %s' % (funcname, paramname, detail)


def unwrapper(func):
    f2 = func
    while 1:
        f = f2
        f2 = getattr(f2, '__wrapped__', None)
        if f2 is None:
            break

    return f


def append_or_join_df(src_df, append_df, axis=0, drop=False, rest=True, drop_errors='ignore'):
    """
    删除 src_df  中与 append_df 相同 axis 部分，生成 df，并将 append_df 添加到 df 中，不改变 src_df
    :param src_df: 源pandas.DataFrame
    :param append_df: 追加的pandas.DataFram
    :param axis: int, axis=0或者axis=1
    :param drop: bool, 是否需要删掉相同列/行
    :param rest: bool, 是否需要重新排列列/行
    :param drop_errors: str, 可为:'ignore', 'raise'
    :return: pandas.DataFrame,合并后的pandas.DataFrame
    """

    def intersection(list1, list2):
        return [i for i in list1 if i in list2]

    if drop:
        if axis == 0:
            arr = intersection(list(src_df.index), list(append_df.index))
        else:
            arr = intersection(list(src_df.columns), list(append_df.columns))
        df = src_df.drop(arr, axis=axis, errors=drop_errors)
    else:
        df = src_df
    if axis == 0:
        df = df.append(append_df)
    else:
        df = df.join(append_df, rsuffix='_r')
    if rest:
        df = df.sort_index(axis=axis)
    return df


def append_or_assign_2d_array_axis0(arr, values, pos):
    axis = 0
    assert pos >= 0, 'Only support pos>=0 value'
    assert len(values.shape) <= 2 and len(values.shape) >= 1, 'Values shape not right'
    if len(values.shape) != 2:
        values = values.reshape(1, values.shape[0])
    if len(arr.shape) != 2:
        if arr.size < 1 or arr.size < values.shape[1]:
            arr = values.copy()
            return arr
        arr = arr.reshape((1, arr.size))
    if arr.shape[axis] > pos:
        if arr.shape[axis] + 1 >= pos + values.shape[axis]:
            arr[pos:pos + values.shape[0]] = values[:]
        else:
            _t = arr.shape[0] - pos
            arr[pos:] = values[:_t]
            arr = np.concatenate((arr, values[_t:]), axis=axis)
    else:
        arr = np.concatenate((arr, values), axis=axis)
    return arr


def append_or_assign_2d_array_axis1(arr, values, pos):
    axis = 1
    assert pos >= 0, 'Only support pos>=0 value'
    assert len(values.shape) <= 2 and len(values.shape) >= 1, 'Values shape not right'
    if len(values.shape) != 2:
        values = values.reshape(values.shape[0], 1)
    if len(arr.shape) != 2:
        if arr.size < 1 or arr.size < values.shape[0]:
            arr = values.copy()
            return arr
        arr = arr.reshape((arr.size, 1))
    if arr.shape[axis] > pos:
        if arr.shape[axis] + 1 >= pos + values.shape[axis]:
            arr[:, pos:pos + values.shape[0]] = values[:, :]
        else:
            _t = arr.shape[0] - pos
            arr[:, pos:] = values[:, :_t]
            arr = np.concatenate((arr, values[:, _t:]), axis=axis)
    else:
        arr = np.concatenate((arr, values), axis=axis)
    return arr


def format_atquant_log(file_or_str, output=print):
    import re
    if isinstance(file_or_str, str):
        temp = file_or_str
    else:
        temp = file_or_str.read()
    results = re.findall('(Begin.+)|(End.+)', temp, re.I | re.M)
    ls, ls2 = [], []
    for item in results:
        line = item[0] if item[0] else item[1]
        if line.startswith('Begin'):
            it = (
             len(ls), line)
            ls.append(it)
            ls2.append(it)
        elif len(ls) > 0:
            begin_s = ls[(-1)][1].split(' ', 2)[(-1)]
            end_s = line.split(' ', 2)[(-1)]
            if begin_s == end_s:
                info = ls.pop()
                ls2.append((info[0], line))

    if output is print:
        for i, item in enumerate(ls2):
            tabs = '\t' * item[0]
            if i + 1 < len(ls2) and item[0] == ls2[(i + 1)][0] and item[1].startswith('End') and ls2[(i + 1)][1].startswith('Begin'):
                output('%s%s\n' % (tabs, item[1]))
            else:
                output('%s%s' % (tabs, item[1]))

    else:
        for i, item in enumerate(ls2):
            tabs = '\t' * item[0]
            if i + 1 < len(ls2) and item[0] == ls2[(i + 1)][0] and item[1].startswith('End') and ls2[(i + 1)][1].startswith('Begin'):
                output('%s%s\n\n' % (tabs, item[1]))
            else:
                output('%s%s\n' % (tabs, item[1]))
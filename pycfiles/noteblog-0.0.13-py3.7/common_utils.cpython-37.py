# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/common_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 12892 bytes
import re, base64, os, io
from random import randint
from pprint import pprint
from functools import wraps
from time import sleep
from json import loads, JSONDecodeError
from demjson import decode
from gc import collect
from spider.bloom_utils import BloomFilter
__all__ = [
 'json_2_dict',
 '_green',
 'delete_list_null_str',
 'list_duplicate_remove',
 'len_pro',
 'deal_with_JSONDecodeError_about_value_invalid_escape',
 '_print',
 'get_random_int_number',
 'wash_sensitive_info',
 'save_base64_img_2_local',
 'save_obj',
 'get_obj',
 'retry',
 'list_remove_repeat_dict_plus_by_bloom_filter']

def json_2_dict(json_str, logger=None, encoding=None, default_res=None):
    """
    json字符串转dict
    :param json_str:
    :param logger:
    :param encoding: 解码格式
    :param default_res: 默认返回结果
    :return:
    """
    _ = default_res if default_res is not None else {}
    if json_str is None:
        return _
    try:
        _ = loads(json_str)
    except JSONDecodeError:
        try:
            _ = decode(json_str, encoding=encoding)
        except Exception as e:
            try:
                _print(msg='遇到json解码错误!', logger=logger, log_level=2, exception=e)
            finally:
                e = None
                del e

    return _


def _green(string):
    """
    将字体转变为绿色
    :param string:
    :return:
    """
    return '\x1b[32m{}\x1b[0m'.format(string)


def delete_list_null_str(_list):
    """
    删除list中的所有空str
    :param _list:
    :return:
    """
    while '' in _list:
        _list.remove('')

    return _list


def list_duplicate_remove(_list: list):
    """
    list去重
    :param _list:
    :return:
    """
    b = []
    [b.append(i) for i in _list if i not in b]
    return b


def deal_with_JSONDecodeError_about_value_invalid_escape(json_str):
    """
    ValueError: Invalid \\escape: line 1 column 35442 (char 35441)
    问题在于编码中是\xa0之类的，当遇到有些 不用转义的\\http之类的，则会出现以上错误。
    :param json_str:
    :return: 正常的str类型的json字符串
    """
    return re.compile('\\\\(?![/u"])').sub('\\\\\\\\', json_str)


def _print(**kwargs):
    """
    fz的输出方式(常规print or logger打印)
        可传特殊形式:
            eg: _print(exception=e, logger=logger)  # logger可以为None
    :param kwargs:
    :return: None
    """
    msg = kwargs.get('msg', None)
    logger = kwargs.get('logger', None)
    log_level = kwargs.get('log_level', 1)
    exception = kwargs.get('exception', None)
    if logger is None:
        if exception is None:
            print(msg)
        elif msg is not None:
            print(msg, exception)
        else:
            print(exception)
    elif msg is not None:
        if isinstance(msg, str):
            if isinstance(log_level, int):
                if log_level == 1:
                    logger.info(msg)
                elif log_level == 2:
                    logger.error(msg)
                else:
                    raise ValueError('log_level没有定义该打印等级!')
            else:
                raise TypeError('log_level类型错误!')
        else:
            raise TypeError('log模式打印时, msg必须是str!')
    elif exception is not None:
        if isinstance(exception, Exception):
            logger.exception(exception)
        else:
            raise TypeError('exception必须是Exception类型!')
    return True


def get_random_int_number(start_num=0, end_num=1000):
    """
    得到一个随机的int数字
    :param start_num:
    :param end_num:
    :return:
    """
    return randint(start_num, end_num)


def wash_sensitive_info(data, replace_str_list=None, add_sensitive_str_list=None):
    """
    清洗敏感字符
    :param data: 待清洗的str
    :param replace_str_list: 需要被替换的list(会被替换为元组中的第2个元素) eg: [('123', '456'), ...]
    :param add_sensitive_str_list: 增加的过滤敏感词汇(会被替换为'') eg: ['123', '456', ...]
    :return: a str
    """
    data = data.lower()
    if replace_str_list is not None:
        if isinstance(replace_str_list, list):
            for item in replace_str_list:
                try:
                    before_str = '{0}'.format(item[0]).lower()
                    end_str = '{0}'.format(item[1]).lower()
                except IndexError:
                    raise IndexError('获取replace_str_list的子元素时索引异常, 请检查!')

                data = re.compile(before_str).sub(end_str, data)

        else:
            raise TypeError('replace_str只支持list类型! eg: [("123", "456"), ...]')
    elif add_sensitive_str_list is not None:
        if isinstance(add_sensitive_str_list, list):
            for item in add_sensitive_str_list:
                try:
                    data = re.compile('{0}'.format(item).lower()).sub('', data)
                except:
                    continue

    else:
        raise TypeError('add_sensitive_str_list只支持list类型! eg: ["123", "456", ...]')
    tmp_str = '\n    淘宝|taobao|TAOBAO|天猫|tmall|TMALL|\n    京东|JD|jd|红书爸爸|共产党|邪教|艹|折800|\n    杀人|胡锦涛|江泽民|习近平|小红薯|毛泽东|\n    拉粑粑\n    '.replace(' ', '').replace('\n', '')
    data = re.compile(tmp_str).sub('', data)
    data = re.compile('\\xa0').sub(' ', data)
    return data


def save_base64_img_2_local(save_path, base64_img_str):
    """
    存储类似data:image/jpg;base64,xxxxxx的图片到本地
    :param save_path: 存储的路径
    :param base64_img_str:
    :return:
    """
    try:
        base64_img_str = base64_img_str[base64_img_str.find(',') + 1:]
        with open(save_path, 'wb') as (f):
            base64_img_str = base64.b64decode(base64_img_str)
            f.write(base64_img_str)
        return True
    except Exception as e:
        try:
            print(e)
            return False
        finally:
            e = None
            del e


def len_pro(obj):
    """
    获取具有 __len__, len, fileno, tell 等属性的对象的长度, 比如: list, tuple, dict, file and so on
    :param obj:
    :return: 长度 int
    """
    total_length = None
    current_position = 0
    if hasattr(obj, '__len__'):
        total_length = len(obj)
    else:
        if hasattr(obj, 'len'):
            total_length = obj.len
        else:
            if hasattr(obj, 'fileno'):
                try:
                    fileno = obj.fileno()
                except io.UnsupportedOperation:
                    pass
                else:
                    total_length = os.fstat(fileno).st_size
            elif hasattr(obj, 'tell'):
                try:
                    current_position = obj.tell()
                except (OSError, IOError):
                    if total_length is not None:
                        current_position = total_length

                if hasattr(obj, 'seek') and total_length is None:
                    try:
                        obj.seek(0, 2)
                        total_length = obj.tell()
                        obj.seek(current_position or 0)
                    except (OSError, IOError):
                        total_length = 0

            if total_length is None:
                total_length = 0
            return max(0, total_length - current_position)


def save_obj(obj, file_name):
    """
    将对象持久化到本地, 方便直接调试
    :param obj:
    :param file_name:
    :return:
    """
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    pickle.dump(obj, open(file_name, 'w'))


def get_obj(file_name):
    """
    使用该持久化对象进行调试
    :param file_name:
    :return:
    """
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    return pickle.load(open(file_name))


class StopRetry(Exception):

    def __repr__(self):
        return 'retry stop!'


def retry(max_retries, delay: (int, float)=0, callback=None, validate_func=None):
    """
    函数执行出现异常时自动重试的装饰器
    :param max_retries: 最多重试次数
    :param delay: 每次重试的延迟, 单位秒
    :param callback: 回调函数, 函数签名应接收一个参数, 每次出现异常时, 会将异常对象传入
    :param validate_func: 验证函数, 用于验证执行结果, 并确定是否继续重试
    :return: 被装饰函数的执行结果
    """

    def decorated(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal max_retries
            func_ex = StopRetry
            while 1:
                if max_retries > 0:
                    try:
                        try:
                            result = func(*args, **kwargs)
                            if not callable(validate_func):
                                if max_retries <= 1:
                                    return result
                                continue
                            else:
                                if validate_func(result) is False:
                                    continue
                                else:
                                    return result
                        except Exception as e:
                            try:
                                if callable(callback):
                                    if callback(e) is True:
                                        return
                                func_ex = e
                            finally:
                                e = None
                                del e

                    finally:
                        max_retries -= 1
                        if delay > 0:
                            sleep(delay)

            else:
                raise func_ex

        return wrapper

    return decorated


def list_remove_repeat_dict_plus_by_bloom_filter(target: list, repeat_key: str, capacity=100000, error_rate=0.0001) -> list:
    """
    通过bloom list 子元素为dict的去重plus
    :param target:
    :param repeat_key:
    :param capacity: 容器大小
    :param error_rate: 错误率
    :return:
    """
    bloom_filter = BloomFilter(capacity=capacity, error_rate=error_rate)
    res_list = []
    for item in target:
        repeat_key_value = item.get(repeat_key)
        if repeat_key_value is not None and repeat_key_value not in bloom_filter:
            res_list.append(item)
            bloom_filter.add(repeat_key_value)

    try:
        del bloom_filter
    except:
        pass

    collect()
    return res_list
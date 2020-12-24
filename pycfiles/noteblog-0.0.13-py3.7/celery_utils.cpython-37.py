# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/celery_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 7365 bytes
"""
@author = super_fazai
@File    : celery_utils.py
@connect : superonesfazai@gmail.com
"""
from time import time
from celery import Celery
from celery.utils.log import get_task_logger
from .common_utils import _print
from .time_utils import fz_set_timeout
__all__ = [
 'init_celery_app',
 'block_get_celery_async_results',
 '_get_celery_async_results',
 'get_current_all_celery_handled_results_list']
DEFAULT_CELERY_ACCEPT_CONTENT = [
 'pickle', 'json']

def init_celery_app(name='proxy_tasks', broker='redis://127.0.0.1:6379', backend='redis://127.0.0.1:6379/0', logger=None, timezone='Asia/Shanghai', task_acks_late=True, accept_content=None, task_serializer='pickle', result_serializer='pickle', celeryd_max_tasks_per_child=200, result_expires=3600, task_soft_time_limit=None, task_time_limit=None, worker_log_color=True) -> Celery:
    """
    初始化一个celery对象
    :param name: 创建一个celery实例, 名叫name
    :param broker: 指定消息中间件 格式: 'transport://userid:password@hostname:port/virtual_host'
    :param backend: 指定存储 格式同上
    :param logger: 最佳实践是在模块的顶层，为你的所有任务创建一个共用的logger
    :param timezone: 默认:'UTC', 配置Celery以使用自定义时区, 时区值可以是pytz支持的任何时区
    :param task_acks_late: 意味着任务消息将在任务执行后被确认，而不仅仅是在执行之前, 默认: False
    :param accept_content: 允许的内容类型/序列化的白名单, 默认: ['json',]
    :param task_serializer: 标识要使用的默认序列化方法的字符串(自4.0起:默认为'json', 早期为:'pickle')('pickle'是一种Python特有的自描述的数据编码, 可序列化自定义对象)
    :param result_serializer: 标识结果序列化的格式(自4.0起:默认为'json', 早期为:'pickle')
    :param celeryd_max_tasks_per_child: 表示每个工作的进程／线程／绿程 在执行 n 次任务后，主动销毁，之后会起一个新的。主要解决一些资源释放的问题。
    :param result_expires: 存储的任务结果在过期后会被删除, 单位s, 默认值: 1天
    :param task_soft_time_limit: 任务软时间限制, 单位s, celery执行任务时, 超过软时间限制, 就在任务中抛出SoftTimeLimitExceeded(from celery.exceptions import SoftTimeLimitExceeded)
    :param task_time_limit: 任务困难时间限制, 单位s, 处理任务的worker将被杀死并在超出此任务时替换为新任务, 实际在task运用: eg: @app.task(time_soft_limit=60, time_limit=120, rate_limit='200/m')
    :param worker_log_color: 启用/禁用Celery程序记录输出中的颜色, bool类型
    :return:
    """
    app = Celery(name,
      broker=broker,
      backend=backend,
      log=logger)
    app.conf.update(CELERY_TIMEZONE=timezone,
      CELERY_ACKS_LATE=task_acks_late,
      CELERY_ACCEPT_CONTENT=(DEFAULT_CELERY_ACCEPT_CONTENT if accept_content is None else accept_content),
      CELERY_TASK_SERIALIZER=task_serializer,
      CELERY_RESULT_SERIALIZER=result_serializer,
      CELERYD_FORCE_EXECV=True,
      CELERYD_MAX_TASKS_PER_CHILD=celeryd_max_tasks_per_child,
      CELERY_TASK_RESULT_EXPIRES=result_expires,
      CELERYD_TASK_SOFT_TIME_LIMIT=task_soft_time_limit,
      CELERYD_TASK_TIME_LIMIT=task_time_limit,
      CELERYD_LOG_COLOR=worker_log_color,
      BROKER_HEARTBEAT=0)
    return app


def block_get_celery_async_results(tasks: list, r_timeout=2.5, func_timeout=1800) -> list:
    """
    得到celery worker的处理结果集合
    :param tasks: celery的tasks任务对象集
    :param r_timeout:
    :param func_timeout: 函数执行超时时间, 单位秒
    :return:
    """

    @fz_set_timeout(seconds=func_timeout)
    def get_res--- This code section failed: ---

 L.  94         0  BUILD_LIST_0          0 
                2  STORE_FAST               'all'

 L.  95         4  LOAD_CONST               1
                6  STORE_FAST               'success_num'

 L.  96         8  SETUP_LOOP          208  'to 208'
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'tasks'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  LOAD_CONST               0
               18  COMPARE_OP               >
               20  POP_JUMP_IF_FALSE   206  'to 206'

 L.  97        22  SETUP_LOOP          204  'to 204'
               24  LOAD_GLOBAL              enumerate
               26  LOAD_FAST                'tasks'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  GET_ITER         
               32  FOR_ITER            202  'to 202'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'r_index'
               38  STORE_FAST               'r'

 L.  98        40  SETUP_EXCEPT        158  'to 158'

 L.  99        42  LOAD_FAST                'r'
               44  LOAD_METHOD              ready
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  POP_JUMP_IF_FALSE   154  'to 154'

 L. 100        50  SETUP_EXCEPT         96  'to 96'

 L. 101        52  LOAD_FAST                'all'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'r'
               58  LOAD_ATTR                get
               60  LOAD_DEREF               'r_timeout'
               62  LOAD_CONST               False
               64  LOAD_CONST               ('timeout', 'propagate')
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  POP_TOP          

 L. 102        72  LOAD_GLOBAL              print
               74  LOAD_STR                 '\r--->>> success_num: {}'
               76  LOAD_METHOD              format
               78  LOAD_FAST                'success_num'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  LOAD_STR                 ''
               84  LOAD_CONST               True
               86  LOAD_CONST               ('end', 'flush')
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  POP_TOP          
               92  POP_BLOCK        
               94  JUMP_FORWARD        116  'to 116'
             96_0  COME_FROM_EXCEPT     50  '50'

 L. 103        96  DUP_TOP          
               98  LOAD_GLOBAL              TimeoutError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   114  'to 114'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 104       110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM           102  '102'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'
            116_1  COME_FROM            94  '94'

 L. 105       116  LOAD_FAST                'success_num'
              118  LOAD_CONST               1
              120  INPLACE_ADD      
              122  STORE_FAST               'success_num'

 L. 106       124  SETUP_EXCEPT        140  'to 140'

 L. 107       126  LOAD_FAST                'tasks'
              128  LOAD_METHOD              pop
              130  LOAD_FAST                'r_index'
              132  CALL_METHOD_1         1  '1 positional argument'
              134  POP_TOP          
              136  POP_BLOCK        
              138  JUMP_ABSOLUTE       154  'to 154'
            140_0  COME_FROM_EXCEPT    124  '124'

 L. 108       140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 109       146  POP_EXCEPT       
              148  JUMP_ABSOLUTE       154  'to 154'
              150  END_FINALLY      
              152  JUMP_FORWARD        154  'to 154'
            154_0  COME_FROM           152  '152'
            154_1  COME_FROM            48  '48'

 L. 111       154  POP_BLOCK        
              156  JUMP_BACK            32  'to 32'
            158_0  COME_FROM_EXCEPT     40  '40'

 L. 112       158  DUP_TOP          
              160  LOAD_GLOBAL              Exception
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   198  'to 198'
              166  POP_TOP          
              168  STORE_FAST               'e'
              170  POP_TOP          
              172  SETUP_FINALLY       186  'to 186'

 L. 114       174  LOAD_GLOBAL              print
              176  LOAD_FAST                'e'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  POP_TOP          

 L. 115       182  BUILD_LIST_0          0 
              184  RETURN_VALUE     
            186_0  COME_FROM_FINALLY   172  '172'
              186  LOAD_CONST               None
              188  STORE_FAST               'e'
              190  DELETE_FAST              'e'
              192  END_FINALLY      
              194  POP_EXCEPT       
              196  JUMP_BACK            32  'to 32'
            198_0  COME_FROM           164  '164'
              198  END_FINALLY      
              200  JUMP_BACK            32  'to 32'
              202  POP_BLOCK        
            204_0  COME_FROM_LOOP       22  '22'
              204  JUMP_BACK            10  'to 10'
            206_0  COME_FROM            20  '20'
              206  POP_BLOCK        
            208_0  COME_FROM_LOOP        8  '8'

 L. 119       208  LOAD_FAST                'all'
              210  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 154

    s_time = time()
    try:
        all = get_res(tasks=tasks)
    except Exception as e:
        try:
            print(e)
            return []
        finally:
            e = None
            del e

    time_consume = time() - s_time
    print('\n执行完毕! 此次耗时 {} s!'.format(round(float(time_consume), 3)))
    return all


async def _get_celery_async_results(tasks: list, r_timeout=2.5, func_timeout=1800) -> list:
    """
    得到celery worker的处理结果集合
        该函数超时可用 from asyncio import wait_for as async_wait_for来处理协程超时, 并捕获后续异常!(超时后协程会被取消，导致无结果!!)
        eg:
            async def run():
                await async_sleep(3)

            # 原生超时
            try:
                res = await async_wait_for(run(), timeout=2)
            except AsyncTimeoutError as e:
                print(e)

        或者直接设置_get_celery_async_results 的func_timeout超时时长

    :param tasks: celery的tasks任务对象集
    :param r_timeout:
    :param func_timeout:
    :return:
    """
    return block_get_celery_async_results(tasks=tasks,
      r_timeout=r_timeout,
      func_timeout=func_timeout)


def get_current_all_celery_handled_results_list(one_res, logger=None) -> list:
    """
    得到当前所有celery处理后子元素的子元素, 并以新集合形式返回!
    :param one_res:
    :return:
    """
    res = []
    for i in one_res:
        try:
            for j in i:
                res.append(j)

        except TypeError as e:
            try:
                continue
            finally:
                e = None
                del e

    return res
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/podchecker/utils/time_profile.py
# Compiled at: 2019-06-17 12:41:12
# Size of source mod 2**32: 3408 bytes
import time

def time_profile_wrapper(func):

    def wrapper(*args, **kwargs):
        begin_time = time.time()
        x = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n---*** cost 【{end_time - begin_time:<.8f}】 seconds in 【{func.__name__}】 ***---\n")
        return x

    return wrapper


def time_profile_acc_wrapper(func):
    """
        两种实现方式：
            1. 给本def增加属性dict[func:const]
            2. 使用装饰器给func增加属性cost
        对比：
            方法1可以集中打印数据信息，方法2会改变func的关联属性
            这里采用更中规中矩的方法1
    """
    outter_func = time_profile_acc_wrapper
    attr_name_cost_dict = 'attr_name_cost_dict'
    if not hasattr(outter_func, attr_name_cost_dict):
        setattr(outter_func, attr_name_cost_dict, {})

    class CallInfo(object):

        def __init__(self, funcname):
            self.func_name = funcname
            self.call_count = 0
            self.cost_time = 0

        def add_count(self):
            self.call_count += 1

        def add_cost_time(self, cost_time):
            self.cost_time += cost_time

        def debug_info(self):
            return f"---*** total call 【{self.call_count}】times and cost total【{self.cost_time:<.8f}】avg 【{self.cost_time / self.call_count if self.call_count > 0 else self.cost_time:<.8f}】 seconds in 【{self.func_name}】 ***---"

    def wrapper(*args, **kwargs):
        begin_time = time.time()
        x = func(*args, **kwargs)
        end_time = time.time()
        cost = end_time - begin_time
        call_info = getattr(outter_func, attr_name_cost_dict).get(func.__name__, CallInfo(func.__name__))
        call_info.call_count += 1
        call_info.cost_time += cost
        getattr(outter_func, attr_name_cost_dict)[func.__name__] = call_info
        return x

    return wrapper


def time_profile_print_all_logs():
    print('--- log all time profiles ---')
    x_func = time_profile_acc_wrapper
    x_key = 'attr_name_cost_dict'
    if hasattr(x_func, x_key):
        attr_dict = getattr(x_func, x_key)
        total_cost_time = 0
        for key in attr_dict:
            total_cost_time += attr_dict[key].cost_time
            print(attr_dict[key].debug_info())

        print(f"--- sum cost 【{total_cost_time:<.8f}】 seconds ---")
    else:
        print('--- no time profiles ---')
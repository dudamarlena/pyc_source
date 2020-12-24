# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/uszipcode-project/uszipcode/pkg/sqlalchemy_mate/crud/inserting.py
# Compiled at: 2018-09-29 23:45:55
# Size of source mod 2**32: 2149 bytes
"""
This module provide utility functions for insert operation.
"""
import math
from sqlalchemy.exc import IntegrityError
try:
    from ..utils import grouper_list
except:
    from sqlalchemy_mate.utils import grouper_list

def smart_insert(engine, table, data, minimal_size=5):
    """
    An optimized Insert strategy. Guarantee successful and highest insertion
    speed. But ATOMIC WRITE IS NOT ENSURED IF THE PROGRAM IS INTERRUPTED.

    **中文文档**

    在Insert中, 如果已经预知不会出现IntegrityError, 那么使用Bulk Insert的速度要
    远远快于逐条Insert。而如果无法预知, 那么我们采用如下策略:

    1. 尝试Bulk Insert, Bulk Insert由于在结束前不Commit, 所以速度很快。
    2. 如果失败了, 那么对数据的条数开平方根, 进行分包, 然后对每个包重复该逻辑。
    3. 若还是尝试失败, 则继续分包, 当分包的大小小于一定数量时, 则使用逐条插入。
      直到成功为止。

    该Insert策略在内存上需要额外的 sqrt(nbytes) 的开销, 跟原数据相比体积很小。
    但时间上是各种情况下平均最优的。
    """
    insert = table.insert()
    if isinstance(data, list):
        try:
            engine.execute(insert, data)
        except IntegrityError:
            n = len(data)
            if n >= minimal_size ** 2:
                n_chunk = math.floor(math.sqrt(n))
                for chunk in grouper_list(data, n_chunk):
                    smart_insert(engine, table, chunk, minimal_size)

            else:
                for row in data:
                    try:
                        engine.execute(insert, row)
                    except IntegrityError:
                        pass

    try:
        engine.execute(insert, data)
    except IntegrityError:
        pass
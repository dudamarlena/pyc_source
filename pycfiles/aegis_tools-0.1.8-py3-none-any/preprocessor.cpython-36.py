# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/aegis_model/model/preprocessor.py
# Compiled at: 2020-01-27 21:51:56
# Size of source mod 2**32: 2805 bytes
import random
from datetime import timedelta
import numpy as np
from pandas import DataFrame, Panel
from pymysql import MySQLError as mysqlErr
from wows_stats import util as ut
from wows_stats.database.database_factory import database_factory

def get_from_db(last_day, timewindow=8, id_column=1, stat_columns=np.array([4, 5, 6, 7])):
    try:
        day_dict = {}
        day_str = 'date '
        day_columns = ['battles', 'wins', 'losses', 'draws']
        db = database_factory(db_type='mongodb')
        i = 0
        count = timewindow
        while count > 0:
            data = np.asarray(db.get_stats_by_date_as_array(args=[last_day - timedelta(i), '100']))
            if data.any():
                ids = data[:, id_column]
                stats = data[:, stat_columns]
                single_frame = DataFrame(data=stats, index=ids, columns=day_columns)
                for d in day_columns:
                    if d != day_columns[0]:
                        single_frame[d] /= single_frame[day_columns[0]] + 0.001

                single_frame[day_columns[0]] = 1
                day_dict[day_str + str(count + 1)] = single_frame
                count -= 1
            i += 1

        result = Panel(day_dict)
        return result
    except mysqlErr:
        print('Get ID list connection failed!')
        return


def split_train_validation(data, y_column=1, train_ratio=0.8, shuffle=False):
    last_day = data.shape[0] - y_column
    max_subsize = ut.max_hundred(data.shape[1])
    discard_index = np.asarray(random.sample(range(data.shape[1]), data.shape[1] - max_subsize))
    filter_dict = {}
    for d in data.keys():
        labels = data[d].axes[0][discard_index]
        filter_dict[d] = data[d].drop(labels)

    data = Panel(filter_dict)
    rd_index = np.asarray(random.sample(range(data.shape[1]), int(train_ratio * data.shape[1])))
    trn_dict = {}
    val_dict = {}
    for d in data.keys():
        labels = data[d].axes[0][rd_index]
        trn_dict[d] = data[d].loc[labels, :]
        val_dict[d] = data[d].drop(labels)

    data_trn = Panel(trn_dict)
    data_val = Panel(val_dict)
    x_trn = data_trn[0:last_day].swapaxes(0, 1)
    x_val = data_val[0:last_day].swapaxes(0, 1)
    y_trn = data_trn[last_day:data.shape[0]].swapaxes(0, 1)
    y_val = data_val[last_day:data.shape[0]].swapaxes(0, 1)
    return (
     x_trn, y_trn, x_val, y_val)
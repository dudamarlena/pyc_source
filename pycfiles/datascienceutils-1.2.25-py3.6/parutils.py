# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/parutils.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 1387 bytes
from IPython.parallel import Client
client = Client()

def where_am_i():
    import os, socket
    return "In process with pid {0} on host: '{1}'".format(os.getpid(), socket.gethostname())


def examples():
    direct_view = client.direct_view()
    where_am_i_direct_results = direct_view.apply(where_am_i)
    where_am_i_direct_results.get()
    lb_view = client.load_balanced_view()
    where_am_i_lb_result = lb_view.apply(where_am_i)
    where_am_i_lb_result.get()


def sample_parallel_proc():
    from pyrallel import mmap_utils, model_selection
    _ = (
     reload(mmap_utils), reload(model_selection))
    from sklearn.datasets import load_digits
    from sklearn.preprocessing import MinMaxScaler
    digits = load_digits()
    X = MinMaxScaler().fit_transform(digits.data)
    y = digits.target
    digits_cv_split_filenames = mmap_utils.persist_cv_splits('digits_10', X, y, 10)
    mmap_utils.warm_mmap_on_cv_splits(client, digits_cv_split_filenames)
    from sklearn.svm import LinearSVC
    from collections import OrderedDict
    import numpy as np
    linear_svc_params = OrderedDict((
     (
      'C', np.logspace(-2, 2, 5)),))
    linear_svc = LinearSVC()
    linear_svc_search = model_selection.RandomizedGridSeach(lb_view)
    linear_svc_search.launch_for_splits(linear_svc, linear_svc_params, digits_cv_split_filenames)
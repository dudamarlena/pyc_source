# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/interface.py
# Compiled at: 2019-11-05 21:15:15
# Size of source mod 2**32: 1613 bytes
import json, numpy as np, matplotlib, mpld3
try:
    import matplotlib, mpld3, bokeh
except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

def is_mpl(val):
    try:
        return isinstance(val, matplotlib.figure.Figure)
    except Exception as e:
        try:
            return False
        finally:
            e = None
            del e


def is_bokeh(val):
    try:
        return isinstance(val, bokeh.model.Model) or isinstance(val, bokeh.document.document.Document)
    except Exception as e:
        try:
            return False
        finally:
            e = None
            del e


def get_var(val, params):
    """
    Val: some value from user
    params: dict of params from frontend
    """
    if is_bokeh(val):
        ret = bokeh.embed.file_html(val, bokeh.resources.Resources('cdn'))
        type_ = 'mpl'
    else:
        if is_mpl(val):
            ret = mpld3.fig_to_html(val)
            type_ = 'mpl'
        else:
            if type(val) == np.ndarray:
                sh = val.shape
                if len(sh) >= 2:
                    if sh[0] > 10 and sh[1] > 10:
                        alpha = np.ones(list(sh[:2]) + [1]) * 255
                        if len(sh) == 2:
                            val = val.reshape(sh[0], -1, 1)
                            val = np.concatenate((val, val, val, alpha), axis=(-1))
                        if len(sh) == 3:
                            val = np.concatenate((val, alpha), axis=(-1))
                        val = val.flatten()
                        ret = list(sh[:2]) + val.tolist()
                        type_ = 'img'
                else:
                    val = val.tolist()
                    ret = val
                    type_ = 'raw'
            else:
                ret = val
                type_ = 'raw'
    msg = {'args':params['varname'], 
     'value':ret, 
     'type':type_}
    return json.dumps(msg)
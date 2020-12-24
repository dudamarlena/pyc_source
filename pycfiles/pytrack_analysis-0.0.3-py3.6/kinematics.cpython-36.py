# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pytrack_analysis/kinematics.py
# Compiled at: 2017-07-29 05:03:49
# Size of source mod 2**32: 8203 bytes
import os, sys, numpy as np, pandas as pd, logging, yaml, os.path as osp, subprocess as sub, sys, traceback, inspect, itertools
from functools import wraps
from ._globals import *
from pkg_resources import get_distribution
__version__ = get_distribution('pytrack_analysis').version
PROFILE, NAME, OS = get_globals()

def get_log_path(_file):
    with open(_file, 'r') as (stream):
        profile = yaml.load(stream)
    return profile[profile['active']]['systems'][NAME]['log']


def get_log(_module, _func, _logfile):
    """
    The main entry point of the logging
    """
    logger = logging.getLogger(_module.__class__.__name__ + '.' + _func)
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(_logfile):
        print('created file:' + _logfile)
        with open(_logfile, 'w+') as (f):
            f.close()
    fh = logging.FileHandler(_logfile)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def logged_f(_logfile):

    def wrapper(func):

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            logger = get_log(args[0], func.__name__, _logfile)
            if func.__name__ == '__init__':
                logger.info('Initializing: ' + args[0].__class__.__name__ + ' (version: ' + args[0].vcommit + ')')
            else:
                logger.info('calling: ' + func.__name__)
            if len(args) > 0:
                args_name = inspect.getargspec(func)[0]
                args_dict = dict(zip(args_name, [type(arg) for arg in args]))
                logger.info('takes arg: ' + str(args_dict))
            if len(args) == 0:
                logger.info('takes arg: ' + str(None))
            if len(kwargs) > 0:
                kwargs_name = inspect.getargspec(func)[2]
                kwargs_dict = dict(zip(kwargs_name, type(kwargs)))
                logger.info('takes kwarg: ' + str(kwargs_dict))
            if len(kwargs) == 0:
                logger.info('takes kwarg: ' + str(None))
            out = func(*args, **kwargs)
            logger.info('returns: ' + str(type(out)))
            return out

        return func_wrapper

    return wrapper


LOG_PATH = get_log_path(PROFILE)

def get_path(outstr):
    print(outstr + '\t' + LOG_PATH)


def get_func():
    out = traceback.extract_stack(None, 2)[0][2]
    return out


class Kinematics(object):

    def __init__(self, _data, _metadata):
        """
        Initializes the class. Setting up internal variables for input data; setting up logging.
        """
        self.filepath = os.path.realpath(__file__)
        self.vcommit = __version__
        self.dt = 1 / _metadata['framerate']
        logger = get_log(self, get_func(), LOG_PATH)
        logger.info('initialized Kinematics pipeline (version: ' + str(self) + ')')

    @logged_f(LOG_PATH)
    def angular_speed(self, _X, _meta):
        angle = np.array(_X['heading'])
        speed = np.diff(angle)
        speed[(speed > 180)] -= 360.0
        speed[(speed < -180)] += 360.0
        speed *= _meta.dict['framerate']
        df = pd.DataFrame({'speed': np.append(0, speed)})
        return df

    @logged_f(LOG_PATH)
    def distance(self, _X, _Y):
        x1, y1 = np.array(_X[_X.columns[0]]), np.array(_X[_X.columns[1]])
        x2, y2 = np.array(_Y[_Y.columns[0]]), np.array(_Y[_Y.columns[1]])
        dist_sq = np.square(x1 - x2) + np.square(y1 - y2)
        dist = np.sqrt(dist_sq)
        dist[dist == np.nan] = -1
        df = pd.DataFrame({'distance': dist})
        return df

    @logged_f(LOG_PATH)
    def distance_to_patch(self, _X, _meta):
        xfly, yfly = np.array(_X['head_x']), np.array(_X['head_y'])
        dist = {}
        for ip, patch in enumerate(_meta.patches()):
            xp, yp = patch['position'][0], patch['position'][1]
            dist_sq = np.square(xfly - xp) + np.square(yfly - yp)
            key = 'dist_patch_' + str(ip)
            dist[key] = np.sqrt(dist_sq)

        df = pd.DataFrame(dist)
        return df

    @logged_f(LOG_PATH)
    def ethogram(self, _X, _Y, _Z, _meta):
        speed = np.array(_X['head'])
        bspeed = np.array(_X['body'])
        smoother = np.array(_X['smoother_head'])
        turn = np.array(_Y['speed'])
        Neach = int(len(_Z.columns) / 2)
        yps = np.zeros((Neach, speed.shape[0]))
        sps = np.zeros((Neach, speed.shape[0]))
        yc = 0
        sc = 0
        for i, col in enumerate(_Z.columns):
            idc = int(col.split('_')[2])
            if _meta.dict['SubstrateType'][idc] == 1:
                yps[yc, :] = np.array(_Z[col])
                yc += 1
            if _meta.dict['SubstrateType'][idc] == 2:
                sps[sc, :] = np.array(_Z[col])
                sc += 1

        ymin = np.amin(yps, axis=0)
        smin = np.amin(sps, axis=0)
        out = np.zeros(speed.shape) - 1
        print(out)
        out[speed > 2] = 2
        mask = (out == 2) & (bspeed < 4) & (np.abs(turn) >= 125.0)
        out[mask] = 3
        out[smoother <= 0.2] = 0
        out[out == -1] = 1
        visits = np.zeros(out.shape)
        for i in range(ymin.shape[0]):
            if ymin[i] <= 2.5:
                visits[i] = 1
            if smin[i] <= 2.5:
                visits[i] = 2
            if visits[(i - 1)] == 1:
                if ymin[i] <= 5.0:
                    visits[i] = 1
                if visits[(i - 1)] == 2 and smin[i] <= 5.0:
                    visits[i] = 2

        mask_yeast = (out == 1) & (visits == 1)
        mask_sucrose = (out == 1) & (visits == 2)
        out[mask_yeast] = 4
        out[mask_sucrose] = 5
        return (
         pd.DataFrame({'etho': out}), pd.DataFrame({'visits': visits}))

    def forward_speed(self, _X):
        pass

    @logged_f(LOG_PATH)
    def head_angle(self, _X):
        xb, yb = np.array(_X['body_x']), np.array(_X['body_y'])
        xh, yh = np.array(_X['head_x']), np.array(_X['head_y'])
        dx, dy = xh - xb, yh - yb
        angle = np.arctan2(dy, dx)
        angle = np.degrees(angle)
        df = pd.DataFrame({'heading': angle})
        return df

    @logged_f(LOG_PATH)
    def linear_speed(self, _X, _meta):
        xfly, yfly = np.array(_X[_X.columns[0]]), np.array(_X[_X.columns[1]])
        xdiff = np.diff(xfly)
        ydiff = np.diff(yfly)
        speed = np.sqrt(np.square(xdiff) + np.square(ydiff)) * _meta.dict['framerate']
        df = pd.DataFrame({'speed': np.append(0, speed)})
        return df

    def sideward_speed(self, _X):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.vcommit
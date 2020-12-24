# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymoso/commands/basecomm.py
# Compiled at: 2019-03-26 15:34:31
# Size of source mod 2**32: 4425 bytes
__doc__ = '\nBase class for implementing CLI commands. Most users will not need to\nuse these functions.\n'
import os, pathlib, time, collections
from datetime import date
from .. import chnutils as mprun
from .. import solvers
from .. import problems
from .. import testers
from random import Random
from json import dump
import traceback

def check_expname(name):
    """
    Check that the experiment file has been generated and load its
    contents.

    Parameters
    ----------
    name : str

    Returns
    -------
    datstr: str
    """
    if not os.path.isdir(name):
        return False
    else:
        fn = name + '/' + name + '.txt'
        fpath = pathlib.Path(fn)
        if not fpath.is_file():
            return False
        with open(fn, 'r') as (f1):
            datstr = json.load(f1)
        return datstr


def save_errortb(name, errmsg):
    """
    Save a message to a file.

    Parameters
    ----------
    name : str
    errmsg : str
    """
    mydir = name
    pathlib.Path(name).mkdir(exist_ok=True)
    humfilen = 'err_' + name + '.txt'
    humpth = os.path.join(name, humfilen)
    with open(humpth, 'w') as (f1):
        f1.write(errmsg)


def save_metadata(name, humantxt):
    """
    Save an experiment metadata string to a file.

    Parameters
    ----------
    name : str
    humantxt : str
    """
    mydir = name
    pathlib.Path(name).mkdir(exist_ok=True)
    humfilen = name + '.txt'
    humpth = os.path.join(name, humfilen)
    with open(humpth, 'w') as (f1):
        dump(humantxt, f1, indent=4, separators=(',', ': '))


def gen_humanfile(name, probn, solvn, budget, runtime, param, vals, startseed, endseed):
    """
    Generate a human-readable experiment metadata string

    Parameters
    ----------
    name : str
    probn : str
    budget : int
    runtime : float
    param : list
    vals : list
    startseed : tuple of int
    endseed : tuple of int

    Returns
    -------
    ddict : dict
        ordered dictionary of the parameters and values
    """
    today = date.today()
    tstr = today.strftime('%A %d. %B %Y')
    timestr = time.strftime('%X')
    dnames = ('Name', 'Problem', 'Algorithm', 'Budget', 'Run time', 'Day', 'Time',
              'Params', 'Param Values', 'start seed', 'end seed')
    ddate = (name, probn, solvn, budget, runtime, tstr, timestr, param, vals, startseed, endseed)
    ddict = collections.OrderedDict(zip(dnames, ddate))
    return ddict


def save_metrics(name, exp, metdata):
    """
    Save metrics data output to the experiment file.

    Parameters
    ----------
    name : str
    exp : int
    metdata : dict
    """
    pref = 'metrics_' + str(exp) + '_'
    ispdatn = pref + name + '.txt'
    metdatpth = os.path.join(name, ispdatn)
    metlst = []
    for i in metdata:
        metlst.append(str(metdata[i]))

    metstr = '\n'.join(metlst)
    with open(metdatpth, 'w') as (f1):
        f1.write(metstr)


def save_isp(name, exp, ispdat):
    """
    Save testsolve output to the experiment file.

    Parameters
    ----------
    name : str
    exp : int
    ispdat : dict
    """
    pref = 'ispdata_' + str(exp) + '_'
    ispdatn = pref + name + '.txt'
    ispdatpth = os.path.join(name, ispdatn)
    isplst = []
    for i in ispdat:
        isplst.append(str(ispdat[i]))

    ispstr = '\n'.join(isplst)
    with open(ispdatpth, 'w') as (f1):
        f1.write(ispstr)


def save_les(name, lesstr):
    """
    Save solve output to experiment file.

    Parameters
    ----------
    name : str
    lesstr : str
    """
    pref = 'rundata_'
    rundatn = pref + name + '.txt'
    rundpth = os.path.join(name, rundatn)
    with open(rundpth, 'w') as (f2):
        f2.write(lesstr)


class BaseComm(object):
    """BaseComm"""

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Placeholder function that must be implemented in command sub-classes.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError('You must implement the run() method yourself!')
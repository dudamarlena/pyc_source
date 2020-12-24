# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/poly/standalone.py
# Compiled at: 2007-03-25 20:28:29
__version__ = '$Revision: 1.3 $'
import tempfile, poly

def _init_job_array():
    jobindex = None
    jobindex_end = None
    firstjob = True
    lastjob = True

    def _chunk(collection):
        return collection

    return (
     jobindex, jobindex_end, firstjob, lastjob, _chunk)


def _init_job():
    jobid = None
    jobname = None

    def local(filename, mode='r', host=poly.headnode, force=False):
        return filename

    gettempdir = tempfile.gettempdir
    NamedTemporaryFile = poly._fixargs(tempfile.NamedTemporaryFile, suffix='.poly')
    TemporaryFile = tempfile.TemporaryFile
    _localfile_cmds = poly._init_localfile_cmds(default=['scp'])
    return (
     jobid, jobname, local, gettempdir,
     NamedTemporaryFile, TemporaryFile, _localfile_cmds)


def _init_headnode():
    return 'localhost'
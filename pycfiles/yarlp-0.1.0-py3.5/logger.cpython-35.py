# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/logger.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 12445 bytes
import os, sys, shutil, os.path as osp, json, time, datetime, tempfile
LOG_OUTPUT_FORMATS = [
 'stdout', 'log', 'csv']
DEBUG = 10
INFO = 20
WARN = 30
ERROR = 40
DISABLED = 50

class KVWriter(object):

    def writekvs(self, kvs):
        raise NotImplementedError


class SeqWriter(object):

    def writeseq(self, seq):
        raise NotImplementedError


class HumanOutputFormat(KVWriter, SeqWriter):

    def __init__(self, filename_or_file):
        if isinstance(filename_or_file, str):
            self.file = open(filename_or_file, 'wt')
            self.own_file = True
        else:
            assert hasattr(filename_or_file, 'read'), 'expected file or str, got %s' % filename_or_file
            self.file = filename_or_file
            self.own_file = False

    def writekvs(self, kvs):
        key2str = {}
        for key, val in sorted(kvs.items()):
            if isinstance(val, float):
                valstr = '%-8.3g' % (val,)
            else:
                valstr = str(val)
            key2str[self._truncate(key)] = self._truncate(valstr)

        if len(key2str) == 0:
            print('WARNING: tried to write empty key-value dict')
            return
        keywidth = max(map(len, key2str.keys()))
        valwidth = max(map(len, key2str.values()))
        dashes = '-' * (keywidth + valwidth + 7)
        lines = [dashes]
        for key, val in sorted(key2str.items()):
            lines.append('| %s%s | %s%s |' % (
             key,
             ' ' * (keywidth - len(key)),
             val,
             ' ' * (valwidth - len(val))))

        lines.append(dashes)
        self.file.write('\n'.join(lines) + '\n')
        self.file.flush()

    def _truncate(self, s):
        if len(s) > 23:
            return s[:20] + '...'
        return s

    def writeseq(self, seq):
        for arg in seq:
            self.file.write(arg)

        self.file.write('\n')
        self.file.flush()

    def close(self):
        if self.own_file:
            self.file.close()


class JSONOutputFormat(KVWriter):

    def __init__(self, filename):
        self.file = open(filename, 'wt')

    def writekvs(self, kvs):
        for k, v in sorted(kvs.items()):
            if hasattr(v, 'dtype'):
                v = v.tolist()
                kvs[k] = float(v)

        self.file.write(json.dumps(kvs) + '\n')
        self.file.flush()

    def close(self):
        self.file.close()


class CSVOutputFormat(KVWriter):

    def __init__(self, filename):
        self.file = open(filename, 'w+t')
        self.keys = []
        self.sep = ','

    def writekvs(self, kvs):
        extra_keys = kvs.keys() - self.keys
        if extra_keys:
            self.keys.extend(extra_keys)
            self.file.seek(0)
            lines = self.file.readlines()
            self.file.seek(0)
            for i, k in enumerate(self.keys):
                if i > 0:
                    self.file.write(',')
                self.file.write(k)

            self.file.write('\n')
            for line in lines[1:]:
                self.file.write(line[:-1])
                self.file.write(self.sep * len(extra_keys))
                self.file.write('\n')

        for i, k in enumerate(self.keys):
            if i > 0:
                self.file.write(',')
            v = kvs.get(k)
            if v:
                self.file.write(str(v))

        self.file.write('\n')
        self.file.flush()

    def close(self):
        self.file.close()


class TensorBoardOutputFormat(KVWriter):
    __doc__ = "\n    Dumps key/value pairs into TensorBoard's numeric format.\n    "

    def __init__(self, dir):
        os.makedirs(dir, exist_ok=True)
        self.dir = dir
        self.step = 1
        prefix = 'events'
        path = osp.join(osp.abspath(dir), prefix)
        import tensorflow as tf
        from tensorflow.python import pywrap_tensorflow
        from tensorflow.core.util import event_pb2
        from tensorflow.python.util import compat
        self.tf = tf
        self.event_pb2 = event_pb2
        self.pywrap_tensorflow = pywrap_tensorflow
        self.writer = pywrap_tensorflow.EventsWriter(compat.as_bytes(path))

    def writekvs(self, kvs):

        def summary_val(k, v):
            kwargs = {'tag': k, 'simple_value': float(v)}
            return self.tf.Summary.Value(**kwargs)

        summary = self.tf.Summary(value=[summary_val(k, v) for k, v in kvs.items()])
        event = self.event_pb2.Event(wall_time=time.time(), summary=summary)
        event.step = self.step
        self.writer.WriteEvent(event)
        self.writer.Flush()
        self.step += 1

    def close(self):
        if self.writer:
            self.writer.Close()
            self.writer = None


def make_output_format(format, ev_dir):
    from mpi4py import MPI
    os.makedirs(ev_dir, exist_ok=True)
    rank = MPI.COMM_WORLD.Get_rank()
    if format == 'stdout':
        return HumanOutputFormat(sys.stdout)
    if format == 'log':
        suffix = '' if rank == 0 else '-mpi%03i' % rank
        return HumanOutputFormat(osp.join(ev_dir, 'log%s.txt' % suffix))
    if format == 'json':
        assert rank == 0
        return JSONOutputFormat(osp.join(ev_dir, 'progress.json'))
    if format == 'csv':
        assert rank == 0
        return CSVOutputFormat(osp.join(ev_dir, 'progress.csv'))
    if format == 'tensorboard':
        assert rank == 0
        return TensorBoardOutputFormat(osp.join(ev_dir, 'tb'))
    raise ValueError('Unknown format specified: %s' % (format,))


def logkv(key, val):
    """
    Log a value of some diagnostic
    Call this once for each diagnostic quantity, each iteration
    """
    Logger.CURRENT.logkv(key, val)


def logkvs(d):
    """
    Log a dictionary of key-value pairs
    """
    for k, v in d.items():
        logkv(k, v)


def dumpkvs():
    """
    Write all of the diagnostics from the current iteration

    level: int. (see logger.py docs) If the global logger level is higher than
                the level argument here, don't print to stdout.
    """
    Logger.CURRENT.dumpkvs()


def getkvs():
    return Logger.CURRENT.name2val


def log(*args, level=INFO):
    """
    Write the sequence of args, with no separators, to the console and output files (if you've configured an output file).
    """
    Logger.CURRENT.log(*args, level=level)


def debug(*args):
    log(*args, level=DEBUG)


def info(*args):
    log(*args, level=INFO)


def warn(*args):
    log(*args, level=WARN)


def error(*args):
    log(*args, level=ERROR)


def set_level(level):
    """
    Set logging threshold on current logger.
    """
    Logger.CURRENT.set_level(level)


def get_dir():
    """
    Get directory that log files are being written to.
    will be None if there is no output directory (i.e., if you didn't call start)
    """
    return Logger.CURRENT.get_dir()


record_tabular = logkv
dump_tabular = dumpkvs

class Logger(object):
    DEFAULT = None
    CURRENT = None

    def __init__(self, dir, output_formats):
        self.name2val = {}
        self.level = INFO
        self.dir = dir
        self.output_formats = output_formats

    def logkv(self, key, val):
        self.name2val[key] = val

    def dumpkvs(self):
        if self.level == DISABLED:
            return
        for fmt in self.output_formats:
            if isinstance(fmt, KVWriter):
                fmt.writekvs(self.name2val)

        self.name2val.clear()

    def log(self, *args, level=INFO):
        if self.level <= level:
            self._do_log(args)

    def set_level(self, level):
        self.level = level

    def get_dir(self):
        return self.dir

    def close(self):
        for fmt in self.output_formats:
            fmt.close()

    def _do_log(self, args):
        for fmt in self.output_formats:
            if isinstance(fmt, SeqWriter):
                fmt.writeseq(map(str, args))


Logger.DEFAULT = Logger.CURRENT = Logger(dir=None, output_formats=[HumanOutputFormat(sys.stdout)])

def configure(dir=None, format_strs=None):
    if dir is None:
        dir = os.getenv('OPENAI_LOGDIR')
    if dir is None:
        dir = osp.join(tempfile.gettempdir(), datetime.datetime.now().strftime('openai-%Y-%m-%d-%H-%M-%S-%f'))
    assert isinstance(dir, str)
    os.makedirs(dir, exist_ok=True)
    if format_strs is None:
        strs = os.getenv('OPENAI_LOG_FORMAT')
        format_strs = strs.split(',') if strs else LOG_OUTPUT_FORMATS
    output_formats = [make_output_format(f, dir) for f in format_strs]
    Logger.CURRENT = Logger(dir=dir, output_formats=output_formats)
    log('Logging to %s' % dir)


def reset():
    if Logger.CURRENT is not Logger.DEFAULT:
        Logger.CURRENT.close()
        Logger.CURRENT = Logger.DEFAULT
        log('Reset logger')


class scoped_configure(object):

    def __init__(self, dir=None, format_strs=None):
        self.dir = dir
        self.format_strs = format_strs
        self.prevlogger = None

    def __enter__(self):
        self.prevlogger = Logger.CURRENT
        configure(dir=self.dir, format_strs=self.format_strs)

    def __exit__(self, *args):
        Logger.CURRENT.close()
        Logger.CURRENT = self.prevlogger


def _demo():
    info('hi')
    debug("shouldn't appear")
    set_level(DEBUG)
    debug('should appear')
    dir = '/tmp/testlogging'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    configure(dir=dir)
    logkv('a', 3)
    logkv('b', 2.5)
    dumpkvs()
    logkv('b', -2.5)
    logkv('a', 5.5)
    dumpkvs()
    info('^^^ should see a = 5.5')
    logkv('b', -2.5)
    dumpkvs()
    logkv('a', 'longasslongasslongasslongasslongasslongassvalue')
    dumpkvs()


def read_json(fname):
    import pandas
    ds = []
    with open(fname, 'rt') as (fh):
        for line in fh:
            ds.append(json.loads(line))

    return pandas.DataFrame(ds)


def read_csv(fname):
    import pandas
    return pandas.read_csv(fname, index_col=None, comment='#')


def read_tb(path):
    """
    path : a tensorboard file OR a directory, where we will find all TB files
           of the form events.*
    """
    import pandas, numpy as np
    from glob import glob
    from collections import defaultdict
    import tensorflow as tf
    if osp.isdir(path):
        fnames = glob(osp.join(path, 'events.*'))
    else:
        if osp.basename(path).startswith('events.'):
            fnames = [
             path]
        else:
            raise NotImplementedError('Expected tensorboard file or directory containing them. Got %s' % path)
    tag2pairs = defaultdict(list)
    maxstep = 0
    for fname in fnames:
        for summary in tf.train.summary_iterator(fname):
            if summary.step > 0:
                for v in summary.summary.value:
                    pair = (
                     summary.step, v.simple_value)
                    tag2pairs[v.tag].append(pair)

                maxstep = max(summary.step, maxstep)

    data = np.empty((maxstep, len(tag2pairs)))
    data[:] = np.nan
    tags = sorted(tag2pairs.keys())
    for colidx, tag in enumerate(tags):
        pairs = tag2pairs[tag]
        for step, value in pairs:
            data[(step - 1, colidx)] = value

    return pandas.DataFrame(data, columns=tags)


if __name__ == '__main__':
    _demo()
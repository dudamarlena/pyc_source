# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/logging.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 32793 bytes
"""
logging.py log file making module
"""
from __future__ import absolute_import, division, print_function
import sys, os, time, datetime, copy, io
from collections import deque, MutableSequence, MutableMapping, Mapping
from ..aid.sixing import *
from .globaling import *
from ..aid.odicting import odict
from ..aid.filing import ocfn
from . import excepting
from . import registering
from . import storing
from . import tasking
from ..aid.consoling import getConsole
console = getConsole()

class Logger(tasking.Tasker):
    __doc__ = '\n    Logger Task Patron Registry Class for managing Logs\n\n    Usage:   logger.send(START) to prepare log formats also reopens files\n             logger.send(RUN) runs logs\n             logger.send(STOP) closes log files needed to flush caches\n\n    '

    def __init__(self, flushPeriod=30.0, prefix='~/.ioflo/log', keep=0, cyclePeriod=0.0, fileSize=0, reuse=False, **kw):
        """
        Initialize instance.

        Inherited Parameters:
            name = unique name for logger
            store = data store
            period = time period between runs of logger
            schedule = tasker shedule such as ACTIVE INACTIVE

        Parameters:
            flushPeriod = time in seconds between flushes
            prefix = prefix used to create log directory
            keep = int number of log copies in rotation <1> means do not cycle
            cyclePeriod = interval in seconds between log rotations,
                     0.0 or None means do not rotate
            fileSize = size in bytes  of log file required to peform rotation
                       Do not rotate is main file is not at least meet file size
                       0 means always rotate
            reuse = Make unique time stamped log directory if True otherwise nonunique
                    useful when rotating

        Inherited Class Attributes:
            Counter = number of instances in class registrar
            Names = odict of instances keyed by name in class registrar

        Inherited instance attributes
            .name = unique name for logger
            .store = data store for house
            .period = desired time in seconds between runs,non negative, zero means asap
            .schedule = initial scheduling context for this logger vis a vis skedder

            .stamp = depends on subclass default is time logger last RUN
            .status = operational status of logger
            .desire = desired control asked by this or other taskers
            .done = logger completion state True or False
            .runner = generator to run logger

        Instance attributes
            .flushPeriod = period between flushes
            .prefix = prefix used to create log directory
            .keep = int number of log copies in rotation, < 1 means do cycle
            .cyclePeriod = interval in seconds between log rotations,
                     0.0 or None means do not rotate
            .fileSize = minimum size in bytes of main log file for rotation to occur
            .reuse = Make unique time stamped log directory if True otherwise nonunique
                    useful when rotating

            .rotateStamp = time logs last rotated
            .flushStamp = time logs last flushed
            .path = full path name of log directory
            .logs = dict of logs

        """
        (super(Logger, self).__init__)(**kw)
        self.flushPeriod = max(1.0, flushPeriod)
        self.prefix = prefix
        self.keep = int(keep)
        self.cyclePeriod = max(0.0, cyclePeriod)
        if self.keep > 0:
            if not self.cyclePeriod:
                self.keep = 0
        self.fileSize = max(0, fileSize)
        self.reuse = True if reuse else False
        self.cycleStamp = 0.0
        self.flushStamp = 0.0
        self.path = ''
        self.logs = []

    def log(self):
        """
        Perform one log action
        """
        for log in self.logs:
            log()

        try:
            if self.store.stamp - self.flushStamp >= self.flushPeriod:
                console.profuse('Logger {0} Flushed at {1}, previous flush at {2}\n'.format(self.name, self.store.stamp, self.flushStamp))
                self.flush()
                self.flushStamp = self.store.stamp
        except TypeError:
            self.flushStamp = self.store.stamp

        if self.keep:
            try:
                if self.store.stamp - self.cycleStamp >= self.cyclePeriod:
                    console.profuse('Logger {0} Cycle rotation at {1}, previous cycle at {2}\n'.format(self.name, self.store.stamp, self.cycleStamp))
                    self.cycle()
                    self.cycleStamp = self.store.stamp
            except TypeError:
                self.cycleStamp = self.store.stamp

    def reopen(self):
        """
        Reopen all log files
        """
        if not self.path:
            self.path = self.createPath(prefix=(self.prefix))
            return self.path or False
        else:
            for log in self.logs:
                if not log.reopen(prefix=(self.path), keep=(self.keep)):
                    return False

            return True

    def close(self):
        """
        Close all log files
        """
        for log in self.logs:
            log.close()

    def flush(self):
        """
        Flush all log files
        """
        for log in self.logs:
            log.flush()

    def cycle(self):
        """
        Cycle (Rotate) all log files
        """
        for log in self.logs:
            log.cycle(size=(self.fileSize))

    def prepare(self):
        """
        Called in runner on control = START
        """
        for log in self.logs:
            log.prepare()

    def resolve(self):
        """
        Called by house to resolve links in tasker
        """
        for log in self.logs:
            log.resolve()

    def addLog(self, log):
        """
        Add log to list of logs
        """
        self.logs.append(log)

    def createPath(self, prefix='~/.ioflo/log'):
        """
        Returns unique logger base directory path
        if successfully creates base logger directory, empty otherwise
        creates unique log directory path
        creates physical directories on disk
        """
        path = ''
        try:
            if self.reuse:
                path = os.path.join(prefix, self.store.house.name, self.name)
                path = os.path.abspath(path)
                if not os.path.exists(path):
                    os.makedirs(path)
            else:
                i = 0
                while True:
                    dt = datetime.datetime.now()
                    dirname = '{0}_{1:04d}{2:02d}{3:02d}_{4:02d}{5:02d}{6:02d}_{7:03d}'.format(self.name, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond // 1000 + i)
                    path = os.path.join(prefix, self.store.house.name, dirname)
                    path = os.path.abspath(path)
                    if not os.path.exists(path):
                        os.makedirs(path)
                        break
                    i += 1

        except OSError as ex:
            console.terse("Error: creating log directory '{0}'\n".format(ex))
            return path

        console.concise("     Created Logger {0} Directory at '{1}'\n".format(self.name, self.path))
        return path

    def makeRunner(self):
        """
        generator factory function to create generator to run this logger
        """
        console.profuse('     Making Logger Task Runner {0}\n'.format(self.name))
        self.status = STOPPED
        self.desire = STOP
        try:
            try:
                while True:
                    control = yield self.status
                    console.profuse('\n     Iterate Logger {0} with control = {1} status = {2}\n'.format(self.name, ControlNames.get(control, 'Unknown'), StatusNames.get(self.status, 'Unknown')))
                    if control == RUN:
                        console.profuse('     Running Logger {0} ...\n'.format(self.name))
                        self.log()
                        self.status = RUNNING
                    else:
                        if control == READY:
                            console.profuse('     Attempting Ready Logger {0}\n'.format(self.name))
                            console.terse('     Readied Logger {0} ...\n'.format(self.name))
                            self.status = READIED
                        else:
                            if control == START:
                                console.profuse('     Attempting Start Logger {0}\n'.format(self.name))
                                if self.reopen():
                                    console.terse('     Starting Logger {0} ...\n'.format(self.name))
                                    self.prepare()
                                    self.log()
                                    self.desire = RUN
                                    self.status = STARTED
                                else:
                                    self.desire = STOP
                                    self.status = STOPPED
                            else:
                                if control == STOP:
                                    if self.status != STOPPED:
                                        console.terse('     Stopping Logger {0} ...\n'.format(self.name))
                                        self.log()
                                        if self.keep:
                                            if self.reuse:
                                                self.cycle()
                                        self.close()
                                        self.desire = STOP
                                        self.status = STOPPED
                                else:
                                    console.profuse('     Aborting Logger {0} ...\n'.format(self.name))
                                    self.close()
                                    self.desire = ABORT
                                    self.status = ABORTED
                    self.stamp = self.store.stamp

            except Exception as ex:
                console.terse('{0}\n'.format(ex))
                console.terse('     Exception in Logger {0} in {1}\n'.format(self.name, self.store.house.name))
                raise

        finally:
            self.close()
            self.desire = ABORT
            self.status = ABORTED


class Log(registering.StoriedRegistrar):
    __doc__ = '\n    Log Class for logging to file\n\n    Iherited instance attributes:\n       .name = unique name for log (group)\n       .store = data store\n\n    Instance attributes:\n       .stamp = time stamp last time logged used by once and update actions\n       .kind = text or binary\n       .fileName = file name only\n       .path = full dir path name of file\n       .file = file where log is written\n       .rule = log rule conditions for log\n       .action = function to use when logging\n       .header = header for log file\n\n       .loggees = odict of loggee shares to be logged keyed by tag\n       .formats = odict of loggee format string odicts keyed by tag\n                  each format string odict is are format strings keyed by data field\n       .lasts = odict of loggee Data instances of last values keyed by tag\n                  each Data instance attribute is data field\n    '
    Counter = 0
    Names = {}

    def __init__(self, kind='text', baseFilename='', rule=NEVER, loggees=None, fields=None, **kw):
        """
        Initialize instance.
        Parameters:
            kind = text or binary
            baseFilename = base for log file name, extension added later when path created
            rule = log rule conditions (NEVER, ONCE, ALWAYS, UPDATE, CHANGE)
            loggees = odict of shares to be logged keyed by tags
            fields = odict of field name lists keyed by loggee tag

        """
        if 'preface' not in kw:
            kw['preface'] = 'Log'
        else:
            (super(Log, self).__init__)(**kw)
            self.stamp = None
            self.first = True
            self.kind = kind
            if baseFilename:
                self.baseFilename = baseFilename
            else:
                self.baseFilename = self.name
        self.path = ''
        self.file = None
        self.paths = []
        self.rule = rule
        self.action = None
        self.assignRuleAction()
        self.header = ''
        self.loggees = odict()
        self.fields = fields if fields is not None else odict()
        self.formats = odict()
        self.lasts = odict()
        if loggees:
            for tag, loggee in loggees.items():
                self.addLoggee(tag, loggee)

    def resolve(self):
        """
        resolves links to loggees

        """
        console.profuse('     Resolving links for Log {0}\n'.format(self.name))
        for tag, loggee in self.loggees.items():
            if not isinstance(loggee, storing.Share):
                share = self.store.fetch(loggee)
                if share is None:
                    raise excepting.ResolveError('Loggee not in store', loggee, self.name)
                self.loggees[tag] = share

    def __call__(self, **kw):
        """
        run .action
        """
        (self.action)(**kw)
        console.profuse('     Log {0} at {1}\n'.format(self.name, self.stamp))

    def createPath(self, prefix):
        """
        Returns full path name of file given prefix and .kind .baseFilename
        """
        if self.kind == 'text':
            ext = '.txt'
        else:
            if self.kind == 'binary':
                ext = '.log'
        filename = '{0}{1}'.format(self.baseFilename, ext)
        path = os.path.join(prefix, filename)
        path = os.path.abspath(path)
        return path

    def reopen(self, prefix='', keep=0):
        """
        Returns True is successful False otherwise
        Closes if open then reopens
        Opens or Creates log file and assign to .path
        If .path empty then creates path using prefix
        If keep then creates cycle (rotation) copy paths in .paths
           trial opens cycle paths.
        """
        keep = int(keep)
        if not self.path:
            self.path = self.createPath(prefix=prefix)
            self.paths = []
        self.close()
        if os.path.exists(self.path):
            self.first = False
        try:
            self.file = ocfn(self.path, 'a+')
        except IOError as ex:
            console.terse("Error: Creating/opening log file '{0}'\n".format(ex))
            self.file = None
            return False

        console.concise("     Created/Opened Log file '{0}'\n".format(self.path))
        if keep > 0:
            self.paths = [
             self.path]
            for k in range(keep):
                k += 1
                root, ext = os.path.splitext(self.path)
                path = '{0}{1:02}{2}'.format(root, k, ext)
                self.paths.append(path)
                try:
                    file = ocfn(path, 'r')
                except IOError as ex:
                    console.terse("Error: Creating/opening log rotate file '{0}'\n".format(ex))
                    return False

                file.close()
                console.concise("     Created Log rotate file '{0}'\n".format(path))

        return True

    def close(self):
        """
        close self.file if open except stdout
        """
        if self.file:
            if not self.file.closed:
                self.flush()
                self.file.close()
                self.file = None

    def flush(self):
        """
        flush self.file if open except stdout
        """
        if self.file:
            if not self.file.closed:
                self.file.flush()
                os.fsync(self.file.fileno())

    def cycle(self, size=0):
        """
        Returns True if cycle rotate successful, False otherwise
        Cycle log files  Only cycle if size > 0 and main log file size >= size
        """
        if self.paths:
            self.flush()
            try:
                if size:
                    if os.path.getsize(self.path) < size:
                        return False
            except OSError as ex:
                console.terse("Error: Reading file size '{0}'\n".format(ex))
                return False

            self.close()
            cycled = True
            for k in reversed(range(len(self.paths) - 1)):
                old = self.paths[k]
                new = self.paths[(k + 1)]
                try:
                    os.rename(old, new)
                except OSError as ex:
                    console.terse("Error: Moving log rotate file '{0}'\n".format(ex))
                    cycled = False
                    break

            if not cycled:
                self.reopen()
                return False
            try:
                self.file = ocfn(self.path, 'w+')
            except IOError as ex:
                console.terse("Error: Truncating log file '{0}'\n".format(ex))
                self.file = None
                return False

            self.file.write(self.header)
            self.reopen()
        return True

    def assignRuleAction(self, rule=None):
        """
        Assigns correct log action based on rule
        """
        if rule is not None:
            self.rule = rule
        else:
            if self.rule == ONCE:
                self.action = self.once
            else:
                if self.rule == ALWAYS:
                    self.action = self.always
                else:
                    if self.rule == UPDATE:
                        self.action = self.update
                    else:
                        if self.rule == CHANGE:
                            self.action = self.change
                        else:
                            if self.rule == STREAK:
                                self.action = self.streak
                            else:
                                if self.rule == DECK:
                                    self.action = self.deck
                                else:
                                    self.action = self.never

    def buildHeader(self):
        """
        Build  .header
        """
        cf = io.StringIO()
        cf.write(ns2u(self.kind))
        cf.write('\t')
        cf.write(ns2u(LogRuleNames[self.rule]))
        cf.write('\t')
        cf.write(ns2u(self.baseFilename))
        cf.write('\n')
        cf.write('_time')
        for tag, fields in self.fields.items():
            if len(fields) > 1:
                for field in fields:
                    cf.write('\t{0}.{1}'.format(tag, field))

            else:
                cf.write('\t{0}'.format(tag))

        cf.write('\n')
        self.header = cf.getvalue()
        cf.close()

    def prepare(self):
        """
        Prepare log formats and values
        """
        console.profuse('     Preparing formats for Log {0}\n'.format(self.name))
        if self.rule in (DECK,):
            tag, loggee = self.loggees.items()[0]
            fields = self.fields.get(tag)
            if not fields:
                raise ValueError("Log {0}: Rule '{1}' requires field list.".format(self.name, LogRuleNames[DECK]))
        else:
            if self.rule in (STREAK,):
                tag, loggee = self.loggees.items()[0]
                if tag in self.fields:
                    if self.fields[tag]:
                        self.fields[tag] = self.fields[tag][:1]
                    else:
                        self.fields[tag] = [loggee.keys()[0]] if loggee else []
                else:
                    self.fields[tag] = [loggee.keys()[0]] if loggee else []
            else:
                for tag, loggee in self.loggees.items():
                    if tag not in self.fields or not self.fields[tag]:
                        self.fields[tag] = [field for field in loggee]

        self.formats.clear()
        self.formats['_time'] = '%s'
        for tag, fields in self.fields.items():
            self.formats[tag] = odict()
            for field in fields:
                fmt = '\t%s'
                self.formats[tag][field] = fmt

        if self.rule in (CHANGE,):
            self.lasts.clear()
            for tag, fields in self.fields.items():
                loggee = self.loggees[tag]
                lasts = [(key, loggee[key]) for key in fields if key in loggee]
                self.lasts[tag] = storing.Data(lasts)

        self.buildHeader()
        if self.stamp is None:
            if self.first:
                self.file.write(self.header)

    def format(self, value):
        """
        returns format string for value type
        """
        if isinstance(value, float):
            return '\t%0.4f'
        else:
            if isinstance(value, bool):
                return '\t%s'
            if isinstance(value, int) or isinstance(value, long):
                return '\t%d'
            return '\t%s'

    def log(self):
        """
        log loggees
        called by conditional actions
        """
        self.stamp = self.store.stamp
        cf = io.StringIO()
        try:
            text = self.formats['_time'] % self.stamp
        except TypeError:
            text = '%s' % self.stamp

        cf.write(ns2u(text))
        for tag, loggee in self.loggees.items():
            for field, fmt in self.formats[tag].items():
                if field in loggee:
                    value = loggee[field]
                    try:
                        text = fmt % value
                    except TypeError:
                        text = '\t%s' % value

                    cf.write(ns2u(text))
                else:
                    cf.write('\t')

        cf.write('\n')
        try:
            self.file.write(cf.getvalue())
        except ValueError as ex:
            console.terse('{0}\n'.format(ex))

        cf.close()

    def logStreak(self):
        """
        called by conditional actions
        Log and remove all elements of sequence in fifo order
        head is left tail is right, Fifo is head to tail

        """
        self.stamp = self.store.stamp
        cf = io.StringIO()
        if self.loggees:
            tag, loggee = self.loggees.items()[0]
            if loggee:
                if not self.fields[tag]:
                    field = loggee.keys()[0]
                    fmt = '\t%s'
                else:
                    field = self.fields[tag][0]
                    fmt = self.formats[tag][field]
                if field in loggee:
                    value = loggee[field]
                    d = deque()
                    if isinstance(value, MutableSequence):
                        while value:
                            d.appendleft(value.pop())

                    else:
                        if isinstance(value, MutableMapping):
                            while value:
                                d.appendleft(value.popitem())

                        else:
                            d.appendleft(value)
                        while d:
                            try:
                                text = self.formats['_time'] % self.stamp
                            except TypeError:
                                text = '%s' % self.stamp

                            cf.write(ns2u(text))
                            element = d.popleft()
                            try:
                                text = fmt % (element,)
                            except TypeError:
                                text = '\t%s' % element

                            cf.write(ns2u(text))
                            cf.write('\n')

                        try:
                            self.file.write(cf.getvalue())
                        except ValueError as ex:
                            console.terse('{0}\n'.format(ex))

        cf.close()

    def logDeck(self):
        """
        called by conditional actions
        Log and remove all elements of deck in fifo order which is pull
        """
        self.stamp = self.store.stamp
        if self.loggees:
            tag, loggee = self.loggees.items()[0]
            fields = self.fields[tag]
            if loggee.deck:
                cf = io.StringIO()
                while loggee.deck:
                    entry = loggee.pull()
                    if not isinstance(entry, Mapping):
                        console.concise("Log {0}: Deck entry of '{1}' = '{2}' not a mapping.\n".format(self.name, loggee.name, entry))
                    else:
                        try:
                            text = self.formats['_time'] % self.stamp
                        except TypeError:
                            text = '%s' % self.stamp

                        cf.write(ns2u(text))
                        for field in fields:
                            if field in entry:
                                fmt = self.formats[tag][field]
                                value = entry[field]
                                try:
                                    text = fmt % value
                                except TypeError:
                                    text = '\t%s' % value

                                cf.write(ns2u(text))
                            else:
                                cf.write('\t')

                        cf.write('\n')

                try:
                    self.file.write(cf.getvalue())
                except ValueError as ex:
                    console.terse('{0}\n'.format(ex))

                cf.close()

    def never(self):
        """
        log never
        This if for manual logging by frame action
        """
        pass

    def once(self):
        """
        log once
        Good for logging paramters that don't change but want record
        """
        if self.stamp is None:
            self.log()

    def always(self):
        """
        log always
        Good for logging every time logger runs unconditionally
        """
        self.log()

    def streak(self):
        """
        log sequence of first field of first loggee only
        log elements in fifo order from sequence until empty
        """
        self.logStreak()

    def deck(self):
        """
        log deck
        log elements in fifo order from deck until empty
        """
        self.logDeck()

    def update(self):
        """
        log if updated
        logs once and then only if updated after first time
        """
        if self.stamp is None:
            self.log()
            return
        for loggee in self.loggees.values():
            if loggee.stamp is not None:
                if loggee.stamp > self.stamp:
                    self.log()
                    return

    def change(self):
        """
        log if changed
        logs once and then only if changed after first time
        requires that self.prepare has been called otherwise fields in
        self.lasts won't match fields in log
        """
        if self.stamp is None:
            self.log()
            return
        change = False
        for tag, fields in self.fields.items():
            last = self.lasts[tag]
            loggee = self.loggees[tag]
            try:
                for field in fields:
                    if not hasattr(last, field):
                        if field in loggee:
                            change = True
                            setattr(last, field, loggee[field])
                        else:
                            if loggee[field] != getattr(last, field):
                                change = True
                                setattr(last, field, loggee[field])

            except AttributeError as ex:
                console.terse("Warning: Log {0}, missing field '{1}' for last value of loggee {2}\n".format(self.name, field, loggee.name))
            except KeyError as ex:
                console.terse("Warning: Log {0}, missing field '{1}' for loggee {2}\n".format(self.name, field, loggee.name))

        if change:
            self.log()

    def addLoggee(self, tag, loggee, fields=None):
        """
        Add a loggee at tag to .loggees
        Optional fields is list of field name strings to sub select fields in loggee
        """
        if self.stamp is None:
            if tag == '_time':
                raise excepting.ResolveError("Bad loggee tag '_time'", self.name, loggee.name)
            if tag in self.loggees:
                raise excepting.ResolveError('Duplicate tag', tag, loggee)
            self.loggees[tag] = loggee
            self.fields[tag] = fields if fields else []
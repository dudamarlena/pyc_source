# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/FoamMon/FoamDataStructures.py
# Compiled at: 2018-09-24 09:00:08
# Size of source mod 2**32: 14907 bytes
from docopt import docopt
from colorama import Fore, Back, Style
import datetime, os
try:
    from walk import walk
except ImportError:
    from os import walk

import time
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from copy import deepcopy
from .Log import Log
from .header import foamMonHeader
import sys

def timedelta(seconds):
    return datetime.timedelta(seconds=(int(max(0, seconds))))


default_elements = [
 'progressbar', 'folder', 'logfile', 'time', 'writeout', 'remaining']

class ColoredProgressBar:
    events = []

    def __init__(self, size, progress=0):
        self.size = size
        self.done_char = Fore.GREEN + '█' + Style.RESET_ALL
        self.undone_char = Fore.BLUE + '█' + Style.RESET_ALL
        self.digits = [self.done_char for _ in range(int(progress * size))]
        self.digits.extend([self.undone_char for _ in range(size - int(progress * size))])

    def add_event(self, percentage, color):
        index = int(percentage * self.size)
        self.digits[index] = color + '█' + Style.RESET_ALL

    def draw(self):
        return ''.join(self.digits)


class ProgressBar:
    events = []

    def __init__(self, size, progress=0):
        self.size = size
        self.done_char = '█'
        self.undone_char = '░'
        self.digits = [self.done_char for _ in range(int(progress * size))]
        self.digits.extend([self.undone_char for _ in range(size - int(progress * size))])

    def add_event(self, percentage, color):
        index = int(percentage * self.size)
        self.digits[index] = '█'

    def draw(self):
        return ''.join(self.digits)


class Cases:

    def __init__(self, path):
        self.path = path
        os.system('clear')
        self.mdates = {}
        self.cases = defaultdict(list)
        self.p = ThreadPoolExecutor(1)
        self.running = True
        self.future = self.p.submit(self.find_cases)

    def get_valid_cases(self):
        case_stats = {}
        cases = deepcopy(self.cases)
        for r, cs in cases.items():
            for c in cs:
                c.refresh()
                if c.log.active:
                    c.log.refresh()

            case_stats[r] = {'active':[c.print_status_short() for c in cs if c.print_status_short() if c.log.active], 
             'inactive':[c.print_status_short() for c in cs if c.print_status_short() if not c.log.active]}

        lengths = self.get_max_lengths(case_stats)
        return (lengths, case_stats)

    def get_max_lengths(self, statuses):
        lengths = {element:0 for element in default_elements}
        for n, folder in statuses.items():
            for s in folder.get('active', []):
                for elem in lengths.keys():
                    lengths[elem] = max(lengths[elem], s.lengths[elem])

            for s in folder.get('inactive', []):
                for elem in lengths.keys():
                    lengths[elem] = max(lengths[elem], s.lengths[elem])

        return lengths

    def find_cases(self):
        while self.running:
            top = self.path
            c = Case(top)
            subfold = top.split('/')[(-1)]
            if c.is_valid:
                exists = False
                for existing in self.cases[subfold]:
                    if c.path == existing.path:
                        exists = True

                if not exists:
                    self.cases[subfold].append(c)
            root_mdate = False
            if root_mdate:
                if os.path.getmtime(top) <= root_mdate:
                    for i in range(10):
                        if not self.running:
                            return
                        time.sleep(10)

                    continue
            root_mdate = os.path.getmtime(top)
            for r, dirs, _ in walk(self.path):
                ignore = [
                 'boundaryData',
                 'uniform',
                 'processor',
                 'constant',
                 'lagrangian',
                 'postProcessing',
                 'dynamicCode',
                 'system']
                for d in deepcopy(dirs):
                    for i in ignore:
                        if d.startswith(i):
                            dirs.remove(d)

                    full_path = os.path.join(r, d)
                    last_mdate = self.mdates.get(full_path)
                    if last_mdate and os.path.getmtime(full_path) <= last_mdate:
                        dirs.remove(d)

                for d in dirs:
                    try:
                        c = Case(os.path.join(r, d))
                        subfold = r.split('/')[(-1)]
                        if c.is_valid:
                            exists = False
                            for existing in self.cases[subfold]:
                                if c.path == existing.path:
                                    exists = True

                            if not exists:
                                full_path = os.path.join(r, d)
                                self.mdates[full_path] = os.path.getmtime(full_path)
                                self.cases[subfold].append(c)
                    except Exception as e:
                        print('innner', e, r, d)

            for i in range(10):
                if not self.running:
                    return
                time.sleep(1)

    def print_legend(self):
        s = '\nLegend: '
        s += Fore.GREEN + '█' + Style.RESET_ALL + ' Progress '
        s += Fore.YELLOW + '█' + Style.RESET_ALL + ' Start Sampling '
        s += Style.BRIGHT + 'Active' + Style.RESET_ALL + ' '
        s += Style.DIM + 'Inactive' + Style.RESET_ALL + '\n'
        print(s)

    def print_status(self):
        str_ = '\n'.join([c.print_status_short() for c in self.cases if c.print_status_short if c.log.active])
        print(str_)


class Case:

    def __init__(self, path, log_format='log', summary=False, log_filter=None):
        self.path = path
        self.folder = os.path.basename(self.path)
        self.log_format = log_format
        self.log_fns = self.find_logs(self.log_format)
        self.current_log_fn = self.find_recent_log_fn()
        self.current_log = Log(self.current_log_fn, self)
        self.log_filter = log_filter
        if summary:
            if self.log.active:
                ret = self.print_status_short()
                if ret:
                    print(ret)

    @property
    def log(self):
        return self.current_log

    def refresh(self):
        log_fns = self.find_logs(self.log_format)
        if set(log_fns) == set(self.log_fns):
            return
        self.log_fns = log_fns
        current_log_fn = self.find_recent_log_fn()
        if self.current_log_fn == current_log_fn:
            return self.current_log
        self.current_log_fn = current_log_fn
        self.current_log = Log(current_log_fn, self)

    @property
    def is_valid(self):
        return self.has_controlDict and self.log.is_valid

    @property
    def started_sampling(self):
        return self.simTime > self.startSampling

    @property
    def has_controlDict(self):
        ctDct = os.path.exists(self.controlDict_file)
        return ctDct

    def status_bar(self, digits=100):
        bar = ProgressBar(digits, self.log.progress(self.endTime))
        bar.add_event(self.startSamplingPerc, Fore.YELLOW)
        return bar.draw()

    def custom_filter_value(self, regex):
        return self.log.get_latest_value(regex, self.log.cached_body)

    def find_logs(self, log_format):
        """ returns a list of filenames and ctimes """
        r, d, files = next(walk(self.path))
        files = list(filter(lambda x: log_format in x, files))
        files = [os.path.join(r, f) for f in files]
        ctimes = [os.path.getctime(os.path.join(self.path, f)) for f in files]
        return list(zip(ctimes, files))

    @property
    def last_timestep_ondisk(self):
        if self.log.is_parallel:
            proc_dir = os.path.join(self.path, 'processor0')
            if not os.path.exists(proc_dir):
                return 0
            else:
                r, ds, _ = next(walk(proc_dir))
                ds = [float(d) for d in ds if 'constant' not in d]
                if ds:
                    return max(ds)
                return 0
        else:
            ts = []
            r, ds, _ = next(walk(self.path))
            for t in ds:
                try:
                    tsf = float(t)
                    ts.append(tsf)
                except:
                    pass

            if ts:
                return max(ts)
            else:
                return 0.0

    def find_recent_log_fn(self):
        try:
            ctimes, files = zip(*self.log_fns)
            latest_index = ctimes.index(max(ctimes))
            return files[latest_index]
        except:
            return False

    @property
    def controlDict_file(self):
        return os.path.join(self.path, 'system/controlDict')

    def get_key_controlDict(self, key):
        """ find given key in controlDict """
        separator = ' '
        key += separator
        if self.has_controlDict:
            with open(self.controlDict_file) as (f):
                for i, line in enumerate(f.readlines()):
                    if key in line:
                        return line.replace(key, '').replace(' ', '').replace(';', '').replace('\n', '')

        else:
            return

    def get_float_controlDict(self, key):
        ret = self.get_key_controlDict(key)
        if ret:
            return float(ret)
        else:
            return 0

    @property
    def endTime(self):
        return self.get_float_controlDict('endTime')

    @property
    def writeControl(self):
        return self.get_key_controlDict('writeControl')

    @property
    def writeInterval(self):
        if self.writeControl == 'runTime' or self.writeControl == 'adjustableRunTime':
            return self.get_float_controlDict('writeInterval')
        else:
            return self.get_float_controlDict('writeInterval') * self.get_float_controlDict('deltaT')

    @property
    def startSampling(self):
        return self.get_float_controlDict('timeStart')

    @property
    def startSamplingPerc(self):
        return self.startSampling / self.endTime

    @property
    def simTime(self):
        return self.log.sim_time

    def print_status_short(self):
        try:
            exc_info = sys.exc_info()
            return Status(self, self.log.progress(self.endTime), 50, self.log.active, self.folder, os.path.basename(self.log.path), self.log.sim_time, timedelta(self.log.time_till_writeout()), timedelta(self.log.timeleft()))
        except Exception as e:
            import traceback
            print(e, self.path)
            print((traceback.print_exception)(*exc_info))
            return False

    def print_status_full(self):
        while True:
            self.log.print_log_body()
            try:
                prog_prec = self.log.progress(self.endTime) * 100.0
                print(self.status_bar(100))
                print('Case properties: ')
                print('Job start time: ', self.log.start_time)
                print('Job elapsed_ time: ', timedelta(seconds=(self.log.wall_time)))
                print('Active: ', self.log.active)
                print('Parallel: ', self.log.is_parallel)
                print('Case end time: ', self.endTime)
                print('Current sim time: ', self.log.sim_time)
                print('Last time step on disk: ', self.last_timestep)
                print('Time next writeout: ', timedelta(self.log.time_till_writeout()))
                print('Progress: ', prog_prec)
                print('Timeleft: ', timedelta(self.log.timeleft()))
            except Exception as e:
                print(e)

            self.log.refresh()
            time.sleep(0.2)
            os.system('clear')


class Status:
    __doc__ = ' Handle status of single case for simple printing  '

    def __init__(self, case, progress, digits, active, folder, logfile, time, writeout, remaining):
        self.case = case
        self.progress = progress
        self.digits = digits
        self.active = active
        self.folder = folder
        self.logfile = logfile
        self.time = str(time)
        self.writeout = str(writeout)
        self.remaining = str(remaining)

    @property
    def lengths(self):
        """ returns the lengths of the returned strings """
        return {'progressbar':self.digits, 
         'folder':len(self.folder), 
         'logfile':len(self.logfile), 
         'time':len(self.time), 
         'writeout':len(self.writeout), 
         'remaining':len(self.remaining)}

    def custom_filter(self, value):
        return self.case.custom_filter_value(value)
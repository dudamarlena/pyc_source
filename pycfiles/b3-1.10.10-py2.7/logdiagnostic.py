# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\logdiagnostic.py
# Compiled at: 2016-03-08 18:42:10
__version__ = '0.9.5'
__author__ = 'GrosBedo'
import os.path, time, re, sys
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(pathname, 'b3', 'lib'))
import math
from statlib import stats as mstats
import corestats, itertools, pprint, cPickle as pickle, yaml
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import csv
try:
    import numpy
except:
    pass

class LogDiagnostic():
    _lineFormat = '^\\s*(?P<minutes>[0-9]+):(?P<seconds>[0-9]+)\\s*.*'
    maxlines = 0
    significantzero = True
    debug = False
    faster = True
    morefaster = False

    def lines_per_second(self, *args):
        self.supermatrix = []
        for game_log in args:
            matrix = []
            previoustime = None
            f = re.compile(self._lineFormat, re.IGNORECASE)
            previouscursor = 0
            try:
                self.file = open(game_log, 'r')
                self.file.seek(0, os.SEEK_SET)
                i = 0
                for line in self.file:
                    i += 1
                    m = re.match(f, line)
                    if m:
                        gametime = int(m.group('seconds')) + int(m.group('minutes')) * 60
                        if self.debug:
                            print '%i- gametime %s %s:%s' % (i, str(gametime), str(m.group('minutes')), str(m.group('seconds')))
                        if previoustime is None:
                            matrix.append(1)
                        elif gametime == previoustime:
                            matrix[(-1)] += 1
                        elif gametime > previoustime + 1:
                            if self.significantzero:
                                matrix.extend([ 0 for j in range(previoustime, gametime - 1) ])
                            matrix.append(1)
                        else:
                            matrix.append(1)
                        previoustime = gametime
                    if i >= self.maxlines and self.maxlines > 0:
                        print 'Reached maxlines, breaking...'
                        break
                    filestats = os.fstat(self.file.fileno())
                    currpos = self.file.tell()
                    filesize = filestats.st_size
                    if previouscursor != currpos:
                        if self.faster:
                            if i % 1000 == 0:
                                print 'Processing %s%% (byte %s of %s)...' % (str(currpos * 100 / filesize), str(currpos), str(filesize))
                        elif not self.morefaster:
                            print 'Processing %s%% (byte %s of %s)...' % (str(currpos * 100 / filesize), str(currpos), str(filesize))
                        previouscursor = currpos
                    time.sleep(0.0001)

                self.file.close()
                if self.debug:
                    pprint.pprint(matrix)
                self.supermatrix.append((game_log, matrix))
            except Exception as e:
                print 'Exception when reading the logs per second: ' + str(e)

        return self.supermatrix

    def stats_per_second(self, *args):
        superstats = []
        for game_log, matrix in args:
            cstats = corestats.Stats()
            stats = {}
            mode = cstats.mode(matrix)
            stats['mode'] = mode[0][0]
            stats['modenext'] = mode[1][0]
            stats['mean'] = cstats.mean(matrix)
            stats['median'] = cstats.median(matrix)
            stats['variance'] = cstats.variance(matrix)
            stats['stddeviation'] = stats['variance'] ** 0.5
            stats['3sigma'] = 3 * stats['stddeviation']
            stats['cumfreq'] = mstats.cumfreq(matrix)
            stats['itemfreq'] = mstats.itemfreq(matrix)
            stats['min'] = min(matrix)
            stats['max'] = max(matrix)
            stats['samplespace'] = stats['max'] - stats['min']
            stats['count'] = len(matrix)
            stats['kurtosis'] = mstats.kurtosis(matrix)
            stats['perfectvalue'] = int(math.ceil(stats['3sigma'] + stats['mean']))
            stats['perfectscore'] = cstats.percentileforvalue(matrix, math.ceil(stats['3sigma'] + stats['mean']))
            scorepercentiles = [10, 30, 50, 70, 80, 85, 90, 95, 99, 99.9, 99.99]
            stats['itemscore'] = [ (percentile, cstats.valueforpercentile(matrix, percentile)) for percentile in scorepercentiles ]
            stats['skew'] = mstats.skew(matrix)
            if stats['skew'] > 0:
                stats['skewmeaning'] = 'There exist more smaller values from the mean than higher'
            else:
                stats['skewmeaning'] = 'There exist more higher values from the mean than smaller'
            superstats.append((game_log, stats))

        return superstats

    def show_results(self, filename=None, *args):
        restorestdout = sys.stdout
        if filename:
            self.stream = open(filename, 'w')
            sys.stdout = self.stream
        else:
            self.stream = sys.stdout
        try:
            for game_log, stats in args:
                print >> self.stream, '\n-------------------------'
                print >> self.stream, '\nStats per second of the log file %s:\n' % game_log
                print >> self.stream, 'Zero is significant (count missing lines): %s' % str(self.significantzero)
                pprint.pprint(stats)

        except:
            pprint.pprint(args)

        sys.stdout = restorestdout

    def save_data_yaml(self, filename=None, *args):
        """ Save or show the results in YAML """
        if filename:
            self.stream = open(filename, 'w')
        else:
            self.stream = sys.stdout
        try:
            for game_log, stats in args:
                print >> self.stream, '### Stats per second of the log file %s:\n' % game_log
                print >> self.stream, '# Zero is significant (count missing lines): %s' % str(self.significantzero)
                print >> self.stream, yaml.dump(stats, default_flow_style=False, Dumper=Dumper)
                print >> self.stream, '---'

        except:
            print >> self.stream, yaml.dump_all(args, default_flow_style=False, Dumper=Dumper)

    def load_data_yaml(self, *args):
        """ Load one or several YAML stats files and merge them with current results """
        superstats = []
        for filename in args:
            self.stream = open(filename, 'r')
            superstats.extend([ data for data in yaml.load_all(self.stream, Loader=Loader) if data is not None ])

        return superstats

    def save_data_csv(self, filename, *args):
        """ much more ressource efficient function but can only save matrixes (better than pickler but not cPickler) """
        try:
            file = open(filename, 'w')
            csvWriter = csv.writer(file, delimiter='\n', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow([ object for object in args ])
            file.close
            return True
        except Exception as e:
            print 'Exception when trying to save the stats: %s' % str(e)
            return False

    def load_data_csv(self, *args):
        """ load the stats in a simple format and preallocate memory, faster than pickler but slower than cPickler """

        def count(file):
            while 1:
                block = file.read(65536)
                if not block:
                    break
                yield block.count('\n')

        superstats = []
        for filename in args:
            try:
                file = open(filename, 'rb')
                linecount = sum(count(file))
                lastindex = len(superstats)
                superstats.extend([0] * linecount)
                file.seek(0)
                i = 0
                for row in file:
                    if row.strip():
                        superstats[lastindex + i] = int(row.strip())
                        i += 1

                file.close
            except Exception as e:
                print 'Exception when trying to load the stats: %s' % str(e)
                return False

        return superstats

    def save_data(self, filename, *args):
        """ an all-round saving to file function, it can dump any python object and restore it later, but it's not very ressource efficient """
        try:
            file = open(filename, 'w')
            for object in args:
                pickle.dump(object, file)

            file.close
            return True
        except Exception as e:
            print 'Exception when trying to save the stats: %s' % str(e)
            return False

    def load_data(self, merge=False, *args):
        """ merge will directly merge the stats asap if enabled, this saves us a lot of memory """
        superstats = []
        for filename in args:
            try:
                file = open(filename, 'r')
                if merge:
                    for object in pickle.load(file):
                        if type(superstats) is numpy.ndarray:
                            superstats = numpy.hstack(superstats, object[1])
                        else:
                            superstats.extend(object[1])

                else:
                    superstats.append(pickle.load(file))
                file.close
            except Exception as e:
                print 'Exception when trying to load the stats: %s' % str(e)
                return False

        return superstats

    def merge_matrix(self, *args):
        merged_matrix = self.flatten([ somelist[1] for somelist in args ])
        return ('merged gamelogs', merged_matrix)

    def weighted_mean_merge(self, *args):
        newstat = {}
        superstats = {}
        args = [ elmt for elmt in args if elmt is not None ]
        for stats in args:
            count = stats['count']
            try:
                del stats['skewmeaning']
                del stats['cumfreq']
                del stats['itemfreq']
                del stats['itemscore']
            except KeyError as e:
                print 'Notice: one of the loaded stat file seems to have been generated by an older version of the Diagnostic tool ! You may miss some important new parameters !'

            for key, value in stats.iteritems():
                if key is not 'count' and key is not 'skewmeaning' and key is not 'cumfreq':
                    newstat[key] = value * count
                    try:
                        superstats[key] += newstat[key]
                    except Exception as e:
                        superstats[key] = newstat[key]

        divisor = sum([ stat['count'] for stat in args ])
        weighted_stats = dict(map(lambda (key, value): (key, float(value) / divisor), superstats.iteritems()))
        weighted_stats['count'] = divisor
        weighted_stats['perfectvalue'] = int(math.ceil(weighted_stats['3sigma'] + weighted_stats['mean']))
        weighted_stats['perfectscore'] = 'NA - Cannot know without the raw datas matrix !'
        if weighted_stats['skew'] > 0:
            weighted_stats['skewmeaning'] = 'There exist more smaller values from the mean than higher'
        else:
            weighted_stats['skewmeaning'] = 'There exist more higher values from the mean than smaller'
        if self.debug:
            pprint.pprint(weighted_stats)
        return [
         (
          'weighted-mean merged log', weighted_stats)]

    def flatten(self, *args):
        return [ item for sublist in args[0] for item in sublist ]

    def flatten2(self, sequence):

        def rflat(seq2):
            seq = []
            for entry in seq2:
                if '__contains__' in dir(entry) and type(entry) != str and type(entry) != dict:
                    seq.extend([ i for i in entry ])
                else:
                    seq.append(entry)

            return seq

        def seqin(sequence):
            for i in sequence:
                if '__contains__' in dir(i) and type(i) != str and type(i) != dict:
                    return True

            return False

        seq = sequence[:]
        while seqin(seq):
            seq = rflat(seq)

        return seq


if __name__ == '__main__':
    p = LogDiagnostic()
    p.significantzero = False
    p.debug = False
    p.maxlines = 0
    supermatrix = p.lines_per_second('/some/dir/games_mp.log', '/some/dir/games_mp2.log')
    superstats = p.stats_per_second(*supermatrix)
    weighted_merged_stats = p.weighted_mean_merge(*superstats)
    merged_matrix = p.merge_matrix(*supermatrix)
    merged_stats = p.stats_per_second(merged_matrix)
    p.show_results(None, *superstats)
    p.show_results(None, *weighted_merged_stats)
    p.show_results(None, *merged_stats)
    p.save_data('/some/dir/somestats.txt', *superstats)
    somestats = p.load_data(False, '/some/dir/somestats.txt')
    p.show_results(None, *somestats)
    testsuperstats = [
     (
      '/some/dir/games_mp.log',
      {'3sigma': 6.945390758841171, 'count': 11, 
         'cumfreq': (
                   [
                    20171,
                    25702,
                    25808,
                    25850,
                    25862,
                    25879,
                    25891,
                    25898,
                    25908,
                    25909],
                   -1.86000005,
                   5.7200001,
                   0), 
         'kurtosis': 114.34922587149542, 
         'max': 53, 
         'mean': 2.651009301787024, 
         'median': 2.0230774326176335, 
         'min': 1, 
         'mode': 2, 
         'modenext': 1, 
         'samplespace': 52, 
         'skew': 7.786981504523521, 
         'skewmeaning': 'There exist more smaller values from the mean than higher', 
         'stddeviation': 2.315130252947057, 
         'variance': 5.359828088110704}),
     (
      '/some/dir/games_mp2.log',
      {'3sigma': 6.945390758841171, 'count': 11, 
         'cumfreq': (
                   [
                    20171,
                    25702,
                    25808,
                    25850,
                    25862,
                    25879,
                    25891,
                    25898,
                    25908,
                    25909],
                   -1.86000005,
                   5.7200001,
                   0), 
         'kurtosis': 114.34922587149542, 
         'max': 53, 
         'mean': 2.651009301787024, 
         'median': 2.0230774326176335, 
         'min': 6, 
         'mode': 2, 
         'modenext': 1, 
         'samplespace': 52, 
         'skew': 7.786981504523521, 
         'skewmeaning': 'There exist more smaller values from the mean than higher', 
         'stddeviation': 2.315130252947057, 
         'variance': 5.359828088110704})]
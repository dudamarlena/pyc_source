# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/statsAndLogging.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 8196 bytes
from __future__ import absolute_import
from builtins import str
from builtins import object
import gzip, json, logging, os, time
from threading import Thread, Event
from toil.lib.expando import Expando
from toil.lib.bioio import getTotalCpuTime
logger = logging.getLogger(__name__)

class StatsAndLogging(object):
    __doc__ = '\n    Class manages a thread that aggregates statistics and logging information on a toil run.\n    '

    def __init__(self, jobStore, config):
        self._stop = Event()
        self._worker = Thread(target=(self.statsAndLoggingAggregator), args=(
         jobStore, self._stop, config),
          daemon=True)

    def start(self):
        """
        Start the stats and logging thread.
        """
        self._worker.start()

    @classmethod
    def formatLogStream(cls, stream, identifier=None):
        """
        Given a stream of text or bytes, and the job name, job itself, or some
        other optional stringifyable identity info for the job, return a big
        text string with the formatted job log, suitable for printing for the
        user.
        
        We don't want to prefix every line of the job's log with our own
        logging info, or we get prefixes wider than any reasonable terminal
        and longer than the messages.
        """
        lines = []
        if identifier is not None:
            if isinstance(identifier, bytes):
                identifier = identifier.decode('utf-8', error='replace')
            else:
                if not isinstance(identifier, str):
                    identifier = str(identifier)
            lines.append('Log from job %s follows:' % identifier)
        else:
            lines.append('Log from job follows:')
        lines.append('=========>')
        for line in stream:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            lines.append('\t' + line.rstrip('\n'))

        lines.append('<=========')
        return '\n'.join(lines)

    @classmethod
    def logWithFormatting(cls, jobStoreID, jobLogs, method=logger.debug, message=None):
        if message is not None:
            method(message)
        method(cls.formatLogStream(jobLogs, jobStoreID))

    @classmethod
    def writeLogFiles(cls, jobNames, jobLogList, config, failed=False):

        def createName(logPath, jobName, logExtension, failed=False):
            logName = jobName.replace('-', '--')
            logName = logName.replace('/', '-')
            logName = logName.replace(' ', '_')
            logName = logName.replace("'", '')
            logName = logName.replace('"', '')
            logName = ('failed_' if failed else '') + logName
            counter = 0
            while True:
                suffix = str(counter).zfill(3) + logExtension
                fullName = os.path.join(logPath, logName + suffix)
                if len(fullName) >= 255:
                    return fullName[:255 - len(suffix)] + suffix
                if not os.path.exists(fullName):
                    return fullName
                counter += 1

        mainFileName = jobNames[0]
        extension = '.log'
        if config.writeLogs:
            path = config.writeLogs
            writeFn = open
        else:
            if config.writeLogsGzip:
                path = config.writeLogsGzip
                writeFn = gzip.open
                extension += '.gz'
            else:
                return
        fullName = createName(path, mainFileName, extension, failed)
        with writeFn(fullName, 'wb') as (f):
            for l in jobLogList:
                try:
                    l = l.decode('utf-8')
                except AttributeError:
                    pass

                if not l.endswith('\n'):
                    l += '\n'
                f.write(l.encode('utf-8'))

        for alternateName in jobNames[1:]:
            name = createName(path, alternateName, extension, failed)
            os.symlink(os.path.relpath(fullName, path), name)

    @classmethod
    def statsAndLoggingAggregator(cls, jobStore, stop, config):
        """
        The following function is used for collating stats/reporting log messages from the workers.
        Works inside of a thread, collates as long as the stop flag is not True.
        """
        startTime = time.time()
        startClock = getTotalCpuTime()

        def callback(fileHandle):
            statsStr = fileHandle.read()
            if not isinstance(statsStr, str):
                statsStr = statsStr.decode()
            stats = json.loads(statsStr, object_hook=Expando)
            try:
                logs = stats.workers.logsToMaster
            except AttributeError:
                pass
            else:
                for message in logs:
                    logger.log(int(message.level), 'Got message from job at time %s: %s', time.strftime('%m-%d-%Y %H:%M:%S'), message.text)

            try:
                logs = stats.logs
            except AttributeError:
                pass
            else:
                jobNames = logs.names
                messages = logs.messages
                cls.logWithFormatting((jobNames[0]), messages, message='Received Toil worker log. Disable debug level logging to hide this output')
                cls.writeLogFiles(jobNames, messages, config=config)

        while 1:
            if stop.is_set():
                jobStore.readStatsAndLogging(callback)
                break
            if jobStore.readStatsAndLogging(callback) == 0:
                time.sleep(0.5)

        text = json.dumps(dict(total_time=(str(time.time() - startTime)), total_clock=(str(getTotalCpuTime() - startClock))),
          ensure_ascii=True)
        jobStore.writeStatsAndLogging(text)

    def check(self):
        """
        Check on the stats and logging aggregator.
        :raise RuntimeError: If the underlying thread has quit.
        """
        if not self._worker.is_alive():
            raise RuntimeError('Stats and logging thread has quit')

    def shutdown(self):
        """
        Finish up the stats/logging aggregation thread
        """
        logger.debug('Waiting for stats and logging collator thread to finish ...')
        startTime = time.time()
        self._stop.set()
        self._worker.join()
        logger.debug('... finished collating stats and logs. Took %s seconds', time.time() - startTime)
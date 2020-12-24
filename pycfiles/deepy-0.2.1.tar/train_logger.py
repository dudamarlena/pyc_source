# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/train_logger.py
# Compiled at: 2016-04-20 00:05:45
import os, datetime, logging as loggers, deepy
logging = loggers.getLogger(__name__)
PROGRESS_LOG_PREFIX = 'progress:'

class TrainLogger(object):

    def __init__(self):
        self.log_pool = []
        self._progress = 0

    def load(self, model_path):
        log_path = self._log_path(model_path)
        if os.path.exists(log_path):
            logging.info('Load training log from %s' % log_path)
            for line in open(log_path).xreadlines():
                if line.startswith(PROGRESS_LOG_PREFIX):
                    self._progress = int(line.replace(PROGRESS_LOG_PREFIX, '').strip())
                    continue
                self.log_pool.append(line.strip())

    def record(self, line):
        time_mark = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S] ')
        self.log_pool.append(time_mark + line)

    def record_progress(self, progress):
        """
        Record current progress in the training[1;3B].
        """
        self._progress = progress

    def progress(self):
        """
        Get loaded progress.
        """
        return self._progress

    def save(self, model_path):
        log_path = self._log_path(model_path)
        logging.info('Save training log to %s' % log_path)
        with open(log_path, 'w') as (outf):
            outf.write('# deepy version: %s\n' % deepy.__version__)
            for line in self.log_pool:
                outf.write(line + '\n')

            if self._progress > 0:
                outf.write('%s %d\n' % (PROGRESS_LOG_PREFIX, self._progress))

    def _log_path(self, model_path):
        log_path = model_path.rsplit('.', 1)[0] + '.log'
        return log_path
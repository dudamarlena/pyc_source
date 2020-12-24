# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hudan/Git/nerlogparser/nerlogparser/model/general_utils.py
# Compiled at: 2019-01-06 22:49:51
# Size of source mod 2**32: 4656 bytes
import time, sys, logging, numpy as np

def get_logger(filename):
    """Return a logger instance that writes in filename

    Args:
        filename: (string) path to log.txt

    Returns:
        logger: (instance of logger)

    """
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger


class Progbar(object):
    __doc__ = 'Progbar class copied from keras (https://github.com/fchollet/keras/)\n\n    Displays a progress bar.\n    Small edit : added strict arg to update\n    # Arguments\n        target: Total number of steps expected.\n        interval: Minimum visual progress update interval (in seconds).\n    '

    def __init__(self, target, width=30, verbose=1):
        self.width = width
        self.target = target
        self.sum_values = {}
        self.unique_values = []
        self.start = time.time()
        self.total_width = 0
        self.seen_so_far = 0
        self.verbose = verbose

    def update(self, current, values=[], exact=[], strict=[]):
        """
        Updates the progress bar.
        # Arguments
            current: Index of current step.
            values: List of tuples (name, value_for_last_step).
                The progress bar will display averages for these values.
            exact: List of tuples (name, value_for_last_step).
                The progress bar will display these values directly.
        """
        for k, v in values:
            if k not in self.sum_values:
                self.sum_values[k] = [
                 v * (current - self.seen_so_far),
                 current - self.seen_so_far]
                self.unique_values.append(k)
            else:
                self.sum_values[k][0] += v * (current - self.seen_so_far)
                self.sum_values[k][1] += current - self.seen_so_far

        for k, v in exact:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = [
             v, 1]

        for k, v in strict:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = v

        self.seen_so_far = current
        now = time.time()
        if self.verbose == 1:
            prev_total_width = self.total_width
            sys.stdout.write('\x08' * prev_total_width)
            sys.stdout.write('\r')
            numdigits = int(np.floor(np.log10(self.target))) + 1
            barstr = '%%%dd/%%%dd [' % (numdigits, numdigits)
            bar = barstr % (current, self.target)
            prog = float(current) / self.target
            prog_width = int(self.width * prog)
            if prog_width > 0:
                bar += '=' * (prog_width - 1)
                if current < self.target:
                    bar += '>'
                else:
                    bar += '='
                bar += '.' * (self.width - prog_width)
                bar += ']'
                sys.stdout.write(bar)
                self.total_width = len(bar)
                if current:
                    time_per_unit = (now - self.start) / current
                else:
                    time_per_unit = 0
                eta = time_per_unit * (self.target - current)
                info = ''
                if current < self.target:
                    info += ' - ETA: %ds' % eta
            else:
                info += ' - %ds' % (now - self.start)
            for k in self.unique_values:
                if type(self.sum_values[k]) is list:
                    info += ' - %s: %.4f' % (k,
                     self.sum_values[k][0] / max(1, self.sum_values[k][1]))
                else:
                    info += ' - %s: %s' % (k, self.sum_values[k])

            self.total_width += len(info)
            if prev_total_width > self.total_width:
                info += (prev_total_width - self.total_width) * ' '
            sys.stdout.write(info)
            sys.stdout.flush()
            if current >= self.target:
                sys.stdout.write('\n')
        if self.verbose == 2 and current >= self.target:
            info = '%ds' % (now - self.start)
            for k in self.unique_values:
                info += ' - %s: %.4f' % (k, self.sum_values[k][0] / max(1, self.sum_values[k][1]))

            sys.stdout.write(info + '\n')

    def add(self, n, values=[]):
        self.update(self.seen_so_far + n, values)
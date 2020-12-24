# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\msg_stats_log_formatter\formatter.py
# Compiled at: 2015-05-07 07:34:08
import json, time, logging, os, sys, datetime, traceback, csv, wcutil
logger = logging.getLogger('stats')

class StatsLog(object):

    def __init__(self):
        self.msg_ids = []
        self.stats = {}
        self.stats_output_interval_secs = 60
        self.stats_input_interval_secs = 30
        self.fields = ['count', 'avg_tps', 'max_tps', 'max_time', 'avg_time', 'acc_time']
        self.output_timestamp_format = '%Y-%m-%d %H:%M'

    def read_file(self, filename):
        logger.info(' - read: ' + filename)
        f = open(filename)
        if f is None:
            return False
        else:
            lines = f.readlines()
            skip = False
            for log in lines:
                try:
                    if -1 < log.find('현재 통계'):
                        skip = False
                    if -1 < log.find('누적 통계'):
                        skip = True
                    if skip or -1 < log.find('=====') or -1 < log.find('-----'):
                        continue
                    tokens = log.replace('\n', '').replace('\t', '').split('|')
                    if tokens is None or 6 > len(tokens):
                        continue
                    tokens[0] = tokens[0].replace('[', '').replace(']', '')
                    tokens = map(str.strip, tokens)
                    timestamp = datetime.datetime.strptime(tokens[0], '%Y-%m-%d %H:%M:%S').strftime(self.output_timestamp_format)
                    msg_id = tokens[1]
                    count = wcutil.to_number(tokens[2])
                    if count is None:
                        continue
                    avg_tps = float(count) / self.stats_input_interval_secs
                    max_tps = avg_tps
                    max_time = wcutil.to_number(tokens[4])
                    avg_time = wcutil.to_number(tokens[5])
                    fake_tps = wcutil.to_number(tokens[3])
                    acc_time = float(count) / fake_tps if fake_tps is not None else 0
                    self._add_stats_item(timestamp, 'total', count, avg_tps, max_tps, avg_time, max_time, acc_time)
                    self._add_stats_item(timestamp, msg_id, count, avg_tps, max_tps, avg_time, max_time, acc_time)
                except Exception as e:
                    logger.error('Exception occurred: ' + e)
                    logger.error(traceback.print_exc())

            return True

    def _add_stats_item(self, timestamp, msg_id, count, avg_tps, max_tps, avg_time, max_time, acc_time):
        if msg_id not in self.msg_ids:
            self.msg_ids.append(msg_id)
        if timestamp not in self.stats:
            self.stats[timestamp] = {}
        if msg_id not in self.stats[timestamp]:
            self.stats[timestamp][msg_id] = {}
            self.stats[timestamp][msg_id]['count'] = count
            self.stats[timestamp][msg_id]['avg_tps'] = avg_tps
            self.stats[timestamp][msg_id]['max_tps'] = max_tps
            self.stats[timestamp][msg_id]['max_time'] = max_time
            self.stats[timestamp][msg_id]['avg_time'] = avg_time
            self.stats[timestamp][msg_id]['acc_time'] = acc_time
        else:
            self.stats[timestamp][msg_id]['count'] += count
            self.stats[timestamp][msg_id]['avg_tps'] = float(self.stats[timestamp][msg_id]['count']) / self.stats_output_interval_secs
            self.stats[timestamp][msg_id]['max_tps'] = max(self.stats[timestamp][msg_id]['max_tps'], max_tps)
            self.stats[timestamp][msg_id]['avg_time'] = (self.stats[timestamp][msg_id]['avg_time'] + avg_time) / 2
            self.stats[timestamp][msg_id]['max_time'] = max(self.stats[timestamp][msg_id]['max_time'], max_time)
            self.stats[timestamp][msg_id]['acc_time'] += acc_time

    def _create_csv(self, date):
        filename = 'output.' + date + '.txt'
        logger.info(' - write: ' + filename)
        is_new_file = True
        try:
            if 0 < os.path.getsize(filename):
                is_new_file = False
        except os.error:
            pass

        f = open(filename, 'w')
        is_new_file = True
        writer = csv.writer(f, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_ALL)
        if is_new_file:
            header = []
            for field in self.fields:
                header.append(field)
                header.extend(self.msg_ids)

            writer.writerow(header)
        return writer

    def write_file(self, daily_rolling_file=True):
        if self.stats is None:
            return False
        else:
            writer = None
            date = ''
            for timestamp, values in self.stats.items():
                row = [timestamp]
                for field in self.fields:
                    for msg_id in self.msg_ids:
                        if msg_id in values:
                            row.append(values[msg_id][field])
                        else:
                            row.append(0)

                    row.append('|')

                if daily_rolling_file:
                    date2 = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d')
                    if date != date2:
                        date = date2
                        writer = self._create_csv(date)
                elif writer is None:
                    writer = self._create_csv(datetime.datetime.now().strftime('%Y%m%d_%H%M'))
                writer.writerow(row)

            return True


def run():
    main(None)
    return


def main(args):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    filenames = wcutil.find_files('./logs', '*.log')
    filenames.sort()
    stats = StatsLog()
    stats.output_timestamp_format = '%Y-%m-%d %H:00'
    stats.stats_output_interval_secs = 3600
    for filename in filenames:
        stats.read_file(filename)

    stats.write_file(False)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    sys.exit(main(sys.argv))
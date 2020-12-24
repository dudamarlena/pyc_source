# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csv2graphite/csv2graphite.py
# Compiled at: 2014-01-17 08:18:01
"""Send CSV CodaHale metrics to a graphite server
"""
import os, sys
from time import sleep
from optparse import OptionParser, TitledHelpFormatter
import csv
USAGE = '%prog [options] CSV_FOLDER | nc graphite 2030\n\nYou need to change temporary your carbon conf to set\nMAX_CREATES_PER_MINUTE = inf\n\nOr use the proper --max_creates_per_minute of %prog.\n'

def get_version():
    """Retrun the package version."""
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        version = get_distribution('csv2graphite').version
    except DistributionNotFound:
        version = 'dev'

    return version


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():
    parser = OptionParser(USAGE, formatter=TitledHelpFormatter(), version='csv2graphite ' + get_version())
    parser.add_option('--prefix', type='string', dest='prefix', default='servers.csv2graphite.nuxeo', help='Setup the metric graphite prefix')
    parser.add_option('--max_creates_per_minute', type='int', default=0, help='The carbon MAX_CREATES_PER_MINUTE used to limit the input')
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')
    csv_dir = args[0]
    prefix = options.prefix
    max_creates_per_minute = options.max_creates_per_minute
    if not os.path.isdir(csv_dir):
        parser.error('Invalid CSV folder: ' + csv_dir)
    wsp_files = 0
    wsp_count = 0
    for csv_file in os.listdir(csv_dir):
        if not csv_file.endswith('.csv'):
            continue
        name = prefix + '.' + csv_file[:-4]
        sys.stderr.write('Processing: ' + name + '\n')
        with open(os.path.join(csv_dir, csv_file), 'rb') as (csvfile):
            reader = csv.reader(csvfile, delimiter=',')
            header = reader.next()
            wsp_count += len(header) - 1
            if wsp_count > max_creates_per_minute:
                wsp_files += wsp_count
                wsp_count = 0
                if max_creates_per_minute > 0:
                    sys.stderr.write('Sleeping 1min before MAX_CREATES_PER_MINUTE is reached')
                    sleep(62)
            for row in reader:
                for i, k in enumerate(header[1:]):
                    v = row[(i + 1)]
                    if is_number(v):
                        print name + '.' + k, row[(i + 1)], row[0]

    sys.stderr.write('Done %d metrics processed' % wsp_files)


if __name__ == '__main__':
    main()
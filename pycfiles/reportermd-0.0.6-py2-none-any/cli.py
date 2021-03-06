# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sambev/projects/ardy/reportermd/cli.py
# Compiled at: 2015-12-06 20:01:06
__VERSION__ = '0.0.6'
import argparse, os, json, subprocess, sys, traceback, dateutil.parser
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('reportermd', 'templates'), trim_blocks=True, lstrip_blocks=True)
snapshotmd = env.get_template('snapshot.md')

def parse_reporter_date(value):
    """Parse the date from a reporterApp report.  It can be one of two formats
    1. Stupid Apple date that is seconds from 01.01.2001
    2. ISO date YYYY-MM-DDTHH:MM:SS
    @param {mixed} value - float (case 1), string (case 2)

    @returns datetime
    """
    iphone_date = 978307200
    if type(value) == type(0.0):
        return datetime.fromtimestamp(iphone_date + value).replace(tzinfo=None)
    else:
        return dateutil.parser.parse(value).replace(tzinfo=None)
        return


def find_by_date(snapshots, date_string):
    """
    Find all snapshots for the given date.
    @param {list} snapshots - dicts of snapshots
    @param {string} date_string - YYYY-MM-DD format string

    @returns {list}
    """
    user_date = parse_reporter_date(date_string)
    matching = []
    for snapshot in snapshots:
        snapshot_date = parse_reporter_date(snapshot['date'])
        if snapshot_date.date() == user_date.date():
            matching.append(snapshot)

    return matching


def main():
    """
    Do the actual work of reading in the reporter export, writing it as md and
    importing it into dayone.
    """
    if sys.argv[1] in ('-v', '--version'):
        print __VERSION__
        return 0
    else:
        parser = argparse.ArgumentParser(description='Import reporter app entries to dayone')
        parser.add_argument('date', type=str, help='Date to import reports from')
        parser.add_argument('--dayone', type=bool, help='Wether or not to import to dayone. (default: False)', default=False)
        args = parser.parse_args()
        if not os.path.isfile('reporter-export.json'):
            print '[ERROR] No reporter-export file found.'
            return 1
        print 'Reading reporter-export.json...'
        file_data = None
        with open('reporter-export.json') as (f):
            file_data = f.read()
        reporter_export = json.loads(file_data)
        snapshots = reporter_export['snapshots']
        date_string = args.date
        import_to_dayone = args.dayone
        dates = find_by_date(snapshots, date_string)
        if len(dates) == 0:
            print 'No entries for date provided'
            return 1
        markdown_file_name = ('entry-{0}.md').format(date_string)
        try:
            with open(markdown_file_name, 'a') as (f):
                print 'Writing markdown file...'
                for snapshot in dates:
                    location = snapshot.get('location', {}).get('placemark', {})
                    weather = snapshot.get('weather', {})
                    date = parse_reporter_date(snapshot['date'])
                    f.write(snapshotmd.render(**{'date': date.date(), 
                       'time': date.time(), 
                       'locality': location.get('locality'), 
                       'postal_code': location.get('postalCode'), 
                       'state': location.get('administrativeArea'), 
                       'lat_long': location.get('region'), 
                       'tempF': weather.get('tempF'), 
                       'humidity': weather.get('relativeHumidity'), 
                       'windMPH': weather.get('windMPH'), 
                       'wind_direction': weather.get('windDirection'), 
                       'responses': snapshot.get('responses')}))

                print ('Markdown file {0} written!').format(markdown_file_name)
        except Exception as e:
            print 'Error writing file. This is probably a bug.'
            print 'Please submit this traceback in your issue:\n'
            print '******* ERROR START ********'
            traceback.print_exc(file=sys.stdout)
            print '*******  ERROR END  ********\n'
            return 1

        if import_to_dayone:
            print 'Importing into DayOne...'
            with open(markdown_file_name, 'r') as (f):
                subprocess.call(['dayone',
                 '-d=%s' % date_string,
                 'new'], stdin=f)
        return


if __name__ == '__main__':
    main()
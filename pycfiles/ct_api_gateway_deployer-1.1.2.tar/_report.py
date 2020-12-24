# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/_report.py
# Compiled at: 2014-07-22 22:39:30
from os import listdir, walk, path, environ
from config import TiConfig as ctznConfig
from titantools.orm import TiORM as ctznORM
CTZNOSX_PATH = environ.get('CTZNOSX_PATH') or '/var/lib/ctznosx/'
CTZNOSX_CONFIG = path.join('/etc/', 'ctznosx.conf')
CONFIG = ctznConfig(CTZNOSX_CONFIG, CTZNOSX_PATH)
DATASTORE = CONFIG['main']['datastore']

def run():
    report = ''
    ORM = ctznORM(DATASTORE)
    all_monitors = ORM.select('sqlite_master', 'name', "type = 'table' and name != 'watcher'")
    for monitor in all_monitors:
        report += '<h2>%s</h2>' % monitor['name']
        module_data = ORM.select(monitor['name'], '*')
        report += '<table>'
        for row in module_data:
            report += '<tr>'
            for column in row:
                report += '<td>'
                report += column
                report += '</td>'
                report += '<td>'
                report += str(row[str(column)])
                report += '</td>'

            report += '</tr>'

        report += '</table>'

    report += helpers.footer()
    print report
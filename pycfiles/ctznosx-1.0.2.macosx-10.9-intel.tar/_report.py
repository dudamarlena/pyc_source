# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
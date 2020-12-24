# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/ejecutaScript.py
# Compiled at: 2020-05-12 23:10:07
# Size of source mod 2**32: 730 bytes
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from polical import SimpleIcsToCSV
from polical import TareasCSVToBD
from polical import SendTaskToTrello

def ejecutaScript():
    SimpleIcsToCSV.convertICStoCSV()
    TareasCSVToBD.LoadCSVTasktoDB()
    SendTaskToTrello.SendTaskToTrello()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(ejecutaScript, 'interval', seconds=3600)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
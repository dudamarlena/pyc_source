# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
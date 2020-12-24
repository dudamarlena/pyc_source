# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/TareasCSVToBD.py
# Compiled at: 2020-05-12 23:12:56
# Size of source mod 2**32: 1598 bytes
from polical import TareaClass
import csv
from polical import connectSQLite
from polical import create_subject
from polical import configuration
from datetime import datetime
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def LoadCSVTasktoDB(username, user_dict):
    with open(configuration.get_file_location('calendar.csv')) as (csv_file):
        logging.info('CSV abierto.')
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
        else:
            if len(row) > 9:
                line_count == 0 or create_subject.create(Get_Subject_Name_From_CSV(row[9]), row[2], user_dict)
                sbjID = connectSQLite.getSubjectID(Get_Subject_Name_From_CSV(row[9]))
                task = TareaClass.Tarea(row[1], row[2], row[3], datetime.strptime(row[7][0:8], '%Y%m%d'), sbjID)
                sql = connectSQLite.saveTask(task, username)
                logging.info('Las tareas nuevas se agregaron a la BD')
                sql.connection.close()


def Get_Subject_Name_From_CSV(full_subject_name):
    list = full_subject_name.split('_', 3)
    return list[1]
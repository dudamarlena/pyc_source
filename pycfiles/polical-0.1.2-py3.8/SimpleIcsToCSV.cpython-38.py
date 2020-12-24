# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/SimpleIcsToCSV.py
# Compiled at: 2020-05-12 23:12:11
# Size of source mod 2**32: 7331 bytes
import wget, os, csv, sys
from polical import configuration
import logging
logging.basicConfig(filename=(configuration.get_file_location('Running.log')), level=(logging.INFO), format='%(asctime)s:%(levelname)s:%(message)s')

def addEvent(header, filename):
    f = open((configuration.get_file_location(filename)), 'r', encoding='utf-8')
    f2 = open(configuration.get_file_location('calendar.csv'), 'w+')
    f1 = f.readlines()
    for x in header:
        f2.write(x)
        if x != 'END':
            f2.write(';')
    else:
        f2.write('\n')
        wrBegin = False
        wrNormal = False
        wrDescription = False
        for x in f1:
            list = x.split(':', 1)
            chars = [c for c in list[0]]
            if list[0] == 'BEGIN' and list[1] == 'VEVENT\n':
                wrNormal = True
                wrBegin = True
                list[1] = 'VEVENT'
            else:
                if list[0] == 'DESCRIPTION':
                    wrDescription = True
                    f2.write('"')
                else:
                    if chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n' and wrDescription:
                        wrDescription = False
                        f2.write('";')
                    else:
                        if list[0] == 'END' and list[1] == 'VEVENT\n':
                            wrNormal = False
                        else:
                            pass
            if wrNormal and wrDescription == False:
                try:
                    removebsn = list[1].split('\n', 1)
                    f2.write(removebsn[0] + ';')
                except Exception as e:
                    try:
                        print(e)
                    finally:
                        e = None
                        del e

            elif wrNormal and wrDescription:
                for y in list:
                    new_list = {x.replace('\n', '').replace('\t', '').replace('DESCRIPTION', '') for x in list}
                else:
                    for x in new_list:
                        f2.write(x)

            elif wrNormal == False and wrBegin:
                f2.write('\n')


def convertICStoCSV(url):
    print('Descargando calendario desde Aula Virtual...')
    logging.info('Descargando calendario desde Aula Virtual...')
    filename = configuration.get_file_location('mycalendar.ics')
    if os.path.exists(filename):
        os.remove(filename)
    wget.download(url, filename)
    addEvent(findHeader(filename), filename)
    print('\nEspere...')
    logging.info('Descarga de calendario finalizada.')


def findHeader(icsCal):
    f = open((configuration.get_file_location(icsCal)), 'r', encoding='utf-8')
    f2 = open(configuration.get_file_location('calendar.csv'), 'w+')
    f1 = f.readlines()
    wrBegin = False
    wrNormal = False
    wrDescription = False
    for x in f1:
        list = x.split(':', 1)
        chars = [c for c in list[0]]

    if list[0] == 'BEGIN' and list[1] == 'VEVENT\n':
        wrNormal = True
        wrBegin = True
    else:
        if list[0] == 'DESCRIPTION':
            wrDescription = True
        else:
            if chars[0] != ' ' and chars[0] != '\t' and chars[0] != '\n':
                if wrDescription:
                    wrDescription = False
                elif list[0] == 'END':
                    wrNormal = False
                else:
                    if wrNormal == False:
                        if wrBegin == True:
                            f2.write('END\n')
                if wrNormal:
                    if wrDescription == False:
                        f2.write(list[0].replace(';', '') + ';')
                if wrNormal:
                    if wrDescription and list[0] == 'DESCRIPTION':
                        f2.write(list[0].replace(';', '') + ';')
                    f2.close()
                    listHeaders = []
                    with open(configuration.get_file_location('calendar.csv')) as (csv_file):
                        csv_reader = csv.reader(csv_file, delimiter=';')
                        for row in csv_reader:
                            listHeaders.append(row)

                    filename = configuration.get_file_location('calendar.csv')
                    if os.path.exists(filename):
                        os.remove(filename)
            return max(listHeaders, key=len)


def main(argv):
    if len(argv) == 2:
        filename = argv[1]
    else:
        print('python icsReader.py file/location/file.ics')
        logging.info('python icsReader.py file/location/file.ics')
    addEvent(findHeader(filename), filename)


if __name__ == '__main__':
    main(sys.argv)
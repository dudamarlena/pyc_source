# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\reader\input_reader.py
# Compiled at: 2017-04-20 23:32:05
# Size of source mod 2**32: 4270 bytes
import os
from mapy.reader.cardtranslator import translator

def addfield(tempcard, field, value):
    field = float(field)
    field += 1
    for k in tempcard.keys():
        if k.find('___') > -1:
            entrynum = float(k.split('___')[2])
            step = float(k.split('___')[3])
            if (field - entrynum) / step == 0 or (field - entrynum) / step == 1:
                tempcard[k].append(value)
                break


def fieldsnum(line):
    print('DEBUG line', line)
    if line.find(',') == -1:
        line = line.split('\n')[0]
        num = len(line) / 8
        if len(line) % 8.0 > 0.0:
            num = num + 1
    else:
        num = len(line.split(','))
    print('DEBUG num', num)
    return num


class InputFile:
    __doc__ = '\n    Input file containing a FEM model bulk\n\n    '

    def __init__(self, abspath, solvername='nastran'):
        self.abspath = abspath
        self.solvername = solvername
        list_cards_translator = translator(self.solvername)
        self.cards = list_cards_translator[0]
        self.translator = list_cards_translator[1]
        self.readfile()
        self.createdata()
        self.memorycleanup()

    def readfile(self):
        if os.path.isfile(self.abspath):
            datfile = open(self.abspath, 'r')
        else:
            raise ValueError('Input file : %s was not found!' % self.abspath)
        self.lines = datfile.readlines()
        datfile.close()

    def memorycleanup(self):
        self.lines = None

    def createdata(self):
        self.data = []
        validentry = False
        countentry = 0
        bulk = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            if line.strip().startswith('$'):
                pass
            else:
                if not bulk:
                    pass
                else:
                    if 'BEGIN BULK' in line.upper():
                        bulk = True
                    if line.find(',') > -1:
                        numfields = fieldsnum(line)
                        fields = [i.strip() for i in line.split(',')]
                    else:
                        numfields = fieldsnum(line)
                        print('DEBUG numfields', numfields)
                        fields = [line[0 + i * 8:8 + i * 8].strip() for i in range(numfields)]
                    if (fields[0].find('+') > -1 or fields[0] == '' or fields[0] == '        ') and validentry == True:
                        countentry += 1
                    else:
                        if fields[0] in self.cards:
                            validentry = True
                            countentry = 0
                            currcard = fields[0]
                            cardfieldsnum = len(self.cards[currcard])
                            try:
                                if len(tempcard) > 0:
                                    self.data.append(tempcard)
                            except NameError:
                                pass

                            tempcard = {}
                        else:
                            validentry = False
                            countentry = 0
            if validentry == True or countentry > 0:
                for field_i in range(numfields):
                    field_j = field_i + 10 * countentry
                    fieldvalue = fields[field_i]
                    if field_j + 1 <= cardfieldsnum:
                        fieldname = self.cards[currcard][field_j]
                        if fieldname.find('___') > -1:
                            tempcard[fieldname] = [
                             fieldvalue]
                        else:
                            tempcard[fieldname] = fieldvalue
                    else:
                        addfield(tempcard, field_i, fieldvalue)

        try:
            if len(tempcard) > 0:
                self.data.append(tempcard)
        except NameError:
            pass
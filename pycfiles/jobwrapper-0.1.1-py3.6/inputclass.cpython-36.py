# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/inputclass.py
# Compiled at: 2018-09-07 05:59:02
# Size of source mod 2**32: 2575 bytes
import os, json

class inputparams:
    __doc__ = 'docstring for inputparams class'

    def __init__(self, path='./'):
        self._path = path
        self.parameters = {}
        self.read_inputfile()

    def getpath(self, path):
        """same function as in other classes, could be refactored"""
        import tkinter
        from tkinter.filedialog import askdirectory
        if path is '':
            root = tkinter.Tk()
            path = askdirectory(parent=root, title='Select the HDF5 path')
            path = path + '/'
            root.destroy()
        self._path = path

    def isdumped(self):
        """just return True or False is the file is already dumped"""
        return os.path.isfile(self._path + 'inputparams.txt')

    def read_inputfile(self):
        """Parser of the input file , creating attributes of the class"""
        reps = {'D':'e', 
         'd':'e', 
         '.TRUE.':'True', 
         '.FALSE.':'False', 
         '.False.':'False', 
         'Xe':'"Xe"', 
         'Ar':'"Ar"', 
         'FAr':'"FAr"', 
         'He':'"He"', 
         'Kr':'"Kr"', 
         '=':''}
        with open(self._path + '/inputs') as (inputfile):
            [self.readinputline(line, reps) for line in inputfile]

    def readinputline(self, line, reps):
        if line[0] is '!':
            pass
        else:
            try:
                key, val = line.split(maxsplit=1)
            except ValueError:
                print('Error : The line is Empty !!')
                exit()

            if len(val.split()) > 1:
                val, __ = val.split(maxsplit=1)
            for old, new in reps.items():
                val = val.replace(old, new)

        try:
            self.parameters[key] = eval(val)
        except SyntaxError:
            print(key, val, line)

    def __str__(self):
        strings = ''
        for key, val in self.parameters.items():
            strings = ''.join([strings, key, ' = ', val, '\n'])

        return strings
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Program Files (x86)\processing.py-3017-windows64\i3_python.py
# Compiled at: 2020-03-02 12:21:35
# Size of source mod 2**32: 2066 bytes
from java.util import Date
d = Date()
print(d)
from java.io import InputStreamReader, BufferedReader
from java.lang import Runtime
i3_file_location = 'C:\\\\Users\\\\Faruk\\\\Desktop\\\\code\\\\Python\\\\i3_python'
i3_python_file = 'i3_test'

def setup():
    size(800, 600)
    create_links(i3_file_location, i3_python_file)
    execute('i3_setup_link.py')


def draw():
    pass


def execute(link):
    try:
        print('a')
        rt = Runtime.getRuntime()
        print('b')
        commands = ['python3', link]
        proc = rt.exec(commands)
        print('c')
        stdInput = BufferedReader(InputStreamReader(proc.getInputStream()))
        stdError = BufferedReader(InputStreamReader(proc.getErrorStream()))
        while True:
            s = stdInput.readLine()
            if s is None:
                break
            println('[OUTPUT] ' + s)
            exec(s)

        while True:
            s = stdError.readLine()
            if s is None:
                break
            println('[Exception] ' + s)

    except BaseException as e:
        try:
            print(e)
            saveStrings('error.txt', [str(e)])
        finally:
            e = None
            del e


def create_links(i3_file_location, i3_python_file):
    words = 'import sys;sys.path.append("' + i3_file_location + '"' + ');from ' + i3_python_file + ' import setup;setup()'
    words_list = split(words, ';')
    saveStrings('i3_setup_link.py', words_list)
    words = 'import sys;sys.path.append("' + i3_file_location + '"' + ');from ' + i3_python_file + ' import draw;draw()'
    words_list = split(words, ';')
    saveStrings('i3_draw_link.py', words_list)
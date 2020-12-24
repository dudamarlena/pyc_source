# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\shared\tim_working\development\github\pylirious\pylirious\mm-api\python\mm\external.py
# Compiled at: 2016-07-24 13:10:59
import os, tempfile, platform

def locate_openscad():
    """local path to OpenSCAD binary on various platforms (currently hardcoded...)"""
    if platform.system() == 'Windows':
        return '"C:\\Program Files (x86)\\OpenSCAD\\openscad.exe"'
    else:
        if platform.system() == 'Darwin':
            return '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
        return 'openscad'


def run_openscad_script(scad_file, output_file):
    """execute an OpenSCAD script stored in scad_file and write the result to output_file"""
    command = locate_openscad() + ' -o ' + output_file + ' ' + scad_file
    status = os.system('"%s"' % command)
    return status == 0


def run_openscad_source(script_source, output_file):
    """execute OpenSCAD source code and write the result to output_file"""
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(script_source)
    f.close()
    command = locate_openscad() + ' -o ' + output_file + ' ' + f.name
    status = os.system('"%s"' % command)
    os.unlink(f.name)
    return status == 0
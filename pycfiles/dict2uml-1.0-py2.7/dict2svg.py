# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/dict2uml/dict2svg.py
# Compiled at: 2017-11-03 13:31:18
from IPython.display import SVG
import subprocess, uuid
from dict2uml import dict2plantuml
import os

def plantuml_exec(*file_names):
    """Run PlantUML"""
    cmd = [
     '/usr/local/bin/plantuml',
     '-tsvg'] + list(file_names)
    subprocess.check_call(cmd, shell=False, stderr=subprocess.STDOUT)
    return [ os.path.splitext(f)[0] + '.svg' for f in file_names ]


def dict2svg(d):
    base_name = str(uuid.uuid4())
    uml_path = base_name + '.uml'
    with open(uml_path, 'w') as (fp):
        fp.write(dict2plantuml(d))
    try:
        output = plantuml_exec(uml_path)
        svg_name = output[0]
        return SVG(filename=svg_name)
    finally:
        if os.path.exists(uml_path):
            os.unlink(uml_path)
        svg_path = base_name + '.svg'
        if os.path.exists(svg_path):
            os.unlink(svg_path)
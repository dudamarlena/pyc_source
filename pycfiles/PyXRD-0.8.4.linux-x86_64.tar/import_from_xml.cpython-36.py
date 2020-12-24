# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/scripts/import_from_xml.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1011 bytes
import os, sys
from pyxrd.project.models import Project

def run(args):
    if args:
        if args.filename != '':
            project = Project.create_from_sybilla_xml(args.filename)
            project_filename = '%s/%s' % (os.path.dirname(args.filename), os.path.basename(args.filename).replace('.xml', '.pyxrd', 1))
            from pyxrd.file_parsers.json_parser import JSONParser
            JSONParser.write(project, project_filename, zipped=True)
            args = [
             sys.argv[0], project_filename]
            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]
            os.execv(sys.executable, args)
            sys.exit(0)
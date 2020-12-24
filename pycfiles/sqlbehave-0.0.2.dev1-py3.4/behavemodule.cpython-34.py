# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-x86_64/egg/sqlbehave/behavemodule.py
# Compiled at: 2016-11-02 09:43:05
# Size of source mod 2**32: 1740 bytes
import os, glob, parse
from lxml import etree
from datetime import datetime, date, time
from sqlbehave.testmodule import connect_config, step_types, link_config

class ModuleStep:
    pass


class FileSqlBehaveModule:

    def __init__(self, module_name, revision=None):
        self.module_name = module_name
        self.features = dict()
        self.steps = dict()

    def get_steps(self):
        predicate_format = '{step_type} {predicate}'
        connect_value_tmpl = '--!connect={value}'
        for st in step_types:
            filetemplate = './features/steps/' + predicate_format + '.sql'
            for g in glob.iglob(filetemplate.format(step_type=st, predicate='*')):
                filename = os.path.basename(os.path.splitext(g)[0])
                ms = ModuleStep()
                ms.id_predicate_type = step_types[st]
                p = parse.parse(predicate_format, filename)
                try:
                    ms.predicate = p.named['predicate']
                except:
                    continue

                with open(g, 'r') as (f):
                    ms.sql_test_command = ''
                    for line in f:
                        if not hasattr(ms, 'id_server'):
                            p = parse.parse(connect_value_tmpl, line)
                            if p != None:
                                if len(p.named) > 0:
                                    vl = p.named['value']
                                    for id_server, connect in connect_config.items():
                                        if connect == vl:
                                            ms.id_server = id_server
                                            continue

                        else:
                            ms.sql_test_command += line

                yield ms
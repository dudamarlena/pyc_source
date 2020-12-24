# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/schemadisplay_sphinx/__init__.py
# Compiled at: 2016-02-21 20:44:13
import os
from sets import Set
import sys
from sqlalchemy.orm import class_mapper
from sqlalchemy_schemadisplay import create_uml_graph

def builder_inited_handler(app):

    def is_valid_folder(folder, skip_folders):
        if len(folder) == 0:
            return False
        for skip_folder in skip_folders:
            if skip_folder in folder:
                return False

        return True

    skip_folders = ''
    if app.config.model_skip_folders:
        skip_folders = app.config.model_skip_folders.split(',')
    str_model_cls = app.config.model_class_name
    if not str_model_cls:
        return
    __import__(str_model_cls[:str_model_cls.rfind('.')])
    obj = sys.modules[str_model_cls[:str_model_cls.rfind('.')]]
    name = str_model_cls[str_model_cls.rfind('.') + 1:]
    model_class = getattr(obj, name)
    app.info('Importing modules')
    cwd = os.getcwd()
    modules = Set()
    for root, directories, filenames in os.walk(cwd):
        for filename in filenames:
            folder = str(root)
            relative_folder = folder.replace(cwd, '')
            if not is_valid_folder(relative_folder, skip_folders):
                continue
            if filename.endswith('.py') and not filename.startswith('__'):
                name = filename[:-3]
                module = '%s.%s' % (relative_folder.replace('/', '.'), name)
                modules.add(module[1:])

    for module in modules:
        try:
            __import__(module)
        except Exception:
            pass

    app.info('Getting mappers')
    mappers = []
    for cls in model_class.__subclasses__():
        for attr in cls.__dict__.keys():
            try:
                mappers.append(class_mapper(cls))
            except Exception:
                pass

    app.info('Creating the db schema')
    graph = create_uml_graph(mappers, show_operations=False, show_multiplicity_one=False)
    graph.write_png(app.config.model_schema_filename)


def setup(app):
    app.add_config_value('model_class_name', '', 'html')
    app.add_config_value('model_schema_filename', 'db-schema.png', 'html')
    app.add_config_value('model_skip_folders', '', 'html')
    app.connect('builder-inited', builder_inited_handler)
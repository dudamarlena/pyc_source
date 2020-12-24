# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ddp\inc.py
# Compiled at: 2015-04-09 20:53:13
import os

def get_project_path():
    """
    get the project path of ddscat
    :return: path
    """
    return os.path.abspath('.')


def get_config_path():
    """
    get the config file path
    :return: path
    """
    project_path = get_project_path()
    config_path = os.path.join(project_path, 'config.ini')
    return config_path


def get_efield_path():
    """
    get the electric file vtr file path
    :return: path
    """
    project_path = get_project_path()
    efield_path = os.path.join(project_path, 'VTRoutput_1.vtr')
    return efield_path


def get_shape_path():
    """
    get the path of shape vtr file path
    :return: path
    """
    project_path = get_project_path()
    shape_path = os.path.join(project_path, 'output_1.vtr')
    return shape_path


def get_ddpostprocess_path():
    """
    get the path of ddpostprocess.par
    :return: path
    """
    project_path = get_project_path()
    ddpostprocess_path = os.path.join(project_path, 'ddpostprocess.par')
    return ddpostprocess_path


def get_tpl_path(tpl_name):
    """
    get the object template path according name
    :param tpl_name:
    :return: path
    """
    real_path = os.path.dirname(os.path.realpath(__file__))
    tpl_path = os.path.join(real_path, 'Template')
    tpl_full_path = ''
    if tpl_name == 'ddpostprocess':
        tpl_full_path = os.path.join(tpl_path, 'ddpostprocess.tpl')
    if tpl_name == 'ddscat_fromfile':
        tpl_full_path = os.path.join(tpl_path, 'ddscat.tpl')
    if tpl_name == 'ddscat_builtin':
        tpl_full_path = os.path.join(tpl_path, 'ddscat_builtin.tpl')
    return tpl_full_path


def get_qtable_path():
    """
    get the path of qtable in project
    :return: path
    """
    project_path = get_project_path()
    qtable_path = os.path.join(project_path, 'qtable')
    return qtable_path
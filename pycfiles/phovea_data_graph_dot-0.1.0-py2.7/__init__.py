# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/phovea_data_graph_dot/__init__.py
# Compiled at: 2017-04-05 09:25:13


def phovea(registry):
    """
  register extension points
  :param registry:
  """
    registry.append('graph-parser', 'parser-dot', 'phovea_data_graph_dot.dot', {'format': 'dot', 
       'factory': 'parse_dot'})


def phovea_config():
    """
  :return: file pointer to config file
  """
    from os import path
    here = path.abspath(path.dirname(__file__))
    config_file = path.join(here, 'config.json')
    if path.exists(config_file):
        return config_file
    else:
        return
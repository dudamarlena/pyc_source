# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/cli/helpers.py
# Compiled at: 2016-02-06 13:50:19
from openaps.config import Config
import json

def install_show_arguments(parser):
    parser.add_argument('--ini', dest='format', action='store_const', const=format_ini, default=format_url)
    parser.add_argument('--json', dest='format', action='store_const', const=format_json)


def format_json(report):
    info = {'name': report.name, report.name: report.fields, 'type': report.prefix}
    if hasattr(report, 'extra'):
        info['extra'] = report.extra.fields
    return json.dumps(info)


def format_ini(report):
    config = Config()
    config.add_device(report)
    if hasattr(report, 'extra'):
        for k, v in report.extra.fields.items():
            config.set(report.section_name(), k, v)

    return config.fmt()


def format_url(report):
    return report.format_url()
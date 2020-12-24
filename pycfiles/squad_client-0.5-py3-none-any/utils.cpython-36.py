# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/utils.py
# Compiled at: 2020-04-08 08:25:25
# Size of source mod 2**32: 667 bytes
import json

def first(_dict):
    if _dict is None or len(_dict) == 0:
        return
    else:
        return next(iter(_dict.values()))


def parse_test_name(name):
    suite_name, test_name = name.split('/', 1)
    return (suite_name, test_name)


def parse_metric_name(name):
    return parse_test_name(name)


def split_group_project_slug(group_project_slug):
    group_slug, project_slug = group_project_slug.split('/')
    return (group_slug, project_slug)


def split_build_url(build_slug):
    group_slug, project_slug, _, build_version = build_slug.split('/')
    return (group_slug, project_slug, build_version)


def to_json(thing):
    return json.dumps(thing)
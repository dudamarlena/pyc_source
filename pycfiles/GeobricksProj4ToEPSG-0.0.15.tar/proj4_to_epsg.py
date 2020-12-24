# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_proj4_to_epsg/geobricks_proj4_to_epsg/core/proj4_to_epsg.py
# Compiled at: 2015-03-16 04:20:24
import json, os
projection_list = None

def get_projection_list():
    global projection_list
    if projection_list is None:
        data_path = os.path.join(os.path.dirname(__file__), os.path.pardir, 'data', 'epsg.json')
        with open(data_path, 'r') as (f):
            projection_list = json.load(f)
    return projection_list


def get_epsg_code_from_proj4(proj4):
    prj = proj4
    if isinstance(proj4, basestring):
        prj = get_proj4_json_from_string(proj4)
    return get_epsg_code_from_proj4_json(prj)


def get_proj4_json_from_epsg_code(epsg_code):
    for proj in get_projection_list():
        if proj['epsg'] == str(epsg_code):
            return proj['proj4']

    return


def get_epsg_code_from_proj4_json(proj_json):
    for proj in get_projection_list():
        if proj['proj4']['proj'] == proj_json['proj']:
            if check_projection_options(proj['proj4'], proj_json):
                return proj['epsg']

    return


def check_projection_options(projection_list_json, proj_json):
    if len(projection_list_json) is not len(proj_json):
        return False
    for v in projection_list_json:
        try:
            if v not in proj_json or proj_json[v] != projection_list_json[v]:
                return False
        except:
            return False

    return True


def get_proj4_json_from_string(proj4):
    proj4 = proj4.strip()
    proj_json = {}
    values = proj4.split(' ')
    for value in values:
        s = value.split('=')
        c = s[0].replace('+', '')
        v = True
        if len(s) > 1:
            v = s[1]
        proj_json[c] = v

    return proj_json
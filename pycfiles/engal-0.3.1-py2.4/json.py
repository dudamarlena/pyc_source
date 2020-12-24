# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/json.py
# Compiled at: 2006-06-27 14:36:06
from turbojson.jsonify import jsonify
from turbojson.jsonify import jsonify_sqlobject
from engal.model import User, Group, Permission

@jsonify.when('isinstance(obj, Group)')
def jsonify_group(obj):
    result = jsonify_sqlobject(obj)
    result['users'] = [ u.user_name for u in obj.users ]
    result['permissions'] = [ p.permission_name for p in obj.permissions ]
    return result


@jsonify.when('isinstance(obj, User)')
def jsonify_user(obj):
    result = jsonify_sqlobject(obj)
    del result['password']
    result['groups'] = [ g.group_name for g in obj.groups ]
    result['permissions'] = [ p.permission_name for p in obj.permissions ]
    return result


@jsonify.when('isinstance(obj, Permission)')
def jsonify_permission(obj):
    result = jsonify_sqlobject(obj)
    result['groups'] = [ g.group_name for g in obj.groups ]
    return result
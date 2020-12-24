# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevogears/jsonify.py
# Compiled at: 2008-01-19 12:10:14
"""Schevo+TurboGears jsonify support.

For copyright, license, and warranty, see bottom of file.
"""
from turbojson import jsonify as tj
from schevo.base import Entity, Extent
jsonify = tj.jsonify

@jsonify.when('isinstance(obj, Entity)')
def jsonify_schevo(obj):
    result = {}
    result['_oid'] = obj.sys.oid
    result['_rev'] = obj.sys.rev
    for (name, value) in obj.sys.fields().value_map().iteritems():
        result[name] = jsonify(value)

    return result
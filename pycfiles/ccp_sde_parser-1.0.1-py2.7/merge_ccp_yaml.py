# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ccp_sde_parser/merge_ccp_yaml.py
# Compiled at: 2012-11-04 23:11:37
"""Merge the CCP-provided YAML files with the JSON produced via the dump extractor."""
import os
from progressbar import ProgressBar, Bar, Percentage, ETA
import sys, yaml, json

def main():
    if len(sys.argv) != 4 or not os.path.isdir(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print "Must specify a directory of JSON files, a JSON schema file, and a directory with CCP's YAML files."
        print 'Usage: %s JSON_DIR SCHEMA_FILE CCP_DIR\n' % sys.argv[0]
        sys.exit(1)
    json_dir = sys.argv[1]
    schema_file = sys.argv[2]
    ccp_dir = sys.argv[3]
    print 'creating graphics table'
    with open(os.path.join(ccp_dir, 'graphicIDs.yaml')) as (f):
        gids = yaml.safe_load(f)
        new_table = dict(table_name='eveGraphics', columns=[
         'graphicID', 'graphicFile', 'description', 'obsolete', 'graphicType', 'collidable', 'explosionID', 'directoryID', 'graphicName'], data=[])
        pbar = ProgressBar(widgets=[Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(gids.keys())).start()
        idx = -1
        for gid in gids.keys():
            idx += 1
            new_table['data'].append(dict(graphicID=int(gid), **gids[gid]))
            pbar.update(idx)

        with open(os.path.join(json_dir, 'eveGraphics.json'), 'w') as (of):
            json.dump(new_table, of)
        del gids
        pbar.finish()
    print 'merging icons'
    origIcons = None
    with open(os.path.join(json_dir, 'eveIcons.json')) as (f):
        origIcons = json.load(f)
    with open(os.path.join(ccp_dir, 'iconIDs.yaml')) as (f):
        iids = yaml.safe_load(f)
        new_ids = set(int(i) for i in iids.keys())
        old_ids = set(int(i['iconID']) for i in origIcons['data'])
        ids_to_add = new_ids - old_ids
        pbar = ProgressBar(widgets=[Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(ids_to_add)).start()
        idx = -1
        for iid in ids_to_add:
            idx += 1
            origIcons['data'].append(dict(iconID=int(iid), **iids[iid]))
            pbar.update(idx)

        with open(os.path.join(json_dir, 'eveIcons.json'), 'w') as (of):
            json.dump(origIcons, of)
        pbar.finish()
    del origIcons
    print 'merging types'
    origTypes = None
    _type_cache = dict()

    def getType(tid):
        if tid not in _type_cache:
            for row in origTypes['data']:
                if row['typeID'] == tid:
                    _type_cache[tid] = row
                    break
            else:
                _type_cache[tid] = dict(typeID=tid)
                origTypes['data'].append(_type_cache[tid])

        return _type_cache[tid]

    with open(os.path.join(json_dir, 'invTypes.json')) as (f):
        origTypes = json.load(f)
    origTypes['columns'].extend(['graphicID', 'radius', 'soundID'])
    with open(os.path.join(ccp_dir, 'typeIDs.yaml')) as (f):
        tids = yaml.safe_load(f)
        pbar = ProgressBar(widgets=[Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(tids.keys())).start()
        idx = -1
        for tid in tids.keys():
            idx += 1
            row = getType(tid)
            trow = tids[tid]
            row.update(trow)
            pbar.update(idx)

        with open(os.path.join(json_dir, 'invTypes.json'), 'w') as (of):
            json.dump(origTypes, of)
        pbar.finish()
    print 'modifying schema'
    schema = None
    with open(schema_file) as (f):
        schema = json.load(f)
    if not schema:
        print 'ERROR: Unable to update schema file!'
        sys.exit(1)
    schema['eveGraphics'] = {'graphicID': ('integer', True), 'graphicFile': ('string', False), 'description': ('string', False), 'obsolete': ('boolean', False), 'graphicType': (
                     'string', False), 
       'collidable': ('boolean', False), 'explosionID': (
                     'integer', False), 
       'directoryID': ('integer', False), 'graphicName': (
                     'string', False)}
    schema['invTypes'].update({'graphicID': ('integer', False), 'radius': ('float', False), 'soundID': (
                 'integer', False)})
    with open(schema_file, 'w') as (f):
        json.dump(schema, f, sort_keys=True, indent=2)
    return


if __name__ == '__main__':
    main()
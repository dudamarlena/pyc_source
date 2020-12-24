# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve240.py
# Compiled at: 2020-04-10 03:06:36
from itertools import chain
import logging
from collections import defaultdict
import simplejson as json, plone.api as api
from emrt.necd.content.browser.tableau import get_historical_data
from emrt.necd.content.browser.tableau import write_historical_data
from emrt.necd.content.browser.tableau import entry_for_cmp
from emrt.necd.content.browser.tableau import GET_TIMESTAMP
logger = logging.getLogger(__name__)

def do_flatten(json_str):
    """ This used to be implemented as a C extension, which is no longer
        required with the current implementation, and was removed.
        This function exists for historical purposes, as there is nothing
        else to migrate.
        Last version released with the C extension is 2.5.2.
    """
    return json.dumps(list(chain(*json.loads(json_str))))


def migrate_historical_data(ctx):
    migrated = defaultdict(list)
    data = sorted(json.loads(do_flatten(get_historical_data(ctx))), key=GET_TIMESTAMP)
    for entry in data:
        entry_key = entry['ID']
        found = migrated[entry_key]
        latest = found and found[(-1)]
        should_append = True
        if latest:
            cmp_latest = entry_for_cmp(latest)
            cmp_entry = entry_for_cmp(entry)
            if cmp_entry == cmp_latest:
                should_append = False
        if should_append:
            found.append(entry)

    return json.dumps(migrated)


def clean_historical_data(ctx):
    data = get_historical_data(ctx)
    cleaned = [ x for x in json.loads(data) if x ]
    write_historical_data(ctx, json.dumps(cleaned))


def run(_):
    catalog = api.portal.get_tool('portal_catalog')
    objs = [ b.getObject() for b in catalog(portal_type='ReviewFolder') ]
    len_objs = len(objs)
    for idx, obj in enumerate(objs, start=1):
        logger.info('[%s/%s] Migrating %s', idx, len_objs, obj.absolute_url(1))
        logger.info('Cleaning before migration...')
        clean_historical_data(obj)
        logger.info('Migrating...')
        migrated = migrate_historical_data(obj)
        write_historical_data(obj, migrated)
        logger.info('Done!')
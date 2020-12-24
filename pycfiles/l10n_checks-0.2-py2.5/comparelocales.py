# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/core/comparelocales.py
# Compiled at: 2009-10-10 22:23:03
import unicodedata, silme.format
from mozilla.core.statistics import Statistics
from mozilla.core.main import *
import copy
from mozilla.playground.hacks import *
import mozilla.fp.diff, mozilla.core.compatibilityPack
try:
    import json
except ImportError:
    import simplejson as json

mozilla.fp.diff.register(silme.format.Manager)

def compareLocales(optionpack):
    """
  Method for accessing the compare-locales library 
  and dumping or returning the result.
  """
    optionpack.fp = silme.format.Manager.get('mozdiff')
    results = []
    stats = []
    optionhelper(optionpack)
    if optionpack.compatibility:
        result = mozilla.core.main.compareApp(optionpack, optionpack.merge)
    else:
        result = doCompare(optionpack)
    for locale in optionpack.locales:
        if result.details[locale] is not None:
            if len(result.details[locale]) > 0:
                if optionpack.verbose > 0 and (optionpack.returnvalue == 'full' or optionpack.returnvalue == 'results'):
                    results.append(('').join(optionpack.fp.serialize(copy.deepcopy(result.details[locale]), output=optionpack.output, space='', indent=0)))
                if optionpack.returnvalue == 'full_json' or optionpack.returnvalue == 'results_json':
                    results.append(mozilla.core.main.toJSON(result.details[locale]))

    for locale in optionpack.locales:
        if optionpack.returnvalue == 'full' or optionpack.returnvalue == 'statistics':
            stats.append(result.statistics[locale].dump_statistics())
            if not optionpack.turbo:
                stats.append(result.statistics[locale].dump_percentage([
                 'unmodifiedEntities',
                 'missingEntities',
                 'missingEntitiesInMissingFiles'], 'changedEntities'))
        if optionpack.returnvalue == 'full_json' or optionpack.returnvalue == 'statistics_json':
            stats.append(result.statistics[locale].to_json())

    if optionpack.returnmode == 'array':
        return [('').join(results).encode('utf_8'), ('').join(stats).encode('utf_8')]
    elif optionpack.returnvalue == 'full_json' or optionpack.returnvalue == 'results_json' or optionpack.returnvalue == 'statistics_json':
        if optionpack.returnvalue != 'statistics_json':
            print json.dumps(results, indent=2)
        if optionpack.returnvalue != 'results_json':
            print json.dumps(stats, indent=2)
    else:
        print ('').join(results).encode('utf_8')
        print ('').join(stats).encode('utf_8')
    return
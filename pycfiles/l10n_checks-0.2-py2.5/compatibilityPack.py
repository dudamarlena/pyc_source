# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/core/compatibilityPack.py
# Compiled at: 2008-12-22 22:40:55
import mozilla.core.main
from collections import defaultdict
mozilla.core.main.EnumerateApp = mozilla.core.main.CompareInit

def compareApp(app, merge_stage=None):
    """
  Wrapper around mozilla.core.main.doCompare to make the results look more 
  like in compare-locales 0.5/0.6
  @param app: instance of mozilla.core.main.CompareInit
  @param merge_stage: (optional) path where the merge files should be stored.
  If None, merge will be disabled (default) 
  """
    app.merge = merge_stage
    mozilla.core.main.optionhelper(app)
    resultset = mozilla.core.main.doCompare(app)
    transitiontable = {'missingEntities': 'missing', 'obsoleteEntities': 'obsolete', 
       'missingEntitiesInMissingFiles': 'missingInFiles', 
       'changedEntities': 'changed', 
       'unmodifiedEntities': 'unchanged', 
       'WARNING': 'warnings', 
       'ERROR': 'errors'}
    for locale in resultset.summary.keys():
        resultset.summary[locale]['completion'] = int(resultset.statistics[locale].get_percentage([
         'unmodifiedEntities', 'missingEntities',
         'missingEntitiesInMissingFiles'], 'changedEntities'))
        for pos in resultset.summary[locale].keys():
            if pos in transitiontable:
                resultset.summary[locale][transitiontable[pos]] = resultset.summary[locale][pos]
                resultset.summary[locale].pop(pos)

    resultset.stat_cats['all'] = []
    for locale in resultset.stat_cats.keys():
        for pos in resultset.stat_cats[locale]:
            if pos not in resultset.stat_cats['all']:
                resultset.stat_cats['all'].append(pos)

    for pos in resultset.stat_cats['all']:
        if pos in transitiontable:
            resultset.stat_cats['all'].append(transitiontable[pos])
            resultset.stat_cats['all'].pop(resultset.stat_cats['all'].index(pos))

    resultset.stat_cats = resultset.stat_cats['all']
    return resultset


mozilla.core.main.compareApp = compareApp

class Observer(object):
    """
  Replaces the Resultset class.
  The only difference is the name
  """

    def __init__(self):
        self.details = {}
        self.summary = defaultdict()
        self.stat_cats = {}
        self.statistics = {}


mozilla.core.main.Resultset = Observer

def toJSON(difflist, previouspath=None):
    """
  Method that converts the diff-like output to a JSON object
  @param difflist:
  @param previouspath: (optional) parameter used only internally through 
  the method! 
  """
    output = {}
    while len(difflist) > 0:
        output['children'] = []
        if isinstance(difflist, list):
            folder = ''
            for i in difflist:
                if isinstance(i, str) or isinstance(i, unicode):
                    if previouspath:
                        folder = previouspath + difflist.pop(difflist.index(i))
                        previouspath = None
                    else:
                        folder = difflist.pop(difflist.index(i))
                    break

            if len(difflist) == 1:
                output['children'].extend(toJSON(difflist=difflist.pop(0), previouspath=folder + '/')['children'])
            else:
                slist = {'children': []}
                while len(difflist) >= 1:
                    slist['children'].extend(toJSON(difflist=difflist.pop(0), previouspath=previouspath)['children'])

                output['children'].append((folder, slist))
        elif isinstance(difflist, tuple):
            if isinstance(difflist[1], unicode):
                if difflist[1] == '// add and localize this file':
                    type = 'missingFile'
                elif difflist[1] == '// remove this file':
                    type = 'obsoleteFile'
                elif difflist[1] == '// remove this folder':
                    type = 'obsoleteFolder'
                else:
                    type = difflist[1]
                if previouspath:
                    output['children'].append((previouspath + difflist[0], {'value': {type: True}}))
                else:
                    output['children'].append((difflist[0], {'value': {type: True}}))
                difflist = ''
            elif isinstance(difflist[1], list):
                entities = {}
                while len(difflist[1]) > 0:
                    entity = difflist[1].pop(0)
                    if entity[1] == '+':
                        type = 'missingEntity'
                    elif entity[1] == '-':
                        type = 'obsoleteEntity'
                    elif entity[1] == 'WARNING: ':
                        type = 'warning'
                    elif entity[1] == 'ERROR: ':
                        type = 'error'
                    else:
                        type = entity[1]
                    try:
                        entities[type].append(entity[0])
                    except KeyError:
                        entities[type] = []
                        entities[type].append(entity[0])

                if previouspath:
                    output['children'].append((previouspath + difflist[0], {'value': entities}))
                else:
                    output['children'].append((difflist[0], {'value': entities}))
                difflist = ''
            else:
                difflist = ''
        else:
            difflist = ''

    return output


mozilla.core.main.toJSON = toJSON
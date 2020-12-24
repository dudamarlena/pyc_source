# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/glatard/code/boutiques/tools/python/boutiques/util/utils.py
# Compiled at: 2020-03-16 20:44:37
# Size of source mod 2**32: 4415 bytes
import os, simplejson as json
from boutiques.logger import raise_error, print_warning
from boutiques import __file__ as bfile

def extractFileName(path):
    if path is None:
        return
    if path[:-1] == '/':
        return os.path.basename(path[:-1]) + '/'
    return os.path.basename(path)


class LoadError(Exception):
    pass


def loadJson(userInput, verbose=False, sandbox=False):
    json_file = None
    if os.path.isfile(userInput):
        json_file = userInput
    elif 'zenodo' in '.'.join(userInput.split('.')[:-1]).lower():
        from boutiques.puller import Puller
        puller = Puller([userInput], verbose, sandbox)
        json_file = puller.pull()[0]
    if json_file is not None:
        with open(json_file, 'r') as (f):
            return json.loads(f.read())
    e = 'Cannot parse input {}: file not found, invalid Zenodo ID, or invalid JSON object'.format(userInput)
    if userInput.isdigit():
        raise_error(LoadError, e)
    try:
        return json.loads(userInput)
    except ValueError:
        raise_error(LoadError, e)


def conditionalExpFormat(s):
    cleanedExpression = ''
    idx = 0
    while idx < len(s):
        c = s[idx]
        if c in ('=', '!', '<', '>'):
            cleanedExpression += ' {0}{1}'.format(c, '=' if s[(idx + 1)] == '=' else ' ')
            idx += 1
        elif c in ('(', ')'):
            cleanedExpression += ' {0} '.format(c)
        else:
            cleanedExpression += c
        idx += 1

    return cleanedExpression


def customSortDescriptorByKey(descriptor, template=os.path.join(os.path.dirname(bfile), 'templates', 'ordered_keys_desc.json')):

    def sortListedObjects(objList, template):
        sortedObjList = []
        for obj in objList:
            sortedObj = {key:obj[key] for key in template if key in obj}
            sortedObj.update(obj)
            sortedObjList.append(sortedObj)

        if len(objList) != len(sortedObjList):
            return objList
        for obj, sobj in zip(objList, sortedObjList):
            if obj != sobj:
                print_warning('Sorted list does not represent original list.')
                return objList

        return sortedObjList

    template = loadJson(template)
    sortedDesc = {}
    for key in [k for k in template if k in descriptor]:
        if type(descriptor[key]) is list:
            sortedDesc[key] = sortListedObjects(descriptor[key], template[key][0])
        else:
            sortedDesc[key] = descriptor[key]

    sortedDesc.update(descriptor)
    if sortedDesc != descriptor:
        print_warning('Sorted descriptor does not represent original descriptor.')
        return descriptor
    return sortedDesc


def customSortInvocationByInput(invocation, descriptor):
    descriptor = loadJson(descriptor)
    sortedInvoc = {key:invocation[key] for key in [inp['id'] for inp in descriptor['inputs'] if descriptor['inputs'] is not None] if key in invocation}
    if sortedInvoc != invocation:
        print_warning('Sorted invocation does not represent original invocation.')
        return invocation
    return sortedInvoc
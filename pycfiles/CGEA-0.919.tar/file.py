# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Desktop/workspace/CGEA-Packages/CGEA/CGEA/lib/file.py
# Compiled at: 2016-04-13 16:44:06
import csv, shutil, os, glob, cPickle, jsonpickle, json
from log import slogger
log = slogger('CGEA')

def read_obj(filename):
    try:
        data = cPickle.load(open(filename, 'rb'))
        return data
    except Exception as e:
        log.error(e)
        return

    return


def write_obj(filename, data):
    try:
        cPickle.dump(data, open(filename, 'wb'))
        return True
    except Exception as e:
        log.error(e)
        return False


def read_file(filename):
    fid = open(filename, 'r')
    data = []
    for line in fid:
        if len(line) > 0:
            line
            data.append(line.strip())

    fid.close()
    return data


def read_JSON(filename, encoding='utf-8'):
    try:
        return json.load(open(filename, 'r'), encoding=encoding)
    except Exception as e:
        log.error(e)
        return

    return


def write_JSON(filename, data, encoding='utf-8'):
    try:
        json.dump(data, open(filename, 'w'), sort_keys=True, indent=4, encoding=encoding)
        return True
    except Exception as e:
        log.error(e)
        return False


def read_csv(filename):
    try:
        reader = csv.reader(open(filename, 'r'), escapechar='\\')
        data = []
        for r in reader:
            data.append(r)

        return data
    except Exception as e:
        log.error(e)
        return False


def read_csv_universal_newline(filename, delimiter=','):
    try:
        reader = csv.reader(open(filename, 'rU'), escapechar='\\', delimiter=delimiter)
        data = []
        for r in reader:
            data.append(r)

        return data
    except Exception as e:
        log.error(e)
        return False


def read_file(filename):
    try:
        fid = open(filename, 'r')
        data = []
        for line in fid:
            if len(line) > 0:
                data.append(line.strip())

        fid.close()
        return data
    except Exception as e:
        log.error(e)
        return False


def write_csv(filename, data, quotechar='"', append=False, delimiter=',', pivot=False):
    if quotechar is None:
        quoting = csv.QUOTE_NONE
    else:
        quoting = csv.QUOTE_ALL
    if append:
        writetype = 'a'
    else:
        writetype = 'wb'
    if pivot:
        data = zip(*data)
    try:
        doc = csv.writer(open(filename, writetype), delimiter=delimiter, quotechar=quotechar, quoting=quoting, escapechar='\\')
        for d in data:
            doc.writerow(d)

        return True
    except Exception as e:
        log.error(e)
        return False

    return


def csvToDictionaryList(filename, delimiter=','):
    try:
        reader = csv.DictReader(open(filename, 'r'), delimiter=delimiter, escapechar='\\')
        data = []
        for r in reader:
            data.append(r)

        return data
    except Exception as e:
        log.error(e)
        return False


def csvToDictionary(filename, key):
    try:
        reader = csv.DictReader(open(filename, 'r'))
        data = {}
        for r in reader:
            keyvalue = r[key]
            if keyvalue in data:
                del r[key]
                data[keyvalue].append(r)
            else:
                del r[key]
                data[keyvalue] = [r]

        return data
    except Exception as e:
        log.error(e)
        return False


def dictionaryListToCSV(filename, data, fieldnames=None, encode=None, delimiter=','):
    if not fieldnames:
        fieldnames = sorted(data[0].keys())
    doc = csv.DictWriter(open(filename, 'wb'), fieldnames=fieldnames, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_ALL, extrasaction='ignore')
    doc.writeheader()
    for d in data:
        if encode:
            for key, value in d.items():
                try:
                    d[key] = value.encode(encode)
                except AttributeError:
                    try:
                        d[key] = (';').join(value).encode(encode)
                    except Exception:
                        d[key] = ''

        doc.writerow(d)

    return True


def prettyPrint(localobject, prefix=''):
    if len(prefix) > 40:
        print prefix + json.dumps(localobject, sort_keys=True, indent=4, separators=(',',
                                                                                     ': '))
    else:
        print prefix
        print json.dumps(localobject, sort_keys=True, indent=4, separators=(',', ': '))
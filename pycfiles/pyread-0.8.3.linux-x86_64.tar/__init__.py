# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pyread/__init__.py
# Compiled at: 2014-03-11 19:27:13
from pandas.io.parsers import read_csv
import numpy, re

def determineSeparatorAndColumnCount(s, newlines):
    num_newlines = min(10, int(len(newlines) / 2) - 1)
    start = int(len(newlines) / 2)
    end = int(len(newlines) / 2) + num_newlines
    if num_newlines > 1:
        s = s[newlines[start]:newlines[end]]
    characters = [
     '","', '"\t"', '" "', ',', '\t', ' ']
    counts = [ s.count(char) for char in characters ]
    candidates = [ (c % num_newlines == 0) & (c != 0) for c in counts ]
    candidate = candidates.index(True)
    return {'sep': characters[candidate], 'num_col': int(counts[candidate] / num_newlines) + 1}


def read_auto(fileName, inferOnly=False, verbose=True):
    with open(fileName) as (f):
        s = f.read(10000)
    newlines = [ m.start() for m in re.finditer('\n', s) ]
    info = determineSeparatorAndColumnCount(s, newlines)
    info['filepath_or_buffer'] = fileName
    info['skiprows'] = determineNSkipLines(s, newlines, info)
    if info['sep'][0] == '"':
        info['quotechar'] = '"'
        info['sep'] = re.sub('"', '', info['sep'])
    skippedN = read_csv(fileName, sep=info['sep'], skiprows=info['skiprows'], dtype=str, header=None)
    info['names'] = determineHeader(skippedN, newlines, info)
    if inferOnly:
        del info['num_col']
        if info['names'] is None:
            info['header'] = None
            del info['names']
        else:
            del info['names']
        if verbose:
            print info
        return info
    if verbose:
        print skippedN
    if info['names'] is not None:
        del info['names']
        del info['num_col']
        return read_csv(**info)
    else:
        return skippedN


def determineNSkipLines(s, newlines, info):
    reg = '^([^' + info['sep'] + '\n]+' + info['sep'] + '){' + str(info['num_col'] - 1) + '}[^' + info['sep'] + '\n]+'
    if re.search(reg, s[:newlines[0] - 1]):
        return 0
    for i in range(len(newlines) - 1):
        if re.search(reg, s[newlines[i] + 1:newlines[(i + 1)] - 1]):
            return i + 1

    return 0


def determineHeader(skippedS, newlines, info):
    strike = 0
    if all([ cannotBeFloat(x) for x in skippedS.ix[0] ]):
        if not all([ cannotBeFloat(x) for x in skippedS.ix[1] ]):
            strike += 1
        elif all([ numpy.sum(skippedS.ix[(0, x)] == skippedS.ix[:, x]) == 1 for x in range(len(skippedS.ix[0])) ]):
            return
    elif all(skippedS.ix[0, :] == sorted(skippedS.ix[0, :])):
        strike += 1
    if strike > 0:
        return skippedS.ix[0, :]
    else:
        return


def cannotBeFloat(x):
    try:
        if isinstance(float(x), float):
            return False
    except ValueError:
        return True
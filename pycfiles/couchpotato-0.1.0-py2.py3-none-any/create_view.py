# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/create_view.py
# Compiled at: 2009-03-18 14:45:37
import simplejson as json

def setitem(v, k):
    (n, key, value) = k
    if n == 1:
        v[key] = value
        return
    try:
        return v[key]
    except KeyError:
        v[key] = {}
        return v[key]


def _set(data, path, value):
    segments = path.split('.')
    s = [ (len(segments) - n, v, value) for (n, v) in enumerate(segments) ]
    return reduce(setitem, s, data)


def getjs(uses):
    data = {}
    for use in uses:
        attr = ('.').join(use.split('.')[1:])
        model_type = use.split('.')[0]
        _set(data, '%s|%s' % (model_type, attr), '#%s#' % use)

    js = json.dumps(data)
    for use in uses:
        attr = ('.').join(use.split('.')[1:])
        model_type = use.split('.')[0]
        target = '"#%s#"' % use
        replacement = 'doc.%s' % attr
        js = js.replace(target, replacement)
        target = '"%s|%s"' % (model_type, attr)
        if '.' in target:
            target = '%s"' % target.split('.')[0]
        replacement = attr
        if '.' in replacement:
            replacement = replacement.split('.')[0]
        js = js.replace(target, replacement)
        target = '"#%s#"' % use

    return js


if __name__ == '__main__':
    uses = [
     'author.first_name', 'author.last_name', 'author.address.city', 'author.address.postcode', 'author.address.street.street2']
    js = getjs(uses)
    print js
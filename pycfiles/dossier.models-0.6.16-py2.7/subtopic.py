# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/subtopic.py
# Compiled at: 2015-07-08 07:34:06
from __future__ import absolute_import, division, print_function
import base64, re
from dossier.fc import StringCounter

def subtopics(store, folders, folder_id, subfolder_id, ann_id=None):
    """Yields an unordered generator of subtopics in a subfolder.

    Each item of the generator is a 4-tuple of ``content_id``,
    ``subtopic_id``, ``subtopic_type`` and ``data``. Subtopic type
    is one of the following Unicode strings: ``text``, ``image``
    or ``manual``. The type of ``data`` is dependent on the
    subtopic type. For ``image``, ``data`` is a ``(unicode, str)``,
    where the first element is the URL and the second element is
    the binary image data. For all other types, ``data`` is a
    ``unicode`` string.

    :param str folder_id: Folder id
    :param str subfolder_id: Subfolder id
    :param str ann_id: Username
    :rtype: generator of
            ``(content_id, subtopic_id, url, subtopic_type, data)``
    """
    items = folders.grouped_items(folder_id, subfolder_id, ann_id=ann_id)
    fcs = dict([ (cid, fc) for cid, fc in store.get_many(items.keys()) ])
    for cid, subids in items.iteritems():
        fc = fcs[cid]
        for subid in subids:
            try:
                data = typed_subtopic_data(fc, subid)
            except KeyError:
                continue

            yield (
             cid, subid, fc['meta_url'], subtopic_type(subid), data)


def typed_subtopic_data(fc, subid):
    """Returns typed subtopic data from an FC."""
    ty = subtopic_type(subid)
    data = get_unicode_feature(fc, subid)
    assert isinstance(data, unicode), 'data should be `unicode` but is %r' % type(data)
    if ty == 'image':
        img_data = get_unicode_feature(fc, subid + '|data')
        img = re.sub('^data:image/[a-zA-Z]+;base64,', '', img_data)
        img = base64.b64decode(img.encode('utf-8'))
        return (
         data, img)
    if ty in ('text', 'manual'):
        return data
    raise ValueError('unrecognized subtopic type "%s"' % ty)


def get_unicode_feature(fc, feat_name):
    feat = fc[feat_name]
    if isinstance(feat, StringCounter) and len(feat) == 0:
        return ''
    return feat


def subtopic_type(subid):
    return subid.split('|')[1]
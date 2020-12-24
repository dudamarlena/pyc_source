# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\transform_bugzilla.py
# Compiled at: 2013-12-18 14:05:11
from datetime import datetime, date
import re
from bzETL.util.cnv import CNV
from bzETL.util.elasticsearch import ElasticSearch
from bzETL.util.logs import Log
from bzETL.util.queries import Q
USE_ATTACHMENTS_DOT = True
MULTI_FIELDS = [
 'cc', 'blocked', 'dependson', 'dupe_by', 'dupe_of', 'flags', 'keywords', 'bug_group', 'see_also']
NUMERIC_FIELDS = ['blocked', 'dependson', 'dupe_by', 'dupe_of',
 'votes',
 'estimated_time',
 'remaining_time',
 'everconfirmed',
 'uncertain']
DATE_PATTERN_STRICT = re.compile('^[0-9]{4}[\\/-][0-9]{2}[\\/-][0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}')
DATE_PATTERN_STRICT_SHORT = re.compile('^[0-9]{4}[\\/-][0-9]{2}[\\/-][0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
DATE_PATTERN_RELAXED = re.compile('^[0-9]{4}[\\/-][0-9]{2}[\\/-][0-9]{2}')

def rename_attachments(bug_version):
    if bug_version.attachments == None:
        return bug_version
    else:
        if not USE_ATTACHMENTS_DOT:
            bug_version.attachments = CNV.JSON2object(CNV.object2JSON(bug_version.attachments).replace('attachments.', 'attachments_'))
        return bug_version


def normalize(bug):
    bug = bug.copy()
    bug.id = unicode(bug.bug_id) + '_' + unicode(bug.modified_ts)[:-3]
    bug._id = None
    bug.flags = Q.sort(bug.flags, 'value')
    if bug.attachments != None:
        if USE_ATTACHMENTS_DOT:
            bug.attachments = CNV.JSON2object(CNV.object2JSON(bug.attachments).replace('attachments_', 'attachments.'))
        bug.attachments = Q.sort(bug.attachments, 'attach_id')
        for a in bug.attachments:
            for k, v in a.items():
                if k.endswith('isobsolete') or k.endswith('ispatch') or k.endswith('isprivate'):
                    a[k.replace('.', '\\.')] = CNV.value2int(v)

            a.flags = Q.sort(a.flags, ['modified_ts', 'value'])

    if bug.changes != None:
        if USE_ATTACHMENTS_DOT:
            json = CNV.object2JSON(bug.changes).replace('attachments_', 'attachments.')
            bug.changes = CNV.JSON2object(json)
        bug.changes = Q.sort(bug.changes, ['attach_id', 'field_name'])
    bug = ElasticSearch.scrub(bug)
    for f in NUMERIC_FIELDS:
        v = bug[f]
        if v == None:
            continue
        elif f in MULTI_FIELDS:
            bug[f] = CNV.value2intlist(v)
        elif CNV.value2number(v) == 0:
            del bug[f]
        else:
            bug[f] = CNV.value2number(v)

    for dateField in ['deadline', 'cf_due_date', 'cf_last_resolved']:
        v = bug[dateField]
        if v == None:
            continue
        try:
            if isinstance(v, datetime) or isinstance(v, date):
                bug[dateField] = CNV.datetime2milli(v)
            elif isinstance(v, long) and len(unicode(v)) in (12, 13):
                bug[dateField] = v
            elif not isinstance(v, basestring):
                Log.error('situation not handled')
            elif DATE_PATTERN_STRICT.match(v):
                bug[dateField] = CNV.datetime2milli(CNV.string2datetime(v + '000', '%Y/%m/%d %H:%M%:S%f'))
            elif DATE_PATTERN_STRICT_SHORT.match(v):
                bug[dateField] = CNV.datetime2milli(CNV.string2datetime(v.replace('-', '/'), '%Y/%m/%d %H:%M:%S'))
            elif DATE_PATTERN_RELAXED.match(v):
                bug[dateField] = CNV.datetime2milli(CNV.string2datetime(v[0:10], '%Y-%m-%d'))
        except Exception as e:
            Log.error('problem with converting date to milli (value={{value}})', {'value': bug[dateField]}, e)

    bug.votes = None
    return ElasticSearch.scrub(bug)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/annotate.py
# Compiled at: 2013-02-15 13:25:53
from __future__ import unicode_literals
from lxml import etree
from collections import defaultdict
import sys
if sys.version_info[0] == 3:
    from urllib.parse import urlsplit
    from urllib.request import urlopen
else:
    from urlparse import urlsplit
    from urllib2 import urlopen
statuses = {b'UNKNOWN': b'Unknown', b'TBW': b'Idea; yet to be specified', 
   b'WIP': b'Being edited right now', 
   b'OCBE': b'Overcome by events', 
   b'FD': b'First draft', 
   b'WD': b'Working draft', 
   b'CWD': b'Controversial Working Draft', 
   b'LC': b'Last call for comments', 
   b'ATRISK': b'Being considered for removal', 
   b'CR': b'Awaiting implementation feedback', 
   b'REC': b'Implemented and widely deployed', 
   b'SPLITFD': b'Marked for extraction - First draft', 
   b'SPLIT': b'Marked for extraction - Awaiting implementation feedback', 
   b'SPLITREC': b'Marked for extraction - Implemented and widely deployed'}
url = b'http://www.whatwg.org/specs/web-apps/current-work/status.cgi?action=get-all-annotations'
w3c_statuses = [
 b'WD', b'LC', b'CR', b'PR', b'REC']
w3c_status_names = {b'WD': b'Working Draft', b'LC': b'Last Call', 
   b'CR': b'Candidate Recommendation', 
   b'PR': b'Proposed Recommendation', 
   b'REC': b'W3C Recommendation'}

def annotate(ElementTree, **kwargs):
    if b'annotation' not in kwargs or not kwargs[b'annotation']:
        return
    annotation_location = kwargs[b'annotation']
    if urlsplit(annotation_location)[0]:
        annotations_data = urlopen(annotation_location)
    else:
        annotations_data = open(annotation_location)
    annotations = etree.parse(annotations_data)
    add_whatwg_status = b'annotate_whatwg_status' in kwargs and kwargs[b'annotate_whatwg_status']
    statuses = {}
    if add_whatwg_status:
        for entry in annotations.xpath(b'//entry'):
            statuses[entry.attrib[b'section']] = entry

    add_w3c_issues = b'annotate_w3c_issues' in kwargs and kwargs[b'annotate_w3c_issues']
    issues = defaultdict(list)
    spec_status = None
    if add_w3c_issues:
        spec_status = annotations.getroot().attrib[b'status']
        assert spec_status in w3c_statuses
        for entry in annotations.xpath(b'//entry[issue]'):
            for issue in entry.xpath(b'./issue'):
                issues[entry.attrib[b'section']].append(issue)

    heading_elements = set([b'h1', b'h2', b'h3', b'h4', b'h5', b'h6'])
    for element in ElementTree.getroot().iterdescendants():
        if b'id' in element.attrib and (element.attrib[b'id'] in statuses or element.attrib[b'id'] in issues) and element.tag in heading_elements:
            status = statuses.get(element.attrib[b'id'], None)
            issue_list = issues.get(element.attrib[b'id'], None)
            annotation = make_annotation(status, issue_list, spec_status)
            element.addnext(annotation)

    return


def make_annotation(entry, issues, spec_status):
    container = etree.Element(b'p')
    container.attrib[b'class'] = b'XXX annotation'
    if entry is not None and entry.attrib[b'status'] != b'UNKNOWN':
        status = etree.Element(b'b')
        status.text = b'Status: '
        status_text = etree.Element(b'i')
        status_text.text = statuses[entry.attrib[b'status']]
        container.append(status)
        container.append(status_text)
        if issues:
            status_text.text += b'. '
    if issues:
        span_issue = etree.Element(b'span')
        multiple_issues = len(issues) > 1

        def cmp_issues(a, b):
            args = tuple([ int(item.attrib[b'name'].split(b'-')[1]) for item in (
             a, b)
                         ])
            return cmp(*args)

        issues.sort(cmp_issues)
        for i, issue in enumerate(issues):
            a = etree.Element(b'a', attrib={b'href': issue.attrib[b'url']})
            a.text = issue.attrib[b'name']
            a.tail = b' (%s)' % issue.attrib[b'shortname']
            if multiple_issues and i == len(issues) - 2:
                a.tail += b' and '
            elif i < len(issues) - 1:
                a.tail += b', '
            else:
                a.tail += b' '
            span_issue.append(a)

        next_status_name = w3c_status_names[w3c_statuses[(w3c_statuses.index(spec_status) + 1)]]
        if multiple_issues:
            span_issue[(-1)].tail += b'block progress to %s' % next_status_name
        else:
            span_issue[(-1)].tail += b'blocks progress to %s' % next_status_name
        container.append(span_issue)
    return container
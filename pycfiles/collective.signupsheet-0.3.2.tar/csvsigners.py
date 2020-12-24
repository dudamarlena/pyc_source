# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/csvsigners.py
# Compiled at: 2011-07-29 07:55:08
import csv, cStringIO

def exportSignersToCsv(brains=None):
    attrs = ['gender', 'firstname', 'lastname', 'email', 'company',
     'function', 'address', 'zipcode', 'city', 'phone', 'fax',
     'bill_to', 'bill_address', 'bill_zipcode', 'bill_city', 'bill_province',
     'vatno', 'delegation_request', 'delegation',
     'penalty_clearance', 'credits_request', 'credits',
     'comment']
    attrsparent = ['event_url', 'title']
    rows = []
    for brain in brains:
        o = brain.getObject()
        row = []
        for attr in attrs:
            itm = getattr(o, attr, '')
            try:
                itm = itm.encode('latin-1', 'ignore')
            except AttributeError:
                itm = 'True' if itm else 'False'

            row.append(itm)

        op = o.getParentNode()
        row.append(brain.getURL().encode('latin-1', 'ignore'))
        row.append(op.title.encode('latin-1', 'ignore'))
        rows.append(row)

    csv_content = cStringIO.StringIO()
    writer = csv.writer(csv_content, quoting=csv.QUOTE_ALL)
    csvattrs = attrs + ['url', 'event_title']
    writer.writerow(csvattrs)
    writer.writerows(rows)
    csv_content = csv_content.getvalue()
    return csv_content
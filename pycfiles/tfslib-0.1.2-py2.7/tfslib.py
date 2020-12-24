# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tfslib.py
# Compiled at: 2014-01-10 07:01:40
import logging, uuid, urlparse
from suds.transport.https import WindowsHttpAuthenticated
from suds.client import Client
from suds.sax.text import Raw

def ensure_list(not_list):
    if isinstance(not_list, (list, tuple)):
        return not_list
    return [
     not_list]


class SoapClient:

    def __init__(self, url, username, password):
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
        url = '%s://%s%s/WorkItemTracking/v4.0/ClientService.asmx' % (scheme, netloc, path)
        ntlm = WindowsHttpAuthenticated(username=username, password=password)
        self.client = Client(url + '?WSDL', transport=ntlm, location=url)
        token = self.client.factory.create('RequestHeader')
        token.Id = 'uuid:%s' % uuid.uuid4()
        self.client.set_options(soapheaders=token)
        cache = self.client.options.cache
        cache.setduration(days=1)


class TfsTabular:

    def __init__(self, table_name, data_rows):
        self.data_rows = data_rows
        self.table_name = table_name

    def __str__(self):
        a = '=== table: ' + self.table_name + ' ===\n'
        import json
        a += json.dumps(self.data_rows, indent=4)
        return a

    def __repr__(self):
        return self.__str__()


class TfsClient(SoapClient):

    def __init__(self, url, username, password):
        SoapClient.__init__(self, url, username, password)

    def create_tabular(self, table_node):
        return TfsTabular(table_node._name, self._read_rows(table_node, True))

    def _unpack_table_row_value(self, values):
        i = 0
        for field in values:
            try:
                fieldIndex = field._k
                for j in range(i, int(fieldIndex)):
                    yield

                try:
                    yield field.value
                except AttributeError:
                    yield

                i = int(fieldIndex)
            except AttributeError:
                yield field

            i += 1

        return

    def _read_rows(self, table, skip_nulls=False):
        rows = []
        columns = table.columns.c
        if table.rows:
            for row_node in ensure_list(table.rows.r):
                values = row_node.f
                if len(values) == 0:
                    return
                tuples = zip(map(lambda a: a.n, ensure_list(columns)), self._unpack_table_row_value(values))
                if skip_nulls:
                    tuples = [ t for t in tuples if t[1] is not None ]
                rows.append(dict(tuples))

        return rows

    def get_work_item(self, item_id, skip_nulls=False):
        result = self.client.service.GetWorkItem(item_id, 0, 0, None, True, None)
        tables = []
        for table in ensure_list(result.workItem.table):
            tabular = self.create_tabular(table)
            tables.append(tabular)

        return tables

    def update_work_item(self, item_id, rev_id, columns={}, computedColumns=['System.RevisedDate', 'System.ChangedDate', 'System.PersonId']):
        import xml.etree.ElementTree as et
        package = et.Element('Package', {'xmlns': ''})
        update = et.SubElement(package, 'UpdateWorkItem', {'WorkItemID': str(item_id), 'Revision': str(rev_id), 'ObjectType': 'WorkItem'})
        cols = et.SubElement(update, 'ComputedColumns')
        for name in computedColumns:
            et.SubElement(cols, 'ComputedColumn', {'Column': name})

        cols = et.SubElement(update, 'Columns')
        for name, value in columns.iteritems():
            col = et.SubElement(cols, 'Column', {'Column': name})
            et.SubElement(col, 'Value').text = value

        raw_xml = Raw(et.tostring(package))
        result = self.client.service.Update(raw_xml)
        return result

    def get_stored_queries(self, item_id):
        result = self.client.service.GetStoredQueries(0, item_id)
        tables = []
        for table in ensure_list(result.table):
            tabular = self.create_tabular(table)
            tables.append(tabular)
            print tabular

        return tables

    def query_work_items(self, query):
        raw_xml = Raw(query)
        result = self.client.service.QueryWorkitems(raw_xml, None, True, None)
        logging.info(result)
        return result
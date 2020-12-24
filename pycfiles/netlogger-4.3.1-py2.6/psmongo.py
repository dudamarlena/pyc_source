# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/datamining/psmongo.py
# Compiled at: 2011-06-13 22:40:21
"""
Query (etc.) Periscope MongoDBs
"""
import bson, pymongo, pprint, csv, sys
SAMPLE_RANGE_KEY = '_samples'
SAMPLE_KEY = 'samples'

def meta_parts(m):
    return {'params': m.get('params', {}), 'subject': m.get('subject', {})}


def bin_to_str(d):
    """Recursively force all BinData items to be a string.
    """
    if isinstance(d, dict):
        for (key, value) in d.iteritems():
            d[key] = bin_to_str(value)

    elif isinstance(d, list):
        d = [ bin_to_str(v) for v in d ]
    if isinstance(d, bson.binary.Binary):
        d = str(d)
    return d


def stringize(items):
    r = []
    for i in items:
        if isinstance(i, int):
            r.append(('{0:d}').format(i))
        elif isinstance(i, float):
            r.append(('{0:f}').format(i))
        elif i == '':
            r.append('"NA"')
        else:
            r.append(str(i))

    return r


class PeriscopeCollection:
    """MongoDB collection with Periscope data.
    """
    META_FIELD = 'meta'
    DATA_FIELD = 'data'
    ID_FIELD = '_id'
    PID_FIELD = '_pid'
    META_ID_FIELD = '_mid'
    TYPE_FIELD = 'event_type'
    SUBJ_FIELD = 'subject'
    PARAM_FIELD = 'params'
    DATA_VALUES_FIELD = 'values'
    TS_FIELD = 'ts'
    TS_VALUE_FIELD = '_ts'

    def __init__(self, collection):
        self._coll = collection
        (self._meta, self._hdr) = (None, None)
        self._reqmeta = set()
        return

    def set_req_meta(self, items):
        """A list of required metadata items
        All entries missing these items will be skipped.
        """
        self._reqmeta = set(items)

    def init_meta(self):
        """Retrieve and store metadata id's internally.
        """
        d = {}
        spec, fields = {'meta.subject': {'$exists': True}}, {'meta': 1}
        for obj in self._coll.find(spec, fields):
            for m in obj['meta']:
                if m.has_key(self.PID_FIELD):
                    pid = [
                     m[self.PID_FIELD]]
                else:
                    pid = []
                d[m[self.ID_FIELD]] = pid

        for (key, pids) in d.iteritems():
            pids0 = pids
            while pids:
                parent = pids[(-1)]
                pids = d[parent]
                pids0.extend(pids)

        self._meta = d

    def init_table_hdr(self):
        """Retrieve and store hdr info internally.
        """
        hdr, hdr_seen = [], set()
        spec, fields = {'meta.subject': {'$exists': True}}, {'meta': 1}
        for obj in self._coll.find(spec, fields):
            for m in obj[self.META_FIELD]:
                event_type = m[self.TYPE_FIELD]
                for part in ('params', 'subject'):
                    for k in m[part].keys():
                        if k != 'ts' and k not in hdr_seen:
                            hdr.append((event_type, part, k))
                        hdr_seen.add(k)

        self._hdr = [
         (None, 'data', 'id'), (None, 'data', 'event'), (None, 'data', 'mid')] + list(hdr) + [
         (None, 'data', 'ts'), (None, 'data', 'name'), (None, 'data', 'value')]
        return

    def get_table_hdr(self, ns=0):
        if self._hdr is None:
            self.init_table_hdr()
        hdr_cols = []
        for (e, p, k) in self._hdr:
            if ns >= 2:
                s = ('{0}.{1}.{2}').format(e, p, k)
            elif ns == 1:
                s = ('{0}.{1}').format(p, k)
            else:
                s = k
            hdr_cols.append(s)

        return hdr_cols

    def get_table_body(self):
        """Get iterator over rows of the table body.
        """
        rows = []
        if self._meta is None:
            self.init_meta()
        if self._hdr is None:
            self.init_table_hdr()
        for (meta_id, pids) in self._meta.iteritems():
            ts = None
            subj, param = {}, {}
            all_ids = [
             meta_id] + pids
            spec = {'meta._id': {'$in': all_ids}}
            for obj in self._coll.find(spec):
                for meta in obj[self.META_FIELD]:
                    if meta[self.ID_FIELD] in all_ids:
                        subj.update(meta[self.SUBJ_FIELD])
                        param.update(meta[self.PARAM_FIELD])

            if self.TS_FIELD in subj:
                ts = subj[self.TS_FIELD]
                del subj[self.TS_FIELD]
            if self.TS_FIELD in param:
                ts = param[self.TS_FIELD]
                del param[self.TS_FIELD]
            spec = {'data.' + self.META_ID_FIELD: meta_id}
            row_meta, row_meta_keys = [], set()
            for (et, part, key) in self._hdr:
                if et is not None:
                    if part == self.SUBJ_FIELD:
                        v = subj.get(key, '')
                        row_meta.append(v)
                        if v:
                            row_meta_keys.add(key)
                    elif part == self.PARAM_FIELD:
                        v = param.get(key, '')
                        row_meta.append(v)
                        if v:
                            row_meta_keys.add(key)

            if not self._reqmeta.issubset(row_meta_keys):
                continue
            (n, m) = (0, 0)
            for obj in self._coll.find(spec):
                n += 1
                row = row_meta + [meta_id]
                for datum in obj[self.DATA_FIELD]:
                    data_id = datum[self.ID_FIELD]
                    etype = datum[self.TYPE_FIELD]
                    values_dict = datum[self.DATA_VALUES_FIELD]
                    ts_values = values_dict.get(self.TS_VALUE_FIELD, None)
                    for (name, values) in values_dict.iteritems():
                        if name == self.TS_VALUE_FIELD:
                            continue
                        for (i, value) in enumerate(values):
                            if ts_values:
                                ts = ts_values[i]
                            assert ts, 'No timestamp'
                            rows.append([data_id, etype] + row + [ts, name, value])
                            m += 1

        return rows


def __test(db, coll):
    mongo = pymongo.Connection()
    ps = PeriscopeCollection(mongo[db][coll])


def usage():
    import os
    prog = os.path.basename(sys.argv[0])
    sys.stderr.write(('usage: {prog} DATABASE COLLECTION\n').format(prog=prog))
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    __test(*sys.argv[1:])
    sys.exit(0)
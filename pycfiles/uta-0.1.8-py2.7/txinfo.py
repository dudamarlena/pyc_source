# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/formats/txinfo.py
# Compiled at: 2014-07-08 18:45:11
import csv, recordtype

class TxInfo(recordtype.recordtype('TxInfo', [
 'origin', 'ac', 'hgnc', 'cds_se_i', 'exons_se_i'])):
    pass


class TxInfoWriter(csv.DictWriter):

    def __init__(self, tsvfile):
        csv.DictWriter.__init__(self, tsvfile, fieldnames=TxInfo._fields, delimiter='\t')
        csv.DictWriter.writeheader(self)

    def write(self, si):
        self.writerow(si._asdict())


class TxInfoReader(csv.DictReader):

    def __init__(self, tsvfile):
        csv.DictReader.__init__(self, tsvfile, delimiter='\t')
        if set(self.fieldnames) != set(TxInfo._fields):
            raise RuntimeError('Format error: expected header with these columns: ' + (',').join(TxInfo._fields) + ' but got: ' + (',').join(self.fieldnames))

    def next(self):
        d = csv.DictReader.next(self)
        return TxInfo(**d)


if __name__ == '__main__':
    tmpfn = '/tmp/txinfo'
    with open(tmpfn, 'w') as (f):
        esw = TxInfoWriter(f)
        for i in range(3):
            es = TxInfo(**dict([ (k, k + ':' + str(i)) for k in TxInfo._fields ]))
            esw.write(es)

    with open(tmpfn, 'r') as (f):
        esr = TxInfoReader(f)
        for es in esr:
            print es
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/formats/exonset.py
# Compiled at: 2014-07-08 18:45:11
import csv, recordtype

class ExonSet(recordtype.recordtype('ExonSet', [
 'tx_ac', 'alt_ac', 'method', 'strand', 'exons_se_i'])):
    pass


class ExonSetWriter(csv.DictWriter):

    def __init__(self, tsvfile):
        csv.DictWriter.__init__(self, tsvfile, fieldnames=ExonSet._fields, delimiter='\t')
        csv.DictWriter.writeheader(self)

    def write(self, si):
        self.writerow(si._asdict())


class ExonSetReader(csv.DictReader):

    def __init__(self, tsvfile):
        csv.DictReader.__init__(self, tsvfile, delimiter='\t')
        if set(self.fieldnames) != set(ExonSet._fields):
            raise RuntimeError('Format error: expected header with these columns: ' + (',').join(ExonSet._fields) + ' but got: ' + (',').join(self.fieldnames))

    def next(self):
        d = csv.DictReader.next(self)
        return ExonSet(**d)


if __name__ == '__main__':
    tmpfn = '/tmp/exonset'
    with open(tmpfn, 'w') as (f):
        esw = ExonSetWriter(f)
        for i in range(3):
            es = ExonSet(**dict([ (k, k + ':' + str(i)) for k in ExonSet._fields ]))
            esw.write(es)

    with open(tmpfn, 'r') as (f):
        esr = ExonSetReader(f)
        for es in esr:
            print es
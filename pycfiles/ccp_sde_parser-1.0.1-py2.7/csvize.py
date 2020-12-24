# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ccp_sde_parser/csvize.py
# Compiled at: 2012-11-04 23:11:04
import csv
from progressbar import ProgressBar, Bar, ETA, Percentage
import os, sys, json

def main():
    if len(sys.argv) != 3:
        print 'Incorrect number of arguments'
        print 'USAGE: %s JSON_FILE OUTPUT_FILE' % sys.argv[0]
        sys.exit(1)
    json_file = sys.argv[1]
    out_file = sys.argv[2]
    if not os.path.isfile(json_file):
        print 'Unable to open specified JSON file.'
        sys.exit(1)
    contents = None
    with open(json_file, 'rb') as (f):
        contents = json.load(f)
    if not contents:
        print 'Unable to parse json'
        sys.exit(1)
    with open(out_file, 'wb') as (f):
        dw = csv.DictWriter(f, contents['columns'])
        dw.writeheader()
        pbar = ProgressBar(widgets=['CSVizing... ', Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(contents['data'])).start()
        for idx, d in enumerate(contents['data']):
            dw.writerow({k:unicode(v).encode('utf-8') for k, v in d.items()})
            pbar.update(idx)

        pbar.finish()
    return


if __name__ == '__main__':
    main()
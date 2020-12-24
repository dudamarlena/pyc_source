# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\parseresults.py
# Compiled at: 2020-02-27 16:28:58
# Size of source mod 2**32: 3380 bytes
import pdb, optparse, csv

def main():
    usage = 'usage: %prog [options] textresults\n\n'
    usage += 'where:\n'
    usage += '  <textresults>\ttext file with results\n'
    usage += '  output is put in .csv file with same name\n'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-H', '--hdr', dest='hdr', type='int', help='row number for header', default=None)
    parser.set_defaults()
    options, args = parser.parse_args()
    textresults = args.pop(0)
    IN = open(textresults, 'r')
    _OUT = open(('{0}.csv'.format(textresults)), 'w', newline='')
    OUT = csv.writer(_OUT)
    hdrqueue = []
    foundhdr = False
    if options.hdr:
        rowsuntilhdr = options.hdr
    for row in IN:
        foundhdr or hdrqueue.append(row)
        if not options.hdr:
            if len(hdrqueue) > 2:
                hdrqueue.pop(0)
            else:
                rowsuntilhdr -= 1
            fields = row.split()
            if options.hdr and rowsuntilhdr == 0 or len(fields) > 1 and fields[0][0:2] == '==':
                foundhdr = True
                boundaries = []
                scanndx = 0
                for field in fields:
                    boundaries.append((scanndx, scanndx + len(field)))
                    scanndx += len(field)
                    while scanndx < len(row) and row[scanndx] != '=':
                        scanndx += 1

                headers = []
                for boundary in boundaries:
                    hdrrow = hdrqueue[0]
                    headers.append(hdrrow[boundary[0]:boundary[1]].strip())

                OUT.writerow(headers)
            else:
                continue
            fields = []
            for boundary in boundaries:
                fields.append(row[boundary[0]:boundary[1]].strip())

            try:
                placeoa = int(fields[0])
            except ValueError:
                continue

            OUT.writerow(fields)

    _OUT.close()


if __name__ == '__main__':
    main()
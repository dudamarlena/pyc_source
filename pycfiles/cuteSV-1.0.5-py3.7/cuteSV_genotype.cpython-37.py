# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuteSV/cuteSV_genotype.py
# Compiled at: 2020-04-17 02:18:29
# Size of source mod 2**32: 3021 bytes
from cuteSV.cuteSV_Description import Generation_VCF_header

def count_coverage(chr, s, e, f):
    read_count = set()
    for i in f.fetch(chr, s, e):
        read_count.add(i.query_name)

    return len(read_count)


def cal_GT(a, b):
    if b == 0:
        return '1/1'
        if a * 1.0 / b < 0.2:
            return '0/0'
    else:
        if a * 1.0 / b >= 0.2:
            if a * 1.0 / b < 0.8:
                return '0/1'
        if a * 1.0 / b >= 0.8 and a * 1.0 / b < 1.0:
            return '1/1'
    return '1/1'


def produce_GT(samfile, chr, bk, sup_read):
    search_start = max(bk - 20, 0)
    search_end = min(bk + 20, samfile.get_reference_length(chr))
    DP = count_coverage(chr, search_start, search_end, samfile)
    output_GT = '{FORMAT}\t{GT}:{DR}:{RE}'.format(FORMAT='GT:DR:DV',
      GT=(cal_GT(sup_read, DP)),
      DR=(max(DP - sup_read, 0)),
      RE=sup_read)
    return output_GT


def generate_output(args, semi_result, contigINFO):
    """
        Generation of VCF format file.
        VCF version: 4.2
        """
    svid = dict()
    svid['INS'] = 0
    svid['DEL'] = 0
    svid['BND'] = 0
    svid['DUP'] = 0
    svid['INV'] = 0
    file = open(args.output, 'w')
    Generation_VCF_header(file, contigINFO, args.sample)
    for i in semi_result:
        if i[1] in ('DEL', 'INS'):
            if i[1] == 'INS':
                cal_end = int(i[2]) + 1
            else:
                cal_end = int(i[2]) + abs(int(float(i[3])))
            info_list = '{PRECISION};SVTYPE={SVTYPE};SVLEN={SVLEN};END={END};BREAKPOINT_STD={BPSTD};SVLEN_STD={LENSTD};RE={RE}'.format(PRECISION='PRECISE',
              SVTYPE=(i[1]),
              SVLEN=(i[3]),
              END=(str(cal_end)),
              BPSTD=(i[5]),
              LENSTD=(i[6]),
              RE=(i[4]))
            file.write('{CHR}\t{POS}\t{ID}\tN\t{ALT}\t.\tPASS\t{INFO}\t{FORMAT}\t{GT}:{DR}:{RE}\n'.format(CHR=(i[0]),
              POS=(i[2]),
              ID=('cuteSV.%s.%d' % (i[1], svid[i[1]])),
              ALT=('<%s>' % i[1]),
              INFO=info_list,
              FORMAT='GT:DR:DV',
              GT=(i[(-1)]),
              DR=(i[(-2)]),
              RE=(i[4])))
            svid[i[1]] += 1
        elif i[1] in ('DUP', 'INV'):
            cal_end = int(i[2]) + abs(int(float(i[3])))
            info_list = '{PRECISION};SVTYPE={SVTYPE};SVLEN={SVLEN};END={END};RE={RE}'.format(PRECISION='PRECISE',
              SVTYPE=(i[1]),
              SVLEN=(i[3]),
              END=(str(cal_end)),
              RE=(i[4]))
            file.write('{CHR}\t{POS}\t{ID}\tN\t{ALT}\t.\tPASS\t{INFO}\t{FORMAT}\t{GT}:{DR}:{RE}\n'.format(CHR=(i[0]),
              POS=(i[2]),
              ID=('cuteSV.%s.%d' % (i[1], svid[i[1]])),
              ALT=('<%s>' % i[1]),
              INFO=info_list,
              FORMAT='GT:DR:DV',
              GT=(i[(-1)]),
              DR=(i[(-2)]),
              RE=(i[4])))
            svid[i[1]] += 1
        else:
            info_list = '{PRECISION};SVTYPE={SVTYPE};CHR2={CHR2};END={END};RE={RE}'.format(PRECISION='PRECISE',
              SVTYPE='BND',
              CHR2=(i[3]),
              END=(i[4]),
              RE=(i[5]))
            file.write('{CHR}\t{POS}\t{ID}\tN\t{ALT}\t.\tPASS\t{INFO}\t{FORMAT}\t{GT}:{DR}:{RE}\n'.format(CHR=(i[0]),
              POS=(i[2]),
              ID=('cuteSV.%s.%d' % ('BND', svid['BND'])),
              ALT=(i[1]),
              INFO=info_list,
              FORMAT='GT:DR:DV',
              GT=(i[(-1)]),
              DR=(i[(-2)]),
              RE=(i[5])))
            svid['BND'] += 1
# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_loc_gff.py
# Compiled at: 2014-06-13 07:51:15
import re, sys, getopt

def usage():
    """Print usage."""
    print('\n    #####################################\n    #  scythe_loc_gff.py  -f FILE.gff3  #\n    #####################################\n\n    -f, --file=gff3_FILE\n    -o, --output=FILE        output file [default: gff3_FILE.loc]\n    -h, --help               prints this\n    -H, --HELP               show help on format\n    ')
    sys.exit(2)


def formatHelp():
    print('\n    #------------ loc output format ---------------------------#\n\n    LOCUS0\tTRANSCRIPT0_0\tTRANSCRIPT0_1\t...\tTRANSCRIPT0_n\n    LOCUS1\tTRANSCRIPT1_0\t...\tTRANSCRIPT1_m\n    .\n    .\n    .\n    LOCUSk\tTRANSCRIPTk_0\t...TRANSCRIPTk_l\n\n    #----------------------------------------------------------#\n\n\n    #-------- gff version 3 input format ----------------------#\n    example (tab is shown as \\t):\n\n    ##gff-version 3\n    L1i\\texample\\tgene\\t1000\\t9000\\t.\\t+\\t.\\tID=L1;Name=L1;Note=example\n    L1.a\\texample\\tmRNA\\t1000\\t9000\\t.\\t+\\t.\\tID=L1.a;Parent=L1;Name=L1.a\n\n\n    Note that this script only relies on the "ID" and "Parent" tags,\n    "Name" will be ignored. If "longest" is specified (eg phytozome)\n    and =="1", the transcript will be placed on the first position\n    for its gene.\n    #----------------------------------------------------------#\n\n    ')


def checkGff3(infile):
    with open(infile, 'r') as (f):
        l = f.readline().strip()
        if l == '##gff-version 3':
            return True
        else:
            return False


def read_gff_attrib(infile, attrib):
    with open(infile, 'r') as (f):
        for l in f:
            if l.strip() == '':
                continue
            if l.startswith('#'):
                continue
                tmp = l.split('\t')[2].lower().strip()
                if tmp == attrib.lower():
                    ln = l.split('\t')[8].strip()
                    yield ln
                    continue


def read_gene_mrna(infile):
    genes = {}
    longest = set()
    p_id = '(ID=)(.*?)(;|$)'
    p_name = '(Name=)(.*?)(;|$)'
    p_parent = '(Parent=)(.*?)(;|$)'
    o_longest = '(longest=)(.*?)(;|$)'
    o_biotype = None
    for g in read_gff_attrib(infile, 'gene'):
        m = re.findall(p_id, g)
        if m:
            mid = m[0][1]
            genes[mid] = []
            continue

    for g in read_gff_attrib(infile, 'mrna'):
        m = re.findall(p_id, g)
        if m:
            mid = m[0][1]
        m = re.findall(p_parent, g)
        if m:
            if m[0][1] in genes:
                l = re.findall(o_longest, g)
                if l:
                    if l[0][1] == '1':
                        longest.add(mid)
                        genes[m[0][1]].insert(0, mid)
                    else:
                        genes[m[0][1]].append(mid)
                else:
                    genes[m[0][1]].append(mid)
            else:
                raise Warning('{}: parent is not in known genes'.format(mid))
                continue

    return genes.copy()


def writeLoc(genesDct, outfile):
    f = lambda x: '\t'.join(genesDct[x])
    tmp = [g + '\t' + f(g) for g in sorted(genesDct.keys())]
    res = '\n'.join(tmp)
    with open(outfile, 'w') as (out):
        out.write(res)


def read_gff2loc(infile, outfile):
    infile = open(infile, 'r')
    outfile = open(outfile, 'w')
    loci = {}
    longest = {}
    rawstr = '(Name=)(.*);pacid.*(longest=)(.*);(Parent=)(.*)'
    cnt = 0
    for ln in infile:
        s = ln
        m = re.findall(rawstr, s)
        if len(m) > 0:
            name = m[0][1]
            isLongest = m[0][3]
            parent = m[0][5]
            if isLongest == str(1):
                if parent in longest:
                    print('#Warning ' + parent + ' has more than one default model\nCheck your gff -> ', longest[parent], name)
                longest[parent] = name
            else:
                if isLongest == str(0):
                    if parent in loci:
                        loci[parent].append(name)
                    else:
                        loci[parent] = [
                         name]
                else:
                    continue

    s_def = sorted(longest.keys())
    for k_def in s_def:
        try:
            outfile.write(k_def + '\t' + longest[k_def] + '\t' + '\t'.join(loci[k_def]) + '\n')
        except KeyError as ke:
            outfile.write(k_def + '\t' + longest[k_def] + '\n')

        if k_def in loci:
            del loci[k_def]
            continue

    s = sorted(loci.keys())
    for k in s:
        try:
            outfile.write(k + '\t' + longest[k] + '\t' + '\t'.join(loci[k]) + '\n')
        except KeyError as ke:
            print('#Warning ' + k + ' has no default model\n')
            outfile.write(k + '\t' + '\t'.join(loci[k]) + '\n')

    return loci


def main():
    outfile = None
    infile = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:hHo:', ['file=', 'help', 'HELP', 'output='])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-f', '--file'):
            infile = a
        elif o in ('-h', '--help'):
            usage()
        elif o in ('-H', '--HELP'):
            formatHelp()
        elif o in ('-o', '--output'):
            outfile = a
        elif not False:
            raise AssertionError('unhandled option')

    if infile is None:
        usage()
    if outfile is None:
        outfile = infile + '.loc'
    if not checkGff3(infile):
        raise Warning('Gff3 line (##gff-version 3) missing at beginning of file. This might not work.')
    genes = read_gene_mrna(infile)
    writeLoc(genes, outfile)
    return


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_loc_tsv.py
# Compiled at: 2014-06-13 07:51:59
import sys, getopt

def usage():
    print('\n    ###########################\n    #  scythe_loc_tsv.py      #\n    ###########################\n    -f, --file=ENSEMBLBioMart.tsv\n                              format: 1st column: gene id, 2nd column:transcript id,\n                                      3rd column: peptide id, 4th column: cds length;\n                                      gene ids can occur multiple times\n    -c, --custom=COLx,COLy,COLz,...   COLi in ["gene","transcript", "protein", "length"]\n                                      Use this if your file is different from the described biomart output.\n                                      "cds_length" is optional but recommended, at least one of\n                                      ["transcript", "protein"] need to be included\n    -o, --output=FILE         output file [default: ENSEMBLEBioMart.tsv.loc]\n    -h, --help                prints this\n    -H, --HELP                show help on format\n    #----------------------------------#\n    ')
    sys.exit(2)


def formatHelp():
    print('\n    #------------ loc output format ---------------------------#\n\n    LOCUS0\tTRANSCRIPT0_0\tTRANSCRIPT0_1\t...\tTRANSCRIPT0_n\n    LOCUS1\tTRANSCRIPT1_0\t...\tTRANSCRIPT1_m\n    .\n    .\n    .\n    LOCUSk\tTRANSCRIPTk_0\t...TRANSCRIPTk_l\n\n    #----------------------------------------------------------#\n\n    ')
    howTo()


def howTo():
    """Print an ENSEMBLE example query"""
    print('\n    example ensembl query:\n\n    http://www.ensembl.org/biomart/\n    <?xml version="1.0" encoding="UTF-8"?>\n    <!DOCTYPE Query>\n    <Query  virtualSchemaName = "default" formatter = "TSV"\n    header = "0" uniqueRows = "0" count = "" datasetConfigVersion = "0.6" >\n    <Dataset name = "hsapiens_gene_ensembl" interface = "default" >\n    <Filter name = "biotype" value = "protein_coding"/>\n    <Attribute name = "ensembl_gene_id" />\n    <Attribute name = "ensembl_transcript_id" />\n    <Attribute name = "ensembl_peptide_id" />\n    <Attribute name = "cds_length" />\n    </Dataset>\n    </Query>\n    ')


class WrongNumberOfColumnsException(Exception):
    pass


def writeLoc(genesDct, outfile):
    f = lambda x: '\t'.join(genesDct[x])
    tmp = [g + '\t' + f(g) for g in sorted(genesDct.keys())]
    res = '\n'.join(tmp)
    with open(outfile, 'w') as (out):
        out.write(res)


def readTsv(infile=None):
    genes = set()
    genest = {}
    genesp = {}
    maxlen = {}
    gene_index = None
    transcript_index = None
    protein_index = None
    length_index = None
    with open(infile, 'r') as (f):
        headers = f.readline().strip().split('\t')
        headers = [h.lower().replace(' ', '') for h in headers]
        for i, h in enumerate(headers):
            if 'gene' in h:
                gene_index = i
            elif 'transcript' in h:
                transcript_index = i
            elif 'protein' in h or 'peptide' in h:
                protein_index = i
            elif 'length' in h:
                length_index = i
                continue

        for l in f:
            tmp = l.strip().split('\t')
            tmpg = tmp[gene_index]
            if tmpg not in genes:
                genes.add(tmpg)
                if transcript_index:
                    genest[tmpg] = [
                     tmp[transcript_index]]
                if protein_index:
                    try:
                        genesp[tmpg] = [
                         tmp[protein_index]]
                    except IndexError as e:
                        sys.stderr.write(str(tmp) + ' (missing protein id field)\n')

                if length_index:
                    try:
                        maxlen[tmpg] = tmp[length_index]
                    except IndexError as e:
                        sys.stderr.write(str(tmp) + ' (missing length field)\n')
                        maxlen[tmpg] = 0

            elif length_index:
                try:
                    if tmp[length_index] > maxlen[tmpg]:
                        maxlen[tmpg] = tmp[length_index]
                        if transcript_index:
                            genest[tmpg].insert(0, tmp[transcript_index])
                        if protein_index:
                            try:
                                genesp[tmpg].insert(0, tmp[protein_index])
                            except KeyError as e:
                                genesp[tmpg] = [
                                 tmp[protein_index]]

                    elif transcript_index:
                        genest[tmpg].append(tmp[transcript_index])
                    if protein_index:
                        genesp[tmpg].append(tmp[protein_index])
                except IndexError as e:
                    sys.stderr.write(str(tmp) + ' (missing length field)\n')

            else:
                if transcript_index:
                    genest[tmpg].append(tmp[transcript_index])
                if protein_index:
                    try:
                        genesp[tmpg].append(tmp[protein_index])
                    except KeyError as e:
                        try:
                            genesp[tmpg] = [
                             tmp[protein_index]]
                        except IndexError as e:
                            sys.stderr.write(str(tmp) + ' (missing protein id field)\n')

                    except IndexError as e:
                        sys.stderr.write(str(tmp) + ' (missing protein id field)\n')

                    continue

    return (
     genest.copy(), genesp.copy())


def main():
    outfile = None
    outfilep = None
    in_tsv = None
    header = ['gene', 'transcript', 'protein', 'length']
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:hHo:', ['file=', 'help', 'HELP', 'output='])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-f', '--file'):
            in_tsv = a
        elif o in ('-h', '--help'):
            usage()
        elif o in ('-H', '--HELP'):
            formatHelp()
        elif o in ('-o', '--output'):
            outfile = a
            outfilep = a + 'p'
        elif not False:
            raise AssertionError('unhandled option')

    if not in_tsv:
        usage()
    if not outfile:
        outfile = in_tsv + '.loc'
        outfilep = in_tsv + '.locp'
    genest, genesp = readTsv(in_tsv)
    if genest:
        writeLoc(genest, outfile)
    if genesp:
        writeLoc(genesp, outfilep)
    return


if __name__ == '__main__':
    main()
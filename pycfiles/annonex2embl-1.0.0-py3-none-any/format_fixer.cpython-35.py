# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/format_fixer.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 4541 bytes
from annogesiclib.gff3 import Gff3Parser

class FormatFixer(object):
    """FormatFixer"""

    def _read_gff(self, gff_file, genes, datas, strain):
        gene_num = 0
        fh = open(gff_file, 'r')
        for entry in Gff3Parser().entries(fh):
            entry.seq_id = strain
            entry.info_without_attributes = '\t'.join([str(field) for field in [
             entry.seq_id, entry.source, entry.feature, entry.start,
             entry.end, entry.score, entry.strand, entry.phase]])
            datas.append(entry)
            if entry.feature == 'gene':
                if 'locus_tag' in entry.attributes.keys():
                    name = entry.attributes['locus_tag']
                if 'gene' in entry.attributes.keys():
                    name = entry.attributes['gene']
                entry.attribute_string = ';'.join(['ID=gene' + str(gene_num),
                 'Name=' + name,
                 entry.attribute_string])
                gene_id = 'gene' + str(gene_num)
                entry.attributes['ID'] = gene_id
                genes.append(entry)
                gene_num += 1

        fh.close()

    def fix_ratt(self, gff_file, strain, out_file):
        out = open(out_file, 'w')
        out.write('##gff-version 3\n')
        nums = {'cds': 0, 'rna': 0, 'gene': 0}
        genes = []
        datas = []
        check_parent = False
        self._read_gff(gff_file, genes, datas, strain)
        check_parent = False
        for data in datas:
            if data.feature == 'gene':
                data = genes[nums['gene']]
                nums['gene'] += 1
            else:
                if data.feature == 'rRNA' or data.feature == 'tRNA':
                    name = data.attributes['locus_tag']
                    data.attribute_string = ';'.join([
                     'ID=rna' + str(nums['rna']),
                     'Name=' + name, data.attribute_string])
                    nums['rna'] += 1
                elif data.feature == 'CDS':
                    if 'protein_id' in data.attributes.keys():
                        name = data.attributes['protein_id']
                    for gene in genes:
                        if gene.start <= data.start and gene.end >= data.end or gene.attributes['locus_tag'] == data.attributes['locus_tag']:
                            data.attribute_string = ';'.join([
                             'ID=cds' + str(nums['cds']), 'Name=' + name,
                             'Parent=' + gene.attributes['ID'],
                             data.attribute_string])
                            check_parent = True
                            break

                    if check_parent:
                        check_parent = False
                    else:
                        data.attribute_string = ';'.join([
                         'ID=cds' + str(nums['cds']),
                         'Name=' + name, data.attribute_string])
                    nums['cds'] += 1
            if 'group' in data.attributes.keys():
                ref_f = open(gff_file, 'r')
                for ref in Gff3Parser().entries(ref_f):
                    if 'group' in ref.attributes.keys() and data.attributes['group'] == ref.attributes['group']:
                        if data.strand != ref.strand:
                            data.strand = ref.strand
                        break

                ref_f.close()
            out.write('\t'.join([data.info_without_attributes,
             data.attribute_string]) + '\n')

        out.close()

    def fix_rnaplex(self, rnaplex_file, out_file):
        out = open(out_file, 'w')
        with open(rnaplex_file, 'r') as (f_h):
            for line in f_h:
                line = line.strip()
                if line != 'Error during initialization of the duplex in duplexfold_XS':
                    out.write(line + '\n')

        out.close()

    def fix_emboss(self, input_file, out_file):
        out = open(out_file, 'w')
        with open(input_file, 'r') as (f_h):
            for line in f_h:
                line = line.strip()
                if line.startswith('>'):
                    out.write(line[:-2] + '\n')
                else:
                    out.write(line + '\n')

        out.close()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pathogenseq/mvcf.py
# Compiled at: 2018-07-14 05:50:46
from __future__ import division
import sys, subprocess
from .files import *
from .fasta import *
from .mutation_db import *
from collections import defaultdict
import itertools, json
from tqdm import tqdm
from ete3 import Tree
from colour import Color
re_seq = re.compile('([0-9\\-]*)([A-Z\\*]+)')
re_I = re.compile('([A-Z\\*]+)')
number_re = re.compile('[0-9\\-]+')

def parse_mutation(x):
    tmp = x.split('>')
    aa_changed = True if len(tmp) > 1 else False
    re_obj = re_seq.search(tmp[0])
    change_num = re_obj.group(1)
    ref_aa = re_obj.group(2)
    alt_aa = re_seq.search(tmp[1]).group(2) if aa_changed else None
    return (change_num, ref_aa, alt_aa)


def get_missing_positions(bcf_file):
    cmd = "bcftools query -f '%%CHROM\\t%%POS\\n' %s" % bcf_file
    results = []
    for l in subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout:
        row = l.rstrip().split()
        results.append((row[0], row[1]))

    return results


v = True

class bcf:

    def __init__(self, filename, prefix=None, threads=4):
        self.samples = []
        self.filename = filename
        self.threads = threads
        if prefix == None:
            if filename[-4:] == '.bcf':
                self.prefix = filename[:-4]
            elif filename[-5:] == '.gbcf':
                self.prefix = filename[:-5]
            elif filename[-7:] == '.vcf.gz':
                self.prefix = filename[-7:] == '.vcf.gz'
            elif filename[-4:] == '.vcf':
                self.prefix = filename[-4:] == '.vcf'
            else:
                self.prefix = filename
        else:
            self.prefix = prefix
        self.prefix = self.prefix
        self.temp_file = '%s.temp' % self.prefix
        index_bcf(filename, self.threads)
        cmd = 'bcftools query -l %(filename)s > %(temp_file)s' % vars(self)
        run_cmd(cmd)
        for l in open(self.temp_file):
            self.samples.append(l.rstrip())

        os.remove(self.temp_file)
        self.vcf = '%s.vcf' % self.prefix
        return

    def del_pos2bed(self):
        self.del_bed = '%s.del_pos.bed' % self.prefix
        OUT = open(self.del_bed, 'w')
        cmd = "bcftools view --threads %(threads)s -Ou -v indels %(filename)s | bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t%%ALT\\n' | awk 'length($3)>1'" % vars(self)
        sys.stderr.write(cmd)
        j = 0
        for l in subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout:
            j += 1
            row = l.rstrip().split()
            start_pos = int(row[1]) + 1
            for i in range(start_pos, start_pos + len(row[2]) - 1):
                OUT.write('%s\t%s\t%s\n' % (row[0], i - 1, i))

        if j == 0:
            OUT.write('dummy\t1\t1\n')
        OUT.close()
        return self.del_bed

    def load_variants(self, chrom=None, pos=None):
        variants = defaultdict(lambda : defaultdict(lambda : defaultdict(dict)))
        raw_variants = defaultdict(lambda : defaultdict(lambda : defaultdict(dict)))
        if chrom and pos:
            cmd = "bcftools view --threads %(threads)s %s %s:%s | bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t%%ALT[\\t%%TGT:%%AD]\\n'  | sed 's/\\.\\/\\./N\\/N/g'" % (self.filename, chrom, pos)
        else:
            cmd = "bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t%%ALT[\\t%%TGT:%%AD]\\n' %s  | sed 's/\\.\\/\\./N\\/N/g'" % self.filename
        log(cmd)
        for l in tqdm(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = l.rstrip().split()
            alts = row[3].split(',')
            alleles = [row[2]] + alts
            for i in range(len(self.samples)):
                calls, ad = row[(i + 4)].split(':')
                call1, call2 = calls.split('/')
                if calls == 'N/N':
                    raw_variants[row[0]][row[1]][self.samples[i]]['N'] = 1.0
                    continue
                else:
                    if calls == '%s/%s' % (row[2], row[2]) and ad == '.':
                        raw_variants[row[0]][row[1]][self.samples[i]][row[2]] = 1.0
                        continue
                    ad = [ int(x) if x != '.' else 0 for x in ad.split(',') ]
                    sum_ad = sum(ad)
                    for j in range(1, len(alleles)):
                        if ad[j] == 0:
                            continue
                        raw_variants[row[0]][row[1]][self.samples[i]][alleles[j]] = ad[j] / sum_ad

        for tchrom in raw_variants:
            for tpos in raw_variants[tchrom]:
                variants[tchrom][int(tpos)] = raw_variants[tchrom][tpos]

        if chrom and pos and len(variants) == 0:
            log('Variant not found', True)
        if chrom and pos:
            return variants[chrom][int(pos)]
        else:
            return variants

    def load_variants_alt(self, chrom=None, pos=None):
        variants = defaultdict(lambda : defaultdict(dict))
        raw_variants = defaultdict(lambda : defaultdict(dict))
        if chrom and pos:
            cmd = "bcftools view --threads %(threads)s %s %s:%s | bcftools query -f '%%CHROM\\t%%POS[\\t%%IUPACGT]\\n'  | sed 's/\\.\\/\\./N/g'" % (self.filename, chrom, pos)
        else:
            cmd = "bcftools query -f '%%CHROM\\t%%POS[\\t%%IUPACGT]\\n' %s  | sed 's/\\.\\/\\./N/g'" % self.filename
        log(cmd)
        for l in tqdm(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = l.rstrip().split()
            for i in range(len(self.samples)):
                raw_variants[row[0]][row[1]][self.samples[i]] = row[(i + 2)]

        for chrom in raw_variants:
            for pos in raw_variants[chrom]:
                variants[chrom][int(pos)] = raw_variants[chrom][pos]

        if chrom and pos and len(variants) == 0:
            log('Variant not found', True)
        if chrom and pos:
            return variants[chrom][int(pos)]
        else:
            return variants

    def load_stats(self, convert=False, ref=None):
        add_arguments_to_self(self, locals())
        self.stats_file = '%s.stats.txt' % self.filename
        if convert:
            cmd = 'bcftools convert --gvcf2vcf --fasta-ref %(ref)s -Ou %(filename)s | bcftools stats -v -s - > %(stats_file)s' % vars(self)
        else:
            cmd = 'bcftools stats -v -s - %(filename)s > %(stats_file)s' % vars(self)
        run_cmd(cmd)
        results = defaultdict(lambda : defaultdict(dict))
        for l in open(self.stats_file):
            row = l.rstrip().split('\t')
            if l[0] == '#':
                continue
            if row[0] == 'SN':
                results['SN'][row[2][:-1]] = int(row[3])
            elif row[0] == 'AF':
                results['AF']['SNP'][float(row[2])] = int(row[3])
                results['AF']['INDEL'][float(row[2])] = int(row[6])
            elif row[0] == 'QUAL':
                results['QUAL']['SNP'][int(row[2])] = int(row[3])
                results['QUAL']['INDEL'][int(row[2])] = int(row[6])
            elif row[0] == 'IDD':
                results['IDD'][int(row[2])] = int(row[3])
            elif row[0] == 'ST':
                results['ST'][row[2]] = int(row[3])
            elif row[0] == 'DP':
                if row[2][0] == '>':
                    continue
                results['DP'][int(row[2])] = int(row[3])
            elif row[0] == 'PSC':
                results['PSC'][row[2]]['nRefHom'] = int(row[3])
                results['PSC'][row[2]]['nNonRefHom'] = int(row[4])
                results['PSC'][row[2]]['nHets'] = int(row[5])

        return results

    def plot_stats(self, outfile):
        stats = self.load_stats()
        output_file(outfile)
        sn = figure(title='Summary stats', x_range=stats['SN'].keys(), toolbar_location=None, tools='')
        sn.vbar(x=stats['SN'].keys(), top=stats['SN'].values(), width=0.9)
        show(sn)
        return

    def split_on_metadata(self, meta_file):
        meta = defaultdict(list)
        for l in open(meta_file):
            row = l.rstrip().split()
            meta[row[1]].append(row[0])

        for m in meta:
            self.tmp_file = '%s.tmp.txt' % self.prefix
            open(self.tmp_file, 'w').write(('\n').join(meta[m]))
            self.tmp_bcf = '%s.%s.bcf' % (self.prefix, m)
            cmd = 'bcftools view --threads %(threads)s -S %(tmp_file)s %(bcf)s -Ob -o %(tmp_bcf)s' % vars(self)
            run_cmd(cmd)

    def annotate(self, ref_file, gff_file):
        self.ref_file = ref_file
        self.gff_file = gff_file
        self.ann_file = '%s.ann.bcf' % self.prefix
        cmd = 'bcftools csq -p m -f %(ref_file)s -g %(gff_file)s %(bcf)s -o %(ann_file)s' % vars(self)
        run_cmd(cmd, verbose=v)

    def extract_matrix(self, matrix_file=None, fmt='old'):
        self.matrix_file = matrix_file if matrix_file == True else self.prefix + '.mat'
        if fmt == 'new':
            O = open(self.matrix_file, 'w').write('chr\tpos\tref\tinfo\ttype\t%s\n' % ('\t').join(self.samples))
            cmd = "bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t.\\t.[\\t%%IUPACGT]\\n' %(filename)s  | sed 's/\\.\\/\\./N/g' >> %(matrix_file)s" % vars(self)
        elif fmt == 'old':
            O = open(self.matrix_file, 'w').write('chr\tpos\tref\t%s\n' % ('\t').join(self.samples))
            cmd = "bcftools query -f '%%CHROM\\t%%POS\\t%%REF[\\t%%IUPACGT]\\n' %(filename)s  | sed 's/\\.\\/\\./N/g' >> %(matrix_file)s" % vars(self)
        else:
            log('Choose valid format [old,new]...Exiting!', ext=True)
        run_cmd(cmd, verbose=v)

    def vcf_to_fasta_alt(self, outfile, ref_file, threads=4, chunk_size=50000, bed_file=None):
        self.ref_file = ref_file
        self.chunk_size = chunk_size
        self.cmd_split_chr = 'splitchr.py %(ref_file)s %(chunk_size)s --bed %(bed_file)s --reformat' % vars(self) if bed_file else 'splitchr.py %(ref_file)s %(chunk_size)s --reformat' % vars(self)
        self.tmp_file = '%s.tmp.txt' % self.prefix
        self.threads = threads
        cmd = '%(cmd_split_chr)s | parallel --col-sep \'\\t\' -j %(threads)s "bcftools view --threads %(threads)s %(filename)s -r {1} -Ou | bcftools query -f \'%%POS[\\t%%IUPACGT]\\n\' |  datamash transpose > %(prefix)s.{2}.tmp.txt"' % vars(self)
        run_cmd(cmd)
        cmd = 'paste `%(cmd_split_chr)s | awk \'{print "%(prefix)s."$2".tmp.txt"}\'` > %(tmp_file)s' % vars(self)
        run_cmd(cmd)
        cmd = 'rm `%(cmd_split_chr)s | awk \'{print "%(prefix)s."$2".tmp.txt"}\'`' % vars(self)
        run_cmd(cmd)
        O = open(outfile, 'w')
        for i, l in enumerate(open(self.tmp_file)):
            row = l.rstrip().split()
            if i == 0:
                continue
            s = self.samples[(i - 1)]
            seq = ('').join(row).replace('./.', 'N')
            O.write('>%s\n%s\n' % (s, seq))

        O.close()

    def vcf_to_fasta(self, filename, threads=4):
        """Create a fasta file from the SNPs"""
        self.threads = threads
        self.tmp_file = '%s.tmp.txt' % self.prefix
        cmd = "bcftools query -f '%%POS[\\t%%IUPACGT]\\n' %(bcf)s |  datamash transpose > %(tmp_file)s" % vars(self)
        run_cmd(cmd)
        O = open(filename, 'w')
        for i, l in enumerate(open(self.tmp_file)):
            row = l.rstrip().split()
            if i == 0:
                continue
            s = self.samples[(i - 1)]
            seq = ('').join(row).replace('./.', 'N')
            O.write('>%s\n%s\n' % (s, seq))

        O.close()

    def bcf2vcf(self):
        if nofile(self.vcf):
            cmd = 'bcftools view --threads %(threads)s %(filename)s -Ov -o %(vcf)s' % vars(self)
            run_cmd(cmd)

    def get_venn_diagram_data(self, samples, outfile):
        samples = samples.split(',')
        if len(samples) > 4:
            log(samples)
            log("Can't handle more than 4 samples...Exiting!", True)
        if nofile(self.vcf):
            self.bcf2vcf()
        vcf_reader = vcf.Reader(open(self.vcf, 'r'))
        results = defaultdict(int)
        tot_snps = defaultdict(int)
        data = defaultdict(int)
        for record in vcf_reader:
            tmp = []
            for s in record.samples:
                if s.sample not in samples:
                    continue
                if s.gt_nums == '1/1':
                    tmp.append(s.sample)
                    tot_snps[s.sample] += 1

            for x in itertools.combinations(tmp, 2):
                tmp_str = ('_').join(sorted([ str(samples.index(d)) for d in x ]))
                data[('overlap_' + tmp_str)] += 1

            for x in itertools.combinations(tmp, 3):
                tmp_str = ('_').join(sorted([ str(samples.index(d)) for d in x ]))
                data[('overlap_' + tmp_str)] += 1

            for x in itertools.combinations(tmp, 4):
                tmp_str = ('_').join(sorted([ str(samples.index(d)) for d in x ]))
                data[('overlap_' + tmp_str)] += 1

        for i, si in enumerate(samples):
            if si not in self.samples:
                log("Can't find %s in samples...Exiting" % si, True)
            data['id_%s' % i] = si
            data['tot_snps_%s' % i] = tot_snps[si]

        data['outfile'] = outfile
        if len(samples) == 2:
            rscript = '\nlibrary(VennDiagram)\npdf("%(outfile)s")\ndraw.pairwise.venn(area1=%(tot_snps_0)s, area2=%(tot_snps_1)s, cross.area=%(overlap_0_1)s, category = c("%(id_0)s","%(id_1)s"),fill=rainbow(2))\ndev.off()\n' % data
        elif len(samples) == 3:
            rscript = '\nlibrary(VennDiagram)\npdf("%(outfile)s")\ndraw.triple.venn(area1=%(tot_snps_0)s, area2=%(tot_snps_1)s, area3=%(tot_snps_2)s, n12=%(overlap_0_1)s, n23=%(overlap_1_2)s, n13=%(overlap_0_2)s, n123=%(overlap_0_1_2)s, category = c("%(id_0)s","%(id_1)s","%(id_2)s"),fill=rainbow(3))\ndev.off()\n' % data
        elif len(samples) == 4:
            rscript = '\nlibrary(VennDiagram)\npdf("%(outfile)s")\ndraw.quad.venn(area1=%(tot_snps_0)s, area2=%(tot_snps_1)s, area3=%(tot_snps_2)s, area4=%(tot_snps_3)s,\nn12=%(overlap_0_1)s, n13=%(overlap_0_2)s, n14=%(overlap_0_3)s, n23=%(overlap_1_2)s, n24=%(overlap_1_3)s, n34=%(overlap_2_3)s,\nn123=%(overlap_0_1_2)s, n124=%(overlap_0_1_3)s, n134=%(overlap_0_2_3)s, n234=%(overlap_1_2_3)s,\nn1234=%(overlap_0_1_2_3)s,\ncategory = c("%(id_0)s","%(id_1)s","%(id_2)s","%(id_3)s"),fill=rainbow(4))\ndev.off()\n' % data
        temp_r_script = '%s.temp.R' % self.prefix
        open(temp_r_script, 'w').write(rscript)
        cmd = 'Rscript %s' % temp_r_script
        run_cmd(cmd)
        rm_files([temp_r_script])

    def merge_in_snps(self, bcf, outfile):
        self.new_bcf = bcf
        self.targets_file = '%(prefix)s.targets' % vars(self)
        self.tmp_file = '%(prefix)s.temp.bcf' % vars(self)
        self.tmp2_file = '%(prefix)s.temp2.bcf' % vars(self)
        self.outfile = outfile
        cmd = 'bcftools view --threads %(threads)s -Ou -v snps %(bcf)s | bcftools query -f \'%%CHROM\\t%%POS\\n\' | awk \'{print $1"\t"$2-1"\t"$2}\' > %(targets_file)s' % vars(self)
        run_cmd(cmd)
        cmd = 'bcftools view --threads %(threads)s -T %(targets_file)s %(new_bcf)s -Ob -o %(tmp_file)s' % vars(self)
        run_cmd(cmd)
        index_bcf(self.tmp_file, self.threads)
        cmd = 'bcftools view --threads %(threads)s -T %(targets_file)s %(bcf)s -Ob -o %(tmp2_file)s' % vars(self)
        run_cmd(cmd)
        index_bcf(self.tmp2_file, self.threads)
        cmd = "bcftools merge --threads %(threads)s -Ou  %(tmp2_file)s %(tmp_file)s | bcftools view --threads %(threads)s -i 'F_MISSING<0.5' -Ob -o %(outfile)s" % vars(self)
        run_cmd(cmd)

    def annotate_from_bed(self, bed_file, outfile=None, nested=False):
        temp_vcf = '%s.temp.vcf' % self.prefix
        self.vcf_from_bed(bed_file, temp_vcf)
        bed_dict = defaultdict(dict)
        for l in open(bed_file):
            row = l.rstrip().split()
            bed_dict[row[0]][int(row[1])] = (row[3], row[4])

        vcf_reader = vcf.Reader(open(temp_vcf))
        results = defaultdict(list)
        for record in tqdm(vcf_reader):
            for s in record.samples:
                if s.gt_bases == None:
                    continue
                nuc = s.gt_bases.split('/')[0]
                if nuc == bed_dict[record.CHROM][record.POS][0]:
                    results[s.sample].append(bed_dict[record.CHROM][record.POS][1])

        if outfile:
            O = open(outfile, 'w')
        for s in self.samples:
            if nested:
                switch = True
                tmp = sorted(list(set(results[s])))
                for i in range(len(tmp) - 1):
                    if tmp[i] not in tmp[(i + 1)]:
                        switch = False

            else:
                switch = False
            meta = tmp[(-1)] if switch else (';').join(sorted(list(set(results[s]))))
            if outfile:
                O.write('%s\t%s\n' % (s, meta))

        if outfile:
            O.close()
        return results

    def extract_compressed_json(self, outfile):
        self.bcf2vcf()
        vcf_reader = vcf.Reader(open(self.vcf))
        results = defaultdict(lambda : defaultdict(dict))
        for record in tqdm(vcf_reader):
            tmp = defaultdict(list)
            for s in record.samples:
                if s.gt_bases == None:
                    tmp['N'].append(self.samples.index(s.sample))
                elif s.gt_nums == '1/1':
                    tmp[s.gt_bases.split('/')[0]].append(self.samples.index(s.sample))

            results[record.CHROM][record.POS] = tmp

        json.dump({'variants': results, 'samples': self.samples}, open(outfile, 'w'))
        return

    def bed_subset(self, bed_file, out_file, vcf=False):
        temp_bed = '%s.temp.bed' % self.prefix
        cmd = 'awk \'{print $1"\\t"$2-1"\\t"$3}\' %s > %s' % (bed_file, temp_bed)
        run_cmd(cmd)
        if vcf:
            cmd = 'bcftools view --threads %(threads)s -R %s %s -o %s ' % (temp_bed, self.filename, out_file)
        else:
            cmd = 'bcftools view --threads %(threads)s -R %s %s -Ob -o %s ' % (temp_bed, self.filename, out_file)
        run_cmd(cmd)
        if not vcf:
            return bcf(out_file)

    def odds_ratio(self, bed_file, meta_file, ann_file):
        drugs, meta = load_tsv(meta_file)
        log(drugs)
        bed_dict = load_bed(bed_file, columns=[5, 6], key1=4, key2=5)
        subset_bcf_name = '%s.subset.bcf' % self.prefix
        subset_bcf = self.bed_subset(bed_file, subset_bcf_name)
        variants = subset_bcf.load_csq(ann_file)
        for gene in bed_dict:
            for drug_combo in bed_dict[gene]:
                for var in bed_dict[gene][drug_combo][1].split(';'):
                    for drug in bed_dict[gene][drug_combo][0].split(';'):
                        if drug not in drugs:
                            continue
                        tbl = [
                         [
                          0.5, 0.5], [0.5, 0.5]]
                        change_num, ref_aa, alt_aa = parse_mutation(var)
                        if gene not in variants:
                            continue
                        if change_num not in variants[gene]:
                            continue
                        try:
                            tbl[0][0] += len([ s for s in meta.keys() if variants[gene][change_num][s] == alt_aa and meta[s][drug] == '1' ])
                            tbl[1][0] += len([ s for s in meta.keys() if variants[gene][change_num][s] == alt_aa and meta[s][drug] == '0' ])
                            tbl[0][1] += len([ s for s in meta.keys() if variants[gene][change_num][s] == ref_aa and meta[s][drug] == '1' ])
                            tbl[1][1] += len([ s for s in meta.keys() if variants[gene][change_num][s] == ref_aa and meta[s][drug] == '0' ])
                        except:
                            pass

                        if tbl[0][0] + tbl[1][0] == 1:
                            continue
                        OR = tbl[0][0] / tbl[0][1] / (tbl[1][0] / tbl[1][1])
                        log('%s\t%s\t%s\t%s\t%s' % (var, gene, drug, OR, tbl))

    def load_csq_alt(self, ann_file=None, changes=False, use_genomic=True, use_gene=True):
        ann = defaultdict(dict)
        if ann_file:
            for l in tqdm(open(ann_file)):
                row = l.rstrip().split()
                ann[row[0]][int(row[1])] = (row[2], row[3])

        nuc_variants = self.load_variants()
        prot_dict = defaultdict(lambda : defaultdict(dict))
        prot_variants = defaultdict(lambda : defaultdict(dict))
        change_num2pos = defaultdict(lambda : defaultdict(set))
        ref_codons = defaultdict(lambda : defaultdict(dict))
        variants = {s:[] for s in self.samples}
        cmd = "bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t%%ALT[\\t%%SAMPLE\\t%%TBCSQ\\t%%TGT\\t%%AD]\\n' %s" % self.filename
        sys.stderr.write('%s\n' % cmd)
        for line in tqdm(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = line.rstrip().split()
            chrom = row[0]
            pos = int(row[1])
            ref = row[2]
            alts = row[3].split(',')
            alleles = [ref] + alts
            if chrom in ann and pos in ann[chrom]:
                ann_pos = int(ann[chrom][pos][1])
                ann_gene = ann[chrom][pos][0]
            else:
                ann_pos = None
            if len(row) == 4:
                for alt in alts:
                    if chrom in ann and pos in ann[chrom]:
                        cng = '%s%s>%s' % (ann_pos, ref, alt)
                        for sample in self.samples:
                            if sample in nuc_variants[chrom][pos] and alt in nuc_variants[chrom][pos][sample]:
                                variants[sample].append({'sample': sample, 'gene_id': ann_gene, 'chr': chrom, 'genome_pos': pos, 'type': 'non_coding', 'change': cng, 'freq': nuc_variants[chrom][pos][sample][alt]})

                continue
            for i in range(4, len(row) - 4, 5):
                sample = row[i]
                info = row[(i + 1)].split('|') if row[(i + 1)] != '.' else row[(i + 2)].split('|')
                call1, call2 = row[(i + 3)].split('/')
                ad = [ int(x) if x != '.' else 0 for x in row[(i + 4)].split(',') ]
                adr = {alleles[i]:d / sum(ad) for i, d in enumerate(ad)}
                if row[(i + 1)][0] == '@':
                    continue
                if info[(-1)] == 'pseudogene':
                    continue
                gene = info[1]
                if info[0] == 'intron':
                    continue
                if info[0] == 'coding_sequence':
                    cng = '%s%s>%s' % (ann_pos, call1, call2)
                    variants[sample].append({'sample': sample, 'gene_id': ann_gene, 'chr': chrom, 'genome_pos': pos, 'type': 'non_coding', 'change': cng, 'freq': adr[call2]})
                elif info[0] == 'frameshift&start_lost' or info[0] == 'missense&inframe_altering' or info[0] == 'missense' or info[0] == '*missense' or info[0] == 'start_lost' or info[0] == '*start_lost' or info[0] == '*stop_lost' or info[0] == 'stop_lost' or info[0] == 'stop_gained' or info[0] == '*stop_gained':
                    variants[sample].append({'sample': sample, 'gene_id': gene, 'chr': chrom, 'genome_pos': pos, 'type': info[0], 'change': info[5], 'freq': adr[call2]})
                elif info[0] == 'synonymous&stop_retained' or info[0] == 'stop_lost&frameshift' or info[0] == 'inframe_insertion' or info[0] == '*inframe_insertion' or info[0] == 'inframe_deletion' or info[0] == '*inframe_deletion' or info[0] == 'frameshift' or info[0] == '*frameshift' or info[0] == 'synonymous' or info[0] == '*synonymous' or info[0] == 'stop_retained':
                    change_num, ref_nuc, alt_nuc = parse_mutation(info[6])
                    change = '%s%s>%s' % (ann_pos, ref_nuc, alt_nuc) if ann_pos else '%s%s>%s' % (pos, ref_nuc, alt_nuc)
                    variants[sample].append({'sample': sample, 'gene_id': gene, 'chr': chrom, 'genome_pos': pos, 'type': info[0], 'change': change, 'freq': adr[call2]})
                elif info[0] == 'non_coding':
                    if chrom in ann and pos in ann[chrom]:
                        gene = ann[chrom][pos][0]
                        gene_pos = ann[chrom][pos][1]
                        change = '%s%s>%s' % (gene_pos, ref, call2)
                        variants[sample].append({'sample': sample, 'gene_id': gene, 'chr': chrom, 'genome_pos': pos, 'type': info[0], 'change': change, 'freq': adr[call2]})
                else:
                    sys.stderr.write(line)
                    sys.stderr.write(info[0] + '\n')
                    sys.stderr.write('Unknown variant type...Exiting!\n')
                    quit(1)

        return variants

    def load_csq(self, ann_file=None, changes=False, use_genomic=True, use_gene=True):
        ann = defaultdict(dict)
        if ann_file:
            for l in tqdm(open(ann_file)):
                row = l.rstrip().split()
                ann[row[0]][int(row[1])] = (row[2], row[3])

        nuc_variants = self.load_variants_alt()
        prot_dict = defaultdict(lambda : defaultdict(dict))
        prot_variants = defaultdict(lambda : defaultdict(dict))
        change_num2pos = defaultdict(lambda : defaultdict(set))
        ref_codons = defaultdict(lambda : defaultdict(dict))
        cmd = "bcftools query -f '%%CHROM\\t%%POS\\t%%REF\\t%%ALT[\\t%%SAMPLE\\t%%TBCSQ]\\n' %s" % self.filename
        sys.stderr.write('%s\n' % cmd)
        for line in tqdm(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = line.rstrip().split()
            chrom = row[0]
            pos = int(row[1])
            ref = row[2]
            alt = row[3]
            if chrom in ann and pos in ann[chrom]:
                ann_pos = int(ann[chrom][pos][1])
                ann_gene = ann[chrom][pos][0]
            else:
                ann_pos = None
            if len(row) == 4:
                if chrom in ann and pos in ann[chrom]:
                    for sample in self.samples:
                        prot_variants[ann_gene][ann_pos][sample] = '%s%s>%s' % (ann_pos, ref, alt)
                        prot_dict[ann_gene][ann_pos][sample] = nuc_variants[chrom][pos][sample]
                        ref_codons[ann_gene][ann_pos] = ref

                continue
            for i in range(4, len(row) - 2, 3):
                sample = row[i]
                info = row[(i + 1)].split('|') if row[(i + 1)] != '.' else row[(i + 2)].split('|')
                if row[(i + 1)][0] == '@':
                    continue
                if info[(-1)] == 'pseudogene':
                    continue
                gene = info[1]
                if info[0] == 'intron':
                    continue
                if info[0] == 'frameshift&start_lost' or info[0] == 'missense&inframe_altering' or info[0] == 'missense' or info[0] == '*missense' or info[0] == 'start_lost' or info[0] == '*start_lost' or info[0] == '*stop_lost' or info[0] == 'stop_lost' or info[0] == 'stop_gained' or info[0] == '*stop_gained':
                    change_num, ref_aa, alt_aa = parse_mutation(info[5])
                    change_num2pos[gene][change_num].add((chrom, pos))
                    ref_codons[gene][change_num] = ref_aa
                    prot_variants[gene][change_num][row[i]] = info[5]
                    prot_dict[gene][change_num][sample] = alt_aa
                elif info[0] == 'stop_lost&frameshift' or info[0] == 'inframe_insertion' or info[0] == '*inframe_insertion' or info[0] == 'inframe_deletion' or info[0] == '*inframe_deletion' or info[0] == 'frameshift' or info[0] == '*frameshift' or info[0] == 'synonymous' or info[0] == '*synonymous' or info[0] == 'stop_retained':
                    change_num, ref_nuc, alt_nuc = parse_mutation(info[6])
                    change_num2pos[gene][change_num].add((chrom, pos))
                    ref_codons[gene][change_num] = ref_nuc
                    change = '%s%s>%s' % (ann_pos, ref_nuc, alt_nuc) if ann_pos else None
                    if use_genomic and use_gene and change:
                        prot_variants[gene][change_num][row[i]] = change
                    elif use_genomic:
                        prot_variants[gene][change_num][row[i]] = info[6]
                    elif use_gene and change:
                        prot_variants[gene][change_num][row[i]] = change
                    else:
                        prot_variants[gene][change_num][row[i]] = info[5]
                    prot_dict[gene][change_num][sample] = alt_nuc
                elif info[0] == 'non_coding':
                    if chrom in ann and pos in ann[chrom]:
                        gene = ann[chrom][pos][0]
                        gene_pos = ann[chrom][pos][1]
                        prot_variants[gene][gene_pos][sample] = '%s%s>%s' % (gene_pos, ref, alt)
                        prot_dict[gene][gene_pos][sample] = alt
                        ref_codons[gene][gene_pos] = ref
                else:
                    sys.stderr.write(line)
                    sys.stderr.write('Unknown variant type...Exiting!\n')
                    quit(1)

        for gene in prot_variants:
            for change_num in prot_variants[gene]:
                for s in set(self.samples) - set(prot_variants[gene][change_num].keys()):
                    if 'N' in [ nuc_variants[chrom][pos][s] for chrom, pos in change_num2pos[gene][change_num] ]:
                        prot_variants[gene][change_num][s] = '?'
                        prot_dict[gene][change_num][s] = '?'
                    else:
                        prot_dict[gene][change_num][s] = ref_codons[gene][change_num]

        for locus in prot_variants:
            prot_variants[locus] = prot_variants[locus].values()

        if changes:
            return prot_variants
        else:
            return prot_dict

    def ancestral_reconstruct(self):
        cmd = "bcftools query -f '%%CHROM\\t%%POS\n' %(bcf)s" % vars(self)
        variants = {}
        for i, l in enumerate(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = l.rstrip().split()
            variants[i] = (row[0], row[1])

        self.reduced_bcf = '%(prefix)s.reduced.bcf' % vars(self)
        cmd = 'bcftools view --threads %(threads)s -c 3 %(bcf)s -Ob -o %(reduced_bcf)s' % vars(self)
        run_cmd(cmd)
        reduced = {}
        cmd = "bcftools query -f '%%CHROM\\t%%POS\n' %(reduced_bcf)s" % vars(self)
        for i, l in enumerate(subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout):
            row = l.rstrip().split()
            reduced[i] = (row[0], row[1])

        new_bcf = bcf(self.reduced_bcf)
        self.fasta_file = '%(prefix)s.reduced.snps.fa' % vars(self)
        new_bcf.vcf_to_fasta(self.fasta_file)
        self.tree_file = '%s.newick.txt' % self.prefix
        self.reconstructed_fasta = '%s.reconstructed.fasta' % self.prefix
        cmd = 'fastml -s %(fasta_file)s -x %(tree_file)s -j %(reconstructed_fasta)s -qf -mn' % vars(self)
        fdict = fasta(self.reconstructed_fasta).fa_dict
        t = Tree(self.tree_file, format=1)
        for i in range(len(fdict.values()[0])):
            num_transitions = 0
            for node in t.traverse('postorder'):
                if len(node.get_ancestors()) == 0:
                    continue
                anc = node.get_ancestors()[0]
                nuc1 = fdict[anc.name][i]
                nuc2 = fdict[node.name][i]
                if nuc1 != '?' and nuc2 != '?' and nuc1 != 'N' and nuc2 != 'N':
                    if nuc1 != nuc2:
                        num_transitions += 1
                        log('%s>%s' % (nuc1, nuc2))

            if num_transitions > 1:
                log('Site: %s' % i)
                log('Number of transitions: %s' % num_transitions)
                log('Location: %s' % reduced[i][1])
                for node in t.traverse('postorder'):
                    nuc = fdict[node.name][i]
                    node.add_features(nuc=nuc)

                log(t.get_ascii(attributes=['name', 'nuc'], show_internal=True))

    def itol_from_bcf(self, mutation_file, amino_acid=False):
        if amino_acid:
            all_csq = self.load_csq()
        for l in open(mutation_file):
            mutation = l.rstrip()
            if amino_acid:
                gene, variant = mutation.split('__')
                change_num, ref_aa, alt_aa = parse_mutation(variant)
                if gene in all_csq and change_num in all_csq[gene]:
                    variant_dict = all_csq[gene][change_num]
                else:
                    continue
            else:
                chrom, pos = mutation.split('__')
                variant_dict = self.load_variants_alt(chrom, pos)
            num_var = len(set(variant_dict.values()))
            cols = [ x.get_hex() for x in list(Color('red').range_to(Color('blue'), num_var)) ]
            col_dict = {d:cols[i] for i, d in enumerate(set(variant_dict.values()))}
            shape_line = ('\t').join([ '1' for x in range(num_var) ])
            col_line = ('\t').join(col_dict.values())
            lab_line = ('\t').join(col_dict.keys())
            outfile = '%s.itol.txt' % mutation
            OUT = open(outfile, 'w')
            OUT.write('DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\t%s\nCOLOR\t#ff0000\n\nLEGEND_TITLE\tAmino acid\nLEGEND_SHAPES\t%s\nLEGEND_COLORS\t%s\nLEGEND_LABELS\t%s\n\nDATA\n' % (mutation, shape_line, col_line, lab_line))
            for s in self.samples:
                if amino_acid:
                    if variant_dict[s] == alt_aa:
                        OUT.write('%s\t%s\n' % (s, col_dict[variant_dict[s]]))
                else:
                    OUT.write('%s\t%s\n' % (s, col_dict[variant_dict[s]]))

            OUT.close()

    def compress_variants(self):
        cmd = "bcftools query -f '%%CHROM\\t%%POS[\\t%%GT]\\n' %(filename)s" % vars(self)
        results = defaultdict(list)
        for l in subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout:
            row = l.rstrip().split()
            results[tuple(row[2:])].append([row[0], row[1]])

        final_results = {}
        for i, key in enumerate(results):
            var_name = 'variant_%s' % i
            O = open(var_name + '.pheno', 'w')
            for j, s in enumerate(self.samples):
                tmp = '-9'
                if key[j] == '0/0':
                    tmp = '1'
                elif key[j] == '1/1':
                    tmp = '2'
                O.write('0\t%s\t%s\n' % (s, tmp))

            final_results[var_name] = results[key]
            O.close()

        json.dump(final_results, open('%s.compressed_variants.json' % self.prefix, 'w'))
        return final_results

    def reheader--- This code section failed: ---

 L. 730         0  BUILD_MAP_0           0  None
                3  STORE_FAST            2  'idx'

 L. 731         6  SETUP_LOOP          109  'to 118'
                9  LOAD_GLOBAL           0  'open'
               12  LOAD_FAST             1  'index_file'
               15  CALL_FUNCTION_1       1  None
               18  GET_ITER         
               19  FOR_ITER             95  'to 117'
               22  STORE_FAST            3  'l'

 L. 732        25  LOAD_FAST             3  'l'
               28  LOAD_ATTR             1  'rstrip'
               31  CALL_FUNCTION_0       0  None
               34  LOAD_ATTR             2  'split'
               37  CALL_FUNCTION_0       0  None
               40  STORE_FAST            4  'row'

 L. 733        43  LOAD_FAST             4  'row'
               46  LOAD_CONST               0
               49  BINARY_SUBSCR    
               50  LOAD_FAST             2  'idx'
               53  COMPARE_OP            6  in
               56  POP_JUMP_IF_FALSE    96  'to 96'
               59  LOAD_GLOBAL           3  'sys'
               62  LOAD_ATTR             4  'stderr'
               65  LOAD_ATTR             5  'write'
               68  LOAD_CONST               'Duplicate values in index file (%s)...Exiting!\n'
               71  LOAD_FAST             4  'row'
               74  LOAD_CONST               0
               77  BINARY_SUBSCR    
               78  BINARY_MODULO    
               79  CALL_FUNCTION_1       1  None
               82  POP_TOP          
               83  LOAD_GLOBAL           6  'quit'
               86  LOAD_CONST               1
               89  CALL_FUNCTION_1       1  None
               92  POP_TOP          
               93  JUMP_FORWARD          0  'to 96'
             96_0  COME_FROM            93  '93'

 L. 734        96  LOAD_FAST             4  'row'
               99  LOAD_CONST               1
              102  BINARY_SUBSCR    
              103  LOAD_FAST             2  'idx'
              106  LOAD_FAST             4  'row'
              109  LOAD_CONST               0
              112  BINARY_SUBSCR    
              113  STORE_SUBSCR     
              114  JUMP_BACK            19  'to 19'
              117  POP_BLOCK        
            118_0  COME_FROM             6  '6'

 L. 736       118  LOAD_CONST               '%(prefix)s.reheader.bcf'
              121  LOAD_GLOBAL           7  'vars'
              124  LOAD_FAST             0  'self'
              127  CALL_FUNCTION_1       1  None
              130  BINARY_MODULO    
              131  STORE_FAST            5  'new_bcf_file'

 L. 737       134  LOAD_CONST               '%(prefix)s.tmp.header'
              137  LOAD_GLOBAL           7  'vars'
              140  LOAD_FAST             0  'self'
              143  CALL_FUNCTION_1       1  None
              146  BINARY_MODULO    
              147  STORE_FAST            6  'tmp_header'

 L. 738       150  LOAD_GLOBAL           0  'open'
              153  LOAD_FAST             6  'tmp_header'
              156  LOAD_CONST               'w'
              159  CALL_FUNCTION_2       2  None
              162  STORE_FAST            7  'OUT'

 L. 739       165  SETUP_LOOP          220  'to 388'
              168  LOAD_GLOBAL           8  'subprocess'
              171  LOAD_ATTR             9  'Popen'
              174  LOAD_CONST               'bcftools view --threads %(threads)s -h %(bcf)s'
              177  LOAD_GLOBAL           7  'vars'
              180  LOAD_FAST             0  'self'
              183  CALL_FUNCTION_1       1  None
              186  BINARY_MODULO    
              187  LOAD_CONST               'shell'
              190  LOAD_GLOBAL          10  'True'
              193  LOAD_CONST               'stdout'
              196  LOAD_GLOBAL           8  'subprocess'
              199  LOAD_ATTR            11  'PIPE'
              202  CALL_FUNCTION_513   513  None
              205  LOAD_ATTR            12  'stdout'
              208  GET_ITER         
              209  FOR_ITER            175  'to 387'
              212  STORE_FAST            3  'l'

 L. 740       215  LOAD_FAST             3  'l'
              218  LOAD_CONST               2
              221  SLICE+2          
              222  LOAD_CONST               '##'
              225  COMPARE_OP            2  ==
              228  POP_JUMP_IF_FALSE   250  'to 250'
              231  LOAD_FAST             7  'OUT'
              234  LOAD_ATTR             5  'write'
              237  LOAD_FAST             3  'l'
              240  CALL_FUNCTION_1       1  None
              243  POP_TOP          
              244  JUMP_BACK           209  'to 209'
              247  JUMP_FORWARD          0  'to 250'
            250_0  COME_FROM           247  '247'

 L. 741       250  LOAD_FAST             3  'l'
              253  LOAD_ATTR             1  'rstrip'
              256  CALL_FUNCTION_0       0  None
              259  LOAD_ATTR             2  'split'
              262  CALL_FUNCTION_0       0  None
              265  STORE_FAST            4  'row'

 L. 742       268  SETUP_LOOP           87  'to 358'
              271  LOAD_GLOBAL          13  'range'
              274  LOAD_CONST               9
              277  LOAD_GLOBAL          14  'len'
              280  LOAD_FAST             4  'row'
              283  CALL_FUNCTION_1       1  None
              286  CALL_FUNCTION_2       2  None
              289  GET_ITER         
              290  FOR_ITER             64  'to 357'
              293  STORE_FAST            8  'i'

 L. 743       296  LOAD_FAST             4  'row'
              299  LOAD_FAST             8  'i'
              302  BINARY_SUBSCR    
              303  LOAD_FAST             2  'idx'
              306  COMPARE_OP            7  not-in
              309  POP_JUMP_IF_FALSE   336  'to 336'
              312  LOAD_GLOBAL          15  'log'
              315  LOAD_CONST               '%s not found in index file...Exiting!'
              318  LOAD_FAST             4  'row'
              321  LOAD_FAST             8  'i'
              324  BINARY_SUBSCR    
              325  BINARY_MODULO    
              326  LOAD_GLOBAL          10  'True'
              329  CALL_FUNCTION_2       2  None
              332  POP_TOP          
              333  JUMP_FORWARD          0  'to 336'
            336_0  COME_FROM           333  '333'

 L. 744       336  LOAD_FAST             2  'idx'
              339  LOAD_FAST             4  'row'
              342  LOAD_FAST             8  'i'
              345  BINARY_SUBSCR    
              346  BINARY_SUBSCR    
              347  LOAD_FAST             4  'row'
              350  LOAD_FAST             8  'i'
              353  STORE_SUBSCR     
              354  JUMP_BACK           290  'to 290'
              357  POP_BLOCK        
            358_0  COME_FROM           268  '268'

 L. 745       358  LOAD_FAST             7  'OUT'
              361  LOAD_ATTR             5  'write'
              364  LOAD_CONST               '%s\n'
              367  LOAD_CONST               '\t'
              370  LOAD_ATTR            16  'join'
              373  LOAD_FAST             4  'row'
              376  CALL_FUNCTION_1       1  None
              379  BINARY_MODULO    
              380  CALL_FUNCTION_1       1  None
              383  POP_TOP          
              384  JUMP_BACK           209  'to 209'
              387  POP_BLOCK        
            388_0  COME_FROM           165  '165'

 L. 746       388  LOAD_FAST             7  'OUT'
              391  LOAD_ATTR            17  'close'
              394  CALL_FUNCTION_0       0  None
              397  POP_TOP          

 L. 747       398  LOAD_CONST               'bcftools reheader -h %s %s > %s'
              401  LOAD_FAST             6  'tmp_header'
              404  LOAD_FAST             0  'self'
              407  LOAD_ATTR            18  'bcf'
              410  LOAD_FAST             5  'new_bcf_file'
              413  BUILD_TUPLE_3         3 
              416  BINARY_MODULO    
              417  STORE_FAST            9  'cmd'

 L. 748       420  LOAD_GLOBAL          19  'run_cmd'
              423  LOAD_FAST             9  'cmd'
              426  CALL_FUNCTION_1       1  None
              429  POP_TOP          

 L. 749       430  LOAD_GLOBAL          20  'rm_files'
              433  LOAD_FAST             6  'tmp_header'
              436  BUILD_LIST_1          1 
              439  CALL_FUNCTION_1       1  None
              442  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 247

    def filt_variants(self, outfile, bed_include=None, bed_exclude=None, threads=4, fmiss=0.1):
        add_arguments_to_self(self, locals())
        self.bed_include = 'bcftools view --threads %(threads)s -T %s -Ou |' % bed_include if bed_include != None else ''
        self.bed_exclude = 'bcftools view --threads %(threads)s -T ^%s -Ou |' % bed_exclude if bed_exclude != None else ''
        cmd = "bcftools view --threads %(threads)s %(filename)s -Ou | %(bed_include)s %(bed_exclude)s bcftools view --threads %(threads)s -i 'AC>=0 && F_MISSING<%(fmiss)s' -o %(outfile)s -O b" % vars(self)
        run_cmd(cmd)
        return bcf(self.outfile, threads=self.threads)

    def extract_variants(self, outfile, min_dp=10, bed_include=None, bed_exclude=None, threads=4):
        add_arguments_to_self(self, locals())
        self.bed_include = 'bcftools view --threads %(threads)s -T %s -Ou |' % bed_include if bed_include != None else ''
        self.bed_exclude = 'bcftools view --threads %(threads)s -T ^%s -Ou |' % bed_exclude if bed_exclude != None else ''
        cmd = "bcftools +setGT %(filename)s -Ou -- -t q -i 'FMT/DP<%(min_dp)s' -n . | %(bed_include)s %(bed_exclude)s bcftools view --threads %(threads)s -i 'AC>=0' -o %(outfile)s -O b" % vars(self)
        run_cmd(cmd)
        return bcf(self.outfile, threads=self.threads)

    def filt_non_uniq(self, mappability_file, outfile):
        """Filter out non unique positions"""
        add_arguments_to_self(self, locals())
        non_uniq = []
        self.non_uniq_bed = '%s.genome.non_uniq.bed' % self.prefix
        O = open(self.non_uniq_bed, 'w')
        for l in open(self.mappability_file):
            arr = l.rstrip().split()
            if float(arr[3]) < 1:
                O.write(l)

        O.close()
        cmd = 'bcftools view --threads %(threads)s -T ^%(non_uniq_bed)s %(filename)s -O b -o %(outfile)s' % vars(self)
        run_cmd(cmd)
        return bcf(self.outfile, threads=self.threads)

    def sample_filt(self, outfile, miss_cut=0.15, mix_cut=0.15, keep_samples=None):
        """Filter out low quality samples"""
        add_arguments_to_self(self, locals())
        self.hq_sample_file = '%s.HQ.samples.txt' % self.prefix
        self.lq_sample_file = '%s.LQ.samples.txt' % self.prefix
        self.qual_file = '%s.sample_quals.txt' % self.prefix
        if keep_samples and filecheck(keep_samples):
            self.keep_samples = [ x.rstrip() for x in open(keep_samples).readlines() ]
        else:
            self.keep_samples = []
        num_calls = int(subprocess.Popen('bcftools view --threads %(threads)s %(filename)s -H | wc -l' % vars(self), shell=True, stdout=subprocess.PIPE).communicate()[0].rstrip())
        miss = {}
        mix = {}
        self.lq_samples = []
        self.hq_samples = []
        HQ = open(self.hq_sample_file, 'w')
        LQ = open(self.lq_sample_file, 'w')
        QF = open(self.qual_file, 'w')
        QF.write('sample\tmix\tmiss\n')
        self.bcftools_stats_file = '%s.bcftools_stats.txt' % self.prefix
        cmd = 'bcftools stats  %(filename)s -s - | grep ^PSC > %(bcftools_stats_file)s' % vars(self)
        run_cmd(cmd)
        for l in open(self.bcftools_stats_file):
            row = l.rstrip().split()
            s = row[2]
            miss[s] = (num_calls - sum([ int(row[i]) for i in [3, 4, 5] ])) / num_calls
            mix[s] = int(row[5]) / num_calls
            QF.write('%s\t%s\t%s\n' % (s, mix[s], miss[s]))
            if s in self.keep_samples:
                self.hq_samples.append(s)
                HQ.write('%s\n' % s)
            elif miss[s] > self.miss_cut or mix[s] > self.mix_cut:
                self.lq_samples.append(s)
                LQ.write('%s\n' % s)
            else:
                self.hq_samples.append(s)
                HQ.write('%s\n' % s)

        HQ.close()
        LQ.close()
        QF.close()
        cmd = 'bcftools view --threads %(threads)s -S %(hq_sample_file)s -a -c 1 -o %(outfile)s -O b %(filename)s' % vars(self)
        run_cmd(cmd)
        return bcf(self.outfile, threads=self.threads)

    def mask_mixed(self, outfile):
        """Create a BCF file with mixed called masked as missing"""
        add_arguments_to_self(self, locals())
        cmd = 'bcftools +setGT %(filename)s -Ou -- -t q -i \'GT="het"\' -n . | bcftools view --threads %(threads)s -Ob -o %(outfile)s' % vars(self)
        run_cmd(cmd)
        return bcf(self.outfile, threads=self.threads)

    def generate_consensus(self, ref):
        add_arguments_to_self(self, locals())
        for s in self.samples:
            self.tmp_sample = s
            cmd = 'bcftools view --threads %(threads)s -s %(tmp_sample)s  %(filename)s -Ou | bcftools filter -e \'GT="het"\' -S . -Ou | bcftools view --threads %(threads)s -i \'GT=="./."\' -Ou | bcftools query -f \'%%CHROM\\t%%POS\\n\'' % vars(self)
            self.tmp_file = '%(prefix)s.%(tmp_sample)s.missing.bed' % vars(self)
            TMP = open(self.tmp_file, 'w')
            for l in cmd_out(cmd):
                row = l.rstrip().split()
                TMP.write('%s\t%s\t%s\n' % (row[0], int(row[1]) - 1, row[1]))

            TMP.close()
            self.tmp_fa = '%(prefix)s.%(tmp_sample)s.tmp.fasta' % vars(self)
            cmd = 'bcftools consensus -f %(ref)s %(filename)s -o %(tmp_fa)s -m %(tmp_file)s -s %(tmp_sample)s' % vars(self)
            run_cmd(cmd)
            fa_dict = fasta(self.tmp_fa).fa_dict
            self.final_fa = '%(prefix)s.%(tmp_sample)s.fasta' % vars(self)
            FA = open(self.final_fa, 'w')
            for seq in fa_dict:
                log('Writing consensus for %s' % seq)
                FA.write('>%s_%s\n%s\n' % (self.tmp_sample, seq, fa_dict[seq]))

            FA.close()
            rm_files([self.tmp_file, self.tmp_fa])

    def distance(self, outfile):
        add_arguments_to_self(self, locals())
        matrix = [ [ 0 for x in self.samples ] for s in self.samples ]
        miss_matrix = [ [ 0 for x in self.samples ] for s in self.samples ]
        sample_idx = {s:self.samples.index(s) for s in self.samples}
        cmd = 'bcftools query -i\'GT!="ref"\' -f \'[\\t%%SAMPLE:%%GT]\\n\' %(filename)s' % vars(self)
        num_snps = 0
        for l in tqdm(cmd_out(cmd)):
            num_snps += 1
            alt_samples = defaultdict(set)
            miss_samples = set()
            row = l.strip().split()
            for x in row:
                s, c = x.split(':')
                if c == './.':
                    miss_samples.add(s)
                else:
                    alt_samples[c].add(s)

            for c in alt_samples:
                others = set(self.samples) - alt_samples[c] - miss_samples
                for s in alt_samples[c]:
                    idx = sample_idx[s]
                    for x in others:
                        matrix[idx][sample_idx[x]] += 1
                        matrix[sample_idx[x]][idx] += 1

            for si in miss_samples:
                for sj in set(self.samples) - miss_samples:
                    miss_matrix[sample_idx[si]][sample_idx[sj]] += 1
                    miss_matrix[sample_idx[sj]][sample_idx[si]] += 1

                for sj in miss_samples:
                    if si == sj:
                        continue
                    if sample_idx[si] > sample_idx[sj]:
                        miss_matrix[sample_idx[si]][sample_idx[sj]] += 1

        for i in range(len(self.samples)):
            for j in range(len(self.samples)):
                if j >= i:
                    continue
                scaler = num_snps / (num_snps - miss_matrix[i][j])
                matrix[i][j] = matrix[i][j] * scaler
                matrix[j][i] = matrix[i][j]

        OUT = open(outfile, 'w')
        OUT.write(('\t').join(self.samples) + '\n')
        OUT.write(('\n').join([ ('\t').join([ str(d) for d in matrix[j] ]) for j in range(len(self.samples)) ]))
        OUT.write('\n')
        OUT.close()
        return {'sample': self.samples, 'matrix': matrix}

    def extract_dosage(self, outfile):
        add_arguments_to_self(self, locals())
        cmd = "bcftools query %(filename)s -f '%%CHROM\\t%%POS\\t%%REF\\t.\\t.[\\t%%AD]\\n'" % vars(self)

        def process_ad(ad):
            if ad == '.':
                return '0.000'
            else:
                dp = [ int(x) if x != '.' else 0 for x in ad.split(',') ]
                if sum(dp) == 0:
                    return 'NA'
                if sum(dp) != 0:
                    return '%.3f' % (dp[0] / sum(dp))
                return '1.000'

        idx = range(5, 5 + len(self.samples))
        O = open(self.outfile, 'w')
        O.write('chr\tpos\tref\tinfo\ttype\t%s\n' % ('\t').join(self.samples))
        for l in tqdm(cmd_out(cmd)):
            row = l.rstrip().split()
            row[5:] = [ process_ad(x) for x in row[5:] ]
            O.write('%s\n' % ('\t').join(row))

        O.close()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /share/data3/lianlin/soft/bin/wes/module-develop/bin/wes.py
# Compiled at: 2019-05-22 09:26:44
import os, sys, subprocess

class Wes(object):
    trimmomatic = '/share/data1/local/bin/trimmomatic-0.38.jar'
    gatk = '/share/data1/src/gatk/gatk'
    seqtk = '/share/data1/src/bwa/bwakit/seqtk'
    alt = '/share/data1/genome/hs38DH.fa.alt'
    annovar = '/share/data1/src/annovar'
    bamdst = '/share/data3/lianlin/soft/bamdst/bamdst'
    dbsnp = '/share/data1/PublicProject/GATK_bundle/dbsnp150_chr.vcf.gz'
    indel = '/share/data1/PublicProject/GATK_bundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz'
    snp = '/share/data1/PublicProject/GATK_bundle/1000G_phase1.snps.high_confidence.hg38.vcf.gz'
    bed = '/share/data2/leon/exom_bed/S07084713_Regions.bed'
    interval = '/share/data2/leon/exom_bed/list.interval_list'
    reference = '/share/data1/genome/hs38DH.fa'

    def __init__(self, input, working_space, prefix):
        self.input = input
        self.working_space = working_space
        self.prefix = prefix
        self.group()

    def group(self):
        self.groups = {}
        with open(self.input, 'r') as (f):
            for i in f:
                line = i.strip().split()
                sample = line[4]
                self.groups[sample] = line

    def info_list_by_sample(self):
        for sample in self.groups:
            info_list = self.groups[sample]
            fq1 = info_list[0]
            fq2 = info_list[1]
            adapter = info_list[2]
            library = info_list[3]
            yield (fq1, fq2, adapter, library, sample)

    def trim_bwa_dedup_bqsr_haplotypecaller(self):
        for fq1, fq2, adapter, library, sample in self.info_list_by_sample():
            if adapter == 'Nextera':
                trim = ('java -jar {tool} PE -threads 30 -phred33 {fq1} {fq2} {library}.{sample}_r1.fq.gz {library}.{sample}_r1_unpaired.fq.gz {library}.{sample}_r2.fq.gz {library}.{sample}_r2_unpaired.fq.gz ILLUMINACLIP:{trimmomatic_dir}/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 ;').format(tool=self.trimmomatic, trimmomatic_dir=os.path.dirname(self.trimmomatic), fq1=fq1, fq2=fq2, library=library, sample=sample)
            elif adapter == 'Truseq':
                trim = ('java -jar {tool} PE -threads 30 -phred33 {fq1} {fq2} {library}.{sample}_r1.fq.gz {library}.{sample}_r1_unpaired.fq.gz {library}.{sample}_r2.fq.gz {library}.{sample}_r2_unpaired.fq.gz ILLUMINACLIP:{trimmomatic_dir}/adapters/NexteraPE-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 ;').format(tool=self.trimmomatic, trimmomatic_dir=os.path.dirname(self.trimmomatic), fq1=fq1, fq2=fq2, library=library, sample=sample)
            else:
                print ('{} :\nadaptor error, Nextera or Truseq accept,not nextera or truseq or others').format(adapter)
                sys.exit()
            bwa = ('{tool} mergepe {library}.{sample}_r1.fq.gz {library}.{sample}_r2.fq.gz |bwa mem -p -t 30 -R"@RG\\tID:{library}\\tLB:{library}\\tSM:{sample}\\tPU:flowcell\\tPL:Illumina" {reference} - 2>{library}.log.bwamem |k8 {bwa_dir}/bwa-postalt.js -p {library}.hla {alt} | samtools sort -@ 2 -m8g - -o {library}.{sample}.aln.bam ;').format(tool=self.seqtk, reference=self.reference, bwa_dir=os.path.dirname(self.seqtk), alt=self.alt, library=library, sample=sample)
            MarkDuplicates = ('{tool} MarkDuplicates -I {library}.{sample}.aln.bam  -O {sample}.dedup.bam -M {sample}.dedup.log -PG null --TMP_DIR ~/tmp/{sample} ;').format(tool=self.gatk, library=library, sample=sample)
            index = ('samtools index -@ 30 {sample}.dedup.bam ;').format(sample=sample)
            CollectHsMetrics = ('{tool} CollectHsMetrics -I {sample}.dedup.bam -O {sample}_hs_metrics.txt -BI {interval} -TI {interval} -R {reference} &').format(tool=self.gatk, sample=sample, interval=self.interval, reference=self.reference)
            if os.path.exists(sample):
                subprocess.call(('rm -rf {}').format(sample), shell=True)
            os.mkdir(sample)
            coverage = ('{tool} -p {bed} -o {sample} {sample}.dedup.bam &').format(tool=self.bamdst, bed=self.bed, sample=sample)
            BaseRecalibrator = ('{tool} BaseRecalibrator -I {sample}.dedup.bam -O {sample}.recal.table --known-sites {snp} --known-sites {indel} -L {bed} -ip {ip} -R {reference} ;').format(tool=self.gatk, sample=sample, bed=self.bed, ip=0, snp=self.snp, indel=self.indel, reference=self.reference)
            ApplyBQSR = ('{tool} ApplyBQSR -I {sample}.dedup.bam -O {sample}.dedup.bqsr.bam -bqsr {sample}.recal.table -L {bed} -ip {ip} -R {reference} ;').format(tool=self.gatk, sample=sample, bed=self.bed, ip=0, reference=self.reference)
            HaplotypeCaller = ('{tool} HaplotypeCaller -I {sample}.dedup.bqsr.bam -O {sample}.HC.g.vcf.gz --emit-ref-confidence GVCF --dbsnp {dbsnp} -L {bed} -ip {ip} -R {reference} ;').format(tool=self.gatk, sample=sample, bed=self.bed, ip=0, dbsnp=self.dbsnp, reference=self.reference)
            sge = ('#$ -N {sample}\n#$ -pe smp 32\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n').format(sample=sample, working_space=self.working_space)
            part = [trim, bwa, MarkDuplicates, index, CollectHsMetrics,
             coverage, BaseRecalibrator, ApplyBQSR, HaplotypeCaller]
            with open(sample + '.bat', 'w') as (f):
                f.write(sge)
                f.write(('\n').join(part) + '\n')
                f.write('wait ;')

        with open('qsub.bat', 'w') as (f):
            for sample in self.groups:
                f.write('qsub ' + sample + '.bat ;' + '\n')

        subprocess.call('chmod +x qsub.bat', shell=True)

    def genotype(self):
        if len(self.groups) == 1:
            mergebam = ''
            cram = ('samtools view -C -T {reference} -@ 4 -o {prefix}.dedup.bqsr.cram {sample}.dedup.bqsr.bam &').format(prefix=self.prefix, reference=self.reference, sample=self.groups.keys())
            CombineGVCFs = ''
            GenotypeGVCFs = ('{tool} GenotypeGVCFs -V {sample}.HC.g.vcf.gz -O han.vcf.gz -R {reference} --dbsnp {dbsnp} -L {bed} -ip {ip} ;').format(tool=self.gatk, sample=self.groups.keys(), dbsnp=self.dbsnp, bed=self.bed, ip=0, reference=self.reference)
        else:
            bams = [ sample + '.dedup.bqsr.bam' for sample in self.groups ]
            mergebam = ('samtools merge -f -@ 32 -O bam {prefix}_bqsr.bam {bams} ;').format(prefix=self.prefix, bams=(' ').join(bams))
            cram = ('samtools view -C -T /share/data1/genome/hs38DH.fa -@ 4 -o {prefix}.dedup.bqsr.cram {prefix}_bqsr.bam &').format(prefix=self.prefix, sample=sample)
            gvcfs = [ sample + '.HC.g.vcf.gz' for sample in self.groups ]
            CombineGVCFs = ('{tool} CombineGVCFs -V {gvcfs} -O cohort.g.vcf.gz -R {reference} ;').format(tool=self.gatk, reference=self.reference, gvcfs=(' -V ').join(gvcfs))
            GenotypeGVCFs = ('{tool} GenotypeGVCFs -V cohort.g.vcf.gz -O han.vcf.gz -R {reference} --dbsnp {dbsnp} -L {bed} -ip {ip} ;').format(tool=self.gatk, sample=sample, dbsnp=self.dbsnp, bed=self.bed, ip=0, reference=self.reference)
        my_snp_Filter = ('{tool} SelectVariants -select-type SNP -V han.vcf.gz -O han.snp.vcf.gz ;').format(tool=self.gatk)
        my_snp_Filter2 = ('{tool} VariantFiltration -V han.snp.vcf.gz --filter-expression "QD < 2.0 || MQ < 40.0 || FS > 60.0 || SOR > 3.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "my_snp_Filter" -O han.snp.hardfilter.vcf.gz ;').format(tool=self.gatk)
        my_indel_Filter = ('{tool} SelectVariants -select-type INDEL -V han.vcf.gz -O han.indel.vcf.gz ;').format(tool=self.gatk)
        my_indel_Filter2 = ('{tool} VariantFiltration -V han.indel.vcf.gz --filter-expression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0" --filter-name "my_indel_Filter" -O han.indel.hardfilter.vcf.gz ;').format(tool=self.gatk)
        MergeVcfs = ('{tool} MergeVcfs -R {reference} -I han.snp.hardfilter.vcf.gz -I han.indel.hardfilter.vcf.gz -O {prefix}.snp.indel.hardfilter.vcf.gz ;').format(tool=self.gatk, prefix=self.prefix, reference=self.reference)
        annotation = ('{tool}/table_annovar.pl {prefix}.snp.indel.hardfilter.vcf.gz {tool}/humandb/ -buildver hg38 -out {prefix} -otherinfo -remove -protocol refGene,cytoBand,exac03,gnomad_exome,clinvar_20170905,dbnsfp33a, -operation g,r,f,f,f,f --vcfinput -nastring . -polish -thread 30').format(tool=self.annovar, prefix=self.prefix)
        sge = ('#$ -N annotation\n#$ -pe smp 32\n#$ -q all.q\n#$ -cwd\nset -e\ncd {working_space}\nsource ~/.bash_profile\n').format(working_space=self.working_space)
        part = [mergebam, cram, CombineGVCFs, GenotypeGVCFs, my_indel_Filter,
         my_indel_Filter2, my_snp_Filter, my_snp_Filter2, MergeVcfs, annotation]
        with open('genotype.bat', 'w') as (f):
            f.write(sge)
            f.write(('\n').join(part) + '\n')
            f.write('wait ;')


def main(p_dict):
    input = p_dict['input']
    prefix = p_dict['prefix']
    working_space = p_dict['working_space']
    result = Wes(input, working_space, prefix)
    result.trim_bwa_dedup_bqsr_haplotypecaller()
    result.genotype()
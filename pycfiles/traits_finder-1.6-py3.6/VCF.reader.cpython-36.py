# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traits_finder/scripts/VCF.reader.py
# Compiled at: 2019-11-11 18:32:19
# Size of source mod 2**32: 2189 bytes
import argparse, vcfpy
parser = argparse.ArgumentParser(formatter_class=(argparse.RawDescriptionHelpFormatter))
parser.add_argument('-i', help='input vcf filename',
  type=str,
  default='input.vcf',
  metavar='input.vcf')
parser.add_argument('-o', help='output filename',
  type=str,
  default='input.vcf.out',
  metavar='input.vcf.out')
args = parser.parse_args()

def process_record(record, output):
    line = [
     record.CHROM, record.POS, record.REF]
    line += [alt.value for alt in record.ALT]
    line += [call.data.get('GT') or './.' for call in record.calls]
    output.write('\t'.join(map(str, line)))


def readvcf(input, output):
    vcf_file = vcfpy.Reader.from_path(input)
    output.write('#' + str(vcf_file.header.samples.names[0]) + '\n')
    header = ['#CHROM', 'POS', 'REF', 'ALT']
    output.write('\t'.join(header) + '\n')
    for record in vcf_file:
        if record.is_snv():
            process_record(record, output)
            output.write('\n')
            print(record.FORMAT)
            print(record.affected_end, record.affected_start, record.begin, record.end)
            print(record.QUAL)
            print(record.calls)
            print(record.is_snv())
            for calls in record.calls:
                print(calls.gt_bases, calls.gt_phase_char, calls.gt_type)
                print(calls.is_het, calls.is_phased, calls.is_variant)
                print(calls.plodity, calls.sample)
                print(calls.site, calls.is_filtered)

            print('\n\n')


readvcf(args.i, open(args.o, 'w'))
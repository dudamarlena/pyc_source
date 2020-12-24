# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngslib/ngsfun.py
# Compiled at: 2019-11-02 01:28:10
# Size of source mod 2**32: 6747 bytes
from subprocess import run
from shlex import split
from multiprocessing import Pool
import os, logging, gzip, re
logging.basicConfig(level=(logging.DEBUG), format='%(asctime)s|%(levelname)s|%(message)s')

def unique(input_list):
    """Function to get unique values.
    Arguments:
        input_list {[list]} -- A list.
    
    Returns:
        [list] -- A unique list.
    """
    list_set = set(input_list)
    unique_list = list(list_set)
    return unique_list


def bash_run(cmd, capture_output=False):
    """Run command in Bash.

    Arguments:
        cmd {str} -- A command.

    Keyword Arguments:
        capture_output {bool} -- [description] (default: {False})

    Returns:
        stdout -- stdout (capture_output=True)
        int -- Return code.
    """
    print('Running: ' + cmd)
    if capture_output:
        run_result = run((split(cmd)), capture_output=capture_output)
        stdout = run_result.stdout
        return_code = run_result.returncode
        return (stdout, return_code)
    run_result = run((split(cmd)), capture_output=capture_output)
    return_code = run_result.returncode
    return return_code


def batch_run(target_list, function, jobs=8):
    """
    Batch run a function on a target list.
    :param target_list: Target list.
    :param function: The function's name. It can only accept 1 parameter.
    :param jobs: Default 8.
    :return:
    """
    with Pool(jobs) as (p):
        p.map(function, target_list)


def is_existing(target_file, verbose=False):
    """To detect whether a file exsits.

    Arguments:
        target_file {str} -- The target file.
        verbose {bool} -- Print information or not.

    Returns:
        True or False -- [description]
    """
    if os.path.exists(target_file):
        if verbose:
            print('INFO: {} detected.'.format(target_file))
        return True
    if verbose:
        print('WARNING: {} not detected.'.format(target_file))
    return False


def get_lib_dir():
    """
    Get the absolute path of current lib.
    :return: The absolute path of 'get_lib_dir()'
    """
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    return lib_dir


def test_bash():
    SCRIPT_DIR = get_script_dir()
    print('{}/test.sh'.format(SCRIPT_DIR))
    bash_run('{}/test.sh'.format(SCRIPT_DIR))


def normalize_vcf(input_vcf, output_vcf):
    """
    Use vt and bcftools to normalize a VCF file.
    :param input_vcf:
    :param output_vcf:
    :return:
    """
    pass


def extract_sample_names_in_vcf(vcf):
    """Extract all the sample names in a VCF.
    
    Arguments:
        vcf {str} -- Name of a VCF file.
    """
    if not is_existing(vcf):
        raise IOError()
    cmd = 'bcftools query -l {}'.format(vcf)
    sample_names, rc = bash_run(cmd, capture_output=True)
    if rc != 0:
        print('ERROR: failed to parse {}'.format(vcf))
        raise IOError()
    sample_name_list = sample_names.decode().strip().split('\n')
    return sample_name_list


def extract_snv_from_vcf(input_vcf, output_vcf, filter=False):
    """
    Generate a vcf of SNVs from the input.

    Arguments:
        input_vcf {[type]} -- [description]
        output_vcf {[type]} -- [description]

    Keyword Arguments:
        filter {bool} -- Whether use FILTER = PASS. (default: {False})
    """
    if filter:
        logging.info('Extracting SNVs from {}, using FILTER...'.format(input_vcf))
        cmd = 'bcftools view -f PASS -v snps -o {} -O v {}'.format(output_vcf, input_vcf)
        bash_run(cmd=cmd, capture_output=False)
    else:
        logging.info('Extracting SNVs from {}...'.format(input_vcf))
        cmd = 'bcftools view -v snps -o {} -O v {}'.format(output_vcf, input_vcf)
        bash_run(cmd=cmd, capture_output=False)


def collect_allelic_counts_for_a_bam(bam, vcfs, output, ref_fasta='/thinker/storage/udata/bing/GATK/hg19/ucsc.hg19.fasta'):
    """Collect allelic counts for a bam, with GATK.
    
    Arguments:
        bam {[type]} -- [description]
        vcfs {list} -- A list of VCFs.
        output {[type]} -- [description]

    Keyword Arguments:
        ref_fasta {str} -- [description] (default: {'/thinker/storage/udata/bing/GATK/hg19/ucsc.hg19.fasta'})
    """
    cmd = 'gatk --java-options -Xmx8g CollectAllelicCounts -I {} -O {} -R {} '.format(bam, output, ref_fasta)
    for vcf in vcfs:
        cmd = cmd + '-L {} '.format(vcf)

    if not is_existing(bam):
        logging.error('Bam does not exist: {}'.format(bam))
    else:
        if is_existing(output):
            logging.info('Skip ' + output)
        else:
            bash_run(cmd)


def add_GT_to_strelka_vcf(input_vcf='test.strelka.somatic.vcf.gz', output_vcf='test.vcf'):
    """Add GT column into Strelka2 VCF.
    
    Keyword Arguments:
        input_vcf {str} -- [description] (default: {'test.strelka.somatic.vcf.gz'})
        output_vcf {str} -- [description] (default: {'test.vcf'})
    """
    if not is_existing(output_vcf, verbose=True):
        with open(output_vcf, 'w') as (f_out):
            if re.search('\\.vcf\\.gz$', input_vcf):
                f_in = gzip.open(input_vcf, 'r')
                f_in_type = 'binary'
            else:
                if re.search('\\.vcf$', input_vcf):
                    f_in = open(input_vcf, 'r')
                    f_in_type = 'text'
                else:
                    logging.error('Bad input vcf: ' + input_vcf)
            for line in f_in:
                if f_in_type == 'binary':
                    line = line.decode()
                if line.startswith('#'):
                    f_out.write(line)
                else:
                    line_list = line.strip().split('\t')
                    line_list[8] = 'GT:' + line_list[8]
                    line_list[9] = './.:' + line_list[9]
                    line_list[10] = './1:' + line_list[10]
                    f_out.write('\t'.join(line_list) + '\n')

            f_in.close()


if __name__ == '__main__':
    pass
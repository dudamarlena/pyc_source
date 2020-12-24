# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krflorek/Documents/dryad/dryad_app/dryad.py
# Compiled at: 2020-05-08 17:22:21
# Size of source mod 2**32: 5328 bytes
import sys, os, re, argparse
from shutil import which, copyfile
from datetime import date
import pexpect, re, sys

def main():
    lib_path = os.path.abspath(os.path.dirname(__file__) + '/' + '../lib')
    dryad_path = os.path.abspath(os.path.dirname(__file__))
    nextflow_path = os.path.join(lib_path, 'nextflow')

    class MyParser(argparse.ArgumentParser):

        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(description='A comprehensive tree building program.')
    parser.add_argument('reads_path', type=str, help='path to the directory of raw reads in the fastq format', nargs='?', default=False)
    parser.add_argument('--output', '-o', metavar='<output_path>', type=str, help='path to ouput directory, default "dryad_results"', default='dryad_results')
    parser.add_argument('--core-genome', '-cg', default=False, action='store_true', help='construct a core-genome tree')
    parser.add_argument('--snp', '-s', default=False, action='store_true', help='construct a SNP tree, requires a reference sequence in fasta format (-r)')
    parser.add_argument('-r', metavar='<path>', type=str, help='reference sequence for SNP pipeline')
    parser.add_argument('-ar', default=False, action='store_true', help='detect AR mechanisms')
    parser.add_argument('--sep', metavar='sep_chars', type=str, help='dryad identifies sample names from the name of the read file by splitting the name on the specified separating characters, default "_"', default='_')
    parser.add_argument('--profile', type=str, choices=['docker', 'singularity'], help='specify nextflow profile, dryad will try to use docker first, then singularity')
    parser.add_argument('--config', '-c', type=str, help='Nextflow custom configureation')
    parser.add_argument('--get_config', action='store_true', help='get a Nextflow configuration template for dryad')
    parser.add_argument('--resume', default='', action='store_const', const='-resume', help='resume a previous run')
    parser.add_argument('--report', action='store_true', help='generte a pdf report')
    args = parser.parse_args()
    if args.get_config:
        config_path = os.path.join(dryad_path, 'configs/dryad_config_template.config')
        dest_path = os.path.join(os.getcwd(), date.today().strftime('%y-%m-%d') + '_dryad.config')
        copyfile(config_path, dest_path)
        sys.exit()
    if not args.reads_path:
        parser.print_help()
        print('Please specify a path to a directory containing the raw reads.')
        sys.exit(1)
    elif args.snp:
        if args.r == None:
            parser.print_help()
            print('Please specify a reference sequence for the SNP pipeline.')
            sys.exit(1)
        if which('docker'):
            profile = '-profile docker'
    elif which('singularity'):
        profile = '-profile singularity'
    else:
        profile = ''
    config = ''
    if args.config:
        config = '-C ' + os.path.abspath(args.config)
        profile = ''
    else:
        if args.profile:
            if which(args.profile):
                profile = '-profile ' + args.profile
            else:
                print(f"{args.profile} is not installed or found in PATH.")
        else:
            if not profile:
                print('Singularity or Docker is not installed or not found in PATH.')
                sys.exit(1)
            else:
                work = ''
                if profile:
                    work = f"-w {args.output}/logs/work"
                selections = ''
                if args.ar:
                    selections += ' --ar'
                if args.core_genome:
                    selections += ' --cg'
                if args.snp:
                    selections += f" --snp --snp_reference {args.r}"
                if args.report:
                    if args.snp and args.core_genome:
                        report_template_path = os.path.abspath(os.path.dirname(__file__) + '/' + '../report/report.Rmd')
                        logo_path = os.path.abspath(os.path.dirname(__file__) + '/' + 'assets/dryad_logo_250.png')
                        selections += f" --report {report_template_path} --logo {logo_path}"
            mqc_config_path = '--multiqc_config ' + os.path.join(dryad_path, 'configs/multiqc_config.yaml')
            mqc_logo_path = '--multiqc_logo ' + os.path.join(dryad_path, 'assets/dryad_logo_250.png')
            other_args = f"--name_split_on {args.sep} --outdir {args.output}"
            command = nextflow_path
            command = command + f" {config} run {dryad_path}/dryad.nf {profile} {args.resume} --reads {args.reads_path} {selections} {other_args} {mqc_config_path} {mqc_logo_path} -with-trace {args.output}/logs/dryad_trace.txt -with-report {args.output}/logs/dryad_execution_report.html {work}"
            print('Starting the Dryad pipeline:')
            child = pexpect.spawn(command)
            child.interact()
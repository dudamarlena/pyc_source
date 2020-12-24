# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/krflorek/Documents/dryad/dryad_app/dryad_report.py
# Compiled at: 2020-05-08 19:07:03
# Size of source mod 2**32: 3763 bytes
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

    parser = MyParser(description='Rebuild a previously generated PDF report.')
    parser.add_argument('rmd', type=str, help='path to Rmarkdown file (.Rmd)', nargs='?', default=False)
    parser.add_argument('snp_matrix', type=str, help='path to snp matrix', nargs='?', default=False)
    parser.add_argument('cg_tree', type=str, help='path to core genome tree', nargs='?', default=False)
    parser.add_argument('--ar', type=str, help='path to ar TSV file')
    parser.add_argument('--profile', type=str, choices=['docker', 'singularity'], help='specify nextflow profile, dryad_report will try to use docker first, then singularity')
    parser.add_argument('--get_config', action='store_true', help='get a Nextflow configuration template for dryad')
    parser.add_argument('--config', '-c', type=str, help='Nextflow custom configuration')
    args = parser.parse_args()
    if args.get_config:
        config_path = os.path.join(dryad_path, 'configs/dryad_config_template.config')
        dest_path = os.path.join(os.getcwd(), date.today().strftime('%y-%m-%d') + '_dryad.config')
        copyfile(config_path, dest_path)
        sys.exit()
    elif args.rmd:
        if not (args.snp_matrix and args.cg_tree):
            parser.print_help()
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
                output_path = os.path.join(os.getcwd(), 'rebuild_results')
                output_work = os.path.join(output_path, 'report_work')
                if profile:
                    work = f"-w {output_work}"
                rmd = os.path.abspath(args.rmd)
                logo_path = os.path.abspath(os.path.dirname(__file__) + '/' + 'assets/dryad_logo_250.png')
                snp_mat = '--snp_matrix ' + os.path.abspath(args.snp_matrix)
                cg_tree = '--cg_tree ' + os.path.abspath(args.cg_tree)
                if args.ar:
                    ar_tsv = '--ar_tsv ' + os.path.abspath(args.ar)
                else:
                    ar_tsv = ''
            command = nextflow_path
            command = command + f" {config} run {dryad_path}/rebuild_report.nf {profile} --logo {logo_path} --outdir {output_path} --rmd {rmd} {snp_mat} {cg_tree} {ar_tsv} {work}"
            print('Rebuilding Dryad Report:')
            child = pexpect.spawn(command)
            child.interact()
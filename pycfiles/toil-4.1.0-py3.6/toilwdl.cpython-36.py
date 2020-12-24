# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/wdl/toilwdl.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 6770 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import argparse, os, logging, sys, subprocess
from toil.wdl.wdl_analysis import AnalyzeWDL
from toil.wdl.wdl_synthesis import SynthesizeWDL, write_AST
import toil.wdl.wdl_parser as wdl_parser
wdllogger = logging.getLogger(__name__)

def main():
    """
    A program to run WDL input files using native Toil scripts.

    Calls two files, described below, wdl_analysis.py and wdl_synthesis.py:

    wdl_analysis reads the wdl, json, and extraneous files and restructures them
    into 2 intermediate data structures before writing (python dictionaries):
        "wf_dictionary": containing the parsed workflow information.
        "tasks_dictionary": containing the parsed task information.

    wdl_synthesis takes the "wf_dictionary" and "tasks_dictionary" and uses them to
    write a native python script for use with Toil.

    Requires a WDL file, and a JSON file.  The WDL file contains ordered commands,
    and the JSON file contains input values for those commands.  To run in Toil,
    these two files must be parsed, restructured into python dictionaries, and
    then compiled into a Toil formatted python script.  This compiled Toil script
    is deleted after running unless the user specifies: "--dont_delete_compiled"
    as an option.

    The WDL parser was auto-generated from the Broad's current WDL grammar file:
    https://github.com/openwdl/wdl/blob/master/parsers/grammar.hgr
    using Scott Frazer's Hermes: https://github.com/scottfrazer/hermes
    Thank you Scott Frazer!

    Currently in alpha testing, and known to work with the Broad's GATK tutorial
    set for WDL on their main wdl site:
    software.broadinstitute.org/wdl/documentation/topic?name=wdl-tutorials

    And ENCODE's WDL workflow:
    github.com/ENCODE-DCC/pipeline-container/blob/master/local-workflows/encode_mapping_workflow.wdl

    Additional support to be broadened to include more features soon.
    """
    parser = argparse.ArgumentParser(description='Runs WDL files with toil.')
    parser.add_argument('wdl_file', help='A WDL workflow file.')
    parser.add_argument('secondary_file', help='A secondary data file (json).')
    parser.add_argument('--jobStore', type=str, required=False, default=None)
    parser.add_argument('-o', '--outdir',
      required=False,
      default=(os.getcwd()),
      help='Optionally specify the directory that outputs are written to.  Default is the current working dir.')
    parser.add_argument('--dev_mode', required=False, default=False, help='1. Creates "AST.out", which holds the printed AST and "mappings.out", which holds the parsed task, workflow dictionaries that were generated.  2. Saves the compiled toil script generated from the wdl/json files from deletion.  3. Skips autorunning the compiled python file.')
    parser.add_argument('--docker_user', required=False, default='root', help='The user permissions that the docker containers will be run with (and the permissions set on any output files produced).  Default is "root".  Setting this to None will set this to the current user.')
    parser.add_argument('--destBucket', type=str, required=False, default=False, help='Specify a cloud bucket endpoint for output files.')
    args, wdl_run_args = parser.parse_known_args()
    wdl_file_path = os.path.abspath(args.wdl_file)
    args.secondary_file = os.path.abspath(args.secondary_file)
    args.outdir = os.path.abspath(args.outdir)
    if args.dev_mode:
        write_AST(wdl_file_path, args.outdir)
    else:
        aWDL = AnalyzeWDL(wdl_file_path, args.secondary_file, args.outdir)
        if args.secondary_file.endswith('.json'):
            aWDL.dict_from_JSON(args.secondary_file)
        else:
            if args.secondary_file.endswith('.yml') or args.secondary_file.endswith('.yaml'):
                aWDL.dict_from_YML(args.secondary_file)
            else:
                raise RuntimeError('Unsupported Secondary File Type.  Use json.')
        with open(wdl_file_path, 'r') as (wdl):
            wdl_string = wdl.read()
            ast = wdl_parser.parse(wdl_string).ast()
            aWDL.create_tasks_dict(ast)
            aWDL.create_workflows_dict(ast)
        sWDL = SynthesizeWDL(aWDL.tasks_dictionary, aWDL.workflows_dictionary, args.outdir, aWDL.json_dict, args.docker_user, args.jobStore, args.destBucket)
        module_section = sWDL.write_modules()
        fn_section = sWDL.write_functions()
        main_section = sWDL.write_main()
        sWDL.write_python_file(module_section, fn_section, main_section, sWDL.output_file)
        if args.dev_mode:
            wdllogger.debug('WDL file compiled to toil script.')
            sWDL.write_mappings(aWDL)
        else:
            wdllogger.debug('WDL file compiled to toil script.  Running now.')
            exe = sys.executable if sys.executable else 'python'
            cmd = [exe, sWDL.output_file]
            cmd.extend(wdl_run_args)
            subprocess.check_call(cmd)
            os.remove(sWDL.output_file)


if __name__ == '__main__':
    main()
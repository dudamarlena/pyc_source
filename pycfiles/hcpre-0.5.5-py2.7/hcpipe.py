# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/hcpre/hcpipe.py
# Compiled at: 2014-05-14 14:19:51
"""
hcpipe.py

Copyright (c) 2013 Ben Acland
"""
import os, sys, getopt
from hcpre.workflows import *
help_message = "\nProvides command line tools to build and work on workflow confiuration files,\nand for launching the pipeline using a specific config. You can either import\nHCPrepWorkflow, then configure and run in from your own code, or use the\nbuilt-in command line tools to launch the workflow on your data.\n\nCommands\n--------\n-h, --help\n    Prints out this message.\n-i, --init\n    Creates a new config file in your current directory.\n-u, --update\n    Reruns part of the config file setup script on any config file in your current directory.\n-g, --graph\n    Draws a graph of the nipype workflow to the current directory.\n-r, --run\n    Runs the workflow using any config file in the current directory.\n\nParameters\n----------\n-c, --config (path)\n    The config file to use.\n-s (comma separated subject numbers)\n    The list of subjects who you'd like to put through the workflow. Overrides\n    setting in the config file.\n-n (integer)\n    The number of threads you would like to use. Higher numbers are faster to\n    a point, but depending on how large your data is (chances are, it is quite\n    large), you may well want to limit yourself to something below 8 for\n    starters if you're working on a large server. Default is 1. Ignored if\n    you use -p.\n-p, --pbs\n    Causes nipype to try to use the PBS plugin. For use on the cluster only.\n    Experimental.\n-o (path)\n    The directory to put preprocessed data in. Default is current directory.\n-v \n    Verbose. At this point, just makes -g print a graph that expands iterables.\n"

class Usage(Exception):

    def __init__(self, msg=help_message):
        self.msg = msg


def main(argv=None):
    import os
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], 'pvrhiugs:n:o:c:', ['run', 'help', 'init', 'update', 'graph', 'config', 'pbs'])
        except getopt.error as msg:
            raise Usage(msg='\n' + str(msg))

        update = False
        graph = False
        subs = None
        N_PROCS = None
        run = False
        verbose = False
        c_file = None
        use_pbs = False
        out_dir = os.getcwd()
        for option, value in opts:
            if option in ('-h', '--help'):
                raise Usage()
            if option in ('-i', '--init'):
                setup_conf()
                return
            if option in ('-u', '--update'):
                update = True
            if option in ('-g', '--graph'):
                graph = True
            if option in ('-r', '--run'):
                run = True
            if option in ('-c', '--config'):
                c_file = value
            if option in ('-p', '--pbs'):
                use_pbs = True
            if option in '-s':
                subs = [ sub.strip() for sub in value.split(',') ]
            if option in '-v':
                verbose = True
            if option in '-n':
                N_PROCS = int_or_none(value)
            if option in '-o':
                out_dir = value

        if not c_file:
            try:
                c_file = select_conf()
            except Exception as e:
                raise Usage(msg='Could not find a config file.')

        if update:
            update_conf(c_file)
            return
        if not run and not graph:
            raise Usage(msg='Nothing to do...')
        conf = get_config_dict(c_file)
        if not conf:
            raise Usage(msg='Could not parse config file.')
        if not validate_config(conf):
            raise Usage(msg='Invalid config file.')
        wk = HCPrepWorkflow(name='hcp_prep_workflow', config=conf)
        if subs:
            wk.subjects_node.iterables = (
             'subject', subs)
        out_dir = os.path.abspath(out_dir)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        wk.data_sink.inputs.base_directory = out_dir
        if graph:
            g2u = 'exec' if verbose else 'orig'
            wk.write_graph(dotfilename='hcp_pipe_graph', graph2use=g2u)
            return
        if not run:
            return
        if use_pbs:
            print 'running using PBS'
            ques = [
             [
              [
               wk.dicom_convert, wk.dicom_info, wk.nii_wrangler], {'qsub_args': '-l nodes=1:ppn=1,mem=1gb,walltime=1:00:00'}],
             [
              [
               wk.hc_pre_fs], {'qsub_args': '-l nodes=1:ppn=2,mem=10gb,vmem=10gb,walltime=6:00:00'}],
             [
              [
               wk.hc_fs], {'qsub_args': '-l nodes=1:ppn=2,mem=5gb,walltime=24:00:00'}],
             [
              [
               wk.hc_post_fs], {'qsub_args': '-l nodes=1:ppn=4,mem=10gb,walltime=4:00:00'}],
             [
              [
               wk.hc_volume, wk.hc_surface], {'qsub_args': '-l nodes=1:ppn=4,mem=10gb,walltime=12:00:00'}]]
            for q in ques:
                p_args = dict(q[1], **{'overwrite': True})
                for n in q[0]:
                    n.plugin_args = p_args

            wk.run(plugin='PBS', plugin_args={'qsub_args': '-l nodes=1:ppn=1,mem=1gb,walltime=1:00:00'})
        elif N_PROCS > 0:
            print 'running with %d processes' % N_PROCS
            wk.run(plugin='MultiProc', plugin_args={'n_procs': N_PROCS, 'non_daemon': True})
        else:
            print 'running single process'
            wk.run()
    except Usage as err:
        f_str = sys.argv[0].split('/')[(-1)] + ':'
        lfs = len(f_str)
        f_str = '%s\n%s\n%s\n' % ('-' * lfs, f_str, '-' * lfs)
        print >> sys.stderr, f_str + str(err.msg)
        print >> sys.stderr, '-------------------\nfor help use --help\n-------------------'
        return 2

    return


if __name__ == '__main__':
    sys.exit(main())
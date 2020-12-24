# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_vg/context.py
# Compiled at: 2018-11-03 15:09:40
"""
context.py: Defines a toil_vg context, which contains (and hides) all the config
file values, IOStore dumping parameters, and other things that need to be passed
around but that toil-vg users shouldn't generally need to dinker with.

Instead of dropping the container runner into the command-line options
namespace, we keep them both in here.

"""
import tempfile, datetime, pkg_resources, copy, os, os.path
from argparse import Namespace
from toil.common import Toil
from toil.job import Job
from toil_vg.vg_config import apply_config_file_args
from toil_vg.vg_common import ContainerRunner, get_container_tool_map
from toil_vg.iostore import IOStore

def run_write_info_to_outstore(job, context, argv):
    """ Writing to the output is still problematic, especially from within jobs.  So 
    we write some options info into the output store first-thing to trigger errors
    before doing all the compute if possible.  To do this, this job needs to be passed
    to the root of the workflow """
    f = tempfile.NamedTemporaryFile(delete=True)
    now = datetime.datetime.now()
    if argv:
        f.write(('{}\n\n').format((' ').join(argv)))
    f.write(('{}\ntoil-vg version {}\nConfiguration:\n').format(now, pkg_resources.get_distribution('toil-vg').version))
    for key, val in context.config.__dict__.items():
        f.write(('{}: {}\n').format(key, val))

    f.flush()
    context.get_out_store().write_output_file(f.name, ('toil-vg-{}.txt').format(argv[1] if argv and len(argv) > 1 else 'info'))
    f.close()


class Context(object):
    """
    Represents a toil-vg context, necessary to use the library.
    """

    def __init__(self, out_store=None, overrides=Namespace()):
        """
        Make a new context, so we can run the library.
        
        Takes an optional Namespace of overrides for default toil-vg and Toil
        configuration values.
        
        Overrides can also have a "config" key, in which case that config file
        will be loaded.
        
        """
        self.config = apply_config_file_args(overrides)
        self.runner = ContainerRunner(container_tool_map=get_container_tool_map(self.config), realtime_stderr=self.config.realTimeStderr)
        if out_store is not None:
            self.out_store_string = IOStore.absolute(out_store)
        else:
            self.out_store_string = None
        return

    def get_toil(self, job_store):
        """
        Produce a new Toil object for running Toil jobs, using the configuration
        used when constructing this context, and the given job_store specifier.
        
        Needs to be used in a "with" statement to actually work.
        """
        toil_options = Job.Runner.getDefaultOptions(job_store)
        for k, v in self.config.__dict__.iteritems():
            toil_options.__dict__[k] = v

        return Toil(toil_options)

    def get_out_store(self):
        """
        Return the IOStore to write output files to, or None if they should not
        be written anywhere besides the Toil file store.
        """
        if self.out_store_string is not None:
            return IOStore.get(self.out_store_string)
        else:
            return
            return

    def write_intermediate_file(self, job, path):
        """
        Write the file at the given path to the given job's Toil FileStore, and
        to the out_store if one is in use and we are trying to dump intermediate
        files.
        
        In the out_store, the file is saved under its basename, in the root
        directory.
        
        Returns the Toil file ID for the written file.
        """
        out_store = self.get_out_store()
        if out_store is not None and self.config.force_outstore:
            out_store.write_output_file(path, os.path.basename(path))
        return job.fileStore.writeGlobalFile(path)

    def write_output_file(self, job, path, out_store_path=None):
        """
        
        Write the file at the given path to the given job's Toil FileStore, and
        to the out_store if one is in use.
        
        In the out_store, the file is saved under its basename, in the root
        directory. If out_store_path is set, the file is saved there instead.
        
        Returns the Toil file ID for the written file.
        """
        out_store = self.get_out_store()
        if out_store is not None:
            name = out_store_path if out_store_path else os.path.basename(path)
            out_store.write_output_file(path, name)
        return job.fileStore.writeGlobalFile(path)

    def to_options(self, options):
        """
        Turn back into an options-format namespace like toil-vg used to use
        everywhere. Merges with the given real command-line options.
        """
        options = copy.deepcopy(options)
        for key, val in self.config.__dict__.items():
            options.__dict__[key] = val

        options.out_store = self.out_store_string
        options.drunner = self.runner
        options.tool = 'library'
        return options
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyneuroml/pynml.py
# Compiled at: 2019-10-15 15:22:31
__doc__ = b'\n\nPython wrapper around jnml command. \nAlso a number of helper functions for \nhandling/generating/running LEMS/NeuroML2 files\n\nThanks to Werner van Geit for an initial version of a python wrapper for jnml.\n\n'
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os, sys, subprocess, math
from datetime import datetime
from pyneuroml import __version__
from pyneuroml import JNEUROML_VERSION
import neuroml, neuroml.loaders as loaders, neuroml.writers as writers, lems.model.model as lems_model
from lems.parser.LEMS import LEMSFileParser
import random, inspect, zipfile, shlex, signal
DEFAULTS = {b'v': False, b'default_java_max_memory': b'400M', 
   b'nogui': False}
lems_model_with_units = None

def parse_arguments():
    """Parse command line arguments"""
    global DEFAULTS
    import argparse
    parser = argparse.ArgumentParser(description=b'pyNeuroML v%s: Python utilities for NeuroML2' % __version__ + b'\n    libNeuroML v%s' % neuroml.__version__ + b'\n    jNeuroML v%s' % JNEUROML_VERSION, usage=b'pynml [-h|--help] [<shared options>] <one of the mutually-exclusive options>', formatter_class=argparse.RawTextHelpFormatter)
    shared_options = parser.add_argument_group(title=b'Shared options', description=b'These options can be added to any of the mutually-exclusive options')
    shared_options.add_argument(b'-verbose', action=b'store_true', default=DEFAULTS[b'v'], help=b'Verbose output')
    shared_options.add_argument(b'-java_max_memory', metavar=b'MAX', default=DEFAULTS[b'default_java_max_memory'], help=b'Java memory for jNeuroML, e.g. 400M, 2G (used in\n-Xmx argument to java)')
    shared_options.add_argument(b'-nogui', action=b'store_true', default=DEFAULTS[b'nogui'], help=b'Suppress GUI,\ni.e. show no plots, just save results')
    shared_options.add_argument(b'lems_file', type=str, metavar=b'<LEMS/NeuroML 2 file>', help=b'LEMS/NeuroML 2 file to process')
    mut_exc_opts_grp = parser.add_argument_group(title=b'Mutually-exclusive options', description=b'Only one of these options can be selected')
    mut_exc_opts = mut_exc_opts_grp.add_mutually_exclusive_group(required=False)
    mut_exc_opts.add_argument(b'-sedml', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert\nsimulation settings (duration, dt, what to save)\nto SED-ML format')
    mut_exc_opts.add_argument(b'-neuron', nargs=argparse.REMAINDER, help=b"(Via jNeuroML) Load a LEMS file, and convert it to\nNEURON format.\nThe full format of the '-neuron' option is:\n-neuron [-nogui] [-run] [-outputdir dir] <LEMS file>\n    -nogui\n        do not generate gtaphical elements in NEURON,\n        just run, save data, and quit\n    -run\n        compile NMODL files and run the main NEURON\n        hoc file (Linux only currently)\n    -outputdir <dir>\n        generate NEURON files in directory <dir>\n    <LEMS file>\n        the LEMS file to use")
    mut_exc_opts.add_argument(b'-svg', action=b'store_true', help=b'(Via jNeuroML) Convert NeuroML2 file (network & cells)\nto SVG format view of 3D structure')
    mut_exc_opts.add_argument(b'-png', action=b'store_true', help=b'(Via jNeuroML) Convert NeuroML2 file (network & cells)\nto PNG format view of 3D structure')
    mut_exc_opts.add_argument(b'-dlems', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto dLEMS format, a distilled form of LEMS in JSON')
    mut_exc_opts.add_argument(b'-vertex', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto VERTEX format')
    mut_exc_opts.add_argument(b'-xpp', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto XPPAUT format')
    mut_exc_opts.add_argument(b'-dnsim', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto DNsim format')
    mut_exc_opts.add_argument(b'-brian', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto Brian format')
    mut_exc_opts.add_argument(b'-sbml', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto SBML format')
    mut_exc_opts.add_argument(b'-matlab', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto MATLAB format')
    mut_exc_opts.add_argument(b'-cvode', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto C format using CVODE package')
    mut_exc_opts.add_argument(b'-nineml', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto NineML format')
    mut_exc_opts.add_argument(b'-spineml', action=b'store_true', help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto SpineML format')
    mut_exc_opts.add_argument(b'-sbml-import', metavar=('<SBML file>', 'duration',
                                                        'dt'), nargs=3, help=b'(Via jNeuroML) Load a SBML file, and convert it\ntoLEMS format using values for duration & dt\nin ms (ignoring SBML units)')
    mut_exc_opts.add_argument(b'-sbml-import-units', metavar=('<SBML file>', 'duration',
                                                              'dt'), nargs=3, help=b'(Via jNeuroML) Load a SBML file, and convert it\nto LEMS format using values for duration & dt\nin ms (attempt to extract SBML units; ensure units\nare valid in the SBML!)')
    mut_exc_opts.add_argument(b'-vhdl', metavar=('neuronid', '<LEMS file>'), nargs=2, help=b'(Via jNeuroML) Load a LEMS file, and convert it\nto VHDL format')
    mut_exc_opts.add_argument(b'-graph', metavar=b'level', nargs=1, help=b'Load a NeuroML file, and convert it to a graph using\nGraphViz. Detail is set by level (1, 2, etc.)')
    mut_exc_opts.add_argument(b'-matrix', metavar=b'level', nargs=1, help=b'Load a NeuroML file, and convert it to a matrix displaying\nconnectivity. Detail is set by level (1, 2, etc.)')
    mut_exc_opts.add_argument(b'-validate', action=b'store_true', help=b'(Via jNeuroML) Validate NeuroML2 file(s) against the\nlatest Schema')
    mut_exc_opts.add_argument(b'-validatev1', action=b'store_true', help=b'(Via jNeuroML) Validate NeuroML file(s) against the\nv1.8.1 Schema')
    return parser.parse_args()


def get_lems_model_with_units():
    global lems_model_with_units
    if lems_model_with_units == None:
        jar_path = get_path_to_jnml_jar()
        jar = zipfile.ZipFile(jar_path, b'r')
        dims_units = jar.read(b'NeuroML2CoreTypes/NeuroMLCoreDimensions.xml')
        lems_model_with_units = lems_model.Model(include_includes=False)
        parser = LEMSFileParser(lems_model_with_units)
        parser.parse(dims_units)
    return lems_model_with_units


def split_nml2_quantity(nml2_quantity):
    magnitude = None
    i = len(nml2_quantity)
    while magnitude is None:
        try:
            part = nml2_quantity[0:i]
            nn = float(part)
            magnitude = nn
            unit = nml2_quantity[i:]
        except ValueError:
            i = i - 1

    return (magnitude, unit)


def get_value_in_si(nml2_quantity):
    try:
        return float(nml2_quantity)
    except:
        model = get_lems_model_with_units()
        m, u = split_nml2_quantity(nml2_quantity)
        si_value = None
        for un in model.units:
            if un.symbol == u:
                si_value = (m + un.offset) * un.scale * pow(10, un.power)

        return si_value

    return


def convert_to_units(nml2_quantity, unit, verbose=DEFAULTS[b'v']):
    model = get_lems_model_with_units()
    m, u = split_nml2_quantity(nml2_quantity)
    si_value = None
    dim = None
    for un in model.units:
        if un.symbol == u:
            si_value = (m + un.offset) * un.scale * pow(10, un.power)
            dim = un.dimension

    for un in model.units:
        if un.symbol == unit:
            new_value = si_value / (un.scale * pow(10, un.power)) - un.offset
            if not un.dimension == dim:
                raise Exception(b'Cannot convert %s to %s. Dimensions of units (%s/%s) do not match!' % (
                 nml2_quantity, unit, dim, un.dimension))

    print_comment(b'Converting %s %s to %s: %s (%s in SI units)' % (m, u, unit, new_value, si_value), verbose)
    return new_value


def validate_neuroml1(nml1_file_name, verbose_validate=True):
    pre_args = b'-validatev1'
    post_args = b''
    return run_jneuroml(pre_args, nml1_file_name, post_args, verbose=verbose_validate, report_jnml_output=verbose_validate, exit_on_fail=False)


def validate_neuroml2(nml2_file_name, verbose_validate=True, max_memory=None):
    pre_args = b'-validate'
    post_args = b''
    if max_memory != None:
        return run_jneuroml(pre_args, nml2_file_name, post_args, max_memory=max_memory, verbose=verbose_validate, report_jnml_output=verbose_validate, exit_on_fail=False)
    else:
        return run_jneuroml(pre_args, nml2_file_name, post_args, verbose=verbose_validate, report_jnml_output=verbose_validate, exit_on_fail=False)
        return


def read_neuroml2_file(nml2_file_name, include_includes=False, verbose=False, already_included=[], optimized=False, check_validity_pre_include=False):
    print_comment(b'Loading NeuroML2 file: %s' % nml2_file_name, verbose)
    if not os.path.isfile(nml2_file_name):
        print_comment(b'Unable to find file: %s!' % nml2_file_name, True)
        sys.exit()
    if nml2_file_name.endswith(b'.h5') or nml2_file_name.endswith(b'.hdf5'):
        nml2_doc = loaders.NeuroMLHdf5Loader.load(nml2_file_name, optimized=optimized)
    else:
        nml2_doc = loaders.NeuroMLLoader.load(nml2_file_name)
    base_path = os.path.dirname(os.path.realpath(nml2_file_name))
    if include_includes:
        print_comment(b'Including included files (included already: %s)' % already_included, verbose)
        incl_to_remove = []
        for include in nml2_doc.includes:
            incl_loc = os.path.abspath(os.path.join(base_path, include.href))
            if incl_loc not in already_included:
                inc = True
                if check_validity_pre_include:
                    inc = validate_neuroml2(incl_loc, verbose_validate=False)
                print_comment(b'Loading included NeuroML2 file: %s (base: %s, resolved: %s, checking %s)' % (include.href, base_path, incl_loc, check_validity_pre_include), verbose)
                if inc:
                    nml2_sub_doc = read_neuroml2_file(incl_loc, True, verbose=verbose, already_included=already_included, check_validity_pre_include=check_validity_pre_include)
                    if incl_loc not in already_included:
                        already_included.append(incl_loc)
                    membs = inspect.getmembers(nml2_sub_doc)
                    for memb in membs:
                        if isinstance(memb[1], list) and len(memb[1]) > 0 and not memb[0].endswith(b'_'):
                            for entry in memb[1]:
                                if memb[0] != b'includes':
                                    print_comment(b'  Adding %s from: %s to list: %s' % (
                                     entry, incl_loc, memb[0]))
                                    getattr(nml2_doc, memb[0]).append(entry)

                    incl_to_remove.append(include)
                else:
                    print_comment(b"Not including file as it's not valid...", verbose)

        for include in incl_to_remove:
            nml2_doc.includes.remove(include)

    return nml2_doc


def quick_summary(nml2_doc):
    """
    Or better just use nml2_doc.summary(show_includes=False)
    """
    info = b'Contents of NeuroML 2 document: %s\n' % nml2_doc.id
    membs = inspect.getmembers(nml2_doc)
    for memb in membs:
        if isinstance(memb[1], list) and len(memb[1]) > 0 and not memb[0].endswith(b'_'):
            info += b'  %s:\n    [' % memb[0]
            for entry in memb[1]:
                extra = b'???'
                extra = entry.name if hasattr(entry, b'name') else extra
                extra = entry.href if hasattr(entry, b'href') else extra
                extra = entry.id if hasattr(entry, b'id') else extra
                info += b' %s (%s),' % (entry, extra)

            info += b']\n'

    return info


def write_neuroml2_file(nml2_doc, nml2_file_name, validate=True, verbose_validate=False):
    writers.NeuroMLWriter.write(nml2_doc, nml2_file_name)
    if validate:
        validate_neuroml2(nml2_file_name, verbose_validate)


def read_lems_file(lems_file_name, include_includes=False, fail_on_missing_includes=False, debug=False):
    if not os.path.isfile(lems_file_name):
        print_comment(b'Unable to find file: %s!' % lems_file_name, True)
        sys.exit()
    model = lems_model.Model(include_includes=include_includes, fail_on_missing_includes=fail_on_missing_includes)
    model.debug = debug
    model.import_from_file(lems_file_name)
    return model


def write_lems_file(lems_model, lems_file_name, validate=False):
    lems_model.export_to_file(lems_file_name)
    if validate:
        from lems.base.util import validate_lems
        validate_lems(lems_file_name)


def run_lems_with_jneuroml(lems_file_name, paths_to_include=[], max_memory=DEFAULTS[b'default_java_max_memory'], skip_run=False, nogui=False, load_saved_data=False, reload_events=False, plot=False, show_plot_already=True, exec_in_dir=b'.', verbose=DEFAULTS[b'v'], exit_on_fail=True, cleanup=False):
    print_comment(b'Loading LEMS file: %s and running with jNeuroML' % lems_file_name, verbose)
    post_args = b''
    post_args += gui_string(nogui)
    post_args += include_string(paths_to_include)
    t_run = datetime.now()
    if not skip_run:
        success = run_jneuroml(b'', lems_file_name, post_args, max_memory=max_memory, exec_in_dir=exec_in_dir, verbose=verbose, report_jnml_output=verbose, exit_on_fail=exit_on_fail)
    if not success:
        return False
    else:
        if load_saved_data:
            return reload_saved_data(lems_file_name, base_dir=exec_in_dir, t_run=t_run, plot=plot, show_plot_already=show_plot_already, simulator=b'jNeuroML', reload_events=reload_events, remove_dat_files_after_load=cleanup)
        return True


def nml2_to_svg(nml2_file_name, max_memory=DEFAULTS[b'default_java_max_memory'], verbose=True):
    print_comment(b'Converting NeuroML2 file: %s to SVG' % nml2_file_name, verbose)
    post_args = b'-svg'
    run_jneuroml(b'', nml2_file_name, post_args, max_memory=max_memory, verbose=verbose)


def nml2_to_png(nml2_file_name, max_memory=DEFAULTS[b'default_java_max_memory'], verbose=True):
    print_comment(b'Converting NeuroML2 file: %s to PNG' % nml2_file_name, verbose)
    post_args = b'-png'
    run_jneuroml(b'', nml2_file_name, post_args, max_memory=max_memory, verbose=verbose)


def include_string(paths_to_include):
    if paths_to_include:
        if type(paths_to_include) is str:
            paths_to_include = [
             paths_to_include]
        if type(paths_to_include) in (tuple, list):
            result = b" -I '%s'" % (b':').join(paths_to_include)
    else:
        result = b''
    return result


def gui_string(nogui):
    if nogui:
        return b' -nogui'
    return b''


def run_lems_with_jneuroml_neuron(lems_file_name, paths_to_include=[], max_memory=DEFAULTS[b'default_java_max_memory'], skip_run=False, nogui=False, load_saved_data=False, reload_events=False, plot=False, show_plot_already=True, exec_in_dir=b'.', only_generate_scripts=False, compile_mods=True, verbose=DEFAULTS[b'v'], exit_on_fail=True, cleanup=False, realtime_output=False):
    print_comment(b'Loading LEMS file: %s and running with jNeuroML_NEURON' % lems_file_name, verbose)
    post_args = b' -neuron'
    if not only_generate_scripts:
        post_args += b' -run'
    if compile_mods:
        post_args += b' -compile'
    post_args += gui_string(nogui)
    post_args += include_string(paths_to_include)
    t_run = datetime.now()
    if skip_run:
        success = True
    else:
        if b'PYTHONPATH' not in os.environ:
            os.environ[b'PYTHONPATH'] = b''
        for path in sys.path:
            if path + b':' not in os.environ[b'PYTHONPATH']:
                os.environ[b'PYTHONPATH'] = b'%s:%s' % (path, os.environ[b'PYTHONPATH'])

        if realtime_output:
            success = run_jneuroml_with_realtime_output(b'', lems_file_name, post_args, max_memory=max_memory, exec_in_dir=exec_in_dir, verbose=verbose, exit_on_fail=exit_on_fail)
        else:
            success = run_jneuroml(b'', lems_file_name, post_args, max_memory=max_memory, exec_in_dir=exec_in_dir, verbose=verbose, report_jnml_output=verbose, exit_on_fail=exit_on_fail)
    if not success:
        return False
    else:
        if load_saved_data:
            return reload_saved_data(lems_file_name, base_dir=exec_in_dir, t_run=t_run, plot=plot, show_plot_already=show_plot_already, simulator=b'jNeuroML_NEURON', reload_events=reload_events, remove_dat_files_after_load=cleanup)
        return True


def run_lems_with_jneuroml_netpyne(lems_file_name, paths_to_include=[], max_memory=DEFAULTS[b'default_java_max_memory'], skip_run=False, nogui=False, num_processors=1, load_saved_data=False, reload_events=False, plot=False, show_plot_already=True, exec_in_dir=b'.', only_generate_scripts=False, verbose=DEFAULTS[b'v'], exit_on_fail=True, cleanup=False):
    print_comment(b'Loading LEMS file: %s and running with jNeuroML_NetPyNE' % lems_file_name, verbose)
    post_args = b' -netpyne'
    if num_processors != 1:
        post_args += b' -np %i' % num_processors
    if not only_generate_scripts:
        post_args += b' -run'
    post_args += gui_string(nogui)
    post_args += include_string(paths_to_include)
    t_run = datetime.now()
    if skip_run:
        success = True
    else:
        success = run_jneuroml(b'', lems_file_name, post_args, max_memory=max_memory, exec_in_dir=exec_in_dir, verbose=verbose, exit_on_fail=exit_on_fail)
    if not success:
        return False
    else:
        if load_saved_data:
            return reload_saved_data(lems_file_name, base_dir=exec_in_dir, t_run=t_run, plot=plot, show_plot_already=show_plot_already, simulator=b'jNeuroML_NEURON', reload_events=reload_events, remove_dat_files_after_load=cleanup)
        return True


def reload_saved_data(lems_file_name, base_dir=b'.', t_run=datetime(1900, 1, 1), plot=False, show_plot_already=True, simulator=None, reload_events=False, verbose=DEFAULTS[b'v'], remove_dat_files_after_load=False):
    if not os.path.isfile(lems_file_name):
        real_lems_file = os.path.realpath(os.path.join(base_dir, lems_file_name))
    else:
        real_lems_file = os.path.realpath(lems_file_name)
    print_comment(b'Reloading data specified in LEMS file: %s (%s), base_dir: %s, cwd: %s' % (
     lems_file_name, real_lems_file, base_dir, os.getcwd()), True)
    traces = {}
    events = {}
    if plot:
        import matplotlib.pyplot as plt
    from lxml import etree
    base_lems_file_path = os.path.dirname(os.path.realpath(lems_file_name))
    tree = etree.parse(real_lems_file)
    sim = tree.getroot().find(b'Simulation')
    ns_prefix = b''
    possible_prefixes = [
     b'{http://www.neuroml.org/lems/0.7.2}']
    if sim is None:
        for pre in possible_prefixes:
            for comp in tree.getroot().findall(pre + b'Component'):
                if comp.attrib[b'type'] == b'Simulation':
                    ns_prefix = pre
                    sim = comp

    if reload_events:
        event_output_files = sim.findall(ns_prefix + b'EventOutputFile')
        for i, of in enumerate(event_output_files):
            name = of.attrib[b'fileName']
            file_name = os.path.join(base_dir, name)
            if not os.path.isfile(file_name):
                file_name = os.path.join(base_lems_file_path, name)
            if not os.path.isfile(file_name):
                raise OSError(b'Could not find simulation output file %s' % file_name)
            format = of.attrib[b'format']
            print_comment(b'Loading saved events from %s (format: %s)' % (file_name, format), True)
            selections = {}
            for col in of.findall(ns_prefix + b'EventSelection'):
                id = int(col.attrib[b'id'])
                select = col.attrib[b'select']
                events[select] = []
                selections[id] = select

            with open(file_name) as (f):
                for line in f:
                    values = line.split()
                    if format == b'TIME_ID':
                        t = float(values[0])
                        id = int(values[1])
                    elif format == b'ID_TIME':
                        id = int(values[0])
                        t = float(values[1])
                    events[selections[id]].append(t)

            if remove_dat_files_after_load:
                print_comment_v(b'Removing file %s after having loading its data!' % file_name)
                os.remove(file_name)

    output_files = sim.findall(ns_prefix + b'OutputFile')
    n_output_files = len(output_files)
    if plot:
        rows = int(max(1, math.ceil(n_output_files / float(3))))
        columns = min(3, n_output_files)
        fig, ax = plt.subplots(rows, columns, sharex=True, figsize=(
         8 * columns, 4 * rows))
        if n_output_files > 1:
            ax = ax.ravel()
    for i, of in enumerate(output_files):
        traces[b't'] = []
        name = of.attrib[b'fileName']
        file_name = os.path.join(base_dir, name)
        if not os.path.isfile(file_name):
            file_name = os.path.join(base_lems_file_path, name)
        if not os.path.isfile(file_name):
            file_name = os.path.join(os.getcwd(), name)
        if not os.path.isfile(file_name):
            file_name = os.path.join(os.getcwd(), b'NeuroML2', b'results', name)
        if not os.path.isfile(file_name):
            raise OSError(b'Could not find simulation output file %s' % file_name)
        t_file_mod = datetime.fromtimestamp(os.path.getmtime(file_name))
        if t_file_mod < t_run:
            raise Exception(b'Expected output file %s has not been modified since %s but the simulation was run later at %s.' % (
             file_name, t_file_mod, t_run))
        print_comment(b'Loading saved data from %s%s' % (
         file_name, b' (%s)' % simulator if simulator else b''), verbose)
        cols = []
        cols.append(b't')
        for col in of.findall(ns_prefix + b'OutputColumn'):
            quantity = col.attrib[b'quantity']
            traces[quantity] = []
            cols.append(quantity)

        with open(file_name) as (f):
            for line in f:
                values = line.split()
                for vi in range(len(values)):
                    traces[cols[vi]].append(float(values[vi]))

        if remove_dat_files_after_load:
            print_comment_v(b'Removing file %s after having loading its data!' % file_name)
            os.remove(file_name)
        if plot:
            info = b'Data loaded from %s%s' % (
             file_name,
             b' (%s)' % simulator if simulator else b'')
            print_comment_v(b'Reloading: %s' % info)
            fig.canvas.set_window_title(info)
            legend = False
            for key in cols:
                if n_output_files > 1:
                    ax_ = ax[i]
                else:
                    ax_ = ax
                ax_.set_xlabel(b'Time (ms)')
                ax_.set_ylabel(b'(SI units...)')
                ax_.xaxis.grid(True)
                ax_.yaxis.grid(True)
                if key != b't':
                    ax_.plot(traces[b't'], traces[key], label=key)
                    print_comment(b'Adding trace for: %s, from: %s' % (
                     key, file_name), verbose)
                    ax_.used = True
                    legend = True
                if legend:
                    if n_output_files > 1:
                        ax_.legend(loc=b'upper right', fancybox=True, shadow=True, ncol=4)
                    else:
                        ax_.legend(loc=b'upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)

    if plot and show_plot_already:
        if n_output_files > 1:
            ax_ = ax
        else:
            ax_ = [
             ax]
        for axi in ax_:
            if not hasattr(axi, b'used') or not axi.used:
                axi.axis(b'off')

        plt.tight_layout()
        plt.show()
    if reload_events:
        return (traces, events)
    else:
        return traces
        return


def get_next_hex_color(my_random=None):
    if my_random != None:
        return b'#%06x' % my_random.randint(0, 16777215)
    else:
        return b'#%06x' % random.randint(0, 16777215)
        return


def evaluate_arguments(args):
    DEFAULTS[b'v'] = args.verbose
    pre_args = b''
    files = b''
    post_args = b''
    exit_on_fail = True
    files = args.lems_file
    if args.nogui:
        post_args = b'-nogui'
    if args.sedml:
        post_args = b'-sedml'
    elif args.neuron is not None:
        num_neuron_args = len(args.neuron)
        if num_neuron_args < 0 or num_neuron_args > 4:
            print_comment(b"ERROR: The '-neuron' option was given an invalid number of arguments: %d given, 0-4 required" % num_neuron_args)
            sys.exit(-1)
        post_args = b'-neuron %s' % (b' ').join(args.neuron[:-1])
    elif args.svg:
        post_args = b'-svg'
    elif args.png:
        post_args = b'-png'
    elif args.dlems:
        post_args = b'-dlems'
    elif args.vertex:
        post_args = b'-vertex'
    elif args.xpp:
        post_args = b'-xpp'
    elif args.dnsim:
        post_args = b'-dnsim'
    elif args.brian:
        post_args = b'-brian'
    elif args.sbml:
        post_args = b'-sbml'
    elif args.matlab:
        post_args = b'-matlab'
    elif args.cvode:
        post_args = b'-cvode'
    elif args.nineml:
        post_args = b'-nineml'
    elif args.spineml:
        post_args = b'-spineml'
    elif args.sbml_import:
        pre_args = b'-sbml-import'
        files = args.sbml_import[0]
        post_args = (b' ').join(args.sbml_import[1:])
    elif args.sbml_import_units:
        pre_args = b'-smbl-import-units'
        files = args.sbml_import_units[0]
        post_args = (b' ').join(args.sbml_import_units[1:])
    elif args.vhdl:
        files = args.vhdl[1]
        post_args = b'-vhdl %s' % args.vhdl[0]
    elif args.graph:
        from neuromllite.GraphVizHandler import GraphVizHandler, engines
        engine = b'dot'
        try:
            level = int(args.graph[0])
        except:
            engine = engines[args.graph[0][-1:]]
            level_int = args.graph[0][:-1]
            level_int = level_int.replace(b'min', b'-')
            level_int = level_int.replace(b'm', b'-')
            level = int(level_int)

        print_comment(b'Converting %s to graphical form, level %i, engine %s' % (args.lems_file, level, engine))
        from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser
        handler = GraphVizHandler(level=level, engine=engine, nl_network=None)
        currParser = NeuroMLXMLParser(handler)
        currParser.parse(args.lems_file)
        handler.finalise_document()
        print_comment(b'Done with GraphViz...')
        exit()
    elif args.matrix:
        from neuromllite.MatrixHandler import MatrixHandler
        level = int(args.matrix[0])
        print_comment(b'Converting %s to matrix form, level %i' % (args.lems_file, level))
        from neuroml.hdf5.NeuroMLXMLParser import NeuroMLXMLParser
        handler = MatrixHandler(level=level, nl_network=None)
        currParser = NeuroMLXMLParser(handler)
        currParser.parse(args.lems_file)
        handler.finalise_document()
        print_comment(b'Done with MatrixHandler...')
        exit()
    elif args.validate:
        pre_args = b'-validate'
        exit_on_fail = True
    elif args.validatev1:
        pre_args = b'-validatev1'
        exit_on_fail = True
    run_jneuroml(pre_args, files, post_args, max_memory=args.java_max_memory, exit_on_fail=exit_on_fail)
    return


def get_path_to_jnml_jar():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    jar_path = os.path.join(script_dir, b'lib', b'jNeuroML-%s-jar-with-dependencies.jar' % JNEUROML_VERSION)
    return jar_path


def run_jneuroml(pre_args, target_file, post_args, max_memory=DEFAULTS[b'default_java_max_memory'], exec_in_dir=b'.', verbose=DEFAULTS[b'v'], report_jnml_output=True, exit_on_fail=True):
    print_comment(b'Running jnml on %s with pre args: %s, post args: %s, in dir: %s, verbose: %s, report: %s, exit on fail: %s' % (
     target_file, pre_args, post_args, exec_in_dir, verbose, report_jnml_output, exit_on_fail), verbose)
    if b'nogui' in post_args and not os.name == b'nt':
        pre_jar = b' -Djava.awt.headless=true'
    else:
        pre_jar = b''
    jar_path = get_path_to_jnml_jar()
    output = b''
    try:
        command = b'java -Xmx%s %s -jar  "%s" %s "%s" %s' % (
         max_memory, pre_jar, jar_path, pre_args, target_file, post_args)
        output = execute_command_in_dir(command, exec_in_dir, verbose=verbose, prefix=b' jNeuroML >>  ')
        if not output:
            if exit_on_fail:
                print_comment(b'Error: execute_command_in_dir returned with output: %s' % output, True)
                sys.exit(-1)
            else:
                return False
        if report_jnml_output:
            print_comment(b'Successfully ran the following command using pyNeuroML v%s: \n    %s' % (__version__, command), True)
            print_comment(b'Output:\n\n%s' % output, True)
    except Exception as e:
        print_comment(b'*** Execution of jnml has failed! ***', True)
        print_comment(b'Error:  %s' % e)
        print_comment(b'*** Command: %s ***' % command, True)
        print_comment(b'Output: %s' % output, True)
        if exit_on_fail:
            sys.exit(-1)
        else:
            return False

    return True


def run_jneuroml_with_realtime_output(pre_args, target_file, post_args, max_memory=DEFAULTS[b'default_java_max_memory'], exec_in_dir=b'.', verbose=DEFAULTS[b'v'], exit_on_fail=True):
    if b'nogui' in post_args and not os.name == b'nt':
        pre_jar = b' -Djava.awt.headless=true'
    else:
        pre_jar = b''
    jar_path = get_path_to_jnml_jar()
    command = b''
    output = b''
    try:
        command = b'java -Xmx%s %s -jar  "%s" %s "%s" %s' % (
         max_memory, pre_jar, jar_path, pre_args, target_file, post_args)
        output = execute_command_in_dir_with_realtime_output(command, exec_in_dir, verbose=verbose, prefix=b' jNeuroML >>  ')
    except KeyboardInterrupt as e:
        raise e
    except:
        print_comment(b'*** Execution of jnml has failed! ***', True)
        print_comment(b'*** Command: %s ***' % command, True)
        if exit_on_fail:
            sys.exit(-1)
        else:
            return False

    return True


def print_comment_v(text, end=b'\n'):
    print_comment(text, True, end)


def print_comment(text, print_it=DEFAULTS[b'v'], end=b'\n'):
    prefix = b'pyNeuroML >>> '
    if not isinstance(text, str):
        text = text.decode(b'ascii')
    if print_it:
        print(b'%s%s' % (prefix, text.replace(b'\n', b'\n' + prefix)), end=end)


def execute_command_in_dir_with_realtime_output(command, directory, verbose=DEFAULTS[b'v'], prefix=b'Output: ', env=None):
    if os.name == b'nt':
        directory = os.path.normpath(directory)
    print_comment(b'Executing: (%s) in directory: %s' % (command, directory), verbose)
    if env is not None:
        print_comment(b'Extra env variables %s' % env, verbose)
    p = None
    try:
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, bufsize=1, cwd=directory, env=env)
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                print_comment(line, end=b'')

        p.wait()
    except KeyboardInterrupt as e:
        print_comment_v(b'*** Command interrupted: \n       %s' % command)
        if p:
            p.kill()
        raise e

    if not p.returncode == 0:
        print_comment_v(b'*** Problem running command (return code: %s): \n       %s' % (p.returncode, command))
    return p.returncode == 0


def execute_command_in_dir(command, directory, verbose=DEFAULTS[b'v'], prefix=b'Output: ', env=None):
    """Execute a command in specific working directory"""
    if os.name == b'nt':
        directory = os.path.normpath(directory)
    print_comment(b'Executing: (%s) in directory: %s' % (command, directory), verbose)
    if env is not None:
        print_comment(b'Extra env variables %s' % env, verbose)
    try:
        if os.name == b'nt':
            return_string = subprocess.check_output(command, cwd=directory, shell=True, env=env, close_fds=False)
        else:
            return_string = subprocess.check_output(command, cwd=directory, shell=True, stderr=subprocess.STDOUT, env=env, close_fds=True)
        return_string = return_string.decode(b'utf-8')
        print_comment(b'Command completed. Output: \n %s%s' % (
         prefix, return_string.replace(b'\n', b'\n ' + prefix)), verbose)
        return return_string
    except AttributeError:
        print_comment_v(b'Assuming Python 2.6...')
        return_string = subprocess.Popen(command, cwd=directory, shell=True, stdout=subprocess.PIPE).communicate()[0]
        return return_string
    except subprocess.CalledProcessError as e:
        print_comment_v(b'*** Problem running command: \n       %s' % e)
        print_comment_v(b'%s%s' % (prefix, e.output.decode().replace(b'\n', b'\n' + prefix)))
        return
    except:
        print_comment_v(b'*** Unknown problem running command: %s' % e)
        return

    print_comment(b'Finished execution', verbose)
    return


def generate_plot(xvalues, yvalues, title, labels=None, colors=None, linestyles=None, linewidths=None, markers=None, markersizes=None, xaxis=None, yaxis=None, xlim=None, ylim=None, show_xticklabels=True, show_yticklabels=True, grid=False, logx=False, logy=False, font_size=12, bottom_left_spines_only=False, cols_in_legend_box=3, legend_position=None, show_plot_already=True, save_figure_to=None, title_above_plot=False, verbose=False):
    print_comment_v(b'Generating plot: %s' % title)
    from matplotlib import pyplot as plt
    from matplotlib import rcParams
    rcParams.update({b'font.size': font_size})
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.canvas.set_window_title(title)
    if title_above_plot:
        plt.title(title)
    if xaxis:
        plt.xlabel(xaxis)
    if yaxis:
        plt.ylabel(yaxis)
    if grid:
        plt.grid(b'on')
    if logx:
        ax.set_xscale(b'log')
    if logy:
        ax.set_yscale(b'log')
    if bottom_left_spines_only:
        ax.spines[b'right'].set_visible(False)
        ax.spines[b'top'].set_visible(False)
        ax.yaxis.set_ticks_position(b'left')
        ax.xaxis.set_ticks_position(b'bottom')
    if not show_xticklabels:
        ax.set_xticklabels([])
    if not show_yticklabels:
        ax.set_yticklabels([])
    for i in range(len(xvalues)):
        linestyle = b'-' if not linestyles else linestyles[i]
        label = b'' if not labels else labels[i]
        marker = None if not markers else markers[i]
        linewidth = 1 if not linewidths else linewidths[i]
        markersize = 6 if not markersizes else markersizes[i]
        if colors:
            plt.plot(xvalues[i], yvalues[i], b'o', color=colors[i], marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, label=label)
        else:
            plt.plot(xvalues[i], yvalues[i], b'o', marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, label=label)

    if labels:
        if legend_position == b'right':
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(loc=b'center left', bbox_to_anchor=(1, 0.5))
        else:
            plt.legend(loc=b'upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=cols_in_legend_box)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    if save_figure_to:
        print_comment(b'Saving image to %s of plot: %s' % (os.path.abspath(save_figure_to), title), verbose)
        plt.savefig(save_figure_to, bbox_inches=b'tight')
        print_comment_v(b'Saved image to %s of plot: %s' % (save_figure_to, title))
    if show_plot_already:
        plt.show()
    return ax


def reload_standard_dat_file(file_name):
    dat_file = open(file_name)
    data = {}
    indeces = []
    for line in dat_file:
        words = line.split()
        if b't' not in data.keys():
            data[b't'] = []
            for i in range(len(words) - 1):
                data[i] = []
                indeces.append(i)

        data[b't'].append(float(words[0]))
        for i in range(len(words) - 1):
            data[i].append(float(words[(i + 1)]))

    print_comment_v(b'Loaded data from %s; columns: %s' % (file_name, indeces))
    dat_file.close()
    return (
     data, indeces)


def _find_elements(el, name, rdf=False):
    ns = b'http://www.neuroml.org/schema/neuroml2'
    if rdf:
        ns = b'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    return el.findall(b'.//{%s}%s' % (ns, name))


def _get_attr_in_element(el, name, rdf=False):
    ns = b'http://www.neuroml.org/schema/neuroml2'
    if rdf:
        ns = b'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    aname = b'{%s}%s' % (ns, name)
    if aname in el.attrib:
        return el.attrib[aname]
    else:
        return


def extract_annotations(nml2_file):
    from lxml import etree
    import pprint
    pp = pprint.PrettyPrinter()
    test_file = open(nml2_file)
    root = etree.parse(test_file).getroot()
    annotations = {}
    for a in _find_elements(root, b'annotation'):
        for r in _find_elements(a, b'Description', rdf=True):
            desc = _get_attr_in_element(r, b'about', rdf=True)
            annotations[desc] = []
            for info in r:
                if isinstance(info.tag, str):
                    kind = info.tag.replace(b'{http://biomodels.net/biology-qualifiers/}', b'bqbiol:')
                    kind = kind.replace(b'{http://biomodels.net/model-qualifiers/}', b'bqmodel:')
                    for li in _find_elements(info, b'li', rdf=True):
                        attr = _get_attr_in_element(li, b'resource', rdf=True)
                        if attr:
                            annotations[desc].append({kind: attr})

    print_comment_v(b'Annotations in %s: ' % nml2_file)
    pp.pprint(annotations)


def evaluate_component(comp_type, req_variables={}, parameter_values={}):
    print_comment(b'Evaluating %s with req:%s; params:%s' % (comp_type.name, req_variables, parameter_values))
    exec_str = b''
    return_vals = {}
    from math import exp
    for p in parameter_values:
        exec_str += b'%s = %s\n' % (p, get_value_in_si(parameter_values[p]))

    for r in req_variables:
        exec_str += b'%s = %s\n' % (r, get_value_in_si(req_variables[r]))

    for c in comp_type.Constant:
        exec_str += b'%s = %s\n' % (c.name, get_value_in_si(c.value))

    for d in comp_type.Dynamics:
        for dv in d.DerivedVariable:
            exec_str += b'%s = %s\n' % (dv.name, dv.value)
            exec_str += b'return_vals["%s"] = %s\n' % (dv.name, dv.name)

        for cdv in d.ConditionalDerivedVariable:
            for case in cdv.Case:
                if case.condition:
                    cond = case.condition.replace(b'.neq.', b'!=').replace(b'.eq.', b'==').replace(b'.gt.', b'<').replace(b'.lt.', b'<')
                    exec_str += b'if ( %s ): %s = %s \n' % (cond, cdv.name, case.value)
                else:
                    exec_str += b'else: %s = %s \n' % (cdv.name, case.value)

            exec_str += b'\n'
            exec_str += b'return_vals["%s"] = %s\n' % (cdv.name, cdv.name)

    exec exec_str
    return return_vals


def main(args=None):
    """Main"""
    if args is None:
        args = parse_arguments()
    evaluate_arguments(args)
    return


if __name__ == b'__main__':
    main()
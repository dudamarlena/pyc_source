# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/multiqc.py
# Compiled at: 2019-11-20 10:30:11
# Size of source mod 2**32: 37801 bytes
"""
multiqc.multiqc
~~~~~~~~~~~~~~~~~~~~~
The main function to run MultiQC. Sorry about the messy namespace.
Primarily called by multiqc.__main__.py
Imported by __init__.py so available as multiqc.run()
"""
from __future__ import print_function
import base64, click
from distutils import version
from distutils.dir_util import copy_tree
import errno, io, jinja2, os, re, shutil, subprocess, sys, tempfile, traceback
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
    reload(sys)
    sys.setdefaultencoding('utf8')

from .plots import table
from .utils import report, plugin_hooks, megaqc, util_functions, lint_helpers, config, log
logger = config.logger

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('analysis_dir', type=click.Path(exists=True),
  nargs=(-1),
  required=True,
  metavar='<analysis directory>')
@click.option('-f', '--force', is_flag=True,
  help='Overwrite any existing reports')
@click.option('-d', '--dirs', is_flag=True,
  help='Prepend directory to sample names')
@click.option('-dd', '--dirs-depth', 'dirs_depth', type=int,
  help='Prepend [INT] directories to sample names. Negative number to take from start of path.')
@click.option('-s', '--fullnames', 'no_clean_sname', is_flag=True,
  help='Do not clean the sample names (leave as full file name)')
@click.option('-i', '--title', type=str,
  help='Report title. Printed as page header, used for filename if not otherwise specified.')
@click.option('-b', '--comment', 'report_comment', type=str,
  help='Custom comment, will be printed at the top of the report.')
@click.option('-n', '--filename', type=str,
  help="Report filename. Use 'stdout' to print to standard out.")
@click.option('-o', '--outdir', type=str,
  help='Create report in the specified output directory.')
@click.option('-t', '--template', type=(click.Choice(config.avail_templates)),
  help='Report template to use.')
@click.option('--tag', 'module_tag', type=str,
  multiple=True,
  help='Use only modules which tagged with this keyword, eg. RNA')
@click.option('--view-tags', '--view_tags', is_flag=True,
  callback=(util_functions.view_all_tags),
  expose_value=False,
  is_eager=True,
  help='View the available tags and which modules they load')
@click.option('-x', '--ignore', type=str,
  multiple=True,
  help='Ignore analysis files (glob expression)')
@click.option('--ignore-samples', 'ignore_samples', type=str,
  multiple=True,
  help='Ignore sample names (glob expression)')
@click.option('--ignore-symlinks', 'ignore_symlinks', is_flag=True,
  help='Ignore symlinked directories and files')
@click.option('--sample-names', 'sample_names', type=click.Path(exists=True, readable=True),
  help='File containing alternative sample names')
@click.option('-l', '--file-list', is_flag=True,
  help='Supply a file containing a list of file paths to be searched, one per row')
@click.option('-e', '--exclude', metavar='[module name]', type=(click.Choice(sorted(['general_stats'] + list(config.avail_modules.keys())))),
  multiple=True,
  help='Do not use this module. Can specify multiple times.')
@click.option('-m', '--module', metavar='[module name]', type=(click.Choice(sorted(config.avail_modules.keys()))),
  multiple=True,
  help='Use only this module. Can specify multiple times.')
@click.option('--data-dir', 'make_data_dir', is_flag=True,
  help='Force the parsed data directory to be created.')
@click.option('--no-data-dir', 'no_data_dir', is_flag=True,
  help='Prevent the parsed data directory from being created.')
@click.option('-k', '--data-format', 'data_format', type=(click.Choice(config.data_format_extensions.keys())),
  help=('Output parsed data in a different format. Default: {}'.format(config.data_format)))
@click.option('-z', '--zip-data-dir', 'zip_data_dir', is_flag=True,
  help='Compress the data directory.')
@click.option('-p', '--export', 'export_plots', is_flag=True,
  help='Export plots as static images in addition to the report')
@click.option('-fp', '--flat', 'plots_flat', is_flag=True,
  help='Use only flat plots (static images)')
@click.option('-ip', '--interactive', 'plots_interactive', is_flag=True,
  help='Use only interactive plots (HighCharts Javascript)')
@click.option('--lint', 'lint', is_flag=True,
  help='Use strict linting (validation) to help code development')
@click.option('--pdf', 'make_pdf', is_flag=True,
  help="Creates PDF report with 'simple' template. Requires Pandoc to be installed.")
@click.option('--no-megaqc-upload', 'no_megaqc_upload', is_flag=True,
  help="Don't upload generated report to MegaQC, even if MegaQC options are found")
@click.option('-c', '--config', 'config_file', type=click.Path(exists=True, readable=True),
  multiple=True,
  help='Specific config file to load, after those in MultiQC dir / home dir / working dir.')
@click.option('--cl-config', '--cl_config', type=str,
  multiple=True,
  help='Specify MultiQC config YAML on the command line')
@click.option('-v', '--verbose', count=True,
  default=0,
  help='Increase output verbosity.')
@click.option('-q', '--quiet', is_flag=True,
  help='Only show log warnings')
@click.option('--no-ansi', is_flag=True,
  help='Disable coloured log output')
@click.version_option((config.version), prog_name='multiqc')
def run_cli(analysis_dir, dirs, dirs_depth, no_clean_sname, title, report_comment, template, module_tag, module, exclude, outdir, ignore, ignore_samples, sample_names, file_list, filename, make_data_dir, no_data_dir, data_format, zip_data_dir, force, ignore_symlinks, export_plots, plots_flat, plots_interactive, lint, make_pdf, no_megaqc_upload, config_file, cl_config, verbose, quiet, no_ansi, **kwargs):
    """
    Main MultiQC run command for use with the click command line, complete with all click function decorators.
    To make it easy to use MultiQC within notebooks and other locations that don't need click, we simply pass the
    parsed variables on to a vanilla python function.
    """
    sys_exit_code = run(analysis_dir=analysis_dir,
      dirs=dirs,
      dirs_depth=dirs_depth,
      no_clean_sname=no_clean_sname,
      title=title,
      report_comment=report_comment,
      template=template,
      module_tag=module_tag,
      module=module,
      exclude=exclude,
      outdir=outdir,
      ignore=ignore,
      ignore_samples=ignore_samples,
      sample_names=sample_names,
      file_list=file_list,
      filename=filename,
      make_data_dir=make_data_dir,
      no_data_dir=no_data_dir,
      data_format=data_format,
      zip_data_dir=zip_data_dir,
      force=force,
      ignore_symlinks=ignore_symlinks,
      export_plots=export_plots,
      plots_flat=plots_flat,
      plots_interactive=plots_interactive,
      lint=lint,
      make_pdf=make_pdf,
      no_megaqc_upload=no_megaqc_upload,
      config_file=config_file,
      cl_config=cl_config,
      verbose=verbose,
      quiet=quiet,
      no_ansi=no_ansi,
      kwargs=kwargs)
    sys.exit(sys_exit_code)


def run(analysis_dir, dirs, dirs_depth, no_clean_sname, title, report_comment, template, module_tag, module, exclude, outdir, ignore, ignore_samples, sample_names, file_list, filename, make_data_dir, no_data_dir, data_format, zip_data_dir, force, ignore_symlinks, export_plots, plots_flat, plots_interactive, lint, make_pdf, no_megaqc_upload, config_file, cl_config, verbose, quiet, no_ansi=FalseNoneFalseNoneNoneNone()()()None()()NoneFalseNoneFalseFalseNoneFalseTrueFalseFalseFalseFalseFalseFalseFalse()()0FalseFalse, kwargs={}):
    """MultiQC aggregates results from bioinformatics analyses across many samples into a single report.

        It searches a given directory for analysis logs and compiles a HTML report.
        It's a general use tool, perfect for summarising the output from numerous
        bioinformatics tools.

        To run, supply with one or more directory to scan for analysis results.
        To run here, use 'multiqc .'

        See http://multiqc.info for more details.

        Author: Phil Ewels (http://phil.ewels.co.uk)
    """
    loglevel = log.LEVELS.get(min(verbose, 1), 'INFO')
    if quiet:
        loglevel = 'WARNING'
    log.init_log(logger, loglevel=loglevel, no_ansi=no_ansi)
    plugin_hooks.mqc_trigger('before_config')
    config.mqc_load_userconfig(config_file)
    plugin_hooks.mqc_trigger('config_loaded')
    if len(cl_config) > 0:
        config.mqc_cl_config(cl_config)
    report.multiqc_command = ' '.join(sys.argv)
    logger.debug('Command used: {}'.format(report.multiqc_command))
    if config.no_version_check is not True:
        try:
            response = urlopen(('http://multiqc.info/version.php?v={}'.format(config.short_version)), timeout=5)
            remote_version = response.read().decode('utf-8').strip()
            if version.StrictVersion(re.sub('[^0-9\\.]', '', remote_version)) > version.StrictVersion(re.sub('[^0-9\\.]', '', config.short_version)):
                logger.warn('MultiQC Version {} now available!'.format(remote_version))
            else:
                logger.debug('Latest MultiQC version is {}'.format(remote_version))
        except Exception as e:
            logger.debug('Could not connect to multiqc.info for version check: {}'.format(e))

    if template is not None:
        config.template = template
    if title is not None:
        config.title = title
    if report_comment is not None:
        config.report_comment = report_comment
    if dirs is True:
        config.prepend_dirs = dirs
    if dirs_depth is not None:
        config.prepend_dirs = True
        config.prepend_dirs_depth = dirs_depth
    else:
        config.analysis_dir = analysis_dir
        if outdir is not None:
            config.output_dir = outdir
        if no_clean_sname:
            config.fn_clean_sample_names = False
            logger.info('Not cleaning sample names')
        if make_data_dir:
            config.make_data_dir = True
        if no_data_dir:
            config.make_data_dir = False
        if force:
            config.force = True
        if ignore_symlinks:
            config.ignore_symlinks = True
        if zip_data_dir:
            config.zip_data_dir = True
        if data_format is not None:
            config.data_format = data_format
        if export_plots:
            config.export_plots = True
        if plots_flat:
            config.plots_force_flat = True
        if plots_interactive:
            config.plots_force_interactive = True
        if lint:
            config.lint = True
            lint_helpers.run_tests()
        if make_pdf:
            config.template = 'simple'
        if no_megaqc_upload:
            config.megaqc_upload = False
        else:
            config.megaqc_upload = True
    if sample_names:
        config.load_sample_names(sample_names)
    if module_tag is not None:
        config.module_tag = module_tag
    if len(module) > 0:
        config.run_modules = module
    if len(exclude) > 0:
        config.exclude_modules = exclude
    config.kwargs = kwargs
    if isinstance(config.analysis_dir, str):
        config.analysis_dir = [
         config.analysis_dir]
    plugin_hooks.mqc_trigger('execution_start')
    logger.info('This is MultiQC v{}'.format(config.version))
    logger.debug('Command     : {}'.format(' '.join(sys.argv)))
    logger.debug('Working dir : {}'.format(os.getcwd()))
    if make_pdf:
        logger.info('--pdf specified. Using non-interactive HTML template.')
    else:
        logger.info('Template    : {}'.format(config.template))
        if lint:
            logger.info('--lint specified. Being strict with validation.')
        if sys.version_info[0] < 3:
            logger.warn('You are running MultiQC with Python {}.{}.{}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
            logger.warn('Please upgrade! MultiQC will soon drop support for Python < 3.6')
        else:
            logger.debug('Running Python {}'.format(sys.version.replace('\n', ' ')))
    if file_list:
        if len(analysis_dir) > 1:
            raise ValueError('If --file-list is giving, analysis_dir should have only one plain text file.')
        config.analysis_dir = []
        with open(analysis_dir[0]) as (in_handle):
            for line in in_handle:
                if os.path.exists(line.strip()):
                    path = os.path.abspath(line.strip())
                    config.analysis_dir.append(path)

        if len(config.analysis_dir) == 0:
            logger.error('No files or directories were added from {} using --file-list option.'.format(analysis_dir[0]))
            logger.error('Please, check that {} contains correct paths.'.format(analysis_dir[0]))
            raise ValueError('Any files or directories to be searched.')
    if len(ignore) > 0:
        logger.debug('Ignoring files, directories and paths that match: {}'.format(', '.join(ignore)))
        config.fn_ignore_files.extend(ignore)
        config.fn_ignore_dirs.extend(ignore)
        config.fn_ignore_paths.extend(ignore)
    if len(ignore_samples) > 0:
        logger.debug('Ignoring sample names that match: {}'.format(', '.join(ignore_samples)))
        config.sample_names_ignore.extend(ignore_samples)
    if filename == 'stdout':
        config.output_fn = sys.stdout
        logger.info('Printing report to stdout')
    elif title is not None:
        if filename is None:
            filename = re.sub('[^\\w\\.-]', '', re.sub('[-\\s]+', '-', title)).strip()
            filename += '_multiqc_report'
        else:
            if filename is not None:
                if filename.endswith('.html'):
                    filename = filename[:-5]
                config.output_fn_name = filename
                config.data_dir_name = '{}_data'.format(filename)
            else:
                if not config.output_fn_name.endswith('.html'):
                    config.output_fn_name = '{}.html'.format(config.output_fn_name)
                if config.title is not None:
                    logger.info('Report title: {}'.format(config.title))
            if dirs:
                logger.info('Prepending directory to sample names')
        for d in config.analysis_dir:
            logger.info('Searching   : {}'.format(os.path.abspath(d)))

        config.top_modules = [m if type(m) is dict else {m: {}} for m in config.top_modules]
        config.module_order = [m if type(m) is dict else {m: {}} for m in config.module_order]
        mod_keys = [list(m.keys())[0] for m in config.module_order]
        if config.lint:
            for m in config.avail_modules.keys():
                if m not in mod_keys:
                    errmsg = "LINT: Module '{}' not found in config.module_order".format(m)
                    logger.error(errmsg)
                    report.lint_errors.append(errmsg)
                else:
                    for mo in config.module_order:
                        if m != 'custom_content' and m in mo.keys() and 'module_tag' not in mo[m]:
                            errmsg = "LINT: Module '{}' in config.module_order did not have 'module_tag' config".format(m)
                            logger.error(errmsg)
                            report.lint_errors.append(errmsg)

    else:
        modules_from_tags = set()
        if config.module_tag is not None:
            tags = config.module_tag
            for m in config.module_order:
                module_name = list(m.keys())[0]
                for tag in tags:
                    for t in m[module_name].get('module_tag', []):
                        if tag.lower() == t.lower():
                            modules_from_tags.add(module_name)

        run_modules = [m for m in config.top_modules if list(m.keys())[0] in config.avail_modules.keys()]
        run_modules.extend([{m: {}} for m in config.avail_modules.keys() if m not in mod_keys if m not in run_modules])
        run_modules.extend([m for m in config.module_order if list(m.keys())[0] in config.avail_modules.keys() if list(m.keys())[0] not in [list(rm.keys())[0] for rm in run_modules]])
        if len(getattr(config, 'run_modules', {})) > 0:
            run_modules = [m for m in run_modules if list(m.keys())[0] in config.run_modules]
            logger.info('Only using modules {}'.format(', '.join(config.run_modules)))
        elif modules_from_tags:
            run_modules = [m for m in run_modules if list(m.keys())[0] in modules_from_tags]
            logger.info("Only using modules with '{}' tag".format(', '.join(module_tag)))
    if len(getattr(config, 'exclude_modules', {})) > 0:
        logger.info("Excluding modules '{}'".format("', '".join(config.exclude_modules)))
        if 'general_stats' in config.exclude_modules:
            config.skip_generalstats = True
            config.exclude_modules = tuple(x for x in config.exclude_modules if x != 'general_stats')
        run_modules = [m for m in run_modules if list(m.keys())[0] not in config.exclude_modules]
    if len(run_modules) == 0:
        logger.critical('No analysis modules specified!')
        sys.exit(1)
    else:
        run_module_names = [list(m.keys())[0] for m in run_modules]
        logger.debug('Analysing modules: {}'.format(', '.join(run_module_names)))
        tmp_dir = tempfile.mkdtemp()
        logger.debug('Using temporary directory for creating report: {}'.format(tmp_dir))
        config.data_tmp_dir = os.path.join(tmp_dir, 'multiqc_data')
        if filename != 'stdout':
            if config.make_data_dir == True:
                config.data_dir = config.data_tmp_dir
                os.makedirs(config.data_dir)
        config.data_dir = None
    config.plots_tmp_dir = os.path.join(tmp_dir, 'multiqc_plots')
    if filename != 'stdout':
        if config.export_plots == True:
            config.plots_dir = config.plots_tmp_dir
            os.makedirs(config.plots_dir)
    template_mod = config.avail_templates[config.template].load()
    try:
        config.output_dir = os.path.join(config.output_dir, template_mod.output_subdir)
    except AttributeError:
        pass

    try:
        if 'custom_content' in run_module_names:
            run_module_names.extend(config.custom_data.keys())
    except AttributeError:
        pass

    report.get_filelist(run_module_names)
    plugin_hooks.mqc_trigger('before_modules')
    report.modules_output = list()
    sys_exit_code = 0
    for mod_dict in run_modules:
        try:
            this_module = list(mod_dict.keys())[0]
            mod_cust_config = list(mod_dict.values())[0]
            mod = config.avail_modules[this_module].load()
            mod.mod_cust_config = mod_cust_config
            output = mod()
            if type(output) != list:
                output = [
                 output]
            for m in output:
                report.modules_output.append(m)

            try:
                for to, path in report.modules_output[(-1)].css.items():
                    copy_to = os.path.join(tmp_dir, to)
                    os.makedirs(os.path.dirname(copy_to))
                    shutil.copyfile(path, copy_to)

            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise
            except AttributeError:
                pass

            try:
                for to, path in report.modules_output[(-1)].js.items():
                    copy_to = os.path.join(tmp_dir, to)
                    os.makedirs(os.path.dirname(copy_to))
                    shutil.copyfile(path, copy_to)

            except OSError as e:
                if e.errno == errno.EEXIST:
                    pass
                else:
                    raise
            except AttributeError:
                pass

        except UserWarning:
            logger.debug('No samples found: {}'.format(list(mod_dict.keys())[0]))
        except KeyboardInterrupt:
            shutil.rmtree(tmp_dir)
            logger.critical('User Cancelled Execution!\n{eq}\n{tb}{eq}\n'.format(eq=('=' * 60),
              tb=(traceback.format_exc())) + 'User Cancelled Execution!\nExiting MultiQC...')
            sys.exit(1)
        except:
            logger.error("Oops! The '{}' MultiQC module broke... \n".format(this_module) + '  Please copy the following traceback and report it at ' + 'https://github.com/ewels/MultiQC/issues \n' + '  If possible, please include a log file that triggers the error - ' + 'the last file found was:\n' + '    {}\n'.format(report.last_found_file) + '=' * 60 + '\nModule {} raised an exception: {}'.format(this_module, traceback.format_exc()) + '=' * 60)
            sys_exit_code = 1

    if len(report.modules_output) == 0:
        logger.warn('No analysis results found. Cleaning up..')
        shutil.rmtree(tmp_dir)
        logger.info('MultiQC complete')
        sys.exit(sys_exit_code)
    if len(getattr(config, 'report_section_order', {})) > 0:
        section_id_order = {}
        idx = 10
        for mod in reversed(report.modules_output):
            section_id_order[mod.anchor] = idx
            idx += 10

        for anchor, ss in config.report_section_order.items():
            if anchor not in section_id_order.keys():
                logger.debug("Reordering sections: anchor '{}' not found.".format(anchor))
            else:
                if ss.get('order') is not None:
                    section_id_order[anchor] = ss['order']
                if ss.get('after') in section_id_order.keys():
                    section_id_order[anchor] = section_id_order[ss['after']] + 1
                if ss.get('before') in section_id_order.keys():
                    section_id_order[anchor] = section_id_order[ss['before']] - 1

        sorted_ids = sorted(section_id_order, key=(section_id_order.get))
        report.modules_output = [mod for i in reversed(sorted_ids) for mod in report.modules_output if mod.anchor == i]
    if len(getattr(config, 'report_section_order', {})) > 0:
        for midx, mod in enumerate(report.modules_output):
            section_id_order = {}
            idx = 10
            for s in mod.sections:
                section_id_order[s['anchor']] = idx
                idx += 10

            for anchor, ss in config.report_section_order.items():
                if anchor not in section_id_order.keys():
                    logger.debug("Reordering sections: anchor '{}' not found for module '{}'.".format(anchor, mod.name))
                else:
                    if ss == 'remove':
                        section_id_order[anchor] = False
                    else:
                        if ss.get('order') is not None:
                            section_id_order[anchor] = ss['order']
                        if ss.get('after') in section_id_order.keys():
                            section_id_order[anchor] = section_id_order[ss['after']] + 1
                        if ss.get('before') in section_id_order.keys():
                            section_id_order[anchor] = section_id_order[ss['before']] - 1

            section_id_order = {s:o for s, o in section_id_order.items() if o is not False if o is not False}
            sorted_ids = sorted(section_id_order, key=(section_id_order.get))
            report.modules_output[midx].sections = [s for i in sorted_ids if s['anchor'] == i for s in mod]

    else:
        plugin_hooks.mqc_trigger('after_modules')
        empty_keys = [i for i, d in enumerate(report.general_stats_data[:]) if len(d) == 0]
        empty_keys.sort(reverse=True)
        for i in empty_keys:
            del report.general_stats_data[i]
            del report.general_stats_headers[i]

        for idx, h in enumerate(report.general_stats_headers):
            for k in h.keys():
                if 'rid' not in h[k]:
                    h[k]['rid'] = re.sub('\\W+', '_', k).strip().strip('_')
                ns_html = re.sub('\\W+', '_', h[k]['namespace']).strip().strip('_').lower()
                report.general_stats_headers[idx][k]['rid'] = report.save_htmlid('mqc-generalstats-{}-{}'.format(ns_html, h[k]['rid']))

        if len(report.general_stats_data) > 0:
            pconfig = {'id':'general_stats_table',  'table_title':'General Statistics', 
             'save_file':True, 
             'raw_data_fn':'multiqc_general_stats'}
            report.general_stats_html = table.plot(report.general_stats_data, report.general_stats_headers, pconfig)
        else:
            config.skip_generalstats = True
        if config.data_dir is not None:
            report.data_sources_tofile()
        logger.info('Compressing plot data')
        report.plot_compressed_json = report.compress_json(report.plot_data)
        plugin_hooks.mqc_trigger('before_report_generation')
        if config.data_dump_file or config.megaqc_url:
            if config.megaqc_upload:
                multiqc_json_dump = megaqc.multiqc_dump_json(report)
                if config.data_dump_file:
                    util_functions.write_data_file(multiqc_json_dump, 'multiqc_data', False, 'json')
                if config.megaqc_url:
                    megaqc.multiqc_api_post(multiqc_json_dump)
        if filename != 'stdout':
            config.output_fn = os.path.join(config.output_dir, config.output_fn_name)
            config.data_dir = os.path.join(config.output_dir, config.data_dir_name)
            if os.path.exists(config.output_fn) or config.make_data_dir and os.path.exists(config.data_dir):
                if config.force:
                    if os.path.exists(config.output_fn):
                        logger.warning('Deleting    : {}   (-f was specified)'.format(os.path.relpath(config.output_fn)))
                        os.remove(config.output_fn)
                    if config.make_data_dir:
                        if os.path.exists(config.data_dir):
                            logger.warning('Deleting    : {}   (-f was specified)'.format(os.path.relpath(config.data_dir)))
                            shutil.rmtree(config.data_dir)
                else:
                    report_num = 1
                    report_base, report_ext = os.path.splitext(config.output_fn_name)
                    dir_base = os.path.basename(config.data_dir)
                    while os.path.exists(config.output_fn) or config.make_data_dir and os.path.exists(config.data_dir):
                        config.output_fn = os.path.join(config.output_dir, '{}_{}{}'.format(report_base, report_num, report_ext))
                        config.data_dir = os.path.join(config.output_dir, '{}_{}'.format(dir_base, report_num))
                        report_num += 1

                    config.output_fn_name = os.path.basename(config.output_fn)
                    config.data_dir_name = os.path.basename(config.data_dir)
                    logger.warning('Previous MultiQC output found! Adjusting filenames..')
                    logger.warning('Use -f or --force to overwrite existing reports instead')
            if not os.path.exists(os.path.dirname(config.output_fn)):
                os.makedirs(os.path.dirname(config.output_fn))
            logger.info('Report      : {}'.format(os.path.relpath(config.output_fn)))
            if config.make_data_dir == False:
                logger.info('Data        : None')
            else:
                logger.info('Data        : {}'.format(os.path.relpath(config.data_dir)))
                if not os.path.exists(config.data_dir):
                    os.makedirs(config.data_dir)
                for f in os.listdir(config.data_tmp_dir):
                    fn = os.path.join(config.data_tmp_dir, f)
                    logger.debug("Moving data file from '{}' to '{}'".format(fn, config.data_dir))
                    shutil.move(fn, config.data_dir)

            if config.export_plots:
                config.plots_dir = os.path.join(config.output_dir, config.plots_dir_name)
                if os.path.exists(config.plots_dir):
                    if config.force:
                        logger.warning('Deleting    : {}   (-f was specified)'.format(os.path.relpath(config.plots_dir)))
                        shutil.rmtree(config.plots_dir)
                    else:
                        logger.error('Output directory {} already exists.'.format(config.plots_dir))
                        logger.info('Use -f or --force to overwrite existing reports')
                        shutil.rmtree(tmp_dir)
                        sys.exit(1)
                os.makedirs(config.plots_dir)
                logger.info('Plots       : {}'.format(os.path.relpath(config.plots_dir)))
                for f in os.listdir(config.plots_tmp_dir):
                    fn = os.path.join(config.plots_tmp_dir, f)
                    logger.debug("Moving plots directory from '{}' to '{}'".format(fn, config.plots_dir))
                    shutil.move(fn, config.plots_dir)

        plugin_hooks.mqc_trigger('before_template')
        try:
            parent_template = config.avail_templates[template_mod.template_parent].load()
            copy_tree(parent_template.template_dir, tmp_dir)
        except AttributeError:
            pass

        copy_tree(template_mod.template_dir, tmp_dir)

        def include_file(name, fdir=tmp_dir, b64=False):
            try:
                if fdir is None:
                    fdir = ''
                else:
                    if b64:
                        with io.open(os.path.join(fdir, name), 'rb') as (f):
                            return base64.b64encode(f.read()).decode('utf-8')
                    else:
                        with io.open((os.path.join(fdir, name)), 'r', encoding='utf-8') as (f):
                            return f.read()
            except (OSError, IOError) as e:
                logger.error("Could not include file '{}': {}".format(name, e))

        try:
            env = jinja2.Environment(loader=(jinja2.FileSystemLoader(tmp_dir)))
            env.globals['include_file'] = include_file
            j_template = env.get_template(template_mod.base_fn)
        except:
            raise IOError("Could not load {} template file '{}'".format(config.template, template_mod.base_fn))

        config.analysis_dir = [os.path.realpath(d) for d in config.analysis_dir]
        report_output = j_template.render(report=report, config=config)
        if filename == 'stdout':
            print((report_output.encode('utf-8')), file=(sys.stdout))
        else:
            try:
                with io.open((config.output_fn), 'w', encoding='utf-8') as (f):
                    print(report_output, file=f)
            except IOError as e:
                raise IOError("Could not print report to '{}' - {}".format(config.output_fn, IOError(e)))

    try:
        for f in template_mod.copy_files:
            fn = os.path.join(tmp_dir, f)
            dest_dir = os.path.join(os.path.dirname(config.output_fn), f)
            copy_tree(fn, dest_dir)

    except AttributeError:
        pass

    shutil.rmtree(tmp_dir)
    if config.zip_data_dir:
        if config.data_dir is not None:
            shutil.make_archive(config.data_dir, 'zip', config.data_dir)
            shutil.rmtree(config.data_dir)
    if make_pdf:
        try:
            pdf_fn_name = config.output_fn.replace('.html', '.pdf')
            pandoc_call = [
             'pandoc',
             '--standalone',
             config.output_fn,
             '--output', pdf_fn_name,
             '--pdf-engine=xelatex',
             '-V', 'documentclass=article',
             '-V', 'geometry=margin=1in',
             '-V', 'title=']
            if config.pandoc_template is not None:
                pandoc_call.append('--template={}'.format(config.pandoc_template))
            logger.debug('Attempting Pandoc conversion to PDF with following command:\n{}'.format(' '.join(pandoc_call)))
            pdf_exit_code = subprocess.call(pandoc_call)
            if pdf_exit_code != 0:
                logger.error('Error creating PDF! Pandoc returned a non-zero exit code.')
            else:
                logger.info('PDF Report  : {}'.format(pdf_fn_name))
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                logger.error('Error creating PDF - pandoc not found. Is it installed? http://pandoc.org/')
            else:
                logger.error('Error creating PDF! Something went wrong when creating the PDF\n' + '=' * 60 + '\n{}\n'.format(traceback.format_exc()) + '=' * 60)

    plugin_hooks.mqc_trigger('execution_finish')
    logger.info('MultiQC complete')
    if lint:
        if len(report.lint_errors) > 0:
            logger.error('Found {} linting errors!\n{}'.format(len(report.lint_errors), '\n'.join(report.lint_errors)))
            sys_exit_code = 1
    log.move_tmp_log(logger)
    return sys_exit_code
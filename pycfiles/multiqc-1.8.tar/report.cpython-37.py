# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/report.py
# Compiled at: 2019-11-13 05:22:42
# Size of source mod 2**32: 16123 bytes
""" MultiQC report module. Holds the output from each
module. Is available to subsequent modules. Contains
helper functions to generate markup for report. """
from __future__ import print_function
from collections import defaultdict, OrderedDict
import click, fnmatch, io, json, inspect, lzstring, mimetypes, os, re, yaml
from multiqc import config
logger = config.logger
from yaml.representer import Representer, SafeRepresenter
yaml.add_representer(defaultdict, Representer.represent_dict)
yaml.add_representer(OrderedDict, Representer.represent_dict)
try:
    yaml.add_representer(unicode, SafeRepresenter.represent_unicode)
except NameError:
    pass

general_stats_data = list()
general_stats_headers = list()
general_stats_html = ''
data_sources = defaultdict(lambda : defaultdict(lambda : defaultdict()))
plot_data = dict()
html_ids = list()
lint_errors = list()
num_hc_plots = 0
num_mpl_plots = 0
saved_raw_data = dict()
last_found_file = None
searchfiles = list()
files = dict()

def get_filelist(run_module_names):
    """
    Go through all supplied search directories and assembly a master
    list of files to search. Then fire search functions for each file.
    """
    spatterns = [{}, {}, {}, {}, {}, {}, {}]
    epatterns = [{}, {}]
    ignored_patterns = []
    for key, sps in config.sp.items():
        mod_name = key.split('/', 1)[0]
        if mod_name.lower() not in [m.lower() for m in run_module_names]:
            ignored_patterns.append(key)
            continue
        files[key] = list()
        if not isinstance(sps, list):
            sps = [
             sps]
        expected_sp_keys = [
         'fn',
         'fn_re',
         'contents',
         'contents_re',
         'num_lines',
         'shared',
         'max_filesize',
         'exclude_fn',
         'exclude_fn_re',
         'exclude_contents',
         'exclude_contents_re']
        unrecognised_keys = [y for x in sps if y not in expected_sp_keys for y in x.keys()]
        if len(unrecognised_keys) > 0:
            logger.warn("Unrecognised search pattern keys for '{}': {}".format(key, ', '.join(unrecognised_keys)))
        if any([x for x in sps if 'contents_re' in x]):
            if any([x for x in sps if 'num_lines' in x]):
                spatterns[4][key] = sps
            else:
                if any([x for x in sps if 'max_filesize' in x]):
                    spatterns[5][key] = sps
                else:
                    spatterns[6][key] = sps
        elif any([x for x in sps if 'contents' in x]):
            if any([x for x in sps if 'num_lines' in x]):
                spatterns[1][key] = sps
            else:
                if any([x for x in sps if 'max_filesize' in x]):
                    spatterns[2][key] = sps
                else:
                    spatterns[3][key] = sps
        else:
            spatterns[0][key] = sps

    if len(ignored_patterns) > 0:
        logger.debug("Ignored {} search patterns as didn't match running modules.".format(len(ignored_patterns)))

    def add_file(fn, root):
        f = {'fn':fn, 
         'root':root}
        if not os.path.isfile(os.path.join(root, fn)):
            return
        i_matches = [n for n in config.fn_ignore_files if fnmatch.fnmatch(fn, n)]
        if len(i_matches) > 0:
            logger.debug('Ignoring file as matched an ignore pattern: {}'.format(fn))
            return
        try:
            f['filesize'] = os.path.getsize(os.path.join(root, fn))
        except (IOError, OSError, ValueError, UnicodeDecodeError):
            logger.debug("Couldn't read file when checking filesize: {}".format(fn))
        else:
            if f['filesize'] > config.log_filesize_limit:
                return False

    multiqc_installation_dir_files = [
     'LICENSE', 'CHANGELOG.md', 'Dockerfile', 'MANIFEST.in', '.gitmodules', 'README.md', 'CSP.txt', 'appveyor.yml', 'setup.py', '.gitignore', '.travis.yml']
    for path in config.analysis_dir:
        if os.path.islink(path):
            if config.ignore_symlinks:
                continue
        else:
            if os.path.isfile(path):
                searchfiles.append([os.path.basename(path), os.path.dirname(path)])
        if os.path.isdir(path):
            for root, dirnames, filenames in os.walk(path, followlinks=(not config.ignore_symlinks), topdown=True):
                bname = os.path.basename(root)
                orig_dirnames = dirnames[:]
                for n in config.fn_ignore_dirs:
                    dirnames[:] = [d for d in dirnames if not fnmatch.fnmatch(d, n.rstrip(os.sep))]
                    if len(orig_dirnames) != len(dirnames):
                        removed_dirs = [os.path.join(root, d) for d in set(orig_dirnames).symmetric_difference(set(dirnames))]
                        logger.debug('Ignoring directory as matched fn_ignore_dirs: {}'.format(', '.join(removed_dirs)))
                        orig_dirnames = dirnames[:]

                for n in config.fn_ignore_paths:
                    dirnames[:] = [d for d in dirnames if not fnmatch.fnmatch(os.path.join(root, d), n.rstrip(os.sep))]
                    if len(orig_dirnames) != len(dirnames):
                        removed_dirs = [os.path.join(root, d) for d in set(orig_dirnames).symmetric_difference(set(dirnames))]
                        logger.debug('Ignoring directory as matched fn_ignore_paths: {}'.format(', '.join(removed_dirs)))

                d_matches = [n for n in config.fn_ignore_dirs if fnmatch.fnmatch(bname, n.rstrip(os.sep))]
                if len(d_matches) > 0:
                    logger.debug('Ignoring directory as matched fn_ignore_dirs: {}'.format(bname))
                    continue
                p_matches = [n for n in config.fn_ignore_paths if fnmatch.fnmatch(root, n.rstrip(os.sep))]
                if len(p_matches) > 0:
                    logger.debug('Ignoring directory as matched fn_ignore_paths: {}'.format(root))
                    continue
                if len(filenames) > 0:
                    if all([fn in filenames for fn in multiqc_installation_dir_files]):
                        logger.error('Error: MultiQC is running in source code directory! {}'.format(root))
                        logger.warn('Please see the docs for how to use MultiQC: https://multiqc.info/docs/#running-multiqc')
                        dirnames[:] = []
                        filenames[:] = []
                        continue
                for fn in filenames:
                    searchfiles.append([fn, root])

    with click.progressbar(searchfiles, label=('Searching {} files..'.format(len(searchfiles)))) as (sfiles):
        for sf in sfiles:
            add_file(sf[0], sf[1])


def search_file(pattern, f, module_key):
    """
    Function to searach a single file for a single search pattern.
    """
    fn_matched = False
    contents_matched = False
    if not re.match('.+_mqc\\.(png|jpg|jpeg)', f['fn']):
        if config.ignore_images:
            ftype, encoding = mimetypes.guess_type(os.path.join(f['root'], f['fn']))
            if encoding is not None:
                return False
            if ftype is not None:
                if ftype.startswith('image'):
                    return False
    if pattern.get('max_filesize') is not None:
        if 'filesize' in f:
            if f['filesize'] > pattern.get('max_filesize'):
                logger.debug('File ignored by {} because it exceeded search pattern filesize limit: {}'.format(module_key, f['fn']))
                return False
    if pattern.get('fn') is not None:
        if fnmatch.fnmatch(f['fn'], pattern['fn']):
            fn_matched = True
            if pattern.get('contents') is None:
                if pattern.get('contents_re') is None:
                    return True
    if pattern.get('fn_re') is not None:
        if re.match(pattern['fn_re'], f['fn']):
            fn_matched = True
            if pattern.get('contents') is None:
                if pattern.get('contents_re') is None:
                    return True
    if pattern.get('contents') is not None or pattern.get('contents_re') is not None:
        if pattern.get('contents_re') is not None:
            repattern = re.compile(pattern['contents_re'])
        try:
            with io.open((os.path.join(f['root'], f['fn'])), 'r', encoding='utf-8') as (f):
                l = 1
                for line in f:
                    if pattern.get('contents') is not None:
                        if pattern['contents'] in line:
                            contents_matched = True
                            if pattern.get('fn') is None:
                                if pattern.get('fn_re') is None:
                                    return True
                            break
                    elif pattern.get('contents_re') is not None:
                        if re.search(repattern, line):
                            contents_matched = True
                            if pattern.get('fn') is None:
                                if pattern.get('fn_re') is None:
                                    return True
                            break
                    if pattern.get('num_lines'):
                        if l >= pattern.get('num_lines'):
                            break
                    l += 1

        except (IOError, OSError, ValueError, UnicodeDecodeError):
            if config.report_readerrors:
                logger.debug("Couldn't read file when looking for output: {}".format(f['fn']))
                return False

    return fn_matched and contents_matched


def exclude_file(sp, f):
    """
    Exclude discovered files if they match the special exclude_
    search pattern keys
    """
    for k in sp:
        if k in ('exclude_fn', 'exclude_fn_reexclude_contents', 'exclude_contents_re'):
            sp[k] = isinstance(sp[k], list) or [
             sp[k]]

    if 'exclude_fn' in sp:
        for pat in sp['exclude_fn']:
            if fnmatch.fnmatch(f['fn'], pat):
                return True

    if 'exclude_fn_re' in sp:
        for pat in sp['exclude_fn_re']:
            if re.match(pat, f['fn']):
                return True

    if 'exclude_contents' in sp or 'exclude_contents_re' in sp:
        if 'exclude_contents_re' in sp:
            sp['exclude_contents_re'] = [re.compile(pat) for pat in sp['exclude_contents_re']]
        with io.open((os.path.join(f['root'], f['fn'])), 'r', encoding='utf-8') as (fh):
            for line in fh:
                if 'exclude_contents' in sp:
                    for pat in sp['exclude_contents']:
                        if pat in line:
                            return True

                if 'exclude_contents_re' in sp:
                    for pat in sp['exclude_contents_re']:
                        if re.search(pat, line):
                            return True

    return False


def data_sources_tofile():
    fn = 'multiqc_sources.{}'.format(config.data_format_extensions[config.data_format])
    with io.open((os.path.join(config.data_dir, fn)), 'w', encoding='utf-8') as (f):
        if config.data_format == 'json':
            jsonstr = json.dumps(data_sources, indent=4, ensure_ascii=False)
            print((jsonstr.encode('utf-8', 'ignore').decode('utf-8')), file=f)
        else:
            if config.data_format == 'yaml':
                yaml.dump(data_sources, f, default_flow_style=False)
            else:
                lines = [
                 [
                  'Module', 'Section', 'Sample Name', 'Source']]
                for mod in data_sources:
                    for sec in data_sources[mod]:
                        for s_name, source in data_sources[mod][sec].items():
                            lines.append([mod, sec, s_name, source])

                body = '\n'.join(['\t'.join(l) for l in lines])
                print((body.encode('utf-8', 'ignore').decode('utf-8')), file=f)


def save_htmlid(html_id, skiplint=False):
    """ Take a HTML ID, sanitise for HTML, check for duplicates and save.
    Returns sanitised, unique ID """
    global html_ids
    global lint_errors
    html_id_clean = html_id.strip()
    html_id_clean = html_id_clean.strip('_')
    if re.match('^[a-zA-Z]', html_id_clean) is None:
        html_id_clean = 'mqc_{}'.format(html_id_clean)
    html_id_clean = re.sub('[^a-zA-Z0-9_-]+', '_', html_id_clean)
    if config.lint:
        if not skiplint:
            modname = ''
            codeline = ''
            callstack = inspect.stack()
            for n in callstack:
                if 'multiqc/modules/' in n[1] and 'base_module.py' not in n[1]:
                    callpath = n[1].split('multiqc/modules/', 1)[(-1)]
                    modname = '>{}< '.format(callpath)
                    codeline = n[4][0].strip()
                    break

    if config.lint:
        if not skiplint:
            if html_id != html_id_clean:
                errmsg = "LINT: {}HTML ID was not clean ('{}' -> '{}') ## {}".format(modname, html_id, html_id_clean, codeline)
                logger.error(errmsg)
                lint_errors.append(errmsg)
    i = 1
    html_id_base = html_id_clean
    while html_id_clean in html_ids:
        html_id_clean = '{}-{}'.format(html_id_base, i)
        i += 1
        if config.lint:
            errmsg = skiplint or 'LINT: {}HTML ID was a duplicate ({}) ## {}'.format(modname, html_id_clean, codeline)
            logger.error(errmsg)
            lint_errors.append(errmsg)

    html_ids.append(html_id_clean)
    return html_id_clean


def compress_json(data):
    """ Take a Python data object. Convert to JSON and compress using lzstring """
    json_string = json.dumps(data).encode('utf-8', 'ignore').decode('utf-8')
    json_string = json_string.replace('NaN', 'null')
    x = lzstring.LZString()
    return x.compressToBase64(json_string)
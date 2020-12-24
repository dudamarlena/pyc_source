# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/utils/utils.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 17541 bytes
"""Various utility functions for the ``jwql`` project.

Authors
-------

    - Matthew Bourque
    - Lauren Chambers

Use
---

    This module can be imported as such:

    >>> import utils
    settings = get_config()

References
----------

    Filename parser modified from Joe Hunkeler:
    https://gist.github.com/jhunkeler/f08783ca2da7bfd1f8e9ee1d207da5ff

    Various documentation related to JWST filename conventions:
    - https://jwst-docs.stsci.edu/display/JDAT/File+Naming+Conventions+and+Data+Products
    - https://innerspace.stsci.edu/pages/viewpage.action?pageId=94092600
    - https://innerspace.stsci.edu/pages/viewpage.action?spaceKey=SCSB&title=JWST+Science+Data+Products
    - https://jwst-docs.stsci.edu/display/JDAT/Understanding+Associations?q=association%20candidate
    - https://jwst-pipeline.readthedocs.io/en/stable/jwst/introduction.html#pipeline-step-suffix-definitions
    - JWST TR JWST-STScI-004800, SM-12
 """
import datetime, getpass, json, os, re, shutil, jsonschema
from jwql.utils import permissions
from jwql.utils.constants import FILE_SUFFIX_TYPES, JWST_INSTRUMENT_NAMES_SHORTHAND
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def copy_files(files, out_dir):
    """Copy a given file to a given directory. Only try to copy the file
    if it is not already present in the output directory.

    Parameters
    ----------
    files : list
        List of files to be copied

    out_dir : str
        Destination directory

    Returns
    -------
    success : list
        Files successfully copied (or that already existed in out_dir)

    failed : list
        Files that were not copied
    """
    success = []
    failed = []
    for input_file in files:
        input_new_path = os.path.join(out_dir, os.path.basename(input_file))
        if os.path.isfile(input_new_path):
            success.append(input_new_path)
        else:
            try:
                shutil.copy2(input_file, out_dir)
                success.append(input_new_path)
                permissions.set_permissions(input_new_path)
            except:
                failed.append(input_file)

    return (
     success, failed)


def download_mast_data(query_results, output_dir):
    """Example function for downloading MAST query results. From MAST
    website (``https://mast.stsci.edu/api/v0/pyex.html``)

    Parameters
    ----------
    query_results : list
        List of dictionaries returned by a MAST query.

    output_dir : str
        Directory into which the files will be downlaoded
    """
    server = 'mast.stsci.edu'
    conn = httplib.HTTPSConnection(server)
    print('Number of query results: {}'.format(len(query_results)))
    for i in range(len(query_results)):
        output_file = os.path.join(output_dir, query_results[i]['filename'])
        print('Output file is {}'.format(output_file))
        uri = query_results[i]['dataURI']
        print('uri is {}'.format(uri))
        conn.request('GET', '/api/v0/download/file?uri=' + uri)
        resp = conn.getresponse()
        file_content = resp.read()
        with open(output_file, 'wb') as (file_obj):
            file_obj.write(file_content)
        if not os.path.isfile(output_file):
            print('ERROR: {} failed to download.'.format(output_file))
        else:
            statinfo = os.stat(output_file)
            if statinfo.st_size > 0:
                print('DOWNLOAD COMPLETE: ', output_file)
            else:
                print('ERROR: {} file is empty.'.format(output_file))

    conn.close()


def ensure_dir_exists(fullpath):
    """Creates dirs from ``fullpath`` if they do not already exist."""
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
        permissions.set_permissions(fullpath)


def filename_parser(filename):
    """Return a dictionary that contains the properties of a given
    JWST file (e.g. program ID, visit number, detector, etc.).

    Parameters
    ----------
    filename : str
        Path or name of JWST file to parse

    Returns
    -------
    filename_dict : dict
        Collection of file properties

    Raises
    ------
    ValueError
        When the provided file does not follow naming conventions
    """
    filename = os.path.basename(filename)
    file_root_name = len(filename.split('.')) < 2
    stage_1_and_2 = 'jw(?P<program_id>\\d{5})(?P<observation>\\d{3})(?P<visit>\\d{3})_(?P<visit_group>\\d{2})(?P<parallel_seq_id>\\d{1})(?P<activity>\\w{2})_(?P<exposure_id>\\d+)_(?P<detector>((?!_)[\\w])+)'
    stage_2c = 'jw(?P<program_id>\\d{5})(?P<observation>\\d{3})(?P<visit>\\d{3})_(?P<visit_group>\\d{2})(?P<parallel_seq_id>\\d{1})(?P<activity>\\w{2})_(?P<exposure_id>\\d+)_(?P<detector>((?!_)[\\w])+)_(?P<ac_id>(o\\d{3}|(c|a|r)\\d{4}))'
    stage_3_target_id = 'jw(?P<program_id>\\d{5})-(?P<ac_id>(o\\d{3}|(c|a|r)\\d{4}))_(?P<target_id>(t)\\d{3})_(?P<instrument>(nircam|niriss|nirspec|miri|fgs))_(?P<optical_elements>((?!_)[\\w-])+)'
    stage_3_source_id = 'jw(?P<program_id>\\d{5})-(?P<ac_id>(o\\d{3}|(c|a|r)\\d{4}))_(?P<source_id>(s)\\d{5})_(?P<instrument>(nircam|niriss|nirspec|miri|fgs))_(?P<optical_elements>((?!_)[\\w-])+)'
    stage_3_target_id_epoch = 'jw(?P<program_id>\\d{5})-(?P<ac_id>(o\\d{3}|(c|a|r)\\d{4}))_(?P<target_id>(t)\\d{3})-epoch(?P<epoch>\\d{1})_(?P<instrument>(nircam|niriss|nirspec|miri|fgs))_(?P<optical_elements>((?!_)[\\w-])+)'
    stage_3_source_id_epoch = 'jw(?P<program_id>\\d{5})-(?P<ac_id>(o\\d{3}|(c|a|r)\\d{4}))_(?P<source_id>(s)\\d{5})-epoch(?P<epoch>\\d{1})_(?P<instrument>(nircam|niriss|nirspec|miri|fgs))_(?P<optical_elements>((?!_)[\\w-])+)'
    time_series = 'jw(?P<program_id>\\d{5})(?P<observation>\\d{3})(?P<visit>\\d{3})_(?P<visit_group>\\d{2})(?P<parallel_seq_id>\\d{1})(?P<activity>\\w{2})_(?P<exposure_id>\\d+)-seg(?P<segment>\\d{3})_(?P<detector>\\w+)'
    guider = 'jw(?P<program_id>\\d{5})(?P<observation>\\d{3})(?P<visit>\\d{3})_gs-(?P<guider_mode>(id|acq1|acq2|track|fg))_((?P<date_time>\\d{13})|(?P<guide_star_attempt_id>\\d{1}))'
    filename_types = [
     stage_1_and_2,
     stage_2c,
     stage_3_target_id,
     stage_3_source_id,
     stage_3_target_id_epoch,
     stage_3_source_id_epoch,
     time_series,
     guider]
    filename_type_names = [
     'stage_1_and_2',
     'stage_2c',
     'stage_3_target_id',
     'stage_3_source_id',
     'stage_3_target_id_epoch',
     'stage_3_source_id_epoch',
     'time_series',
     'guider']
    for filename_type, filename_type_name in zip(filename_types, filename_type_names):
        if not file_root_name:
            filename_type += '_(?P<suffix>{}).*'.format('|'.join(FILE_SUFFIX_TYPES))
        else:
            filename_type += '$'
        elements = re.compile(filename_type)
        jwst_file = elements.match(filename)
        if jwst_file is not None:
            name_match = filename_type_name
            break

    try:
        filename_dict = jwst_file.groupdict()
        filename_dict['filename_type'] = name_match
        if 'instrument' not in filename_dict.keys():
            if name_match == 'guider':
                filename_dict['instrument'] = 'fgs'
            elif 'detector' in filename_dict.keys():
                filename_dict['instrument'] = JWST_INSTRUMENT_NAMES_SHORTHAND[filename_dict['detector'][:3]]
    except AttributeError:
        jdox_url = 'https://jwst-docs.stsci.edu/display/JDAT/File+Naming+Conventions+and+Data+Products'
        raise ValueError('Provided file {} does not follow JWST naming conventions.  See {} for further information.'.format(filename, jdox_url))

    return filename_dict


def filesystem_path(filename):
    """Return the full path to a given file in the filesystem

    Parameters
    ----------
    filename : str
        File to locate (e.g. ``jw86600006001_02101_00008_guider1_cal.fits``)

    Returns
    -------
    full_path : str
        Full path to the given file, including filename
    """
    filesystem_base = get_config()['filesystem']
    subdir = 'jw{}'.format(filename_parser(filename)['program_id'])
    full_path = os.path.join(filesystem_base, subdir, filename)
    if os.path.isfile(full_path):
        return full_path
    raise FileNotFoundError('{} is not in the predicted location: {}'.format(filename, full_path))


def get_base_url():
    """Return the beginning part of the URL to the ``jwql`` web app
    based on which user is running the software.

    If the admin account is running the code, the ``base_url`` is
    assumed to be the production URL.  If not, the ``base_url`` is
    assumed to be local.

    Returns
    -------
    base_url : str
        The beginning part of the URL to the ``jwql`` web app
    """
    username = getpass.getuser()
    if username == get_config()['admin_account']:
        base_url = 'https://dljwql.stsci.edu'
    else:
        base_url = 'http://127.0.0.1:8000'
    return base_url


def get_config():
    """Return a dictionary that holds the contents of the ``jwql``
    config file.

    Returns
    -------
    settings : dict
        A dictionary that holds the contents of the config file.
    """
    config_file_location = os.path.join(__location__, 'config.json')
    if not os.path.isfile(config_file_location):
        raise FileNotFoundError('The JWQL package requires a configuration file (config.json) to be placed within the jwql/utils directory. This file is missing. Please read the relevant wiki page (https://github.com/spacetelescope/jwql/wiki/Config-file) for more information.')
    with open(config_file_location, 'r') as (config_file_object):
        try:
            settings = json.load(config_file_object)
        except json.JSONDecodeError as e:
            raise ValueError('Incorrectly formatted config.json file. Please fix JSON formatting: {}'.format(e))

    _validate_config(settings)
    return settings


def check_config_for_key(key):
    """Check that the config.json file contains the specified key
    and that the entry is not empty

    Parameters
    ----------
    key : str
        The configuration file key to verify
    """
    try:
        get_config()[key]
    except KeyError:
        raise KeyError('The key `{}` is not present in config.json. Please add it.'.format(key) + ' See the relevant wiki page (https://github.com/spacetelescope/jwql/wiki/Config-file) for more information.')

    if get_config()[key] == '':
        raise ValueError('Please complete the `{}` field in your config.json. '.format(key) + ' See the relevant wiki page (https://github.com/spacetelescope/jwql/wiki/Config-file) for more information.')


def _validate_config(config_file_dict):
    """Check that the config.json file contains all the needed entries with
    expected data types

    Parameters
    ----------
    config_file_dict : dict
        The configuration JSON file loaded as a dictionary

    Notes
    -----
    See here for more information on JSON schemas:
        https://json-schema.org/learn/getting-started-step-by-step.html
    """
    schema = {'type':'object', 
     'properties':{'connection_string':{'type': 'string'}, 
      'database':{'type':'object', 
       'properties':{'engine':{'type': 'string'}, 
        'name':{'type': 'string'}, 
        'user':{'type': 'string'}, 
        'password':{'type': 'string'}, 
        'host':{'type': 'string'}, 
        'port':{'type': 'string'}}, 
       'required':[
        'engine', 'name', 'user', 'password', 'host', 'port']}, 
      'filesystem':{'type': 'string'}, 
      'preview_image_filesystem':{'type': 'string'}, 
      'thumbnail_filesystem':{'type': 'string'}, 
      'outputs':{'type': 'string'}, 
      'jwql_dir':{'type': 'string'}, 
      'admin_account':{'type': 'string'}, 
      'log_dir':{'type': 'string'}, 
      'test_dir':{'type': 'string'}, 
      'test_data':{'type': 'string'}, 
      'setup_file':{'type': 'string'}, 
      'auth_mast':{'type': 'string'}, 
      'client_id':{'type': 'string'}, 
      'client_secret':{'type': 'string'}, 
      'mast_token':{'type': 'string'}}, 
     'required':[
      'connection_string', 'database', 'filesystem',
      'preview_image_filesystem', 'thumbnail_filesystem',
      'outputs', 'jwql_dir', 'admin_account', 'log_dir',
      'test_dir', 'test_data', 'setup_file', 'auth_mast',
      'client_id', 'client_secret', 'mast_token']}
    try:
        jsonschema.validate(instance=config_file_dict, schema=schema)
    except jsonschema.ValidationError as e:
        raise jsonschema.ValidationError('Provided config.json does not match the ' + 'required JSON schema: {}'.format(e.message))


def initialize_instrument_monitor(module):
    """Configures a log file for the instrument monitor run and
    captures the start time of the monitor

    Parameters
    ----------
    module : str
        The module name (e.g. ``dark_monitor``)

    Returns
    -------
    start_time : datetime object
        The start time of the monitor
    log_file : str
        The path to where the log file is stored
    """
    from jwql.utils.logging_functions import configure_logging
    start_time = datetime.datetime.now()
    log_file = configure_logging(module)
    return (
     start_time, log_file)


def update_monitor_table(module, start_time, log_file):
    """Update the ``monitor`` database table with information about
    the instrument monitor run

    Parameters
    ----------
    module : str
        The module name (e.g. ``dark_monitor``)
    start_time : datetime object
        The start time of the monitor
    log_file : str
        The path to where the log file is stored
    """
    from jwql.database.database_interface import Monitor
    new_entry = {}
    new_entry['monitor_name'] = module
    new_entry['start_time'] = start_time
    new_entry['end_time'] = datetime.datetime.now()
    new_entry['log_file'] = os.path.basename(log_file)
    Monitor.__table__.insert().execute(new_entry)
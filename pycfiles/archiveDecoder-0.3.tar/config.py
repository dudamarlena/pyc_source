# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/archivedb/config.py
# Compiled at: 2011-11-17 19:50:34
import os, sys, logging, archivedb.common
_py3 = sys.version_info > (3, )
if _py3:
    import configparser
else:
    import ConfigParser as configparser

def get_default_params(section):
    """
    Args:
    section - section of config
    
    Returns: tuple (keys_sorted[section], defaults[section])
    keys_sorted[section] - since dict doesn't preserve order, this is used to keep order when writing
    defaults[section] - dict of default values
    required_keys[section] - list of keys that require user modification
    """
    defaults = {}
    keys_sorted = {}
    required_keys = {}
    defaults['general'] = {'watch_dirs': '', 
       'ignore_dirs': '', 
       'ignore_files': '.*\\!ut.* ^\\.', 
       'scan_interval': '12', 
       'log_path': '/tmp/archivedb.log', 
       'debug': 'false'}
    defaults['db'] = {'host': 'localhost', 
       'port': '3306', 
       'user': 'username', 
       'pass': 'password'}
    keys_sorted['general'] = [
     'watch_dirs', 'ignore_dirs', 'ignore_files', 'scan_interval',
     'log_path', 'debug']
    keys_sorted['db'] = [
     'host', 'port', 'user', 'pass']
    required_keys['general'] = [
     'watch_dirs']
    required_keys['db'] = [
     'user', 'pass']
    return (
     keys_sorted[section], defaults[section], required_keys[section])


def create_default_config(conf_file):
    """ Create the default config file for archivedb """
    config = configparser.RawConfigParser()
    for section in ['general', 'db']:
        (keys_sorted, defaults) = get_default_params(section)[0:2]
        config.add_section(section)
        for k in keys_sorted:
            config.set(section, k, defaults[k])

    with open(conf_file, 'wb') as (configfile):
        config.write(configfile)


def validate_config(conf_file):
    """
    perform sanity checks on conf_file
    
    Args:
    conf_file - path to config file
    
    Returns:
    config - ConfigParser() object
    """
    config = configparser.ConfigParser()
    config.read(conf_file)
    required_sections = [
     'general', 'db']
    for sec in required_sections:
        (keys_sorted, defaults, required_keys) = get_default_params(sec)
        if not config.has_section(sec):
            log.warning(("section '{0}' not found in config, using defaults").format(sec))
            config.add_section(sec)
            for k in keys_sorted:
                config.set(sec, k, defaults[k])

        conf_dict = dict((pair[0], pair[1]) for pair in config.items(sec))
        log.debug(('conf_dict = {0}').format(str(conf_dict)))
        for k in keys_sorted:
            if k in conf_dict:
                log.debug(('conf_dict[{0}]    = {1}').format(k, conf_dict[k]))
            else:
                log.debug(('conf_dict[{0}]    = N/A').format(k))
            log.debug(('defaults[{0}]    = {1}').format(k, defaults[k]))
            if k in required_keys:
                if k not in conf_dict:
                    log.fatal(("config file missing required key '{0}' (section: {1}) , exiting.").format(k, sec))
                    sys.exit(1)
                elif conf_dict[k] == defaults[k]:
                    log.fatal(("config file has required key '{0}' (section: {1}), but default value is not allowed, exiting").format(k, sec))
                    sys.exit(1)
            elif k not in conf_dict:
                log.warning(("key: '{0}' not found in config, using default value: '{1}'").format(k, defaults[k]))
                config.set(sec, k, defaults[k])
            else:
                config.set(sec, k, conf_dict[k])

    return config


def parse_config(config):
    """
    Args:
    config - ConfigParser() object
    
    Returns:
    args - a dict of variables parsed from conf_file
    """
    args = {}
    sections = [
     'general', 'db']
    for sec in sections:
        for (k, v) in config.items(sec):
            if v == None:
                continue
            if sec == 'db':
                args[('db_{0}').format(k)] = v
            else:
                args[k] = v

    return args


def format_args(args):
    """
    Perform various type-casting, string splitting on given variables
    
    Args:
    args - dict (from parse_config())
    
    Return:
    args - new and improved
    """
    cast_int = [
     'db_port', 'scan_interval']
    cast_bool = ['debug']
    for k in cast_int:
        if k in args:
            try:
                args[k] = int(args[k])
            except ValueError:
                log.critical(("Given value for key '{0}' is not a valid integer. Check config.").format(k))
                sys.exit(1)

    for k in cast_bool:
        if k in args:
            if args[k].lower() in ('true', '1'):
                args[k] = True
            elif args[k].lower() in ('false', '0'):
                args[k] = False
            else:
                log.critical(("Given value for key '{0}' is not valid. Check config.").format(k))
                sys.exit(1)

    split_dict = {'watch_dirs': '|', 'ignore_dirs': '|', 
       'ignore_files': ' '}
    for k in split_dict:
        if k in args:
            args[k] = [ e.strip() for e in args[k].split(split_dict[k]) ]

    return args


def get_args():
    args = format_args(parse_config(config))
    return args


if __name__ == 'archivedb.config':
    log = logging.getLogger(__name__)
    CONF_FILE = os.path.expanduser('~/.archivedb.conf')
    if not os.path.exists(CONF_FILE):
        log.critical(('{0} not found, edit example.conf and copy.').format(CONF_FILE))
        sys.exit(1)
    config = validate_config(CONF_FILE)
    args = get_args()
    args['threads'] = [
     'inotify', 'oswalk']
    args['db_name'] = 'archivedb'
    args['tables'] = {'archive': ('CREATE TABLE `archivedb`.`archive` (\n    `id` mediumint(9) NOT NULL AUTO_INCREMENT,\n    `watch_dir` {0} NOT NULL,\n    `path` longtext NOT NULL,\n    `filename` longtext NOT NULL,\n    `md5` varchar(32) NOT NULL,\n    `mtime` int(10) NOT NULL,\n    `size` varchar(12) NOT NULL,\n    PRIMARY KEY (`id`),\n    FULLTEXT `path` (path),\n    FULLTEXT `filename` (filename)\n) ENGINE=`MyISAM` AUTO_INCREMENT=1 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ROW_FORMAT=DYNAMIC CHECKSUM=0 DELAY_KEY_WRITE=0;').format(archivedb.common.list_to_enum(args['watch_dirs']))}
    args['table_struct'] = {'archive': ('id', 'watch_dir', 'path', 'filename', 'md5', 'mtime', 'size')}
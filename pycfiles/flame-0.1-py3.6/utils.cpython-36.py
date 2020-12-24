# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/util/utils.py
# Compiled at: 2018-06-26 10:56:01
# Size of source mod 2**32: 5727 bytes
import hashlib, os, sys, yaml, random, string, pathlib

def get_conf_yml_path():
    """
    recovers the path of the configuration yml file

    Returns:
    --------
    str, path where conf.yaml is

    TODO: be sure that the conf.yaml exists and raise
    err if doesn't
    """
    source_dir = pathlib.Path(__file__).resolve().parents[1]
    return os.path.join(source_dir, 'config.yaml')


def _read_configuration():
    """
    Reads configuration file "config.yaml".

    Returns:
    --------
    dict
    """
    conf = {}
    with open(get_conf_yml_path(), 'r') as (config_file):
        conf = yaml.load(config_file)
    model_abs_path = pathlib.Path(conf['model_repository_path']).resolve()
    conf['model_repository_path'] = str(model_abs_path)
    return conf


def set_model_repository(path=None):
    """
    Set the model repository path.
    This is the dir where flame is going to create and load models.

    if path is None, model dir will be set to the default in the
    flame root directory.

    Returns:
    --------
    None
    """
    with open(get_conf_yml_path(), 'r') as (f):
        configuration = yaml.load(f)
    if path is None:
        model_root_path = os.path.join(pathlib.Path(__file__).resolve().parents[1], 'models/')
        configuration['model_repository_path'] = str(model_root_path)
    else:
        new_path = pathlib.Path(path)
        configuration['model_repository_path'] = str(new_path.resolve())
    with open(get_conf_yml_path(), 'w') as (f):
        yaml.dump(configuration, f, default_flow_style=False)


def model_repository_path():
    """
    Returns the path to the root of the model repository,
    containing all models and versions
    """
    configuration = _read_configuration()
    return configuration['model_repository_path']


def model_tree_path(model):
    """
    Returns the path to the model given as argumen, containg all versions
    """
    return os.path.join(model_repository_path(), model)


def model_path(model, version):
    """
    Returns the path to the model and version given as arguments
    """
    modpath = model_tree_path(model)
    if version == 0:
        modpath = os.path.join(modpath, 'dev')
    else:
        modpath = os.path.join(modpath, 'ver%0.6d' % version)
    return modpath


def module_path(model, version):
    """
    Returns the path to the model and version given as arguments,
    in Python synthax (separated by ".").

    Also adds the model repository path to the Python path, so the relative
    module path can be understood and the module imported.
    """
    modreppath = model_repository_path()
    if modreppath not in sys.path:
        sys.path.insert(0, modreppath)
    else:
        modpath = model
        if version == 0:
            modpath += '.dev'
        else:
            modpath += '.ver%0.6d' % version
    return modpath


def md5sum(filename, blocksize=65536):
    """
    Returns the MD5 sum of the file given as argument
    """
    hash = hashlib.md5()
    with open(filename, 'rb') as (f):
        for block in iter(lambda : f.read(blocksize), b''):
            hash.update(block)

    return hash.hexdigest()


def intver(raw_version):
    """
    Returns an int describing at best the model version provided as argument
    """
    if raw_version is None:
        return 0
    else:
        try:
            version = int(raw_version)
        except:
            version = 0

        return version


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    """ Return a random ID (used for temp files) with uppercase letters and numbers """
    return ''.join(random.choice(chars) for _ in range(size))


def add_result(results, var, _key, _label, _type, _dimension='objs', _description=None, _relevance=None):
    if 'manifest' not in results:
        results['manifest'] = []
    manifest = results['manifest']
    results[_key] = var
    manifest_item = {'key':_key, 
     'label':_label, 
     'type':_type, 
     'dimension':_dimension, 
     'description':_description, 
     'relevance':_relevance}
    manifest.append(manifest_item)
    if _relevance == 'main':
        if 'meta' not in results:
            results['meta'] = {'main': [_key]}
        else:
            results['meta']['main'].append(_key)


def is_empty(mylist):
    for i in mylist:
        if i is not None:
            return False

    return True
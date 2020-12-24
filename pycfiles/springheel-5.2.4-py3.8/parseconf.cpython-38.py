# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/parseconf.py
# Compiled at: 2019-12-16 02:05:38
# Size of source mod 2**32: 2415 bytes
import configparser, os

def comicCParse(conf):
    """
    Parse a configuration file.

    Parameters
    ----------
    conf : str
        The path to the configuration file.
    Returns
    -------
    comic_config : dict
        The comic's configuration file formatted as a dictionary.
    """
    cc = configparser.ConfigParser()
    cc.read(conf, encoding='utf-8')
    cc.sections()
    category = cc.get('ComicConfig', 'category')
    author = cc.get('ComicConfig', 'author')
    email = cc.get('ComicConfig', 'email')
    header = cc.get('ComicConfig', 'header')
    banner = cc.get('ComicConfig', 'banner')
    language = cc.get('ComicConfig', 'language')
    mode = cc.get('ComicConfig', 'mode')
    status = cc.get('ComicConfig', 'status')
    chapters = cc.get('ComicConfig', 'chapters')
    desc = cc.get('ComicConfig', 'desc')
    chars = cc.get('ComicConfig', 'chars')
    clicense = cc.get('ComicConfig', 'license')
    comic_config = {'category':category, 
     'author':author,  'email':email, 
     'header':header,  'banner':banner,  'language':language, 
     'mode':mode,  'status':status,  'chapters':chapters, 
     'desc':desc,  'license':clicense,  'chars':chars}
    try:
        clicense_uri = cc.get('ComicConfig', 'license_uri')
        comic_config['license_uri'] = clicense_uri
    except configparser.NoOptionError:
        pass
    else:
        try:
            category_theme = cc.get('ComicConfig', 'category_theme')
            comic_config['category_theme'] = category_theme
        except configparser.NoOptionError:
            pass
        else:
            return comic_config
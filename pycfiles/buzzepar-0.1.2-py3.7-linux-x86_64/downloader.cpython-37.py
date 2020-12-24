# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benepar/downloader.py
# Compiled at: 2020-05-05 12:30:15
# Size of source mod 2**32: 1186 bytes
import json
BENEPAR_SERVER_INDEX = 'https://kitaev.io/benepar_models/index.xml'
_downloader = None

def get_downloader():
    global _downloader
    if _downloader is None:
        import nltk.downloader
        _downloader = nltk.downloader.Downloader(server_index_url=BENEPAR_SERVER_INDEX)
    return _downloader


def download(*args, **kwargs):
    return (get_downloader().download)(*args, **kwargs)


def load_model(name):
    import nltk.data
    name_gz = 'models/{}.gz'.format(name)
    name_zip = 'models/{}.zip'.format(name)
    use_gz = False
    try:
        nltk.data.find(name_gz)
        use_gz = True
    except LookupError:
        pass

    try:
        if use_gz:
            return nltk.data.load(name_gz, format='raw')
        return {'meta':json.loads(nltk.data.load((name_zip + '/meta.json'), format='text')), 
         'model':nltk.data.load(name_zip + '/model.pb', format='raw'), 
         'vocab':nltk.data.load(name_zip + '/vocab.txt', format='text', encoding='utf-8')}
    except LookupError as e:
        try:
            arg = e.args[0].replace('nltk.download', 'benepar.download')
        finally:
            e = None
            del e

    raise LookupError(arg)
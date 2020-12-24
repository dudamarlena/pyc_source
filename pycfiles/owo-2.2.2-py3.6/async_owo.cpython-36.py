# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/owo/async_owo.py
# Compiled at: 2017-05-02 07:34:37
# Size of source mod 2**32: 3697 bytes
import asyncio
from functools import lru_cache
from .utils import check_size, BASE_URL, MAX_FILES, UPLOAD_PATH, SHORTEN_PATH, UPLOAD_STANDARD, SHORTEN_STANDARD, UPLOAD_BASES, SHORTEN_BASES

@asyncio.coroutine
def async_upload_files(key, *files, **kwargs):
    verbose = kwargs.get('verbose', False)
    loop = kwargs.get('loop', None)
    if len(files) > MAX_FILES:
        raise OverflowError('Maximum amout of files to send at onceis {}'.format(MAX_FILES))
    try:
        from . import aiohttp2
        import aiohttp
    except ImportError:
        raise ImportError('Please install the `aiohttp` module to use this function')

    results = {}
    for file in files:
        check_size(file)

    with aiohttp2.MultipartWriter('form-data') as (mp):
        for file in files:
            part = mp.append(open(file, 'rb'))
            part.set_content_disposition('form-data',
              should_quote=False,
              name='files[]',
              filename=(file.lower()))

        with aiohttp.ClientSession(loop=loop) as (session):
            with yield from session.post((BASE_URL + UPLOAD_PATH), data=mp, params={'key': key}) as (response):
                if response.status != 200:
                    raise ValueError('Expected 200, got {}\n{}'.format(response.status, (yield from response.text())))
                for item in (yield from response.json())['files']:
                    if item.get('error') is True:
                        raise ValueError('Expected 200, got {}\n{}'.format(item['errorcode'], item['description']))
                    else:
                        if verbose:
                            results[item['name']] = {base:base + item['url'] for base in UPLOAD_BASES}
                        else:
                            results[item['name']] = UPLOAD_STANDARD + item['url']

    return results
    if False:
        yield None


@asyncio.coroutine
def async_shorten_urls(key, *urls, **kwargs):
    verbose = kwargs.get('verbose', False)
    loop = kwargs.get('loop', None)
    try:
        import aiohttp
    except ImportError:
        raise ImportError('Please install the `aiohttp` module to use this function')

    results = []
    with aiohttp.ClientSession(loop=loop) as (session):
        for url in urls:
            with (yield from session.get((BASE_URL + SHORTEN_PATH), params={'action':'shorten', 
             'url':url, 
             'key':key})) as (response):
                if response.status != 200:
                    raise ValueError('Expected 200, got {}\n{}'.format(response.status, (yield from response.text())))
            path = (yield from response.text()).split('/')[(-1)]
            if verbose:
                results.append({base:base + path for base in SHORTEN_BASES})
            else:
                results.append(SHORTEN_STANDARD + path)

    return results
    if False:
        yield None


class Client:

    @asyncio.coroutine
    def async_upload_files(self, *files):
        return async_upload_files(self.key, *files, **{'loop':self.loop, 
         'verbose':self.verbose})

    @asyncio.coroutine
    def async_shorten_urls(self, *urls):
        return async_shorten_urls(self.key, *urls, **{'loop':self.loop, 
         'verbose':self.verbose})
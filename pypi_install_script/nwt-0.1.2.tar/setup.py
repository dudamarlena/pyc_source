#! -*- coding: utf-8 -*-
"""
nwt.controllers.setup
---------------------

Download, install and epub bible.
"""
import shutil

import click
from logzero import logger as log

from .error import NwtWarning

from ..models.epuber import EpubBible
from ..models.config import Config
from ..models import BIBLE_DIR, CACHE_DIR, touch

from ..views.console.printer import echo


def install(epub_file: str, initial=None):
    """
    Install existing epub file.
    """
    epub_bible = EpubBible(epub_file)

    conf = Config()
    if conf['installed'] is None:
        echo('Writing configuration... ', nl=False)
        conf['installed'] = [epub_bible.stand]
    else:
        if epub_bible.stand in conf['installed']:
            raise NwtWarning('This bible is already installed')
        else:
            echo('Writing configuration... ', nl=False)
            conf['installed'].append(epub_bible.stand)
    echo('done')

    echo('Installation... ', nl=False)
    touch(BIBLE_DIR / f'{epub_bible.stand}.epub', create_dirs=True)
    log.debug(f'Copy: {epub_bible.path} -> {BIBLE_DIR / f"{epub_bible.stand}.epub"}')  # noqa
    shutil.copy(epub_bible.path, BIBLE_DIR / f'{epub_bible.stand}.epub')
    conf['active'] = {
        'name': epub_bible.stand,
        'path': str(BIBLE_DIR / f'{epub_bible.stand}.epub'),
    }
    echo('done')


def download(url: str):
    import requests

    echo('Downloading...')
    log.debug(f'url: {url}')
    r = requests.get(url)
    log.debug(f'status_code: {r.status_code}')
    log.debug(f'header: {r.headers}')
    with open(CACHE_DIR / 'bible', 'wb') as f:
        with click.progressbar(r.iter_content(1024)) as bar:
            for chunk in bar:
                f.write(chunk)
    echo('done')

    return CACHE_DIR / 'bible'

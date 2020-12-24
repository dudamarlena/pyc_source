# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/papis_zotero/bibtex.py
# Compiled at: 2019-10-21 05:56:29
# Size of source mod 2**32: 2200 bytes
import os, papis.bibtex, papis.api
from papis.commands.add import run as papis_add
import papis.config, papis.utils, logging, tqdm, colorama
logger = logging.getLogger('zotero:bibtex')
info_template = '{c.Back.BLACK}\n{c.Fore.RED}||\n{c.Fore.RED}||{c.Fore.YELLOW}    ref: {c.Fore.GREEN}{ref}\n{c.Fore.RED}||{c.Fore.YELLOW} author: {c.Fore.GREEN}{author}\n{c.Fore.RED}||{c.Fore.YELLOW}  title: {c.Fore.GREEN}{title}\n{c.Fore.RED}||{c.Style.RESET_ALL}\n'

def add_from_bibtex(bib_file, out_folder=None, link=False):
    if out_folder is not None:
        papis.config.set_lib_from_name(out_folder)
    entries = papis.bibtex.bibtex_to_dict(bib_file)
    with tqdm.tqdm(entries) as (t):
        for entry in t:
            if 'keywords' in entry.keys():
                entry['tags'] = entry['keywords']
                del entry['keywords']
            if 'author' not in entry.keys():
                entry['tags'] = 'Unkown'
            if 'ref' in entry.keys():
                entry['ref'] = entry['ref'].replace('?', '')
            print(info_template.format(c=colorama, author=entry.get('author'), title=entry.get('title'), ref=entry.get('ref')))
            pdf_file = None
            if 'file' in entry.keys():
                pdf_file = entry.get('file').split(':')[1]
                pdf_file = os.path.join(os.path.dirname(bib_file), pdf_file)
                logger.info('\tINFO: File field detected (%s)' % pdf_file)
                if not os.path.exists(pdf_file):
                    logger.warning(colorama.Back.YELLOW + colorama.Fore.BLACK + 'Path (%s)' % pdf_file + colorama.Back.RED + ' not found! Ignoring it' + colorama.Style.RESET_ALL)
                    del entry['file']
                    pdf_file = None
                papis_add([pdf_file] if pdf_file is not None else [], data=entry, link=link)
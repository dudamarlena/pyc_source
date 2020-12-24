# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/impex/impex.py
# Compiled at: 2019-06-06 17:59:22
# Size of source mod 2**32: 10219 bytes
import logging, os, ssl, time, requests, urllib3
from pyfiglet import Figlet
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry
from pathlib import Path
from onedesk.auth.auth import get_token
from onedesk.automaton.automaton import export_automata, import_automaton, get_automaton_list_for_client, delete_automata, automaton_exists, submit_automaton_for_approval, approve_automaton, get_automaton_version_latest, get_automaton_list_for_category
from onedesk.category.category import get_category_list_for_client, get_category_tree, delete_category, create_parent
from onedesk.client.client import get_client
from util.arguments import parser
from util.arguments import version
from util.models import Category, Automaton, ExportedAutomaton
from util.util import get_directory_tree, write_json_file, clean_file_name
f = Figlet(font='slant')
ch = logging.StreamHandler()
formatter = logging.Formatter('{asctime} {levelname} {name} {filename} {lineno} | {message}', style='{')
ch.setFormatter(formatter)
logger = logging.getLogger('main')
logger.addHandler(ch)

def do_export(args):
    print(f.renderText('Export Start !!'))
    start_time = time.time()
    try:
        directory = Path(args.directory)
        directory.mkdir(parents=True, exist_ok=True)
        logger.info('Exporting to local directory: %s', directory.absolute())
    except Exception:
        logger.error('Failed to create export directory: %s', args.directory)
        raise SystemExit

    s = requests.Session()
    s.verify = not args.ignorecert
    if int(args.retry) > 0:
        retries = Retry(total=(int(args.retry)), backoff_factor=0.2,
          status_forcelist=[
         500, 502, 503, 504],
          method_whitelist=False)
        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}
    client = get_client(s, args.instance, args.client)
    category_tree = get_category_tree(s, args.instance, client, args.category)
    for node in tqdm(category_tree, desc=('Exporting automata to {}'.format(directory))):
        if type(node.val) is Automaton:
            node_path = Path(directory, node.path)
            try:
                logger.debug('Creating directory %s', node_path.parent.absolute())
                node_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                logger.error('Failed to create export directory: %s', node_path)
                raise SystemExit

            data = export_automata(s, args.instance, node.val.json())
            if data is None:
                continue
            write_json_file(node_path.with_suffix('.json'), data)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format(time.time() - start_time)))


def do_import(args):
    print(f.renderText('Import Start !!'))
    start_time = time.time()
    directory = Path(args.directory)
    if not directory.exists():
        logger.error('Given directory does not exist! {}'.format(args.directory))
        raise SystemExit(1)
    logger.info('Importing automata from directory %s', directory.absolute())
    directory_tree = get_directory_tree(directory)
    s = requests.Session()
    s.verify = not args.ignorecert
    if int(args.retry) > 0:
        retries = Retry(total=(int(args.retry)), backoff_factor=0.2,
          status_forcelist=[
         500, 502, 503, 504],
          method_whitelist=False)
        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}
    client = get_client(s, args.instance, args.client)
    for node in tqdm(directory_tree, desc=('Importing node tree into {}'.format(args.instance))):
        if type(node.val) is ExportedAutomaton:
            logger.debug('<Importing automaton: [{} > {}]'.format(node.path, node.val.name))
            existing_automaton = automaton_exists(s, args.instance, client, node.val.name)
            if existing_automaton:
                delete_automata(s, args.instance, existing_automaton)
            parent = create_parent(s, args.instance, client, node.path)
            if parent is None:
                logger.error('Skipping automaton because parent could not be found')
                continue
            automata = import_automaton(s, args.instance, parent.json(), node.val.name, node.val.json())
            if automata is None:
                continue
            automata = get_automaton_list_for_category(s, args.instance, parent)
            for automaton in automata:
                if automaton['name'] == node.val.name:
                    latest = get_automaton_version_latest(s, args.instance, automaton)
                    submitted = submit_automaton_for_approval(s, args.instance, latest)
                    if submitted is None:
                        logger.error('Failed to submit automaton %s for approval', node.val.name)
                        continue
                    approved = approve_automaton(s, args.instance, submitted)
                    if approved:
                        logger.debug('Successfully imported and approved %s', node.val.name)
                    else:
                        logger.debug('Failed to approve automaton %s', node.val.name)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format(time.time() - start_time)))


def do_wipe(args):
    print(f.renderText('Wipe Start !!'))
    start_time = time.time()
    s = requests.Session()
    s.verify = not args.ignorecert
    if int(args.retry) > 0:
        retries = Retry(total=(int(args.retry)), backoff_factor=0.2,
          status_forcelist=[
         500, 502, 503, 504],
          method_whitelist=False)
        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}
    client = get_client(s, args.instance, args.client)
    automata_list = get_automaton_list_for_client(s, args.instance, client)
    category_list = get_category_list_for_client(s, args.instance, client)
    for automaton in tqdm(automata_list, desc=('Deleting automata in {} {}'.format(args.instance, client['name']))):
        delete_automata(s, args.instance, automaton)

    for category in tqdm(category_list, desc=('Deleting categories {} {}'.format(args.instance, client['name']))):
        delete_category(s, args.instance, category)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format(time.time() - start_time)))


def main():
    print(f.renderText('clicmod v{}'.format(version)))
    subparsers = parser.add_subparsers()
    export_parser = subparsers.add_parser('export', help='Export automata from the given client/category')
    export_parser.set_defaults(func=do_export)
    import_parser = subparsers.add_parser('import', help='Import automata to the given client/category')
    import_parser.set_defaults(func=do_import)
    wipe_parser = subparsers.add_parser('wipe', help='Delete all automata and categories in the given client/category')
    wipe_parser.set_defaults(func=do_wipe)
    args = parser.parse_args()
    logger.setLevel(logging._nameToLevel[args.log])
    logger.debug(ssl.OPENSSL_VERSION)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    args.func(args)


if __name__ == '__main__':
    main()
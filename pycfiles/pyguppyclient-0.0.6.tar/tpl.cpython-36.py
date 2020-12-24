# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\template_cli\tpl.py
# Compiled at: 2019-04-15 15:03:59
# Size of source mod 2**32: 2348 bytes
__doc__ = 'PQI\nUsage:\n  pqi add (<path>) [<projectName>]\n  pqi (-h | --help)\n  pqi (-v | --version)\nOptions:\n  add              Create Template.\n  -h --help        Show this screen.\n  -v --version     Show version.\n'
import json, shutil, os, platform
from docopt import docopt
APP_DESC = '\n         TPL ---- PyQt5 template\n         @author qq 625781186  (https://github.com/625781186/pygui_cli) \n'
NAME = 'pygui_cli'
CONFIG_FILE_NAME = '~\\pip\\{}.json'.format(NAME) if 'Windows' in platform.system() else '~/.pip/{}.json'.format(NAME)
CONFIG_FILE_PATH = os.path.expanduser(CONFIG_FILE_NAME)
CONFIG_DIR_PATH = os.path.dirname(CONFIG_FILE_PATH)
if not os.path.exists(CONFIG_DIR_PATH):
    os.mkdir(CONFIG_DIR_PATH)
else:
    if not os.path.exists(CONFIG_FILE_PATH):
        source_path = None
        print('Sorry, not found {} , please install {}'.format(CONFIG_FILE_PATH, NAME))
    else:
        with open(CONFIG_FILE_PATH, 'r', encoding='uft-8') as (f):
            raw_data = f.read()
            data = json.loads(raw_data, encoding='utf-8')
            source_path = data['source_path']
print('read template: %s' % source_path)

def copy_folder(to_folder: str, to_folder_name='source'):
    if source_path is None:
        print('Sorry, not found {} , please install {}'.format(CONFIG_FILE_PATH, NAME))
        return False
    else:
        if to_folder_name is None:
            to_folder_name = 'source'
        if os.path.exists(source_path):
            if os.path.exists(to_folder):
                to_folder = os.path.join(os.path.abspath('.'), to_folder_name)
                print('copy to: ', to_folder)
                shutil.copytree(source_path, to_folder)
                return True
            else:
                print('%s is not exists, please create it' % to_folder)
                return False
        else:
            print('%s is not exists, please install %s' % (source_path, NAME))
        return False


def main():
    arguments = docopt(__doc__, version='0.0.1')
    if arguments['add']:
        ok = copy_folder(arguments['<path>'], arguments['<projectName>'])
        if ok:
            print('Success!')
        else:
            print('Fail!')
    else:
        print('input error!')


if __name__ == '__main__':
    print(APP_DESC)
    main()
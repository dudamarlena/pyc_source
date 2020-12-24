# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/query.py
# Compiled at: 2015-07-08 07:34:06
from __future__ import absolute_import, division, print_function
import argparse, sys
from dossier.label import LabelStore
from dossier.store import Store
import kvlayer, yakonfig
from dossier.models.subtopic import Folders

class Factory(yakonfig.factory.AutoFactory):
    config_name = 'sortingdesk_report'
    kvlclient = property(lambda self: kvlayer.client())
    auto_config = lambda self: []


def main():
    p = argparse.ArgumentParser(description='SortingDesk report generation tool')
    p.add_argument('-c', '--config', required=True, help='Dossier stack YAML config file')
    p.add_argument('folder_name', nargs='?', default=None, help='Folder name')
    p.add_argument('-u', '--user', default=None, help='user name (default=ALL)')
    args = p.parse_args()
    config = yakonfig.set_default_config([kvlayer], filename=args.config)
    factory = Factory(config)
    store = factory.create(Store)
    label_store = factory.create(LabelStore)
    folders = Folders(store, label_store)
    list_projects(folders, args.folder_name, args.user)
    return


def list_projects(folders, folder=None, user=None):
    """List all folders or all subfolders of a folder.

    If folder is provided, this method will output a list of subfolders
    contained by it.  Otherwise, a list of all top-level folders is produced.

    :param folders: reference to folder.Folders instance
    :param folder: folder name or None
    :param user: optional user name

    """
    fid = None if folder is None else Folders.name_to_id(folder)
    if fid is None:
        for f in folders.folders(user):
            print(Folders.id_to_name(f))

        return
    try:
        for sid in folders.subfolders(fid, user):
            print(Folders.id_to_name(sid))

    except KeyError:
        print('E: folder not found: %s' % folder, file=sys.stderr)

    return


if __name__ == '__main__':
    main()
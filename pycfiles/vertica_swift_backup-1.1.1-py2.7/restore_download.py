# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vertica_backup/restore_download.py
# Compiled at: 2014-08-20 12:04:44
""" vertica restore download
Download a restore from Vertica to the local disk. This script does not run the vbr restore process.
The script will always grab the latest DirectoryMetadata in swift and compare that with a new DirectoryMetadata
of the local disk, in this way only doing incremental downloads as needed.

Copyright 2014 Hewlett-Packard Development Company, L.P.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF 
OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import logging, os, sys, yaml
from directory_metadata import DirectoryMetadata
from epoch import EpochFiles
from object_store.swift import SwiftStore
from object_store.fs import FSStore
from utils import calculate_paths, choose_one, delete_pickles, LogTime, sizeof_fmt

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 5 or len(argv) < 4:
        print 'Usage: ' + argv[0] + ' <config file> <domain> <v_node> [YYYY_MM_DD]'
        print 'The config file is the same format as used for backups, backup dir, snapshot name and swift credentials are used'
        print 'The domain is the domain to be restored from swift and the v_node is the vertica node name to restore data for'
        print 'If the year/month/day is specified the most recent backup on that day will be downloaded rather than prompting'
        return 1
    else:
        config_file = argv[1]
        domain = argv[2]
        v_node_name = argv[3]
        if len(argv) == 5:
            day = argv[4]
        else:
            day = None
        config = yaml.load(open(config_file, 'r'))
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        log = logging.getLogger(__name__)
        with LogTime(log.info, 'Restore download completed'):
            base_dir, prefix_dir = calculate_paths(config, v_node_name)
            swift_store = SwiftStore(config['swift_key'], config['swift_region'], config['swift_tenant'], config['swift_url'], config['swift_user'], prefix_dir, domain=domain, vnode=v_node_name)
            fs_store = FSStore(base_dir, prefix_dir)
            current_metadata = DirectoryMetadata(fs_store)
            if day is None:
                pickle = choose_one(swift_store.list_pickles(), 'Please choose a pickle to restore from')
            else:
                pickle = None
                for option in swift_store.list_pickles():
                    if option.startswith(day):
                        pickle = option

            if pickle is None:
                log.error('No backups found in swift.')
                sys.exit(1)
            swift_metadata = DirectoryMetadata.load_pickle(swift_store, pickle)
            with LogTime(log.debug, 'Diff completed', seconds=True):
                to_download, to_del = swift_metadata.diff(current_metadata)
            size_downloaded = 0
            with LogTime(log.info, 'Download Completed'):
                for relative_path in to_download:
                    size_downloaded += swift_store.download(relative_path, base_dir)

            log.info('\tDownloaded %s in %d items' % (sizeof_fmt(size_downloaded), len(to_download)))
            with LogTime(log.info, 'Deleted %d items' % len(to_del)):
                for relative_path in to_del:
                    fs_store.delete(relative_path)

            EpochFiles(os.path.join(base_dir, prefix_dir), config['snapshot_name'], swift_metadata.date).restore()
            swift_metadata.save(fs_store)
        delete_pickles(fs_store)
        return


if __name__ == '__main__':
    sys.exit(main())
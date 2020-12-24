# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/DupeRelink.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = '\nDupeRelink.py -- Searches for HTML files that are the same, writes a single\nfile into a common area and deletes all the others. Then re-links all the\nremaining HTML files that linked to the original files to link to the file\nin the common area. This is a space saving optimisation after CPIPMain.py\nhas processed a directory of source files.\n'
import argparse, collections, fnmatch, hashlib, logging, os, shutil, sys, time
from cpip import TokenCss
__author__ = 'Paul Ross'
__date__ = '2017-09-26'
__rights__ = 'Copyright (c) 2017 Paul Ross'
SUB_DIR_FOR_COMMON_FILES = '_common_html'
FILE_GLOB = '*.html'
LINK_FORMAT_STR = '<a href="{:s}'

def _get_hash_result(dir_path, file_glob):
    """Returns a dict of {hash : [file_path, ...], ...} from a root
    directory."""
    hash_result = collections.defaultdict(list)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if fnmatch.fnmatch(file, file_glob):
                fpath = os.path.join(root, file)
                with open(fpath, 'rb') as (fobj):
                    hsh = hashlib.md5(fobj.read()).hexdigest()
                    hash_result[hsh].append(fpath)

    return hash_result


def _prune_hash_result(hash_result):
    """Prunes a dict of {hash : [file_path, ...], ...} to just those entries
    that have >1 file_path."""
    keys = []
    for k in hash_result:
        if len(hash_result[k]) == 1:
            keys.append(k)

    for k in keys:
        del hash_result[k]


def _replace_in_file(fpath, text_find, text_repl, nervous_mode, len_root_dir):
    """Reads the contents of the file at fpath, replaces text_from with
    text_repl and writes it back out to the same fpath."""
    if nervous_mode:
        logging.info(('Would replace links in "{:s}" swap: "{:s}" for: "{:s}"').format(fpath[len_root_dir:], text_find, text_repl))
    else:
        logging.debug(('Replacing links in "{:s}" swap: "{:s}" for: "{:s}"').format(fpath[len_root_dir:], text_find, text_repl))
        with open(fpath, 'r') as (fobj):
            content = fobj.read()
        with open(fpath, 'w') as (fobj):
            fobj.write(content.replace(text_find, text_repl))


def _prepare_to_process(root_dir, file_glob):
    """Create a dict {hash : [file_paths, ...], ...} for duplicated files"""
    logging.info((' Searching ').center(75, '='))
    hash_result = _get_hash_result(root_dir, file_glob)
    logging.info(('Hash result: hashes={:d}, files={:d}').format(len(hash_result), sum([ len(v) for v in hash_result.values() ])))
    _prune_hash_result(hash_result)
    logging.info(('Hash result: hashes={:d}, duplicate files={:d}').format(len(hash_result), sum([ len(v) for v in hash_result.values() ])))
    logging.info((' DONE Searching ').center(75, '='))
    return hash_result


def _copy_delete_duplicates_fix_links(hash_result, common_dir, nervous_mode, len_root_dir):
    """Copy a single file that is duplicated to the common area, rewrite the
    links in that copy to the original location then delete all duplicates."""
    count_deleted = 0
    count_bytes_saved = 0
    logging.info((' Copying and deleting ').center(75, '='))
    for k, v in hash_result.items():
        assert len(v) > 1, '_pruneHashResult(hash_result) not called or failed.'
        copy_from = v[0]
        copy_to = os.path.join(common_dir, os.path.basename(v[0]))
        if nervous_mode:
            logging.info(('Would copy "{:s}" to "{:s}"').format(copy_from[len_root_dir:], copy_to[len_root_dir:]))
        else:
            logging.debug(('Copying "{:s}" to "{:s}"').format(copy_from[len_root_dir:], copy_to[len_root_dir:]))
            shutil.copy(copy_from, copy_to)
        count_bytes_saved += os.stat(v[0]).st_size * (len(v) - 1)
        text_find = LINK_FORMAT_STR.format('')
        depth_diff = 1 + copy_from.count(os.sep) - copy_to.count(os.sep)
        args = [os.pardir]
        args.extend(copy_from[len_root_dir:].split(os.sep)[:depth_diff])
        args.append('')
        text_repl = LINK_FORMAT_STR.format(os.path.join(*args))
        _replace_in_file(copy_to, text_find, text_repl, nervous_mode, len_root_dir)
        for dupe_file_path in v:
            if nervous_mode:
                logging.info(('Would delete "{:s}"').format(dupe_file_path[len_root_dir:]))
            else:
                logging.debug('Remove:', dupe_file_path[len_root_dir:])
                os.remove(dupe_file_path)
            count_deleted += 1

    logging.info((' DONE Copying and deleting ').center(75, '='))
    return (
     count_deleted, count_bytes_saved)


def _rewrite_links_where_files_deleted(root_dir, sub_dir_for_common_files, nervous_mode, hash_result, len_root_dir):
    """In the directories where we have deleted files rewrite the links to the
    common directory."""
    logging.info((' Rewriting links ').center(75, '='))
    root_depth = root_dir.count(os.sep)
    count = 1
    for k, v in hash_result.items():
        assert len(v) > 1
        count_str = ('[{:d}/{:d}]').format(count, len(hash_result))
        logging.info(('{:16s} Rewriting links to "{:s}"').format(count_str, os.path.basename(v[0])))
        for dupe_file_path in v:
            for root, dirs, files in os.walk(os.path.dirname(dupe_file_path)):
                depth = root.count(os.sep)
                assert depth >= root_depth
                text_find = LINK_FORMAT_STR.format(os.path.basename(dupe_file_path))
                args = [os.pardir] * (depth - root_depth)
                args.append(sub_dir_for_common_files)
                args.append(os.path.basename(dupe_file_path))
                text_repl = LINK_FORMAT_STR.format(os.path.join(*args))
                for file in files:
                    if fnmatch.fnmatch(file, FILE_GLOB):
                        _replace_in_file(os.path.join(root, file), text_find, text_repl, nervous_mode, len_root_dir)

        count += 1

    logging.info((' DONE: Rewriting links ').center(75, '='))


def process(root_dir, sub_dir_for_common_files=SUB_DIR_FOR_COMMON_FILES, file_glob=FILE_GLOB, nervous_mode=False, verbose=False):
    """Process a directory in-place by making a single copy of common files,
    deleting the rest and fixing the links."""
    if not (os.path.exists(root_dir) and os.path.isdir(root_dir)):
        raise ValueError(('Root directory "{!r:s}" does not exist.').format(root_dir))
    root_dir = os.path.normpath(root_dir)
    len_root_dir = len(root_dir) + 1
    logging.info(('Root directory "{:s}" ').format(root_dir))
    hash_result = _prepare_to_process(root_dir, file_glob)
    common_dir = os.path.join(root_dir, sub_dir_for_common_files)
    if len(hash_result):
        if not os.path.exists(common_dir):
            if nervous_mode:
                logging.info(('Would create "{:s}"').format(common_dir))
            else:
                os.mkdir(common_dir)
                TokenCss.writeCssToDir(common_dir)
    statistics = _copy_delete_duplicates_fix_links(hash_result, common_dir, nervous_mode, len_root_dir)
    _rewrite_links_where_files_deleted(root_dir, sub_dir_for_common_files, nervous_mode, hash_result, len_root_dir)
    if verbose:
        file_map = {v[0]:len(v) for v in hash_result.values()}
        print ('Files and sizes [{:d}]. Columns are file bytes, file MB, count, file bytes * count, file MB * count, name:').format(len(file_map))
        hdr = ('{:>12s} {:>8s}      [{:5s}] {:12s} {:8s}      {:s}').format('Bytes', 'MB', 'Count', 'Bytes*count', 'MB*count', 'Name')
        print hdr
        print '-' * len(hdr)
        for f in sorted(file_map.keys()):
            siz = os.stat(f).st_size
            print ('{:12d} {:8.3f} (MB) [{:5d}] {:12d} {:8.3f} (MB) {:s}').format(siz, siz / 1048576, file_map[f], siz * file_map[f], siz / 1048576 * file_map[f], os.path.basename(f))

    return statistics


def main():
    """Delete and relink common files."""
    program_version = 'v%s' % __version__
    program_shortdesc = 'DupeRelink.py - Delete duplicate HTML files and relink them to save space. WARNING: This deletes in-place.'
    program_license = '%s\n  Version: %s\n  Created by Paul Ross on %s.\n  Copyright 2017. All rights reserved.\n  Licensed under GPL 2.0\nUSAGE\n' % (program_shortdesc, program_version, str(__date__))
    parser = argparse.ArgumentParser(description=program_license, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-s', '--subdir', type=str, dest='subdir', default=SUB_DIR_FOR_COMMON_FILES, help='Sub-directory for writing the common files. [default: %(default)s]')
    parser.add_argument('-n', '--nervous', action='store_true', dest='nervous', default=False, help="Nervous mode, don't do anything but report what would be done. Use -l20 to see detailed result. [default: %(default)s]")
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Verbose, lists duplicate files and sizes. [default: %(default)s]')
    parser.add_argument('-l', '--loglevel', type=int, dest='loglevel', default=30, help='Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %(default)s]')
    parser.add_argument(dest='path', nargs=1, help='Path to source directory. WARNING: This will be rewritten in-place.')
    args = parser.parse_args()
    clkStart = time.clock()
    inPath = args.path[0]
    log_level = args.loglevel
    logFormat = '%(asctime)s %(levelname)-8s %(message)s'
    logging.basicConfig(level=log_level, format=logFormat, stream=sys.stdout)
    if os.path.isfile(inPath):
        logging.fatal(('Path "{:s}" must be a directory.').format(inPath))
        return 1
    if os.path.isdir(inPath):
        print ('Procesing: "{:s}" ').format(inPath)
        count_deleted, count_bytes_saved = process(inPath, sub_dir_for_common_files=args.subdir, file_glob=FILE_GLOB, nervous_mode=args.nervous, verbose=args.verbose)
        print ('Files deleted: {:12d}').format(count_deleted)
        print ('  Bytes saved: {:12d} {:8.3f} (MB)').format(count_bytes_saved, count_bytes_saved / 1048576)
    else:
        logging.fatal('%s is neither a file or a directory!' % inPath)
        return 1
    clkExec = time.clock() - clkStart
    print 'CPU time = %8.3f (S)' % clkExec
    print 'Bye, bye!'
    return 0


if __name__ == '__main__':
    exit(main())
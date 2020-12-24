# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ImageMetaTag/db.py
# Compiled at: 2017-12-11 08:50:23
"""
This module contains a set of functions to create/write to/read
and maintain an sqlite3 database of image files and their associated metadata.

In normal usage it is primarily used by  :func:`ImageMetaTag.savefig` to create the database
as figures are saved. Once the metadata database has been built up then the metadata can be
loaded with :func:`ImageMetaTag.db.read`.

(C) Crown copyright Met Office. All rights reserved.
Released under BSD 3-Clause License. See LICENSE for more details.
"""
import os, sqlite3, fnmatch, time, errno, pdb
from ImageMetaTag import META_IMG_FORMATS, DEFAULT_DB_TIMEOUT, DEFAULT_DB_ATTEMPTS
from ImageMetaTag.img_dict import readmeta_from_image, check_for_required_keys
from datetime import datetime
import numpy as np
from cStringIO import StringIO
SQLITE_IMG_INFO_TABLE = 'img_info'

def info_key_to_db_name(in_str):
    """Consistently convert a name in the img_info dict to something to be used in the database"""
    return in_str.replace(' ', '__')


def db_name_to_info_key(in_str):
    """Inverse of info_key_to_db_name"""
    return str(in_str).replace('__', ' ')


def write_img_to_dbfile(db_file, img_filename, img_info, add_strict=False, attempt_replace=False, timeout=DEFAULT_DB_TIMEOUT):
    """
    Writes image metadata to a database.

    Arguments:

    * db_file - the database file to write to. If it does not exist, it will be created.
    * img_filename - the filename of the image to which the metadata applies. Usually                      this is either the absolute path, or it is useful to make this                      the relative path, from the location of the database file.
    * img_info - a dictionary containing any number of  {tag_name: value}  pairs to be                  stored.

    Options:

    * add_strict - passed into :func:`ImageMetaTag.db.write_img_to_open_db`
    * attempt_replace - passed into :func:`ImageMetaTag.db.write_img_to_open_db`
    * timeout - default timeout to try and write to the database.

    This is commonly used in :func:`ImageMetaTag.savefig`
    """
    if len(img_info) == 0:
        raise ValueError('Size of image info dict is zero')
    if db_file is None:
        pass
    else:
        dbcn, dbcr = open_or_create_db_file(db_file, img_info, timeout=timeout)
        write_img_to_open_db(dbcr, img_filename, img_info, add_strict=add_strict, attempt_replace=attempt_replace)
        dbcn.commit()
        dbcn.close()
    return


def read(db_file, required_tags=None, tag_strings=None, db_timeout=DEFAULT_DB_TIMEOUT, db_attempts=DEFAULT_DB_ATTEMPTS):
    """
    reads in the database written by write_img_to_dbfile

    Options:
     * required_tags - a list of image tags to return, and to fail if not all are                        present
     * tag_strings - an input list that will be populated with the unique values of                      the image tags.

    Returns:
     * a list of filenames (payloads for the :class:`ImageMetaTag.ImageDict` class )
     * a dictionary, by filename, containing a dictionary of the image metadata        as *tagname: value*

    If tag_strings is not supplied, then the returned dictionary will contain a
    large number of duplicated strings, which can be an inefficient use of memory
    with large databases. If tag_strings is supplied, it will be populated with a
    unique list of strings used as tags and the dictionary will only contain
    references to this list. This can reduce memory usage considerably, both for
    the dictionary itself but also of an :class:`ImageMetaTag.ImageDict` produced
    with the dictionary.

    Will return None, None if there is a problem.

    In older versions, this was named read_img_info_from_dbfile which will still work.
    """
    if db_file is None:
        return (None, None)
    else:
        if not os.path.isfile(db_file):
            return (None, None)
        else:
            n_tries = 1
            read_db = False
            while not read_db and n_tries <= db_attempts:
                try:
                    dbcn, dbcr = open_db_file(db_file, timeout=db_timeout)
                    f_list, out_dict = read_img_info_from_dbcursor(dbcr, required_tags=required_tags, tag_strings=tag_strings)
                    dbcn.close()
                    read_db = True
                except sqlite3.OperationalError as OpErr:
                    if 'database is locked' in OpErr.message:
                        print '%s database timeout reading from file "%s", %s s' % (
                         dt_now_str(), db_file, n_tries * db_timeout)
                        n_tries += 1
                    else:
                        if OpErr.message == ('no such table: {}').format(SQLITE_IMG_INFO_TABLE):
                            return (None, None)
                        msg = ('{} for file {}').format(OpErr.message, db_file)
                        raise sqlite3.OperationalError(msg)

            if n_tries > db_attempts:
                msg = ('{} for file {}').format(OpErr.message, db_file)
                raise sqlite3.OperationalError(msg)
            dbcn.close()
            return (f_list, out_dict)

        return


read_img_info_from_dbfile = read

def merge_db_files(main_db_file, add_db_file, delete_add_db=False, delete_added_entries=False, attempt_replace=False, db_timeout=DEFAULT_DB_TIMEOUT, db_attempts=DEFAULT_DB_ATTEMPTS):
    """
    Merges two ImageMetaTag database files, with the contents of add_db_file added
    to the main_db_file. The databases should have the same tags within them for the
    merge to work.

    Options:

    * delete_add_db - if True, the added database file will be deleted afterwards
    * delete_added_entries - if delete_add_db is False, this will keep the add_db_file                              but remove the entries from it which were added to the                              main_db_file.                              This is useful if parallel processes are writing to the                              databases.  It does nothing if delete_add_db is True.
    """
    add_filelist, add_tags = read(add_db_file, db_timeout=db_timeout, db_attempts=db_attempts)
    if add_filelist is not None:
        if len(add_filelist) > 0:
            n_tries = 1
            wrote_db = False
            while not wrote_db and n_tries <= db_attempts:
                try:
                    dbcn, dbcr = open_db_file(main_db_file, timeout=db_timeout)
                    for add_file, add_info in add_tags.iteritems():
                        write_img_to_open_db(dbcr, add_file, add_info, attempt_replace=attempt_replace)

                    dbcn.commit()
                    wrote_db = True
                    dbcn.close()
                except sqlite3.OperationalError as OpErr:
                    if 'database is locked' in OpErr.message:
                        print '%s database timeout writing to file "%s", %s s' % (
                         dt_now_str(), main_db_file, n_tries * db_timeout)
                        n_tries += 1
                    else:
                        msg = ('{} for file {}').format(OpErr.message, main_db_file)
                        raise sqlite3.OperationalError(msg)

            if n_tries > db_attempts:
                msg = ('{} for file {}').format(OpErr.message, main_db_file)
                raise sqlite3.OperationalError(msg)
    if delete_add_db:
        rmfile(add_db_file)
    elif delete_added_entries:
        del_plots_from_dbfile(add_db_file, add_filelist, do_vacuum=False, allow_retries=True, skip_warning=True)
    return


def open_or_create_db_file(db_file, img_info, restart_db=False, timeout=DEFAULT_DB_TIMEOUT):
    """
    Opens a database file and sets up initial tables, then returns the connection and cursor.

    Arguments:
     * db_file - the database file to open.
     * img_info - a dictionary of image metadata to be saved to the database.

    Options:
     * restart_db - when Truem this deletes the current db file and starts again,                    if it already exists.

    Returns an open database connection (dbcn) and cursor (dbcr)
    """
    if not os.path.isfile(db_file) or restart_db:
        if os.path.isfile(db_file):
            os.remove(db_file)
        dbcn = sqlite3.connect(db_file)
        dbcr = dbcn.cursor()
        create_table_for_img_info(dbcr, img_info)
    else:
        dbcn, dbcr = open_db_file(db_file, timeout=timeout)
        table_names = list_tables(dbcr)
        if SQLITE_IMG_INFO_TABLE not in table_names:
            create_table_for_img_info(dbcr, img_info)
    return (
     dbcn, dbcr)


def create_table_for_img_info(dbcr, img_info):
    """Creates a database table, in a database cursor, to store for the input img_info"""
    create_command = ('CREATE TABLE {}(fname TEXT PRIMARY KEY,').format(SQLITE_IMG_INFO_TABLE)
    for key in img_info.keys():
        create_command += (' "{}" TEXT,').format(info_key_to_db_name(key))

    create_command = create_command[0:-1] + ')'
    try:
        dbcr.execute(create_command)
    except sqlite3.OperationalError as OpErr:
        if ('table {} already exists').format(SQLITE_IMG_INFO_TABLE) in OpErr.message:
            time.sleep(1)
        else:
            raise sqlite3.OperationalError(OpErr.message)
    except sqlite3.Error as SqErr:
        raise sqlite3.Error(SqErr.message)


def open_db_file(db_file, timeout=DEFAULT_DB_TIMEOUT):
    """
    Just opens an existing db_file, using timeouts but no retries.

    Returns an open database connection (dbcn) and cursor (dbcr)
    """
    dbcn = sqlite3.connect(db_file, timeout=timeout)
    dbcr = dbcn.cursor()
    return (
     dbcn, dbcr)


def read_db_file_to_mem(db_file, timeout=DEFAULT_DB_TIMEOUT):
    """
    Opens a pre-existing database file into a copy held in memory. This can be accessed much
    faster when doing extenstive work (a lot of select operations, for instance).

    There is a time cost in doing this; it takes a few seconds to read in a large database,
    so it is only worth doing when doing a lot of operations.

    Tests on selects on a large-ish database (250k rows) suggested it was worth doing
    for > 100 selects.

    Returns an open database connection (dbcn) and cursor (dbcr)
    """
    dbcn, _ = open_db_file(db_file, timeout=timeout)
    memfile = StringIO()
    for line in dbcn.iterdump():
        memfile.write('%s\n' % line)

    dbcn.close()
    memfile.seek(0)
    dbcn = sqlite3.connect(':memory:')
    dbcn.cursor().executescript(memfile.read())
    dbcn.commit()
    dbcr = dbcn.cursor()
    return (
     dbcn, dbcr)


def write_img_to_open_db(dbcr, filename, img_info, add_strict=False, attempt_replace=False):
    """
    Does the work for write_img_to_dbfile to add an image to the open database cursor (dbcr)

    * add_strict: if True then it will report a ValueError if you                   try and include fields that aren't defined in the table
    * attempt_replace: if True, then it will attempt to replace a database                   entry if the image is already present. Otherwise it will ignore it.
    """
    _ = dbcr.execute('select * from %s' % SQLITE_IMG_INFO_TABLE).fetchone()
    field_names = [ r[0] for r in dbcr.description ]
    field_names = [ db_name_to_info_key(x) for x in field_names ]
    add_command = ('INSERT INTO {}(fname,').format(SQLITE_IMG_INFO_TABLE)
    add_list = [filename]
    for key, item in img_info.iteritems():
        if key in field_names:
            add_command += (' "{}",').format(info_key_to_db_name(key))
            add_list.append(item)
        elif add_strict:
            raise ValueError('Attempting to add a line to the database that include invalid fields')

    add_command = add_command[0:-1] + ') VALUES(' + '?,' * (len(add_list) - 1) + '?)'
    try:
        try:
            dbcr.execute(add_command, add_list)
        except sqlite3.IntegrityError:
            if attempt_replace:
                add_repl_command = add_command.replace('INSERT ', 'INSERT OR REPLACE ')
                dbcr.execute(add_repl_command, add_list)

    finally:
        pass


def list_tables(dbcr):
    """lists the tables present, from a database cursor"""
    result = dbcr.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = sorted(zip(*result)[0])
    return table_names


def read_img_info_from_dbcursor(dbcr, required_tags=None, tag_strings=None):
    """
    Reads from an open database cursor (dbcr) for :func:`ImageMetaTag.db.read` and other routines.

    Options
     * required_tags - a list of image tags to return, and to fail if not all are present
     * tag_strings - an input list that will be populated with the unique values of the image tags
    """
    db_contents = dbcr.execute('select * from %s' % SQLITE_IMG_INFO_TABLE).fetchall()
    filename_list, out_dict = process_select_star_from(db_contents, dbcr, required_tags=required_tags, tag_strings=tag_strings)
    return (filename_list, out_dict)


def process_select_star_from(db_contents, dbcr, required_tags=None, tag_strings=None):
    """
    Converts the output from a select * from ....  command into a standard output format
    Requires a database cursor (dbcr) to identify the field names.

    Options:
     * required_tags - a list of image tags to return, and to fail if not all are present
     * tag_strings - an input list that will be populated with the unique values of the image tags

    Returns:
     * as :func:`ImageMetaTag.db.read`, but filtered according to the select.
     * a list of filenames (payloads for the :class:`ImageMetaTag.ImageDict`)
     * a dictionary, by filename, containing a dictionary of the image metadata        as tagname: value
    """
    out_dict = {}
    filename_list = []
    field_names = [ r[0] for r in dbcr.description ]
    if required_tags is not None:
        if not isinstance(required_tags, list):
            raise ValueError('Input required_tags should be a list of strings')
        else:
            for test_str in required_tags:
                if not isinstance(test_str, str):
                    raise ValueError('Input required_tags should be a list of strings')

    if tag_strings is not None:
        if not isinstance(tag_strings, list):
            raise ValueError('Input tag_strings should be a list')
    if required_tags is None and tag_strings is None:
        for row in db_contents:
            fname = str(row[0])
            filename_list.append(fname)
            img_info = {}
            for tag_name, tag_val in zip(field_names[1:], row[1:]):
                img_info[db_name_to_info_key(tag_name)] = str(tag_val)

            out_dict[fname] = img_info
            if len(filename_list) == 0 and len(out_dict) == 0:
                return (None, None)

    elif required_tags is not None and tag_strings is None:
        for row in db_contents:
            fname = str(row[0])
            filename_list.append(fname)
            img_info = {}
            for tag_name, tag_val in zip(field_names[1:], row[1:]):
                tag_name_full = db_name_to_info_key(tag_name)
                if tag_name_full in required_tags:
                    img_info[tag_name_full] = str(tag_val)

            if len(img_info) != len(required_tags):
                raise ValueError('Database entry does not contain all of the required_tags')
            out_dict[fname] = img_info
            if len(filename_list) == 0 and len(out_dict) == 0:
                return (None, None)

    elif required_tags is None and tag_strings is not None:
        for row in db_contents:
            fname = str(row[0])
            filename_list.append(fname)
            img_info = {}
            for tag_name, tag_val in zip(field_names[1:], row[1:]):
                str_tag_val = str(tag_val)
                try:
                    tag_index = tag_strings.index(str_tag_val)
                    img_info[db_name_to_info_key(tag_name)] = tag_strings[tag_index]
                except ValueError:
                    tag_strings.append(str_tag_val)
                    img_info[db_name_to_info_key(tag_name)] = tag_strings[(-1)]

            out_dict[fname] = img_info
            if len(filename_list) == 0 and len(out_dict) == 0:
                return (None, None)

    else:
        for row in db_contents:
            fname = str(row[0])
            filename_list.append(fname)
            img_info = {}
            for tag_name, tag_val in zip(field_names[1:], row[1:]):
                tag_name_full = db_name_to_info_key(tag_name)
                if tag_name_full in required_tags:
                    str_tag_val = str(tag_val)
                    try:
                        tag_index = tag_strings.index(str_tag_val)
                        img_info[tag_name_full] = tag_strings[tag_index]
                    except ValueError:
                        tag_strings.append(str_tag_val)
                        img_info[tag_name_full] = tag_strings[(-1)]

            out_dict[fname] = img_info
            if len(filename_list) == 0 and len(out_dict) == 0:
                return (None, None)

    return (filename_list, out_dict)


def del_plots_from_dbfile(db_file, filenames, do_vacuum=True, allow_retries=True, db_timeout=DEFAULT_DB_TIMEOUT, db_attempts=DEFAULT_DB_ATTEMPTS, skip_warning=False):
    """
    deletes a list of files from a database file created by :mod:`ImageMetaTag.db`

    * do_vacuum - if True, the database will be restructured/cleaned after the delete
    * allow_retries - if True, retries will be allowed if the database is locked.                    If False there are no retries, but sleep commands try to avoid the need                    when doing a large number of deletes.
    * db_timeout - overide default database timeouts, if doing retries
    * db_attempts - overide default number of attempts, if doing retries
    * skip_warning - do not warn if a filename, that has been requested to be deleted,                   does not exist in the database
    """
    if not isinstance(filenames, list):
        fn_list = [
         filenames]
    else:
        fn_list = filenames
    if db_file is None:
        pass
    elif not os.path.isfile(db_file) or len(fn_list) == 0:
        pass
    else:
        if allow_retries:
            chunk_size = 200
            chunks = __gen_chunk_of_list(fn_list, chunk_size)
            for chunk_o_filenames in chunks:
                n_tries = 1
                wrote_db = False
                while not wrote_db and n_tries <= db_attempts:
                    try:
                        dbcn, dbcr = open_db_file(db_file, timeout=db_timeout)
                        for fname in chunk_o_filenames:
                            del_cmd = 'DELETE FROM {} WHERE fname=?'
                            try:
                                dbcr.execute(del_cmd.format(SQLITE_IMG_INFO_TABLE), (fname,))
                            except sqlite3.OperationalError as OpErr_file:
                                err_check = ('no such table: {}').format(SQLITE_IMG_INFO_TABLE)
                                if OpErr_file.message == err_check:
                                    if not skip_warning:
                                        msg = 'WARNING: Unable to delete file entry "{}" from database "{}" as database table is missing'
                                        print msg.format(fname, db_file)
                                    return
                                if not skip_warning:
                                    msg = 'WARNING: unable to delete file entry: "{}", type "{}" from database'
                                    print msg.format(fname, type(fname))

                        dbcn.commit()
                        wrote_db = True
                        dbcn.close()
                    except sqlite3.OperationalError as OpErr:
                        if 'database is locked' in OpErr.message:
                            print '%s database timeout deleting from file "%s", %s s' % (
                             dt_now_str(), db_file, n_tries * db_timeout)
                            n_tries += 1
                        else:
                            raise ValueError(OpErr.message)

                if n_tries > db_attempts:
                    msg = ('{} for file {}').format(OpErr.message, db_file)
                    raise sqlite3.OperationalError(msg)

        else:
            dbcn, dbcr = open_db_file(db_file)
            for i_fn, fname in enumerate(fn_list):
                try:
                    dbcr.execute('DELETE FROM %s WHERE fname=?' % SQLITE_IMG_INFO_TABLE, (fname,))
                except:
                    if not skip_warning:
                        msg = 'WARNING: unable to delete file entry: "{}", type "{}" from database'
                        print msg.format(fname, type(fname))

                if i_fn % 100 == 0:
                    dbcn.commit()
                    time.sleep(1)

            dbcn.commit()
        if do_vacuum:
            if allow_retries:
                dbcn, dbcr = open_db_file(db_file)
            dbcn.execute('VACUUM')
            dbcn.close()
        elif not allow_retries:
            dbcn.close()
    return


def __gen_chunk_of_list(in_list, chunk_size):
    """gnerator that yields a chunk of list, of length chunk size"""
    for ndx in range(0, len(in_list), chunk_size):
        yield in_list[ndx:min(ndx + chunk_size, len(in_list))]


def select_dbfile_by_tags(db_file, select_tags):
    """
    Selects from a database file the entries that match a dict of field names/acceptable values.

    Returns the output, processed by :func:`ImageMetaTag.db.process_select_star_from`
    """
    if db_file is None:
        sel_results = None
    elif not os.path.isfile(db_file):
        sel_results = None
    else:
        dbcn, dbcr = open_db_file(db_file)
        sel_results = select_dbcr_by_tags(dbcr, select_tags)
        dbcn.close()
    return sel_results


def select_dbcr_by_tags(dbcr, select_tags):
    """
    Selects from an open database cursor (dbcr) the entries that match a dict of field
    names & acceptable values.

    Returns the output, processed by :func:`ImageMetaTag.db.process_select_star_from`
    """
    if len(select_tags) == 0:
        return read_img_info_from_dbcursor(dbcr)
    tag_names = select_tags.keys()
    tag_values = [ select_tags[x] for x in tag_names ]
    select_command = 'SELECT * FROM %s WHERE ' % SQLITE_IMG_INFO_TABLE
    n_tags = len(tag_names)
    use_tag_values = []
    for i_tag, tag_name, tag_val in zip(range(n_tags), tag_names, tag_values):
        if isinstance(tag_val, (list, tuple)):
            select_command += '%s IN (' % info_key_to_db_name(tag_name)
            select_command += (', ').join(['?'] * len(tag_val))
            select_command += ')'
            if i_tag + 1 < n_tags:
                select_command += ' AND '
            use_tag_values.extend(tag_val)
        else:
            if i_tag + 1 < n_tags:
                select_command += '%s = ? AND ' % info_key_to_db_name(tag_name)
            else:
                select_command += '%s = ?' % info_key_to_db_name(tag_name)
            use_tag_values.append(tag_val)

    db_contents = dbcr.execute(select_command, use_tag_values).fetchall()
    filename_list, out_dict = process_select_star_from(db_contents, dbcr)
    return (
     filename_list, out_dict)


def scan_dir_for_db(basedir, db_file, img_tag_req=None, subdir_excl_list=None, known_file_tags=None, verbose=False, no_file_ext=False, return_timings=False, restart_db=False):
    """
    A useful utility that scans a directory on disk for images that can go into a database.
    This should only be used to build a database from a directory of tagged images that
    did not previously use a database, or where the database file has been deleted but the
    images have not.

    For optimal performance, build the database as the plots are created (or do not delete
    the database by accident).

    Arguments:
     * basedir - the directory to start scanning.
     * db_file - the database file to save the image metadata to. A pre-existing database file                will fail unless restart_db is True

    Options:
     * img_tag_req - a list of tag names that are to be applied/created. Tags not in this list                     will not be stored. Images without all of these tags are ignored.
     * subdir_excl_list - a list of subdirectories that don't need to be scanned. ['thumbnail']                         for instance, will prevent the image thumbnails being included.
     * no_file_ext - logical to exclude the file extension in the filenames saved to the database.
     * known_file_tags - if supplied, this is a dict (keyed by filename entry),                         contains a dictionary, structured: {filename: {tag name: value}}                          for the images that are already known (so you don't need to read them                          from the files themselves as that is slow). This can be useful                          if you have a old backup of a database file that needs updating.
     * restart_db - if True, the db_file will be restarted from an empty database.
     * verbose - verbose output.
    """
    if os.path.isfile(db_file) and not restart_db:
        raise ValueError('scan_dir_for_db will not work on a pre-existing file unless restart_db\nis True, in which case the database file will be restarted as empty. Use with care.')
    if known_file_tags is not None:
        known_files = known_file_tags.keys()
    else:
        known_files = []
    if return_timings:
        prev_time = datetime.now()
        add_interval = 1
        n_added = 0
        n_add_this_timer = 0
        n_adds = []
        timings_per_add = []
    os.chdir(basedir)
    first_img = True
    for root, dirs, files in os.walk('./', followlinks=True, topdown=True):
        if subdir_excl_list is not None:
            dirs[:] = [ d for d in dirs if d not in subdir_excl_list ]
        for meta_img_format in META_IMG_FORMATS:
            for filename in fnmatch.filter(files, '*%s' % meta_img_format):
                if root == './':
                    img_path = filename
                else:
                    img_path = '%s/%s' % (root[2:], filename)
                if no_file_ext:
                    img_name = os.path.splitext(img_path)[0]
                else:
                    img_name = img_path
                if img_name in known_files:
                    known_files.remove(img_name)
                    img_info = known_file_tags.pop(img_name)
                    read_ok = True
                else:
                    read_ok, img_info = readmeta_from_image(img_path)
                if read_ok:
                    if img_tag_req:
                        use_img = check_for_required_keys(img_info, img_tag_req)
                    else:
                        use_img = True
                    if use_img:
                        if first_img:
                            db_cn, db_cr = open_or_create_db_file(db_file, img_info, restart_db=True)
                            first_img = False
                        write_img_to_open_db(db_cr, img_name, img_info)
                        if verbose:
                            print img_name
                        if return_timings:
                            n_added += 1
                            n_add_this_timer += 1
                            if n_add_this_timer % add_interval == 0:
                                time_interval_s = (datetime.now() - prev_time).total_seconds()
                                timings_per_add.append(time_interval_s / add_interval)
                                n_adds.append(n_added)
                                add_interval = np.ceil(np.sqrt(n_added))
                                n_add_this_timer = 0
                                if verbose:
                                    print 'len(n_adds)=%s, currently every %s' % (
                                     len(n_adds), add_interval)

    if not first_img:
        db_cn.commit()
        db_cn.close()
    if return_timings:
        return (n_adds, timings_per_add)
    else:
        return


def rmfile(path):
    """
    os.remove, but does not complain if the file has already been
    deleted (by a parallel process, for instance).
    """
    try:
        os.remove(path)
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            pass
        else:
            raise


def dt_now_str():
    """returns datetime.now(), as a string, in a common format"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
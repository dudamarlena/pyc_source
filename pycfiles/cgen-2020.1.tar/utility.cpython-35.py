# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/utility.py
# Compiled at: 2020-04-01 11:09:31
# Size of source mod 2**32: 22796 bytes
__doc__ = ' THIS MODULE CONTAINS ALL THE SHARED WRAPPER FUNCTIONS '
import sys, os, gzip, shutil, glob, re, json
from subprocess import Popen
from zipfile import ZipFile
from contextlib import closing

class Debug:
    """Debug"""

    def __init__(self):
        """  """
        self.debug = False
        self.logfile = sys.stderr
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.caught_error = None

    def setup(self, debug=None, logfile=None, stdout=None, stderr=None):
        """  """
        if debug is not None:
            self.debug = debug
        if logfile is not None:
            self.logfile = logfile
        if stdout is not None:
            self.stdout = stdout
        if stderr is not None:
            self.stderr = stderr

    def print_out(self, *lst):
        """ Print list of strings to the predefined stdout. """
        self.print2file(self.stdout, True, True, *lst)

    def print_err(self, *lst):
        """ Print list of strings to the predefined stdout. """
        self.print2file(self.stderr, False, True, *lst)

    def print2file(self, logfile, print2screen, addLineFeed, *lst):
        """ This function prints to the screen and logs to a file, all the strings
      given.
      # print2screen eg. True, *lst is a commaseparated list of strings
      """
        if addLineFeed:
            linefeed = '\n'
        else:
            linefeed = ''
        if print2screen:
            print(linefeed.join(str(string) for string in lst))
        try:
            file_instance = isinstance(logfile, file)
        except NameError as e:
            from io import IOBase
            try:
                file_instance = isinstance(logfile, IOBase)
            except:
                raise e

        if file_instance:
            logfile.write(linefeed.join(str(string) for string in lst) + linefeed)
        elif isinstance(logfile, str) and os.path.exists(logfile):
            with open_(logfile, 'a') as (f):
                f.write(linefeed.join(str(string) for string in lst) + linefeed)
        if not print2screen:
            print(linefeed.join(str(string) for string in lst))

    def log(self, *lst):
        """ Print list of strings to the predefined logfile if debug is set. and
      sets the caught_error message if an error is found
      """
        self.print2file(self.logfile, self.debug, True, *lst)
        if 'Error' in '\n'.join([str(x) for x in lst]):
            self.caught_error = '\n'.join([str(x) for x in lst])

    def log_no_newline(self, msg):
        """ print the message to the predefined log file without newline """
        self.print2file(self.logfile, False, False, msg)

    def graceful_exit(self, msg):
        """ This function Tries to update the MSQL database before exiting. """
        if self.caught_error:
            self.print2file(self.stderr, False, False, self.caught_error)
        self.log(msg)
        sys.exit(1)


class adv_dict(dict):
    """adv_dict"""

    def get_tree(self, list_of_keys):
        """ gettree will extract the value from a nested tree
      
      INPUT
         list_of_keys: a list of keys ie. ['key1', 'key2']
      USAGE
      >>> # Access the value for key2 within the nested dictionary
      >>> adv_dict({'key1': {'key2': 'value'}}).gettree(['key1', 'key2'])
      'value'
      """
        cur_obj = self
        for key in list_of_keys:
            cur_obj = cur_obj.get(key)
            if not cur_obj:
                break

        return cur_obj

    def invert(self):
        """ Return inverse mapping of dictionary with sorted values.
      USAGE
         >>> # Switch the keys and values
         >>> adv_dict({
         ...     'A': [1, 2, 3],
         ...     'B': [4, 2],
         ...     'C': [1, 4],
         ... }).invert()
         {1: ['A', 'C'], 2: ['A', 'B'], 3: ['A'], 4: ['B', 'C']}
      """
        inv_map = {}
        for k, v in self.items():
            if sys.version_info < (3, 0):
                acceptable_v_instance = isinstance(v, (str, int, float, long))
            else:
                acceptable_v_instance = isinstance(v, (str, int, float))
            if acceptable_v_instance:
                v = [v]
            elif not isinstance(v, list):
                raise Exception('Error: Non supported value format! Values may only be numerical, strings, or lists of numbers and strings.')
            for val in v:
                inv_map[val] = inv_map.get(val, [])
                inv_map[val].append(k)
                inv_map[val].sort()

        return inv_map


class Reg:
    """Reg"""

    def __init__(self, pattern, *flags):
        sd = {'T': 1, 'I': 2, 'L': 4, 'M': 8, 'S': 16, 'U': 32, 'X': 64}
        try:
            flag = sum([sd[f] if f in sd else int(f) for f in set(flags)]) if flags else 0
        except:
            for f in flags:
                if not isinstance(f, int) and f not in sd:
                    raise Exception("Error: Unrecognised flag argument '%s' for Reg call." % f)

            flag = 0

        if flag:
            self.re = re.compile(pattern, flag)
        else:
            self.re = re.compile(pattern)
        self.matches = None

    def sub(self, replace, string, count=0):
        """ returns new string where the matching cases (limited by the count) in
      the string is replaced. """
        return self.re.sub(replace, string, count)

    def find_all(self, s):
        """ Finds all matches in the string and returns them in a tuple. """
        return self.re.findall(s)

    def match(self, s):
        """ Matches the string to the stored regular expression, and stores all
      groups in mathches. Returns False on negative match. """
        self.matches = self.re.search(s)
        return self.matches

    def get_group(self, x):
        """ Returns requested subgroup. """
        return self.matches.group(x)

    def get_groups(self):
        """ Returns all subgroups. """
        return self.matches.groups()


class REGroup:
    """REGroup"""

    def __init__(self, pattern, flags=''):
        self.re = Reg(pattern, flags)
        self.list = []

    def match(self, s):
        """ Matching the pattern to the input string, returns True/False and
          saves the matched string in the internal list
      """
        if self.re.match(s):
            self.list.append(s)
            return True
        else:
            return False


def seqs_from_file(filename, exit_on_err=False, return_qual=False):
    """Extract sequences from a file
   
   Name:
      seqs_from_file
   Author(s):
      Martin C F Thomsen
   Date:
      18 Jul 2013
   Description:
      Iterator which extract sequence data from the input file
   Args:
      filename: string which contain a path to the input file
   Supported Formats:
      fasta, fastq
   
   USAGE:
   >>> import os, sys
   >>> # Create fasta test file
   >>> file_content = ('>head1 desc1
this_is_seq_1
>head2 desc2
'
                       'this_is_seq_2
>head3 desc3
this_is_seq_3
')
   >>> with open_('test.fsa', 'w') as f: f.write(file_content)
   >>> # Parse and print the fasta file
   >>> for seq, name, desc in SeqsFromFile('test.fsa'):
   ...    print ">%s %s
%s"%(name, desc, seq)
   ...
   >head1 desc1
   this_is_seq_1
   >head2 desc2
   this_is_seq_2
   >head3 desc3
   this_is_seq_3
   """
    if not isinstance(filename, str):
        msg = 'Filename has to be a string.'
        if exit_on_err:
            sys.stderr.write('Error: %s\n' % msg)
            sys.exit(1)
        else:
            raise IOError(msg)
        if not os.path.exists(filename):
            msg = 'File "%s" does not exist.' % filename
            if exit_on_err:
                sys.stderr.write('Error: %s\n' % msg)
                sys.exit(1)
            else:
                raise IOError(msg)
            with open_(filename, 'rt') as (f):
                query_seq_segments = []
                seq, name, desc, qual = ('', '', '', '')
                add_segment = query_seq_segments.append
                for l in f:
                    if len(l.strip()) == 0:
                        pass
                    else:
                        fields = l.strip().split()
                        if l.startswith('>'):
                            if query_seq_segments != []:
                                seq = ''.join(query_seq_segments)
                                yield (seq, name, desc)
                                seq, name, desc = ('', '', '')
                                del query_seq_segments[:]
                            name = fields[0][1:]
                            desc = ' '.join(fields[1:])
                        else:
                            if l.startswith('@'):
                                name = fields[0][1:]
                                desc = ' '.join(fields[1:])
                                try:
                                    seq = next(f).strip().split()[0]
                                    l = next(f)
                                    qual = next(f).strip()
                                except:
                                    break

                                if return_qual:
                                    yield (
                                     seq, qual, name, desc)
                                else:
                                    yield (
                                     seq, name, desc)
                                seq, name, desc, qual = ('', '', '', '')
                            elif len(fields[0]) > 0:
                                add_segment(fields[0])

                if query_seq_segments != []:
                    seq = ''.join(query_seq_segments)
                    yield (seq, name, desc)


def open_(filename, mode=None, compresslevel=9):
    """Switch for both open() and gzip.open().
   
   Determines if the file is normal or gzipped by looking at the file
   extension.
   
   The filename argument is required; mode defaults to 'rb' for gzip and 'r'
   for normal and compresslevel defaults to 9 for gzip.
   
   >>> import gzip
   >>> from contextlib import closing
   >>> with open_(filename) as f:
   ...     f.read()
   """
    if filename[-3:] == '.gz':
        if mode is None:
            mode = 'rt'
        return closing(gzip.open(filename, mode, compresslevel))
    else:
        if mode is None:
            mode = 'r'
        return open(filename, mode)


def load_json(json_object):
    """ Load json from file or file name """
    content = None
    if isinstance(json_object, str) and os.path.exists(json_object):
        with open_(json_object) as (f):
            try:
                content = json.load(f)
            except Exception as e:
                debug.log("Warning: Content of '%s' file is not json." % f.name)

    else:
        if hasattr(json_object, 'read'):
            try:
                content = json.load(json_object)
            except Exception as e:
                debug.log("Warning: Content of '%s' file is not json." % json_object.name)

        else:
            debug.log('%s\nWarning: Object type invalid!' % json_object)
        return content


def sort2groups(array, gpat=['_R1', '_R2']):
    """ Sort an array of strings to groups by patterns """
    groups = [REGroup(gp) for gp in gpat]
    unmatched = []
    for item in array:
        matched = False
        for m in groups:
            if m.match(item):
                matched = True
                break

        if not matched:
            unmatched.append(item)

    return ([sorted(m.list) for m in groups], sorted(unmatched))


def sort_and_distribute(array, splits=2):
    """ Sort an array of strings to groups by alphabetically continuous
       distribution
   """
    if not isinstance(array, (list, tuple)):
        raise TypeError('array must be a list')
    if not isinstance(splits, int):
        raise TypeError('splits must be an integer')
    remaining = sorted(array)
    if sys.version_info < (3, 0):
        myrange = xrange(splits)
    else:
        myrange = range(splits)
    groups = [[] for i in myrange]
    while len(remaining) > 0:
        for i in myrange:
            if len(remaining) > 0:
                groups[i].append(remaining.pop(0))

    return groups


def mkpath(filepath, permissions=511):
    """ This function executes a mkdir command for filepath and with permissions
   (octal number with leading 0 or string only)
   # eg. mkpath("path/to/file", "0o775")
   """
    if isinstance(permissions, str):
        permissions = sum([int(x) * 8 ** i for i, x in enumerate(reversed(permissions))])
    if not os.path.exists(filepath):
        debug.log('Creating Directory %s (permissions: %s)' % (
         filepath, permissions))
        os.makedirs(filepath, permissions)
    else:
        debug.log('Warning: The directory ' + filepath + ' already exists')
    return filepath


def create_zip_dir(zipfile_path, *file_list):
    """ This function creates a zipfile located in zipFilePath with the files in
   the file list
   # fileList can be both a comma separated list or an array
   """
    try:
        if isinstance(file_list, (list, tuple)) and len(file_list) == 1 and isinstance(file_list[0], (list, tuple)):
            file_list = file_list[0]
        if isinstance(file_list, str):
            file_list = [file_list]
        if file_list:
            with ZipFile(zipfile_path, 'w') as (zf):
                for cur_file in file_list:
                    if '/' in cur_file:
                        os.chdir('/'.join(cur_file.split('/')[:-1]))
                    elif '/' in zipfile_path:
                        os.chdir('/'.join(zipfile_path.split('/')[:-1]))
                    zf.write(cur_file.split('/')[(-1)])

        else:
            debug.log('Error: No Files in list!', zipfile_path + ' was not created!')
    except Exception as e:
        debug.log('Error: Could not create zip dir! argtype: ' + str(type(file_list)), 'FileList: ' + str(file_list), 'Errormessage: ' + str(e))


def file_zipper(root_dir):
    """ This function will zip the files created in the runroot directory and
   subdirectories """
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if root != '':
            if root[(-1)] != '/':
                root += '/'
            for current_file in files:
                filepath = '%s/%s' % (root, current_file)
                try:
                    file_size = os.path.getsize(filepath)
                except Exception as e:
                    file_size = 0
                    debug.log('Error: file_zipper failed to zip following file ' + filepath, e)

                if file_size > 50 and current_file[-3:] != '.gz' and not os.path.islink(filepath) and current_file[-4:] == '.zip':
                    ec = Popen('unzip -qq "%s" -d %s > /dev/null 2>&1' % (filepath, root), shell=True).wait()
                    if ec > 0:
                        debug.log('Error: fileZipper failed to unzip following file %s' % filepath)
                        continue
                    else:
                        ec = Popen('rm -f "%s" > /dev/null 2>&1' % filepath, shell=True).wait()
                        if ec > 0:
                            debug.log('Error: fileZipper failed to delete the original zip file (%s)' % filepath)
                        filepath = filepath[:-4]
                    with open_(filepath, 'rb') as (f):
                        with open_(filepath + '.gz', 'wb', 9) as (gz):
                            gz.writelines(f)
                    try:
                        os.remove(filepath)
                    except OSError as e:
                        debug.log('WARNING! The file %s could not be removed!\n%s' % (
                         current_file, e))


def file_unzipper(directory):
    """ This function will unzip all files in the runroot directory and
   subdirectories
   """
    debug.log('Unzipping directory (%s)...' % directory)
    for root, dirs, files in os.walk(directory, topdown=False):
        if root != '':
            orig_dir = os.getcwd()
            os.chdir(directory)
            Popen('gunzip -q -f *.gz > /dev/null 2>&1', shell=True).wait()
            Popen('unzip -qq -o "*.zip" > /dev/null 2>&1', shell=True).wait()
            Popen('rm -f *.zip > /dev/null 2>&1', shell=True).wait()
            os.chdir(orig_dir)


def move_file(src, dst):
    """ this function will simply move the file from the source path to the dest
   path given as input
   """
    src = re.sub('[^\\w/\\-\\.\\*]', '', src)
    dst = re.sub('[^\\w/\\-\\.\\*]', '', dst)
    if len(re.sub('[\\W]', '', src)) < 5 or len(re.sub('[\\W]', '', dst)) < 5:
        debug.log("Error: Moving file failed. Provided paths are invalid! src='%s' dst='%s'" % (src, dst))
    else:
        check = False
        if dst[(-1)] == '/':
            if os.path.exists(dst):
                check = True
            else:
                debug.log('Error: Moving file failed. Destination directory does not exist (%s)' % dst)
        else:
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    check = True
                    dst += '/'
                else:
                    debug.log('Error: Moving file failed. %s exists!' % dst)
            else:
                if os.path.exists(os.path.dirname(dst)):
                    check = True
                else:
                    debug.log('Error: Moving file failed. %s is an invalid distination!' % dst)
                if check:
                    files = glob.glob(src)
                    if len(files) != 0:
                        debug.log('Moving File(s)...', 'Move from %s' % src, 'to %s' % dst)
                        for file_ in files:
                            invalid_chars = re.findall('[^\\w/\\-\\.\\*]', os.path.basename(file_))
                            if invalid_chars:
                                debug.graceful_exit('Error: File %s contains invalid characters %s!' % (
                                 os.path.basename(file_), invalid_chars))
                                continue
                                if os.path.isfile(file_):
                                    debug.log('Moving file: %s' % file_)
                                    shutil.move(file_, dst)
                                else:
                                    debug.log('Error: Moving file failed. %s is not a regular file!' % file_)

                else:
                    debug.log('Error: Moving file failed. No files were found! (%s)' % src)


def copy_file(src, dst, ignore=None):
    """ this function will simply copy the file from the source path to the dest
   path given as input
   """
    src = re.sub('[^\\w/\\-\\.\\*]', '', src)
    dst = re.sub('[^\\w/\\-\\.\\*]', '', dst)
    if len(re.sub('[\\W]', '', src)) < 5 or len(re.sub('[\\W]', '', dst)) < 5:
        debug.log("Error: Copying file failed. Provided paths are invalid! src='%s' dst='%s'" % (src, dst))
    else:
        check = False
        if dst[(-1)] == '/':
            if os.path.exists(dst):
                check = True
            else:
                debug.log('Error: Copying file failed. Destination directory does not exist (%s)' % dst)
        else:
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    check = True
                    dst += '/'
                else:
                    debug.log('Error: Copying file failed. %s exists!' % dst)
            else:
                if os.path.exists(os.path.dirname(dst)):
                    check = True
                else:
                    debug.log('Error: Copying file failed. %s is an invalid distination!' % dst)
                if check:
                    files = glob.glob(src)
                    if ignore is not None:
                        files = [fil for fil in files if ignore not in fil]
                    if len(files) != 0:
                        debug.log('Copying File(s)...', 'Copy from %s' % src, 'to %s' % dst)
                        for file_ in files:
                            if os.path.isfile(file_):
                                debug.log('Copying file: %s' % file_)
                                shutil.copy(file_, dst)
                            else:
                                debug.log('Error: Copying file failed. %s is not a regular file!' % file_)

                else:
                    debug.log('Error: Copying file failed. No files were found! (%s)' % src)


def copy_dir(src, dst):
    """ this function will simply copy the file from the source path to the dest
   path given as input
   """
    try:
        debug.log('copy dir from ' + src, 'to ' + dst)
        shutil.copytree(src, dst)
    except Exception as e:
        debug.log('Error: happened while copying!\n%s\n' % e)


debug = Debug()
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/topper/file_io.py
# Compiled at: 2020-02-16 18:04:47
# Size of source mod 2**32: 7522 bytes
import json, re
from datetime import datetime, timedelta
from pathlib import Path
from topper.utils.logging import get_logger

class FileReader:
    __doc__ = '\n    Utils class managing read, parse and move of data files\n    '
    REJECT_FOLDER = 'errors'
    ARCHIVE_FOLDER = 'archive'
    CURRENT_FOLDER = 'current'

    def __init__(self, path, checkpoint_dir):
        self.path = Path(path)
        self._checkpoint_dir = Path(checkpoint_dir)
        self.logger = get_logger(__name__)

    def read_file(self):
        """
        Parse valid files and returns content as a generator
        :return: Generator(tuple(country, user_id, sng_id))
        """
        if self.path.is_file():
            if self.check_file_name(self.path.name):
                return self._parse_log_file()
        self.logger.error("Can't process file={}".format(self.path))
        self.reject_file()
        return None

    def check_file_name--- This code section failed: ---

 L.  40         0  LOAD_STR                 'listen-(\\d{8}).log'
                2  STORE_FAST               'regex_filename'

 L.  42         4  LOAD_GLOBAL              re
                6  LOAD_METHOD              findall
                8  LOAD_FAST                'regex_filename'
               10  LOAD_FAST                'file_name'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'date_str'

 L.  43        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'date_str'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_CONST               1
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    90  'to 90'

 L.  45        28  SETUP_FINALLY        48  'to 48'

 L.  46        30  LOAD_GLOBAL              datetime
               32  LOAD_METHOD              strptime
               34  LOAD_FAST                'date_str'
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_STR                 '%Y%m%d'
               42  CALL_METHOD_2         2  ''
               44  POP_BLOCK        
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    28  '28'

 L.  47        48  DUP_TOP          
               50  LOAD_GLOBAL              ValueError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    86  'to 86'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  48        62  LOAD_FAST                'self'
               64  LOAD_ATTR                logger
               66  LOAD_METHOD              warning
               68  LOAD_STR                 'Date cannot be parsed in file name: {}'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'file_name'
               74  CALL_METHOD_1         1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L.  49        80  POP_EXCEPT       
               82  LOAD_CONST               False
               84  RETURN_VALUE     
             86_0  COME_FROM            54  '54'
               86  END_FINALLY      
               88  JUMP_FORWARD        112  'to 112'
             90_0  COME_FROM            26  '26'

 L.  52        90  LOAD_FAST                'self'
               92  LOAD_ATTR                logger
               94  LOAD_METHOD              warning
               96  LOAD_STR                 'File name is invalid {}'
               98  LOAD_METHOD              format
              100  LOAD_FAST                'file_name'
              102  CALL_METHOD_1         1  ''
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          

 L.  53       108  LOAD_CONST               False
              110  RETURN_VALUE     
            112_0  COME_FROM            88  '88'

Parse error at or near `POP_TOP' instruction at offset 58

    def _parse_log_file(self):
        """
        Parse the input file and yield results as a tuple (country, user_id, song_id)
        :return: list(tuple(str, str, str)): tuple of (country, user_id, song_id)
        """
        regex_line = '^\\d+\\|\\d+\\|[A-Z]{2}$'
        countries = self._countries_iso2()
        with self.path.open() as (file):
            for raw_line in file.readlines():
                if re.matchregex_lineraw_line:
                    sng_id, user_id, country = raw_line.rstrip().split(sep='|')
                    if country in countries:
                        (yield (
                         country, user_id, sng_id))
                    else:
                        self.logger.warning("Line is incorrect. The country '{}' doesn't exists".format(country))
                else:
                    self.logger.warning('Line is incorrect. Pattern invalid: {}'.format(raw_line))

    def reject_file(self):
        """
        Move invalid files to error folder
        """
        if not (self._checkpoint_dir / self.REJECT_FOLDER).exists():
            (self._checkpoint_dir / self.REJECT_FOLDER).mkdir(parents=True)
        self.path.rename(self._checkpoint_dir / self.REJECT_FOLDER / self.path.name)

    def move_file_archive(self):
        """
        Move old files to archive folder
        """
        if not (self._checkpoint_dir / self.ARCHIVE_FOLDER).exists():
            (self._checkpoint_dir / self.ARCHIVE_FOLDER).mkdir(parents=True)
        self.path.rename(self._checkpoint_dir / self.ARCHIVE_FOLDER / self.path.name)

    def move_file_top_days(self):
        """
        Move current files to top_days folder
        """
        if self.path.is_file():
            if self.check_file_name(self.path.name):
                if not (self._checkpoint_dir / self.CURRENT_FOLDER).exists():
                    (self._checkpoint_dir / self.CURRENT_FOLDER).mkdir(parents=True)
                self.path.rename(self._checkpoint_dir / self.CURRENT_FOLDER / self.path.name)

    @staticmethod
    def _countries_iso2--- This code section failed: ---

 L. 107         0  LOAD_GLOBAL              Path
                2  LOAD_GLOBAL              __file__
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_ATTR                parent
                8  STORE_FAST               'current_dir'

 L. 108        10  LOAD_FAST                'current_dir'
               12  LOAD_STR                 'resources'
               14  BINARY_TRUE_DIVIDE
               16  LOAD_STR                 'countries.json'
               18  BINARY_TRUE_DIVIDE
               20  STORE_FAST               'countries_path'

 L. 109        22  LOAD_GLOBAL              open
               24  LOAD_FAST                'countries_path'
               26  CALL_FUNCTION_1       1  ''
               28  SETUP_WITH           76  'to 76'
               30  STORE_FAST               'raw_file'

 L. 110        32  LOAD_GLOBAL              json
               34  LOAD_METHOD              load
               36  LOAD_FAST                'raw_file'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'json_data'

 L. 111        42  LOAD_GLOBAL              list
               44  LOAD_GLOBAL              map
               46  LOAD_LAMBDA              '<code_object <lambda>>'
               48  LOAD_STR                 'FileReader._countries_iso2.<locals>.<lambda>'
               50  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               52  LOAD_FAST                'json_data'
               54  CALL_FUNCTION_2       2  ''
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'code_list'

 L. 112        60  LOAD_FAST                'code_list'
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM_WITH       28  '28'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 64


class FolderReader:
    __doc__ = '\n    Utils class managing folders of data files\n    '

    def __init__(self, _path_dir, _checkpoint_directory):
        self._path_dir = Path(_path_dir)
        self._checkpoint_directory = _checkpoint_directory
        self.logger = get_logger(__name__)

    def process_folder_landing(self):
        """
        Process landing folder and move valid files to folder `current`, invalid ones to `errors`
        :return:
        """
        if self._path_dir.is_dir():
            for valid_file in self._list_files():
                valid_file.move_file_top_days()

        else:
            self.logger.error('Path provided is not a directory: {}'.format(self._path_dir))

    def read_folder_current(self):
        """
        Scan every files in path self._path_dir and returns every valid files.
        Invalid files are thrown to errors' folder
        :return: list(pathlib.Path): list of files to process
        """
        if self._path_dir.is_dir():
            res = []
            for valid_file in self._list_files():
                res.append(valid_file.read_file())
            else:
                return res

        self.logger.error('Path provided is not a directory: {}'.format(self._path_dir))
        return None

    def _list_files(self):
        """
        Get files to process and send invalid files to error folder
        :return: a list of valid pathlib.Path
        """
        file = []
        for file_name in self._path_dir.iterdir():
            file_reader = FileReader(path=(str(file_name)), checkpoint_dir=(self._checkpoint_directory))
            if file_name.is_file() and file_reader.check_file_name(file_name.name):
                file.append(file_reader)
            else:
                file_reader.reject_file()
        else:
            return file

    def archive_old_files(self, days):
        """
        Move files oldest than X days from process to archive folder
        :param days: number of days to keep
        """
        oldest_day = datetime.today() - timedelta(days=days)
        if self._path_dir.is_dir():
            for file_name in self._path_dir.iterdir():
                file_reader = FileReader(self._path_dir / file_name, self._checkpoint_directory)
                file_date = file_reader.check_file_name(file_name.name)
                if file_date < oldest_day:
                    file_reader.move_file_archive()


class FileWriter:
    __doc__ = '\n    Utils class managing write of output files\n    '

    def __init__(self, path):
        self._path = Path(path)
        self.logger = get_logger(__name__)

    def write_result(self, dict_result):
        """
        Write result file
        :param dict_result: dictionary to write
        """
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True)
        with open((self._path), mode='w') as (output_file):
            for country, data in dict_result.items():
                format_song_nber_list = map(lambda x: '{},{}'.formatx[0]x[1], data)
                line = '{c}|'.format(c=country)
                line += ':'.join(format_song_nber_list)
                line += '\n'
                output_file.write(line)
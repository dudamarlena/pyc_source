# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/topper/__main__.py
# Compiled at: 2020-02-16 18:04:27
# Size of source mod 2**32: 2306 bytes
import sys
from datetime import datetime
from pathlib import Path
from topper.file_io import FolderReader, FileReader, FileWriter
from topper.process import Process
from topper.utils.logging import get_logger
from topper.utils.parser import parse_args

class Topper:
    __doc__ = '\n    Main class running Topper application\n    '

    def __init__(self, arguments):
        self.checkpoint_directory = Path(arguments.checkpoint_directory)
        self.logger = get_logger(__name__)
        self.landing_folder = Path(arguments.landing_folder)
        self.current_folder = self.checkpoint_directory / FileReader.CURRENT_FOLDER
        self.output_directory = Path(arguments.output_directory)
        self.mode = arguments.mode
        self.nb_days = 7

    def main(self):
        """
        Main processing
        """
        self.logger.info('Topper')
        start_time = datetime.now()
        landing_folder = FolderReader(self.landing_folder, self.checkpoint_directory)
        landing_folder.process_folder_landing()
        current_reader = FolderReader(self.current_folder, self.checkpoint_directory)
        current_reader.archive_old_files(days=(self.nb_days))
        days_data = current_reader.read_folder_current()
        if days_data:
            process = Process(self.mode)
            process.reduce_days(days_data)
            res = process.get_top50()
            output_file = self.output_directory / '{mode}_top50_{d}.txt'.format(mode=(self.mode), d=(datetime.now().strftime('%Y%m%d')))
            result_writer = FileWriter(output_file)
            result_writer.write_result(res)
        now = datetime.now()
        time_run = (now - start_time).total_seconds()
        self.logger.info('Processing time: {} seconds'.format(time_run))


def main():
    """main"""
    args = parse_args(args=(sys.argv[1:]))
    Topper(args).main()


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/omkarpathak27/Documents/GITS/py-resume-parser/pyresparser/command_line.py
# Compiled at: 2019-11-30 22:26:20
# Size of source mod 2**32: 5203 bytes
import os, json, argparse
from pprint import pprint
import io, multiprocessing as mp, urllib
from urllib.request import Request, urlopen
from pyresparser import ResumeParser

def print_cyan(text):
    print('\x1b[96m {}\x1b[00m'.format(text))


class ResumeParserCli(object):

    def __init__(self):
        self._ResumeParserCli__parser = argparse.ArgumentParser()
        self._ResumeParserCli__parser.add_argument('-f',
          '--file',
          help='resume file to be extracted')
        self._ResumeParserCli__parser.add_argument('-d',
          '--directory',
          help='directory containing all the resumes to be extracted')
        self._ResumeParserCli__parser.add_argument('-r',
          '--remotefile',
          help='remote path for resume file to be extracted')
        self._ResumeParserCli__parser.add_argument('-re',
          '--custom-regex',
          help='custom regex for parsing mobile numbers')
        self._ResumeParserCli__parser.add_argument('-sf',
          '--skillsfile',
          help='custom skills CSV file against                   which skills are searched for')
        self._ResumeParserCli__parser.add_argument('-e',
          '--export-format',
          help='the information export format (json)')

    def __banner(self):
        banner_string = '\n                 ____  __  __________  _________  ____  _____________  _____\n                / __ \\/ / / / ___/ _ \\/ ___/ __ \\/ __ `/ ___/ ___/ _ \\/ ___/\n               / /_/ / /_/ / /  /  __(__  ) /_/ / /_/ / /  (__  )  __/ /\n              / .___/\\__, /_/   \\___/____/ .___/\\__,_/_/  /____/\\___/_/\n             /_/    /____/              /_/\n\n           - By Omkar Pathak (omkarpathak27@gmail.com)\n        '
        print(banner_string)

    def export_data(self, exported_data, args):
        """function to export resume data in specified format
        """
        if args.export_format:
            if args.export_format == 'json':
                json_data = json.dumps(exported_data)
                return json_data
        else:
            return exported_data

    def extract_resume_data(self):
        args = self._ResumeParserCli__parser.parse_args()
        if not args.export_format:
            self._ResumeParserCli__banner()
        if args.remotefile:
            return self.export_data(self._ResumeParserCli__extract_from_remote_file(args.remotefile, args.skillsfile, args.custom_regex), args)
        if args.file:
            if not args.directory:
                return self.export_data(self._ResumeParserCli__extract_from_file(args.file, args.skillsfile, args.custom_regex), args)
        if args.directory:
            if not args.file:
                return self.export_data(self._ResumeParserCli__extract_from_directory(args.directory, args.skillsfile, args.custom_regex), args)
        self._ResumeParserCli__parser.print_help()

    def __extract_from_file(self, file, skills_file=None, custom_regex=None):
        if os.path.exists(file):
            print_cyan('Extracting data from: {}'.format(file))
            resume_parser = ResumeParser(file, skills_file, custom_regex)
            return [
             resume_parser.get_extracted_data()]
        else:
            return 'File not found. Please provide a valid file name.'

    def __extract_from_directory(self, directory, skills_file=None, custom_regex=None):
        if os.path.exists(directory):
            pool = mp.Pool(mp.cpu_count())
            resumes = []
            for root, _, filenames in os.walk(directory):
                for filename in filenames:
                    file = os.path.join(root, filename)
                    resumes.append([file, skills_file, custom_regex])

            results = pool.map(resume_result_wrapper, resumes)
            pool.close()
            pool.join()
            return results
        else:
            return 'Directory not found. Please provide a valid directory.'

    def __extract_from_remote_file(self, remote_file, skills_file, custom_regex):
        try:
            print_cyan('Extracting data from: {}'.format(remote_file))
            req = Request(remote_file, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            _file = io.BytesIO(webpage)
            _file.name = remote_file.split('/')[(-1)]
            resume_parser = ResumeParser(_file, skills_file, custom_regex)
            return [resume_parser.get_extracted_data()]
        except urllib.error.HTTPError:
            return 'File not found. Please provide correct URL for resume file'


def resume_result_wrapper(args):
    print_cyan('Extracting data from: {}'.format(args[0]))
    parser = ResumeParser(args[0], args[1], args[2])
    return parser.get_extracted_data()


def main():
    cli_obj = ResumeParserCli()
    pprint(cli_obj.extract_resume_data())
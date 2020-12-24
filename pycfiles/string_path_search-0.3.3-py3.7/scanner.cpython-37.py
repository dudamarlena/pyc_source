# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\string_path_search\scanner.py
# Compiled at: 2019-08-13 15:21:29
# Size of source mod 2**32: 15858 bytes
"""Classes and methods to support recursive string searching within a directory"""
from abc import abstractmethod
import codecs, csv, math, os, re, shutil, sys, tarfile
from time import strftime
import unicodedata, zipfile, xlsxwriter
from PIL import Image
from .utils import calculate_md5, LOGGER, make_dir_safe, random_string
DIR_REGEX = re.compile('[/]$')
JAR_REGEX = re.compile('\\.jar$')
TAR_REGEX = re.compile('\\.(?:tar|tar.gz|tgz|tar.bzip2|tar.bz2|tbz2|txz|tar.xz)$')
ZIP_REGEX = re.compile('\\.zip$')
ARCH_REGEX = re.compile('\\.(?:cab|cpio|ear|jar|rpm|tar|tar.gz|tgz|tar.bzip2|tar.bz2|tbz2|tgz|tar.xz|war|zip)$')

class Scanner:
    __doc__ = 'Class to scan a directory tree for a set of strings'
    HEADERS = ('String', 'MD5 Digest', 'Name', 'Location')

    def __init__(self, configs):
        """
        Setup the class instance.

        Parameters:
            configs -- Dictionary of settings populated from the command line by parse_args()
        """
        self.scan_root = configs['scan_root']
        self.temp_dir = configs['temp_dir']
        self.ignore_case = configs['ignore_case']
        self.search_strings = []
        for search_string in configs['search_strings']:
            normal_string = unicodedata.normalize('NFKD', search_string)
            if self.ignore_case:
                normal_string = normal_string.casefold()
            self.search_strings.append((normal_string, search_string))

        self.exclusions = configs['exclusions']
        self.scan_archives = configs['scan_archives']
        self.scan_results = {}
        self.stats = {}
        if sys.version_info[0] + sys.version_info[1] / 10 < 3.4:
            LOGGER.error('ERROR: This script requires Python 3.4 or greater.')
            sys.exit(-1)
        if not os.path.exists(configs['scan_root']):
            raise ValueError('scan_root {0} does not exist'.format(configs['scan_root']))
        if not self.search_strings:
            raise ValueError('No strings to search!')
        if self.scan_archives:
            make_dir_safe(configs['temp_dir'])

    def _walk(self, thing=None, parent=None):
        """Walk a tree based on thing."""
        if not thing:
            thing = self.scan_root
        else:
            if os.path.isdir(thing):
                yield from self._dir_walk(thing)
            else:
                if self.scan_archives:
                    if ZIP_REGEX.search(thing) or JAR_REGEX.search(thing):
                        yield from self._zip_walk(thing, parent)
            if self.scan_archives and TAR_REGEX.search(thing):
                yield from self._tar_walk(thing, parent)
            else:
                if ARCH_REGEX.search(thing):
                    if self.scan_archives:
                        LOGGER.warning('Skipping unsupported archive %s', thing)
                else:
                    if not os.path.isfile(thing):
                        LOGGER.warning("Thing '%s' is neither a directory nor is it a file", thing)
                        return
                    try:
                        with open(thing, 'rb') as (fid):
                            file_bytes = fid.read()
                            location = self.scan_root
                            if thing.startswith(location):
                                location = os.path.dirname(thing)
                            else:
                                location = os.path.join(location, os.path.dirname(thing))
                            yield (
                             os.path.basename(thing), location,
                             calculate_md5(file_bytes), file_bytes)
                    except FileNotFoundError:
                        LOGGER.error("Can't open file=%s", thing)
                        return

    def _dir_walk(self, path):
        """Walk a directory."""
        LOGGER.info('Walking dir=%s', path)
        for entry in os.scandir(path):
            if os.path.basename(entry.path).casefold() in self.exclusions:
                continue
            yield from self._walk(entry.path)

        if False:
            yield None

    def _zip_walk(self, zip_file, parent=None):
        """
        Generate name, filebuf tuples from a recursive zip scan.

        Args:
            zip_file -- The full path to the .zip file to scan.
            parent - The root for the extraction if this is an inner archive.
        """
        archive_type = 'jar' if JAR_REGEX.search(zip_file) else 'zip'
        LOGGER.info('Walking %s file=%s', archive_type, zip_file)
        parent = '/'.join([parent, os.path.basename(zip_file)]) if parent else os.path.basename(zip_file)
        with zipfile.ZipFile(zip_file) as (zip_archive):
            for info in zip_archive.infolist():
                name = info.filename
                if DIR_REGEX.search(name):
                    continue
                elif os.path.basename(name).casefold() in self.exclusions:
                    continue
                elif ARCH_REGEX.search(name):
                    extract_dir = os.path.join(self.temp_dir, random_string())
                    make_dir_safe(extract_dir)
                    inner_archive = os.path.join(extract_dir, name)
                    try:
                        try:
                            zip_archive.extract(name, extract_dir)
                            if ARCH_REGEX.search(name):
                                yield from self._walk(inner_archive, parent)
                        except BaseException:
                            LOGGER.error('Caught an exception of type=%s while processing inner archive %s', sys.exc_info()[0], name)
                            continue

                    finally:
                        shutil.rmtree(extract_dir)

                else:
                    fid = None
                    try:
                        with zip_archive.open(name) as (fid):
                            file_bytes = fid.read()
                            yield (os.path.basename(name),
                             '/'.join([self.scan_root, parent,
                              os.path.dirname(name)]),
                             calculate_md5(file_bytes), file_bytes)
                    except BaseException:
                        LOGGER.error('Caught an exception of type=%s: %s', sys.exc_info()[0], sys.exc_info()[1])

    def _tar_walk(self, tar_file, parent=None):
        """
        Generate name, filebuf tuples from a recursive tar scan.

        Args:
            tar_file -- The name of the .tar (or compressed variant) file
            to scan.
        """
        LOGGER.info('Walking tar file=%s', tar_file)
        parent = '/'.join([parent, os.path.basename(tar_file)]) if parent else os.path.basename(tar_file)
        with tarfile.open(tar_file, 'r') as (tar_archive):
            for entry in tar_archive:
                if not entry.isreg():
                    continue
                elif os.path.basename(entry.name).casefold() in self.exclusions:
                    continue
                elif ARCH_REGEX.search(entry.name):
                    extract_dir = os.path.join(self.temp_dir, random_string())
                    make_dir_safe(extract_dir)
                    inner_archive = os.path.join(extract_dir, entry.name)
                    try:
                        try:
                            tar_archive.extract(entry, extract_dir)
                            if ARCH_REGEX.search(inner_archive):
                                yield from self._walk(inner_archive, parent)
                        except BaseException:
                            LOGGER.error('Caught an exception of type=%s while processing inner archive=%s', sys.exc_info()[0], entry.name)
                            continue

                    finally:
                        shutil.rmtree(extract_dir)

                    continue
                else:
                    try:
                        with tar_archive.extractfile(entry) as (fid):
                            file_bytes = fid.read()
                            yield (os.path.basename(entry.name),
                             '/'.join([self.scan_root, parent, os.path.dirname(entry.name)]),
                             calculate_md5(file_bytes), file_bytes)
                    except BaseException:
                        LOGGER.error('Caught an exception of type=%s while extracting file=%s', sys.exc_info()[0], entry.name)

    def _scan_file(self, file_bytes):
        """
        Generator method that yields matching search_strings.

        Args:
            file_bytes -- The content of a file, as a byte string.
        """
        file_str = unicodedata.normalize('NFKD', codecs.decode(file_bytes, 'utf-8',
          errors='ignore'))
        if not file_str:
            return
        if self.ignore_case:
            file_str = file_str.casefold()
        for normal_str, search_str in self.search_strings:
            if normal_str in file_str:
                yield search_str

    def scan(self):
        """Scan scan_root and print matches."""
        LOGGER.info('Scanning %s', self.scan_root)
        self.scan_results = {}
        md5s = set()
        self.stats = {'files_scanned':0,  'files_matched':0}
        for name, path, md5, file_bytes in self._walk(None):
            self.stats['files_scanned'] += 1
            if self.stats['files_scanned'] % 1000 == 0:
                LOGGER.info('Matched %d of %d files scanned so far.', self.stats['files_matched'], self.stats['files_scanned'])
            for matched_string in self._scan_file(file_bytes):
                if matched_string not in self.scan_results.keys():
                    self.scan_results[matched_string] = []
                self.scan_results[matched_string].append((name, md5, path))
                LOGGER.debug('Matched String=%s, Name=%s, MD5 Digest=%s, Location=%s', matched_string, name, md5, path)
                if md5 not in md5s:
                    md5s.add(md5)
                    self.stats['files_matched'] += 1

        LOGGER.info('Scan complete. Matched %d of %d files.', self.stats['files_matched'], self.stats['files_scanned'])

    def get_results(self):
        """Flatten search_results into a list of tuples."""
        results = []
        for match_str, result_rows in self.scan_results.items():
            for name, md5, path in result_rows:
                results.append((match_str, md5, name, path))

        return results


class Output:
    __doc__ = '\n    Format an output tuple to the desired device.\n    '

    def __init__(self, header, rows, configs):
        """
        Set it up.

        Args:
            header - A list of column labels (No Default).
            rows - A list of lists of cell values (No Default).
            config:
                output_file - A file for output (Default: Output to the console).
                branding_text - A list of cell values to be output before the header.
                branding_logo - (Excel output only) Optional image to be inserted
            before the header.

        """
        self.rows = rows
        self.output_file = configs['output_file']
        self.header = header
        self.branding_logo = configs['branding_logo']
        self.branding_text = configs['branding_text']

    @classmethod
    def get_output(cls, headers, rows, configs):
        """Factory method for constructing the output object."""
        configs['output_file'] = os.path.join(configs['output_dir'], '-'.join(['scan', strftime('%Y%m%d%H%M')]))
        if configs['excel_output']:
            configs['output_file'] += '.xlsx'
            return ExcelOutput(headers, rows, configs)
        configs['output_file'] += '.csv'
        return CSVOutput(headers, rows, configs)

    @abstractmethod
    def output(self):
        """Output the rows."""
        pass


class CSVOutput(Output):
    __doc__ = "\n    Outputter for text (CSV) file output.\n\n    Output goes to the console if the file attribute isn't set.\n    "

    def output(self):
        """Output the rows."""
        out_fh = sys.stdout
        if self.output_file:
            try:
                make_dir_safe(os.path.dirname(self.output_file))
            except IOError:
                LOGGER.error("Can't open file=%s", self.output_file)
                raise

        LOGGER.info('Writing output to %s', self.output_file)
        with open((self.output_file), newline='', encoding='utf-8', mode='w') as (out_fh):
            csv_writer = csv.writer(out_fh, dialect='excel')
            if self.branding_text:
                csv_writer.writerow(self.branding_text)
            csv_writer.writerow(self.header)
            for row in self.rows:
                csv_writer.writerow(row)


class ExcelOutput(Output):
    __doc__ = '\n    Outputter for Microsoft Excel (.xlsx) output.\n\n    '
    CELL_BUFFER_CHARS = 1
    CHAR_PIXEL_WIDTH = 8.63
    CHAR_PIXEL_HEIGHT = 16

    def set_col_widths(self, sheet):
        """
        Calculate sheet column widths sufficient to fit the longest data value.

        Args:
            workbook - An XlsxWriter Workbook containing the columns to resize.
            logo_img_char_width - If using a branding_logo, the width, in 12-pica "characters",
            of the image.
        """
        for col_num, col_vals in enumerate(tuple(zip(self.header, *self.rows))):
            max_width = 1
            for col_val in col_vals:
                if len(col_val) > max_width:
                    max_width = len(col_val)

            sheet.set_column(col_num, col_num, max_width + self.CELL_BUFFER_CHARS)

    def output(self):
        """Output the rows."""
        workbook = xlsxwriter.Workbook(self.output_file)
        sheet = workbook.add_worksheet()
        row_num = 0
        if self.branding_logo:
            if os.path.exists(self.branding_logo):
                sheet.insert_image(row_num, 0, self.branding_logo)
                with Image.open(self.branding_logo) as (img):
                    row_num += math.ceil(img.size[1] / self.CHAR_PIXEL_HEIGHT)
        if self.branding_text:
            sheet.write(row_num, 0, self.branding_text)
            row_num += 2
        for col_num, cell_value in enumerate(self.header):
            sheet.write(row_num, col_num, cell_value)

        for row in self.rows:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                sheet.write(row_num, col_num, cell_value)

        self.set_col_widths(sheet)
        LOGGER.info('Writing output to %s', self.output_file)
        workbook.close()
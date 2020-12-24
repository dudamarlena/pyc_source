# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/subcommand/Search.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 34096 bytes
import argparse, datetime, logging, multiprocessing, sys, tempfile
from os import path, mkdir
import numpy as np, pandas as pd
import staramr.SubCommand as SubCommand
from staramr.Utils import get_string_with_spacing
import staramr.blast.JobHandler as JobHandler
import staramr.blast.plasmidfinder.PlasmidfinderBlastDatabase as PlasmidfinderBlastDatabase
import staramr.blast.pointfinder.PointfinderBlastDatabase as PointfinderBlastDatabase
import staramr.databases.AMRDatabasesManager as AMRDatabasesManager
import staramr.databases.exclude.ExcludeGenesList as ExcludeGenesList
import staramr.databases.resistance.ARGDrugTable as ARGDrugTable
import staramr.detection.AMRDetectionFactory as AMRDetectionFactory
import staramr.exceptions.CommandParseException as CommandParseException
logger = logging.getLogger('Search')

class Search(SubCommand):
    BLANK = '-'
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, subparser, script_name, version):
        super().__init__(subparser, script_name)
        self._version = version

    def _setup_args(self, arg_parser):
        name = self._script_name
        epilog = 'Example:\n\t' + name + ' search -o out *.fasta\n\t\tSearches the files *.fasta for AMR genes using only the ResFinder database, storing results in the out/ directory.\n\n' + '\t' + name + ' search --pointfinder-organism salmonella --output-excel results.xlsx *.fasta\n' + '\t\tSearches *.fasta for AMR genes using ResFinder and PointFinder database with the passed organism, storing results in results.xlsx.'
        arg_parser = self._subparser.add_parser('search', epilog=epilog,
          formatter_class=(argparse.RawTextHelpFormatter),
          help='Search for AMR genes')
        self._default_database_dir = AMRDatabasesManager.get_default_database_directory()
        cpu_count = multiprocessing.cpu_count()
        arg_parser.add_argument('--pointfinder-organism', action='store', dest='pointfinder_organism', type=str, help=('The organism to use for pointfinder {' + ', '.join(PointfinderBlastDatabase.get_available_organisms()) + '}. Defaults to disabling search for point mutations. [None].'),
          default=None,
          required=False)
        arg_parser.add_argument('--plasmidfinder-database-type', action='store', dest='plasmidfinder_database_type', type=str,
          help=('The database type to use for plasmidfinder {' + ', '.join(PlasmidfinderBlastDatabase.get_available_databases()) + '}. Defaults to using all available database types to search for plasmids. [None].'),
          default=None,
          required=False)
        arg_parser.add_argument('-d', '--database', action='store', dest='database', type=str, help=('The directory containing the resfinder/pointfinder/plasmidfinder databases [' + self._default_database_dir + '].'),
          default=(self._default_database_dir),
          required=False)
        arg_parser.add_argument('-n', '--nprocs', action='store', dest='nprocs', type=int, help=('The number of processing cores to use [' + str(cpu_count) + '].'),
          default=cpu_count,
          required=False)
        arg_parser.add_argument('--ignore-invalid-files', action='store_true', dest='ignore_valid_files', help='Skips over invalid input files',
          required=False)
        arg_parser.add_argument('--mlst-scheme', action='store', dest='mlst_scheme', help='Specify scheme name, visit https://github.com/tseemann/mlst/blob/master/db/scheme_species_map.tab for supported scheme genus available. [None] ',
          required=False)
        arg_parser.add_argument('--genome-size-lower-bound', action='store', dest='genome_size_lower_bound', type=int, help='The lower bound for our genome size for the quality metrics. Defaults to 4 Mbp. [4000000].',
          default=4000000,
          required=False)
        arg_parser.add_argument('--genome-size-upper-bound', action='store', dest='genome_size_upper_bound', type=int, help='The upper bound for our genome size for the quality metrics. Defaults to 6 Mbp. [6000000].',
          default=6000000,
          required=False)
        arg_parser.add_argument('--minimum-N50-value', action='store', dest='minimum_N50_value', type=int, help='The minimum N50 value for the quality metrics. Defaults to 10000. [10000].',
          default=10000,
          required=False)
        arg_parser.add_argument('--minimum-contig-length', action='store', dest='minimum_contig_length', type=int, help='The minimum contig length for the quality metrics. Defaults to 300 bp. [300].',
          default=300,
          required=False)
        arg_parser.add_argument('--unacceptable-number-contigs', action='store', dest='unacceptable_num_contigs', type=int, help='The minimum, unacceptable number of contigs which are equal to or above the minimum contig length for our quality metrics. Defaults to 1000. [1000].',
          default=1000,
          required=False)
        threshold_group = arg_parser.add_argument_group('BLAST Thresholds')
        threshold_group.add_argument('--pid-threshold', action='store', dest='pid_threshold', type=float, help='The percent identity threshold [98.0].',
          default=98.0,
          required=False)
        threshold_group.add_argument('--percent-length-overlap-resfinder', action='store', dest='plength_threshold_resfinder',
          type=float,
          help='The percent length overlap for resfinder results [60.0].',
          default=60.0,
          required=False)
        threshold_group.add_argument('--percent-length-overlap-pointfinder', action='store', dest='plength_threshold_pointfinder',
          type=float,
          help='The percent length overlap for pointfinder results [95.0].',
          default=95.0,
          required=False)
        threshold_group.add_argument('--percent-length-overlap-plasmidfinder', action='store', dest='plength_threshold_plasmidfinder',
          type=float,
          help='The percent length overlap for resfinder results [60.0].',
          default=60.0,
          required=False)
        report_group = arg_parser.add_argument_group('Reporting options')
        report_group.add_argument('--no-exclude-genes', action='store_true', dest='no_exclude_genes', help='Disable the default exclusion of some genes from ResFinder/PointFinder/PlasmidFinder [False].',
          required=False)
        report_group.add_argument('--exclude-genes-file', action='store', dest='exclude_genes_file', help=('A containing a list of ResFinder/PointFinder/PlasmidFinder gene names to exclude from results [{}].'.format(ExcludeGenesList.get_default_exclude_file())),
          default=(ExcludeGenesList.get_default_exclude_file()),
          required=False)
        report_group.add_argument('--exclude-negatives', action='store_true', dest='exclude_negatives', help='Exclude negative results (those sensitive to antimicrobials) [False].',
          required=False)
        report_group.add_argument('--exclude-resistance-phenotypes', action='store_true', dest='exclude_resistance_phenotypes',
          help='Exclude predicted antimicrobial resistances [False].',
          required=False)
        report_group.add_argument('--report-all-blast', action='store_true', dest='report_all_blast', help='Report all blast hits (vs. only top blast hits) [False].',
          required=False)
        output_group = arg_parser.add_argument_group(title='Output', description='Use either --output-dir or specify individual output files')
        output_group.add_argument('-o', '--output-dir', action='store', dest='output_dir', type=str, help='The output directory for results [None].',
          default=None,
          required=False)
        output_group.add_argument('--output-summary', action='store', dest='output_summary', type=str, help="The name of the output file containing the summary results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-detailed-summary', action='store', dest='output_detailed_summary', type=str, help="The name of the output file containing the detailed summary results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-resfinder', action='store', dest='output_resfinder', type=str, help="The name of the output file containing the resfinder results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-pointfinder', action='store', dest='output_pointfinder', type=str, help="The name of the output file containing the pointfinder results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-plasmidfinder', action='store', dest='output_plasmidfinder', type=str, help="The name of the output file containing the plasmidfinder results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-settings', action='store', dest='output_settings', type=str, help="The name of the output file containing the settings. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-excel', action='store', dest='output_excel', type=str, help="The name of the output file containing the excel results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-hits-dir', action='store', dest='hits_output_dir', type=str, help="The name of the directory to contain the BLAST hit files. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        output_group.add_argument('--output-mlst', action='store', dest='output_mlst', type=str, help="The name of the output file containing the mlst results. Not be be used with '--output-dir'. [None]",
          default=None,
          required=False)
        arg_parser.add_argument('files', nargs='+')
        return arg_parser

    def _print_dataframes_to_excel(self, outfile_path, summary_dataframe, resfinder_dataframe, pointfinder_dataframe, plasmidfinder_dataframe, detailed_summary_dataframe, mlst_dataframe, settings_dataframe, minimum_contig_length):
        writer = pd.ExcelWriter(outfile_path, engine='xlsxwriter')
        sheetname_dataframe = {}
        sheetname_dataframe['Summary'] = summary_dataframe
        sheetname_dataframe['Detailed_Summary'] = detailed_summary_dataframe
        sheetname_dataframe['ResFinder'] = resfinder_dataframe
        sheetname_dataframe['PlasmidFinder'] = plasmidfinder_dataframe
        sheetname_dataframe['MLST_Summary'] = mlst_dataframe
        if pointfinder_dataframe is not None:
            sheetname_dataframe['PointFinder'] = pointfinder_dataframe
        for name in ('Summary', 'Detailed_Summary', 'ResFinder', 'PointFinder', 'PlasmidFinder',
                     'MLST_Summary'):
            if name in sheetname_dataframe:
                if name == 'Summary':
                    sheetname_dataframe[name].to_excel(writer, name, freeze_panes=[1, 2], float_format='%0.2f', na_rep=(self.BLANK))
                else:
                    sheetname_dataframe[name].to_excel(writer, name, freeze_panes=[1, 1], float_format='%0.2f', na_rep=(self.BLANK))
            self._resize_columns(sheetname_dataframe, writer, max_width=50)
            settings_dataframe.to_excel(writer, 'Settings')
            self._resize_columns({'Settings': settings_dataframe}, writer, max_width=75, text_wrap=False)
            writer.save()

    def _resize_columns(self, sheetname_dataframe, writer, max_width, text_wrap=True):
        """
        Resizes columns in workbook.
        :param sheetname_dataframe: A map mapping the sheet name to a dataframe.
        :param writer: The ExcelWriter, which the worksheets already added using writer.to_excel
        :param max_width: The maximum width of the columns.
        :param text_wrap: Whether or not to turn on text wrapping if columns surpass max_width.
        :return: None
        """
        workbook = writer.book
        wrap_format = workbook.add_format({'text_wrap': text_wrap})
        for name in sheetname_dataframe:
            for i, width in enumerate(self._get_col_widths(sheetname_dataframe[name])):
                if width > max_width:
                    writer.sheets[name].set_column(i, i, width=max_width, cell_format=wrap_format)
                else:
                    writer.sheets[name].set_column(i, i, width=width)

    def _get_col_widths(self, df):
        """
        Calculate column widths based on column headers and contents
        :param df: The dataframe.
        :return: A generator giving the max width for each column.
        """
        idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
        (yield idx_max)
        extra = 2
        for c in df.columns:
            (yield np.max([df[c].astype(str).str.len().max(), len(c)]) + extra)

    def _print_dataframe_to_text_file_handle(self, dataframe, file_handle):
        dataframe.to_csv(file_handle, sep='\t', float_format='%0.2f', na_rep=(self.BLANK))

    def _print_settings_to_file(self, settings, file):
        file_handle = open(file, 'w')
        file_handle.write(get_string_with_spacing(settings))
        file_handle.close()

    def _generate_results(self, database_repos, resfinder_database, pointfinder_database, plasmidfinder_database, nprocs, include_negatives, include_resistances, hits_output, pid_threshold, plength_threshold_resfinder, plength_threshold_pointfinder, plength_threshold_plasmidfinder, report_all_blast, genes_to_exclude, files, ignore_invalid_files, mlst_scheme, genome_size_lower_bound, genome_size_upper_bound, minimum_N50_value, minimum_contig_length, unacceptable_num_contigs):
        """
        Runs AMR detection and generates results.
        :param database_repos: The database repos object.
        :param resfinder_database: The resfinder database.
        :param pointfinder_database: The pointfinder database.
        :param plasmidfinder_database: The plasmidfinder database.
        :param nprocs: The number of processing cores to use for BLAST.
        :param include_negatives: Whether or not to include negative results in output.
        :param include_resistances: Whether or not to include resistance phenotypes in output.
        :param hits_output: Output directory for hit files.
        :param pid_threshold: The pid threshold.
        :param plength_threshold_resfinder: The plength threshold for resfinder.
        :param plength_threshold_pointfinder: The plength threshold for pointfinder.
        :param plength_threshold_plasmidfinder: The plength threshold for plasmidfinder.
        :param report_all_blast: Whether or not to report all BLAST results.
        :param genes_to_exclude: A list of gene IDs to exclude from the results.
        :param files: The list of files to scan.
        :param ignore_invalid_files: Skips over invalid input files.
        :param mlst_scheme: Specifys scheme name MLST uses.
        :return: A dictionary containing the results as dict['results'] and settings as dict['settings'].
        """
        results = {'results':None, 
         'settings':None}
        with tempfile.TemporaryDirectory() as (blast_out):
            start_time = datetime.datetime.now()
            blast_handler = JobHandler({'resfinder':resfinder_database,  'pointfinder':pointfinder_database,  'plasmidfinder':plasmidfinder_database}, nprocs, blast_out)
            amr_detection_factory = AMRDetectionFactory()
            amr_detection = amr_detection_factory.build(plasmidfinder_database, resfinder_database,
              blast_handler,
              pointfinder_database,
              include_negatives=include_negatives,
              include_resistances=include_resistances,
              output_dir=hits_output,
              genes_to_exclude=genes_to_exclude)
            amr_detection.run_amr_detection(files, pid_threshold, plength_threshold_resfinder, plength_threshold_pointfinder, plength_threshold_plasmidfinder, genome_size_lower_bound, genome_size_upper_bound, minimum_N50_value, minimum_contig_length, unacceptable_num_contigs, report_all_blast, ignore_invalid_files, mlst_scheme)
            results['results'] = amr_detection
            end_time = datetime.datetime.now()
            time_difference = end_time - start_time
            time_difference_minutes = '%0.2f' % (time_difference.total_seconds() / 60)
            logger.info('Finished. Took %s minutes.', time_difference_minutes)
            settings = database_repos.info()
            settings['mlst_version'] = JobHandler.get_mlst_version(JobHandler)
            settings['command_line'] = ' '.join(sys.argv)
            settings['version'] = self._version
            settings['start_time'] = start_time.strftime(self.TIME_FORMAT)
            settings['end_time'] = end_time.strftime(self.TIME_FORMAT)
            settings['total_minutes'] = time_difference_minutes
            settings.move_to_end('total_minutes', last=False)
            settings.move_to_end('end_time', last=False)
            settings.move_to_end('start_time', last=False)
            settings.move_to_end('version', last=False)
            settings.move_to_end('command_line', last=False)
            if include_resistances:
                arg_drug_table = ARGDrugTable()
                info = arg_drug_table.get_resistance_table_info()
                settings.update(info)
                logger.info('Predicting AMR resistance phenotypes is enabled. The predictions are for microbiological resistance and *not* clinical resistance. These results are continually being improved and we welcome any feedback.')
            results['settings'] = settings
        return results

    def run--- This code section failed: ---

 L. 324         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Search
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_METHOD              run
               10  LOAD_FAST                'args'
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L. 326        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'args'
               20  LOAD_ATTR                files
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_FALSE    46  'to 46'

 L. 327        30  LOAD_GLOBAL              CommandParseException
               32  LOAD_STR                 'Must pass a fasta file to process'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _root_arg_parser
               38  LOAD_CONST               True
               40  LOAD_CONST               ('print_help',)
               42  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            28  '28'

 L. 329        46  LOAD_FAST                'args'
               48  LOAD_ATTR                files
               50  GET_ITER         
             52_0  COME_FROM            64  '64'
               52  FOR_ITER             88  'to 88'
               54  STORE_FAST               'file'

 L. 330        56  LOAD_GLOBAL              path
               58  LOAD_METHOD              exists
               60  LOAD_FAST                'file'
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_TRUE     52  'to 52'

 L. 331        66  LOAD_GLOBAL              CommandParseException
               68  LOAD_STR                 'File ['
               70  LOAD_FAST                'file'
               72  BINARY_ADD       
               74  LOAD_STR                 '] does not exist'
               76  BINARY_ADD       
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _root_arg_parser
               82  CALL_FUNCTION_2       2  ''
               84  RAISE_VARARGS_1       1  'exception instance'
               86  JUMP_BACK            52  'to 52'

 L. 333        88  LOAD_GLOBAL              path
               90  LOAD_METHOD              isdir
               92  LOAD_FAST                'args'
               94  LOAD_ATTR                database
               96  CALL_METHOD_1         1  ''
               98  POP_JUMP_IF_TRUE    162  'to 162'

 L. 334       100  LOAD_FAST                'args'
              102  LOAD_ATTR                database
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _default_database_dir
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   126  'to 126'

 L. 335       112  LOAD_GLOBAL              CommandParseException

 L. 336       114  LOAD_STR                 "Default database does not exist. Perhaps try restoring with 'staramr db restore-default'"

 L. 337       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _root_arg_parser

 L. 335       120  CALL_FUNCTION_2       2  ''
              122  RAISE_VARARGS_1       1  'exception instance'
              124  JUMP_FORWARD        162  'to 162'
            126_0  COME_FROM           110  '110'

 L. 339       126  LOAD_GLOBAL              CommandParseException

 L. 340       128  LOAD_STR                 'Database directory ['
              130  LOAD_FAST                'args'
              132  LOAD_ATTR                database
              134  BINARY_ADD       
              136  LOAD_STR                 '] does not exist. Perhaps try building with'
              138  BINARY_ADD       

 L. 341       140  LOAD_STR                 "'staramr db build --dir "

 L. 340       142  BINARY_ADD       

 L. 341       144  LOAD_FAST                'args'
              146  LOAD_ATTR                database

 L. 340       148  BINARY_ADD       

 L. 341       150  LOAD_STR                 "'"

 L. 340       152  BINARY_ADD       

 L. 342       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _root_arg_parser

 L. 339       158  CALL_FUNCTION_2       2  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           124  '124'
            162_1  COME_FROM            98  '98'

 L. 344       162  LOAD_FAST                'args'
              164  LOAD_ATTR                database
              166  LOAD_GLOBAL              AMRDatabasesManager
              168  LOAD_METHOD              get_default_database_directory
              170  CALL_METHOD_0         0  ''
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   190  'to 190'

 L. 345       176  LOAD_GLOBAL              AMRDatabasesManager
              178  LOAD_METHOD              create_default_manager
              180  CALL_METHOD_0         0  ''
              182  LOAD_METHOD              get_database_repos
              184  CALL_METHOD_0         0  ''
              186  STORE_FAST               'database_repos'
              188  JUMP_FORWARD        204  'to 204'
            190_0  COME_FROM           174  '174'

 L. 347       190  LOAD_GLOBAL              AMRDatabasesManager
              192  LOAD_FAST                'args'
              194  LOAD_ATTR                database
              196  CALL_FUNCTION_1       1  ''
              198  LOAD_METHOD              get_database_repos
              200  CALL_METHOD_0         0  ''
              202  STORE_FAST               'database_repos'
            204_0  COME_FROM           188  '188'

 L. 349       204  LOAD_GLOBAL              AMRDatabasesManager
              206  LOAD_METHOD              is_database_repos_default_commits
              208  LOAD_FAST                'database_repos'
              210  CALL_METHOD_1         1  ''
              212  POP_JUMP_IF_TRUE    224  'to 224'

 L. 350       214  LOAD_GLOBAL              logger
              216  LOAD_METHOD              warning
              218  LOAD_STR                 'Using non-default ResFinder/PointFinder. This may lead to differences in the detected AMR genes depending on how the database files are structured.'
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
            224_0  COME_FROM           212  '212'

 L. 353       224  LOAD_FAST                'database_repos'
              226  LOAD_METHOD              build_blast_database
              228  LOAD_STR                 'resfinder'
              230  CALL_METHOD_1         1  ''
              232  STORE_FAST               'resfinder_database'

 L. 354       234  LOAD_FAST                'args'
              236  LOAD_ATTR                pointfinder_organism
          238_240  POP_JUMP_IF_FALSE   302  'to 302'

 L. 355       242  LOAD_FAST                'args'
              244  LOAD_ATTR                pointfinder_organism
              246  LOAD_GLOBAL              PointfinderBlastDatabase
              248  LOAD_METHOD              get_available_organisms
              250  CALL_METHOD_0         0  ''
              252  COMPARE_OP               not-in
          254_256  POP_JUMP_IF_FALSE   282  'to 282'

 L. 356       258  LOAD_GLOBAL              CommandParseException
              260  LOAD_STR                 'The only Pointfinder organism(s) currently supported are '
              262  LOAD_GLOBAL              str

 L. 357       264  LOAD_GLOBAL              PointfinderBlastDatabase
              266  LOAD_METHOD              get_available_organisms
              268  CALL_METHOD_0         0  ''

 L. 356       270  CALL_FUNCTION_1       1  ''
              272  BINARY_ADD       

 L. 357       274  LOAD_FAST                'self'
              276  LOAD_ATTR                _root_arg_parser

 L. 356       278  CALL_FUNCTION_2       2  ''
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           254  '254'

 L. 358       282  LOAD_FAST                'database_repos'
              284  LOAD_METHOD              build_blast_database
              286  LOAD_STR                 'pointfinder'

 L. 359       288  LOAD_STR                 'organism'
              290  LOAD_FAST                'args'
              292  LOAD_ATTR                pointfinder_organism
              294  BUILD_MAP_1           1 

 L. 358       296  CALL_METHOD_2         2  ''
              298  STORE_FAST               'pointfinder_database'
              300  JUMP_FORWARD        316  'to 316'
            302_0  COME_FROM           238  '238'

 L. 361       302  LOAD_GLOBAL              logger
              304  LOAD_METHOD              info
              306  LOAD_STR                 'No --pointfinder-organism specified. Will not search the PointFinder databases'
              308  CALL_METHOD_1         1  ''
              310  POP_TOP          

 L. 362       312  LOAD_CONST               None
              314  STORE_FAST               'pointfinder_database'
            316_0  COME_FROM           300  '300'

 L. 364       316  LOAD_FAST                'args'
              318  LOAD_ATTR                plasmidfinder_database_type
          320_322  POP_JUMP_IF_FALSE   384  'to 384'

 L. 365       324  LOAD_FAST                'args'
              326  LOAD_ATTR                plasmidfinder_database_type
              328  LOAD_GLOBAL              PlasmidfinderBlastDatabase
              330  LOAD_METHOD              get_available_databases
              332  CALL_METHOD_0         0  ''
              334  COMPARE_OP               not-in
          336_338  POP_JUMP_IF_FALSE   364  'to 364'

 L. 366       340  LOAD_GLOBAL              CommandParseException
              342  LOAD_STR                 'The only Plasmidfinder databases that are currently supported are '
              344  LOAD_GLOBAL              str

 L. 367       346  LOAD_GLOBAL              PlasmidfinderBlastDatabase
              348  LOAD_METHOD              get_available_databases
              350  CALL_METHOD_0         0  ''

 L. 366       352  CALL_FUNCTION_1       1  ''
              354  BINARY_ADD       

 L. 367       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _root_arg_parser

 L. 366       360  CALL_FUNCTION_2       2  ''
              362  RAISE_VARARGS_1       1  'exception instance'
            364_0  COME_FROM           336  '336'

 L. 368       364  LOAD_FAST                'database_repos'
              366  LOAD_METHOD              build_blast_database
              368  LOAD_STR                 'plasmidfinder'

 L. 369       370  LOAD_STR                 'database_type'

 L. 369       372  LOAD_FAST                'args'
              374  LOAD_ATTR                plasmidfinder_database_type

 L. 368       376  BUILD_MAP_1           1 
              378  CALL_METHOD_2         2  ''
              380  STORE_FAST               'plasmidfinder_database'
              382  JUMP_FORWARD        404  'to 404'
            384_0  COME_FROM           320  '320'

 L. 371       384  LOAD_GLOBAL              logger
              386  LOAD_METHOD              info
              388  LOAD_STR                 'No --plasmidfinder-database-type specified. Will search the entire PlasmidFinder database'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

 L. 372       394  LOAD_FAST                'database_repos'
              396  LOAD_METHOD              build_blast_database
              398  LOAD_STR                 'plasmidfinder'
              400  CALL_METHOD_1         1  ''
              402  STORE_FAST               'plasmidfinder_database'
            404_0  COME_FROM           382  '382'

 L. 374       404  LOAD_CONST               None
              406  STORE_FAST               'hits_output_dir'

 L. 375       408  LOAD_CONST               None
              410  STORE_FAST               'output_summary'

 L. 376       412  LOAD_CONST               None
              414  STORE_FAST               'output_detailed_summary'

 L. 377       416  LOAD_CONST               None
              418  STORE_FAST               'output_resfinder'

 L. 378       420  LOAD_CONST               None
              422  STORE_FAST               'output_pointfinder'

 L. 379       424  LOAD_CONST               None
              426  STORE_FAST               'output_plasmidfinder'

 L. 380       428  LOAD_CONST               None
              430  STORE_FAST               'output_mlst'

 L. 381       432  LOAD_CONST               None
              434  STORE_FAST               'output_excel'

 L. 382       436  LOAD_CONST               None
              438  STORE_FAST               'output_settings'

 L. 383       440  LOAD_FAST                'args'
              442  LOAD_ATTR                output_dir
          444_446  POP_JUMP_IF_FALSE   716  'to 716'

 L. 384       448  LOAD_GLOBAL              path
              450  LOAD_METHOD              exists
              452  LOAD_FAST                'args'
              454  LOAD_ATTR                output_dir
              456  CALL_METHOD_1         1  ''
          458_460  POP_JUMP_IF_FALSE   486  'to 486'

 L. 385       462  LOAD_GLOBAL              CommandParseException
              464  LOAD_STR                 'Output directory ['
              466  LOAD_FAST                'args'
              468  LOAD_ATTR                output_dir
              470  BINARY_ADD       
              472  LOAD_STR                 '] already exists'
              474  BINARY_ADD       

 L. 386       476  LOAD_FAST                'self'
              478  LOAD_ATTR                _root_arg_parser

 L. 385       480  CALL_FUNCTION_2       2  ''
              482  RAISE_VARARGS_1       1  'exception instance'
              484  JUMP_FORWARD        714  'to 714'
            486_0  COME_FROM           458  '458'

 L. 387       486  LOAD_FAST                'args'
              488  LOAD_ATTR                output_summary
          490_492  POP_JUMP_IF_TRUE    542  'to 542'
              494  LOAD_FAST                'args'
              496  LOAD_ATTR                output_detailed_summary
          498_500  POP_JUMP_IF_TRUE    542  'to 542'
              502  LOAD_FAST                'args'
              504  LOAD_ATTR                output_resfinder
          506_508  POP_JUMP_IF_TRUE    542  'to 542'
              510  LOAD_FAST                'args'
              512  LOAD_ATTR                output_pointfinder
          514_516  POP_JUMP_IF_TRUE    542  'to 542'
              518  LOAD_FAST                'args'
              520  LOAD_ATTR                output_plasmidfinder
          522_524  POP_JUMP_IF_TRUE    542  'to 542'
              526  LOAD_FAST                'args'
              528  LOAD_ATTR                output_excel
          530_532  POP_JUMP_IF_TRUE    542  'to 542'

 L. 388       534  LOAD_FAST                'args'
              536  LOAD_ATTR                hits_output_dir

 L. 387   538_540  POP_JUMP_IF_FALSE   556  'to 556'
            542_0  COME_FROM           530  '530'
            542_1  COME_FROM           522  '522'
            542_2  COME_FROM           514  '514'
            542_3  COME_FROM           506  '506'
            542_4  COME_FROM           498  '498'
            542_5  COME_FROM           490  '490'

 L. 389       542  LOAD_GLOBAL              CommandParseException
              544  LOAD_STR                 'You cannot use --output-[type] with --output-dir'
              546  LOAD_FAST                'self'
              548  LOAD_ATTR                _root_arg_parser
              550  CALL_FUNCTION_2       2  ''
              552  RAISE_VARARGS_1       1  'exception instance'
              554  JUMP_FORWARD        714  'to 714'
            556_0  COME_FROM           538  '538'

 L. 391       556  LOAD_GLOBAL              mkdir
              558  LOAD_FAST                'args'
              560  LOAD_ATTR                output_dir
              562  CALL_FUNCTION_1       1  ''
              564  POP_TOP          

 L. 393       566  LOAD_GLOBAL              path
              568  LOAD_METHOD              join
              570  LOAD_FAST                'args'
              572  LOAD_ATTR                output_dir
              574  LOAD_STR                 'hits'
              576  CALL_METHOD_2         2  ''
              578  STORE_FAST               'hits_output_dir'

 L. 394       580  LOAD_GLOBAL              path
              582  LOAD_METHOD              join
              584  LOAD_FAST                'args'
              586  LOAD_ATTR                output_dir
              588  LOAD_STR                 'resfinder.tsv'
              590  CALL_METHOD_2         2  ''
              592  STORE_FAST               'output_resfinder'

 L. 395       594  LOAD_GLOBAL              path
              596  LOAD_METHOD              join
              598  LOAD_FAST                'args'
              600  LOAD_ATTR                output_dir
              602  LOAD_STR                 'pointfinder.tsv'
              604  CALL_METHOD_2         2  ''
              606  STORE_FAST               'output_pointfinder'

 L. 396       608  LOAD_GLOBAL              path
              610  LOAD_METHOD              join
              612  LOAD_FAST                'args'
              614  LOAD_ATTR                output_dir
              616  LOAD_STR                 'plasmidfinder.tsv'
              618  CALL_METHOD_2         2  ''
              620  STORE_FAST               'output_plasmidfinder'

 L. 397       622  LOAD_GLOBAL              path
              624  LOAD_METHOD              join
              626  LOAD_FAST                'args'
              628  LOAD_ATTR                output_dir
              630  LOAD_STR                 'summary.tsv'
              632  CALL_METHOD_2         2  ''
              634  STORE_FAST               'output_summary'

 L. 398       636  LOAD_GLOBAL              path
              638  LOAD_METHOD              join
              640  LOAD_FAST                'args'
              642  LOAD_ATTR                output_dir
              644  LOAD_STR                 'detailed_summary.tsv'
              646  CALL_METHOD_2         2  ''
              648  STORE_FAST               'output_detailed_summary'

 L. 399       650  LOAD_GLOBAL              path
              652  LOAD_METHOD              join
              654  LOAD_FAST                'args'
              656  LOAD_ATTR                output_dir
              658  LOAD_STR                 'mlst.tsv'
              660  CALL_METHOD_2         2  ''
              662  STORE_FAST               'output_mlst'

 L. 400       664  LOAD_GLOBAL              path
              666  LOAD_METHOD              join
              668  LOAD_FAST                'args'
              670  LOAD_ATTR                output_dir
              672  LOAD_STR                 'settings.txt'
              674  CALL_METHOD_2         2  ''
              676  STORE_FAST               'output_settings'

 L. 401       678  LOAD_GLOBAL              path
              680  LOAD_METHOD              join
              682  LOAD_FAST                'args'
              684  LOAD_ATTR                output_dir
              686  LOAD_STR                 'results.xlsx'
              688  CALL_METHOD_2         2  ''
              690  STORE_FAST               'output_excel'

 L. 403       692  LOAD_GLOBAL              mkdir
              694  LOAD_FAST                'hits_output_dir'
              696  CALL_FUNCTION_1       1  ''
              698  POP_TOP          

 L. 405       700  LOAD_GLOBAL              logger
              702  LOAD_METHOD              info
              704  LOAD_STR                 '--output-dir set. All files will be output to [%s]'
              706  LOAD_FAST                'args'
              708  LOAD_ATTR                output_dir
              710  CALL_METHOD_2         2  ''
              712  POP_TOP          
            714_0  COME_FROM           554  '554'
            714_1  COME_FROM           484  '484'
              714  JUMP_FORWARD        920  'to 920'
            716_0  COME_FROM           444  '444'

 L. 406       716  LOAD_FAST                'args'
              718  LOAD_ATTR                output_summary
          720_722  POP_JUMP_IF_TRUE    740  'to 740'
              724  LOAD_FAST                'args'
              726  LOAD_ATTR                output_excel
          728_730  POP_JUMP_IF_TRUE    740  'to 740'
              732  LOAD_FAST                'args'
              734  LOAD_ATTR                output_detailed_summary
          736_738  POP_JUMP_IF_FALSE   908  'to 908'
            740_0  COME_FROM           728  '728'
            740_1  COME_FROM           720  '720'

 L. 407       740  LOAD_GLOBAL              logger
              742  LOAD_METHOD              info
              744  LOAD_STR                 '--output-dir not set. Files will be output to the respective --output-[type] setting'
              746  CALL_METHOD_1         1  ''
              748  POP_TOP          

 L. 408       750  LOAD_FAST                'args'
              752  LOAD_ATTR                output_resfinder
              754  STORE_FAST               'output_resfinder'

 L. 409       756  LOAD_FAST                'args'
              758  LOAD_ATTR                output_pointfinder
              760  STORE_FAST               'output_pointfinder'

 L. 410       762  LOAD_FAST                'args'
              764  LOAD_ATTR                output_plasmidfinder
              766  STORE_FAST               'output_plasmidfinder'

 L. 411       768  LOAD_FAST                'args'
              770  LOAD_ATTR                output_summary
              772  STORE_FAST               'output_summary'

 L. 412       774  LOAD_FAST                'args'
              776  LOAD_ATTR                output_detailed_summary
              778  STORE_FAST               'output_detailed_summary'

 L. 413       780  LOAD_FAST                'args'
              782  LOAD_ATTR                output_mlst
              784  STORE_FAST               'output_mlst'

 L. 414       786  LOAD_FAST                'args'
              788  LOAD_ATTR                output_settings
              790  STORE_FAST               'output_settings'

 L. 415       792  LOAD_FAST                'args'
              794  LOAD_ATTR                output_excel
              796  STORE_FAST               'output_excel'

 L. 416       798  LOAD_FAST                'args'
              800  LOAD_ATTR                hits_output_dir
              802  STORE_FAST               'hits_output_dir'

 L. 418       804  LOAD_FAST                'hits_output_dir'
              806  LOAD_CONST               None
              808  COMPARE_OP               is-not
          810_812  POP_JUMP_IF_FALSE   920  'to 920'

 L. 419       814  LOAD_GLOBAL              path
              816  LOAD_METHOD              exists
              818  LOAD_FAST                'hits_output_dir'
              820  CALL_METHOD_1         1  ''
          822_824  POP_JUMP_IF_FALSE   860  'to 860'
              826  LOAD_GLOBAL              path
              828  LOAD_METHOD              isdir
              830  LOAD_FAST                'hits_output_dir'
              832  CALL_METHOD_1         1  ''
          834_836  POP_JUMP_IF_TRUE    860  'to 860'

 L. 420       838  LOAD_GLOBAL              CommandParseException

 L. 421       840  LOAD_STR                 '--output-hits-dir ['
              842  LOAD_FAST                'hits_output_dir'
              844  BINARY_ADD       
              846  LOAD_STR                 '] exists and is not a directory'
              848  BINARY_ADD       

 L. 422       850  LOAD_FAST                'self'
              852  LOAD_ATTR                _root_arg_parser

 L. 420       854  CALL_FUNCTION_2       2  ''
              856  RAISE_VARARGS_1       1  'exception instance'
              858  JUMP_FORWARD        906  'to 906'
            860_0  COME_FROM           834  '834'
            860_1  COME_FROM           822  '822'

 L. 423       860  LOAD_GLOBAL              path
              862  LOAD_METHOD              exists
              864  LOAD_FAST                'hits_output_dir'
              866  CALL_METHOD_1         1  ''
          868_870  POP_JUMP_IF_FALSE   886  'to 886'

 L. 424       872  LOAD_GLOBAL              logger
              874  LOAD_METHOD              debug
              876  LOAD_STR                 'Found --output-hits-dir [%s] and is a directory. Will write hits here'

 L. 425       878  LOAD_FAST                'hits_output_dir'

 L. 424       880  CALL_METHOD_2         2  ''
              882  POP_TOP          
              884  JUMP_FORWARD        906  'to 906'
            886_0  COME_FROM           868  '868'

 L. 427       886  LOAD_GLOBAL              logger
              888  LOAD_METHOD              debug
              890  LOAD_STR                 'Making directory [%s]'
              892  LOAD_FAST                'hits_output_dir'
              894  CALL_METHOD_2         2  ''
              896  POP_TOP          

 L. 428       898  LOAD_GLOBAL              mkdir
              900  LOAD_FAST                'hits_output_dir'
              902  CALL_FUNCTION_1       1  ''
              904  POP_TOP          
            906_0  COME_FROM           884  '884'
            906_1  COME_FROM           858  '858'
              906  JUMP_FORWARD        920  'to 920'
            908_0  COME_FROM           736  '736'

 L. 430       908  LOAD_GLOBAL              CommandParseException

 L. 431       910  LOAD_STR                 'You must set one of --output-dir, --output-summary, --output-detailed-summary, or --output-excel'

 L. 432       912  LOAD_FAST                'self'
              914  LOAD_ATTR                _root_arg_parser

 L. 430       916  CALL_FUNCTION_2       2  ''
              918  RAISE_VARARGS_1       1  'exception instance'
            920_0  COME_FROM           906  '906'
            920_1  COME_FROM           810  '810'
            920_2  COME_FROM           714  '714'

 L. 434       920  LOAD_FAST                'args'
              922  LOAD_ATTR                no_exclude_genes
          924_926  POP_JUMP_IF_FALSE   944  'to 944'

 L. 435       928  LOAD_GLOBAL              logger
              930  LOAD_METHOD              info
              932  LOAD_STR                 '--no-exclude-genes enabled. Will not exclude any ResFinder/PointFinder genes.'
              934  CALL_METHOD_1         1  ''
              936  POP_TOP          

 L. 436       938  BUILD_LIST_0          0 
              940  STORE_FAST               'exclude_genes'
              942  JUMP_FORWARD       1008  'to 1008'
            944_0  COME_FROM           924  '924'

 L. 438       944  LOAD_GLOBAL              path
              946  LOAD_METHOD              exists
              948  LOAD_FAST                'args'
              950  LOAD_ATTR                exclude_genes_file
              952  CALL_METHOD_1         1  ''
          954_956  POP_JUMP_IF_TRUE    980  'to 980'

 L. 439       958  LOAD_GLOBAL              CommandParseException
              960  LOAD_STR                 '--exclude-genes-file [{}] does not exist'
              962  LOAD_METHOD              format
              964  LOAD_FAST                'args'
              966  LOAD_ATTR                exclude_genes_file
              968  CALL_METHOD_1         1  ''

 L. 440       970  LOAD_FAST                'self'
              972  LOAD_ATTR                _root_arg_parser

 L. 439       974  CALL_FUNCTION_2       2  ''
              976  RAISE_VARARGS_1       1  'exception instance'
              978  JUMP_FORWARD       1008  'to 1008'
            980_0  COME_FROM           954  '954'

 L. 442       980  LOAD_GLOBAL              logger
              982  LOAD_METHOD              info

 L. 443       984  LOAD_STR                 'Will exclude ResFinder/PointFinder genes listed in [%s]. Use --no-exclude-genes to disable'

 L. 444       986  LOAD_FAST                'args'
              988  LOAD_ATTR                exclude_genes_file

 L. 442       990  CALL_METHOD_2         2  ''
              992  POP_TOP          

 L. 445       994  LOAD_GLOBAL              ExcludeGenesList
              996  LOAD_FAST                'args'
              998  LOAD_ATTR                exclude_genes_file
             1000  CALL_FUNCTION_1       1  ''
             1002  LOAD_METHOD              tolist
             1004  CALL_METHOD_0         0  ''
             1006  STORE_FAST               'exclude_genes'
           1008_0  COME_FROM           978  '978'
           1008_1  COME_FROM           942  '942'

 L. 447      1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                _generate_results
             1012  LOAD_FAST                'database_repos'

 L. 448      1014  LOAD_FAST                'resfinder_database'

 L. 449      1016  LOAD_FAST                'pointfinder_database'

 L. 450      1018  LOAD_FAST                'plasmidfinder_database'

 L. 451      1020  LOAD_FAST                'args'
             1022  LOAD_ATTR                nprocs

 L. 452      1024  LOAD_FAST                'args'
             1026  LOAD_ATTR                exclude_negatives
             1028  UNARY_NOT        

 L. 453      1030  LOAD_FAST                'args'
             1032  LOAD_ATTR                exclude_resistance_phenotypes
             1034  UNARY_NOT        

 L. 454      1036  LOAD_FAST                'hits_output_dir'

 L. 455      1038  LOAD_FAST                'args'
             1040  LOAD_ATTR                pid_threshold

 L. 456      1042  LOAD_FAST                'args'
             1044  LOAD_ATTR                plength_threshold_resfinder

 L. 457      1046  LOAD_FAST                'args'
             1048  LOAD_ATTR                plength_threshold_pointfinder

 L. 458      1050  LOAD_FAST                'args'
             1052  LOAD_ATTR                plength_threshold_plasmidfinder

 L. 459      1054  LOAD_FAST                'args'
             1056  LOAD_ATTR                report_all_blast

 L. 460      1058  LOAD_FAST                'exclude_genes'

 L. 461      1060  LOAD_FAST                'args'
             1062  LOAD_ATTR                files

 L. 462      1064  LOAD_FAST                'args'
             1066  LOAD_ATTR                ignore_valid_files

 L. 463      1068  LOAD_FAST                'args'
             1070  LOAD_ATTR                mlst_scheme

 L. 464      1072  LOAD_FAST                'args'
             1074  LOAD_ATTR                genome_size_lower_bound

 L. 465      1076  LOAD_FAST                'args'
             1078  LOAD_ATTR                genome_size_upper_bound

 L. 466      1080  LOAD_FAST                'args'
             1082  LOAD_ATTR                minimum_N50_value

 L. 467      1084  LOAD_FAST                'args'
             1086  LOAD_ATTR                minimum_contig_length

 L. 468      1088  LOAD_FAST                'args'
             1090  LOAD_ATTR                unacceptable_num_contigs

 L. 447      1092  LOAD_CONST               ('database_repos', 'resfinder_database', 'pointfinder_database', 'plasmidfinder_database', 'nprocs', 'include_negatives', 'include_resistances', 'hits_output', 'pid_threshold', 'plength_threshold_resfinder', 'plength_threshold_pointfinder', 'plength_threshold_plasmidfinder', 'report_all_blast', 'genes_to_exclude', 'files', 'ignore_invalid_files', 'mlst_scheme', 'genome_size_lower_bound', 'genome_size_upper_bound', 'minimum_N50_value', 'minimum_contig_length', 'unacceptable_num_contigs')
             1094  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
             1096  STORE_FAST               'results'

 L. 469      1098  LOAD_FAST                'results'
             1100  LOAD_STR                 'results'
             1102  BINARY_SUBSCR    
             1104  STORE_FAST               'amr_detection'

 L. 470      1106  LOAD_FAST                'results'
             1108  LOAD_STR                 'settings'
             1110  BINARY_SUBSCR    
             1112  STORE_FAST               'settings'

 L. 472      1114  LOAD_FAST                'output_resfinder'
         1116_1118  POP_JUMP_IF_FALSE  1172  'to 1172'

 L. 473      1120  LOAD_GLOBAL              logger
             1122  LOAD_METHOD              info
             1124  LOAD_STR                 'Writing resfinder to [%s]'
             1126  LOAD_FAST                'output_resfinder'
             1128  CALL_METHOD_2         2  ''
             1130  POP_TOP          

 L. 474      1132  LOAD_GLOBAL              open
             1134  LOAD_FAST                'output_resfinder'
             1136  LOAD_STR                 'w'
             1138  CALL_FUNCTION_2       2  ''
             1140  SETUP_WITH         1164  'to 1164'
             1142  STORE_FAST               'fh'

 L. 475      1144  LOAD_FAST                'self'
             1146  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1148  LOAD_FAST                'amr_detection'
             1150  LOAD_METHOD              get_resfinder_results
             1152  CALL_METHOD_0         0  ''
             1154  LOAD_FAST                'fh'
             1156  CALL_METHOD_2         2  ''
             1158  POP_TOP          
             1160  POP_BLOCK        
             1162  BEGIN_FINALLY    
           1164_0  COME_FROM_WITH     1140  '1140'
             1164  WITH_CLEANUP_START
             1166  WITH_CLEANUP_FINISH
             1168  END_FINALLY      
             1170  JUMP_FORWARD       1182  'to 1182'
           1172_0  COME_FROM          1116  '1116'

 L. 477      1172  LOAD_GLOBAL              logger
             1174  LOAD_METHOD              info
             1176  LOAD_STR                 '--output-dir or --output-resfinder unset. No resfinder file will be written'
             1178  CALL_METHOD_1         1  ''
             1180  POP_TOP          
           1182_0  COME_FROM          1170  '1170'

 L. 479      1182  LOAD_FAST                'args'
             1184  LOAD_ATTR                pointfinder_organism
         1186_1188  POP_JUMP_IF_FALSE  1248  'to 1248'
             1190  LOAD_FAST                'output_pointfinder'
         1192_1194  POP_JUMP_IF_FALSE  1248  'to 1248'

 L. 480      1196  LOAD_GLOBAL              logger
             1198  LOAD_METHOD              info
             1200  LOAD_STR                 'Writing pointfinder to [%s]'
             1202  LOAD_FAST                'output_pointfinder'
             1204  CALL_METHOD_2         2  ''
             1206  POP_TOP          

 L. 481      1208  LOAD_GLOBAL              open
             1210  LOAD_FAST                'output_pointfinder'
             1212  LOAD_STR                 'w'
             1214  CALL_FUNCTION_2       2  ''
             1216  SETUP_WITH         1240  'to 1240'
             1218  STORE_FAST               'fh'

 L. 482      1220  LOAD_FAST                'self'
             1222  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1224  LOAD_FAST                'amr_detection'
             1226  LOAD_METHOD              get_pointfinder_results
             1228  CALL_METHOD_0         0  ''
             1230  LOAD_FAST                'fh'
             1232  CALL_METHOD_2         2  ''
             1234  POP_TOP          
             1236  POP_BLOCK        
             1238  BEGIN_FINALLY    
           1240_0  COME_FROM_WITH     1216  '1216'
             1240  WITH_CLEANUP_START
             1242  WITH_CLEANUP_FINISH
             1244  END_FINALLY      
             1246  JUMP_FORWARD       1258  'to 1258'
           1248_0  COME_FROM          1192  '1192'
           1248_1  COME_FROM          1186  '1186'

 L. 484      1248  LOAD_GLOBAL              logger
             1250  LOAD_METHOD              info
             1252  LOAD_STR                 '--output-dir or --output-pointfinder unset. No pointfinder file will be written'
             1254  CALL_METHOD_1         1  ''
             1256  POP_TOP          
           1258_0  COME_FROM          1246  '1246'

 L. 486      1258  LOAD_FAST                'output_plasmidfinder'
         1260_1262  POP_JUMP_IF_FALSE  1316  'to 1316'

 L. 487      1264  LOAD_GLOBAL              logger
             1266  LOAD_METHOD              info
             1268  LOAD_STR                 'Writing plasmidfinder to [%s]'
             1270  LOAD_FAST                'output_plasmidfinder'
             1272  CALL_METHOD_2         2  ''
             1274  POP_TOP          

 L. 488      1276  LOAD_GLOBAL              open
             1278  LOAD_FAST                'output_plasmidfinder'
             1280  LOAD_STR                 'w'
             1282  CALL_FUNCTION_2       2  ''
             1284  SETUP_WITH         1308  'to 1308'
             1286  STORE_FAST               'fh'

 L. 489      1288  LOAD_FAST                'self'
             1290  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1292  LOAD_FAST                'amr_detection'
             1294  LOAD_METHOD              get_plasmidfinder_results
             1296  CALL_METHOD_0         0  ''
             1298  LOAD_FAST                'fh'
             1300  CALL_METHOD_2         2  ''
             1302  POP_TOP          
             1304  POP_BLOCK        
             1306  BEGIN_FINALLY    
           1308_0  COME_FROM_WITH     1284  '1284'
             1308  WITH_CLEANUP_START
             1310  WITH_CLEANUP_FINISH
             1312  END_FINALLY      
             1314  JUMP_FORWARD       1326  'to 1326'
           1316_0  COME_FROM          1260  '1260'

 L. 491      1316  LOAD_GLOBAL              logger
             1318  LOAD_METHOD              info
             1320  LOAD_STR                 '--output-dir or --output-plasmidfinder unset. No plasmidfinder file will be written'
             1322  CALL_METHOD_1         1  ''
             1324  POP_TOP          
           1326_0  COME_FROM          1314  '1314'

 L. 493      1326  LOAD_FAST                'output_summary'
         1328_1330  POP_JUMP_IF_FALSE  1384  'to 1384'

 L. 494      1332  LOAD_GLOBAL              logger
             1334  LOAD_METHOD              info
             1336  LOAD_STR                 'Writing summary to [%s]'
             1338  LOAD_FAST                'output_summary'
             1340  CALL_METHOD_2         2  ''
             1342  POP_TOP          

 L. 495      1344  LOAD_GLOBAL              open
             1346  LOAD_FAST                'output_summary'
             1348  LOAD_STR                 'w'
             1350  CALL_FUNCTION_2       2  ''
             1352  SETUP_WITH         1376  'to 1376'
             1354  STORE_FAST               'fh'

 L. 496      1356  LOAD_FAST                'self'
             1358  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1360  LOAD_FAST                'amr_detection'
             1362  LOAD_METHOD              get_summary_results
             1364  CALL_METHOD_0         0  ''
             1366  LOAD_FAST                'fh'
             1368  CALL_METHOD_2         2  ''
             1370  POP_TOP          
             1372  POP_BLOCK        
             1374  BEGIN_FINALLY    
           1376_0  COME_FROM_WITH     1352  '1352'
             1376  WITH_CLEANUP_START
             1378  WITH_CLEANUP_FINISH
             1380  END_FINALLY      
             1382  JUMP_FORWARD       1394  'to 1394'
           1384_0  COME_FROM          1328  '1328'

 L. 498      1384  LOAD_GLOBAL              logger
             1386  LOAD_METHOD              info
             1388  LOAD_STR                 '--output-dir or --output-summary unset. No summary file will be written'
             1390  CALL_METHOD_1         1  ''
             1392  POP_TOP          
           1394_0  COME_FROM          1382  '1382'

 L. 500      1394  LOAD_FAST                'output_mlst'
         1396_1398  POP_JUMP_IF_FALSE  1452  'to 1452'

 L. 501      1400  LOAD_GLOBAL              logger
             1402  LOAD_METHOD              info
             1404  LOAD_STR                 'Writing MLST summary to [%s]'
             1406  LOAD_FAST                'output_mlst'
             1408  CALL_METHOD_2         2  ''
             1410  POP_TOP          

 L. 502      1412  LOAD_GLOBAL              open
             1414  LOAD_FAST                'output_mlst'
             1416  LOAD_STR                 'w'
             1418  CALL_FUNCTION_2       2  ''
             1420  SETUP_WITH         1444  'to 1444'
             1422  STORE_FAST               'fh'

 L. 503      1424  LOAD_FAST                'self'
             1426  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1428  LOAD_FAST                'amr_detection'
             1430  LOAD_METHOD              get_mlst_results
             1432  CALL_METHOD_0         0  ''
             1434  LOAD_FAST                'fh'
             1436  CALL_METHOD_2         2  ''
             1438  POP_TOP          
             1440  POP_BLOCK        
             1442  BEGIN_FINALLY    
           1444_0  COME_FROM_WITH     1420  '1420'
             1444  WITH_CLEANUP_START
             1446  WITH_CLEANUP_FINISH
             1448  END_FINALLY      
             1450  JUMP_FORWARD       1462  'to 1462'
           1452_0  COME_FROM          1396  '1396'

 L. 505      1452  LOAD_GLOBAL              logger
             1454  LOAD_METHOD              info
             1456  LOAD_STR                 '--output-dir or --output-mlst unset. No mlst file will be written'
             1458  CALL_METHOD_1         1  ''
             1460  POP_TOP          
           1462_0  COME_FROM          1450  '1450'

 L. 507      1462  LOAD_FAST                'output_detailed_summary'
         1464_1466  POP_JUMP_IF_FALSE  1520  'to 1520'

 L. 508      1468  LOAD_GLOBAL              logger
             1470  LOAD_METHOD              info
             1472  LOAD_STR                 'Writing detailed summary to [%s]'
             1474  LOAD_FAST                'output_detailed_summary'
             1476  CALL_METHOD_2         2  ''
             1478  POP_TOP          

 L. 509      1480  LOAD_GLOBAL              open
             1482  LOAD_FAST                'output_detailed_summary'
             1484  LOAD_STR                 'w'
             1486  CALL_FUNCTION_2       2  ''
             1488  SETUP_WITH         1512  'to 1512'
             1490  STORE_FAST               'fh'

 L. 510      1492  LOAD_FAST                'self'
             1494  LOAD_METHOD              _print_dataframe_to_text_file_handle
             1496  LOAD_FAST                'amr_detection'
             1498  LOAD_METHOD              get_detailed_summary_results
             1500  CALL_METHOD_0         0  ''
             1502  LOAD_FAST                'fh'
             1504  CALL_METHOD_2         2  ''
             1506  POP_TOP          
             1508  POP_BLOCK        
             1510  BEGIN_FINALLY    
           1512_0  COME_FROM_WITH     1488  '1488'
             1512  WITH_CLEANUP_START
             1514  WITH_CLEANUP_FINISH
             1516  END_FINALLY      
             1518  JUMP_FORWARD       1530  'to 1530'
           1520_0  COME_FROM          1464  '1464'

 L. 512      1520  LOAD_GLOBAL              logger
             1522  LOAD_METHOD              info
             1524  LOAD_STR                 '--output-dir or --output-detailed-summary unset. No detailed summary file will be written'
             1526  CALL_METHOD_1         1  ''
             1528  POP_TOP          
           1530_0  COME_FROM          1518  '1518'

 L. 514      1530  LOAD_FAST                'output_settings'
         1532_1534  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 515      1536  LOAD_GLOBAL              logger
             1538  LOAD_METHOD              info
             1540  LOAD_STR                 'Writing settings to [%s]'
             1542  LOAD_FAST                'output_settings'
             1544  CALL_METHOD_2         2  ''
             1546  POP_TOP          

 L. 516      1548  LOAD_FAST                'self'
             1550  LOAD_METHOD              _print_settings_to_file
             1552  LOAD_FAST                'settings'
             1554  LOAD_FAST                'output_settings'
             1556  CALL_METHOD_2         2  ''
             1558  POP_TOP          
             1560  JUMP_FORWARD       1572  'to 1572'
           1562_0  COME_FROM          1532  '1532'

 L. 518      1562  LOAD_GLOBAL              logger
             1564  LOAD_METHOD              info
             1566  LOAD_STR                 '--output-dir or --output-settings unset. No settings file will be written'
             1568  CALL_METHOD_1         1  ''
             1570  POP_TOP          
           1572_0  COME_FROM          1560  '1560'

 L. 520      1572  LOAD_FAST                'output_excel'
         1574_1576  POP_JUMP_IF_FALSE  1686  'to 1686'

 L. 521      1578  LOAD_GLOBAL              logger
             1580  LOAD_METHOD              info
             1582  LOAD_STR                 'Writing Excel to [%s]'
             1584  LOAD_FAST                'output_excel'
             1586  CALL_METHOD_2         2  ''
             1588  POP_TOP          

 L. 522      1590  LOAD_GLOBAL              pd
             1592  LOAD_ATTR                DataFrame
             1594  LOAD_ATTR                from_dict
             1596  LOAD_FAST                'settings'
             1598  LOAD_STR                 'index'
             1600  LOAD_CONST               ('orient',)
             1602  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1604  STORE_FAST               'settings_dataframe'

 L. 523      1606  LOAD_STR                 'Key'
             1608  LOAD_FAST                'settings_dataframe'
             1610  LOAD_ATTR                index
             1612  STORE_ATTR               name

 L. 524      1614  LOAD_FAST                'settings_dataframe'
             1616  LOAD_ATTR                set_axis
             1618  LOAD_STR                 'Value'
             1620  BUILD_LIST_1          1 
             1622  LOAD_STR                 'columns'
             1624  LOAD_CONST               True
             1626  LOAD_CONST               ('axis', 'inplace')
             1628  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1630  POP_TOP          

 L. 526      1632  LOAD_FAST                'self'
             1634  LOAD_METHOD              _print_dataframes_to_excel
             1636  LOAD_FAST                'output_excel'

 L. 527      1638  LOAD_FAST                'amr_detection'
             1640  LOAD_METHOD              get_summary_results
             1642  CALL_METHOD_0         0  ''

 L. 528      1644  LOAD_FAST                'amr_detection'
             1646  LOAD_METHOD              get_resfinder_results
             1648  CALL_METHOD_0         0  ''

 L. 529      1650  LOAD_FAST                'amr_detection'
             1652  LOAD_METHOD              get_pointfinder_results
             1654  CALL_METHOD_0         0  ''

 L. 530      1656  LOAD_FAST                'amr_detection'
             1658  LOAD_METHOD              get_plasmidfinder_results
             1660  CALL_METHOD_0         0  ''

 L. 531      1662  LOAD_FAST                'amr_detection'
             1664  LOAD_METHOD              get_detailed_summary_results
             1666  CALL_METHOD_0         0  ''

 L. 532      1668  LOAD_FAST                'amr_detection'
             1670  LOAD_METHOD              get_mlst_results
             1672  CALL_METHOD_0         0  ''

 L. 533      1674  LOAD_FAST                'settings_dataframe'

 L. 534      1676  LOAD_FAST                'args'
             1678  LOAD_ATTR                minimum_contig_length

 L. 526      1680  CALL_METHOD_9         9  ''
             1682  POP_TOP          
             1684  JUMP_FORWARD       1696  'to 1696'
           1686_0  COME_FROM          1574  '1574'

 L. 536      1686  LOAD_GLOBAL              logger
             1688  LOAD_METHOD              info
             1690  LOAD_STR                 '--output-dir or --output-excel unset. No excel file will be written'
             1692  CALL_METHOD_1         1  ''
             1694  POP_TOP          
           1696_0  COME_FROM          1684  '1684'

 L. 538      1696  LOAD_FAST                'hits_output_dir'
         1698_1700  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 539      1702  LOAD_GLOBAL              logger
             1704  LOAD_METHOD              info
             1706  LOAD_STR                 'BLAST hits are stored in [%s]'
             1708  LOAD_FAST                'hits_output_dir'
             1710  CALL_METHOD_2         2  ''
             1712  POP_TOP          
             1714  JUMP_FORWARD       1726  'to 1726'
           1716_0  COME_FROM          1698  '1698'

 L. 541      1716  LOAD_GLOBAL              logger
             1718  LOAD_METHOD              info
             1720  LOAD_STR                 '--output-dir or --output-hits-dir not set. No BLAST hits will be saved.'
             1722  CALL_METHOD_1         1  ''
             1724  POP_TOP          
           1726_0  COME_FROM          1714  '1714'

Parse error at or near `JUMP_FORWARD' instruction at offset 554
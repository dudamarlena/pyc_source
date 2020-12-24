# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyp_beagle/command_line.py
# Compiled at: 2019-07-16 04:25:49
import sys, os, argparse, re, numpy as np, ConfigParser, logging
from matplotlib import rc
from astropy.io import ascii
from astropy.io import fits
from pathos.multiprocessing import ProcessingPool
from pyp_beagle import *
from _version import __version__

def main():
    parser = standard_parser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__ + ' - Author: Jacopo Chevallard')
    args = parser.parse_args()
    args_dict = vars(args)
    logging.basicConfig(level=args.loglevel)
    BeagleDirectories.results_dir = args.results_dir
    configure_matplotlib()
    config = ConfigParser.SafeConfigParser()
    BeagleDirectories.fontsize = args.fontsize
    BeagleDirectories.inset_fontsize_fraction = args.inset_fontsize_fraction
    font = {'size': BeagleDirectories.fontsize}
    rc('font', **font)
    param_file = None
    if args.param_file is not None:
        param_file = args.param_file
    else:
        for file in os.listdir(os.path.join(BeagleDirectories.results_dir, BeagleDirectories.beagle_input_files)):
            if file.endswith('.param'):
                file_name = os.path.join(BeagleDirectories.results_dir, BeagleDirectories.beagle_input_files, file)
                if '[main]' in open(file_name).readline():
                    param_file = file
                    break

        if param_file is None:
            raise ValueError('No parameter file has been specified, nor a parameter file can be found in the Beagle results directory')
        BeagleDirectories.param_file = param_file
        name = os.path.join(BeagleDirectories.results_dir, BeagleDirectories.beagle_input_files, param_file)
        config.read(name)
        has_spectra = config.has_option('main', 'LIST OF SPECTRA')
        has_photometry = config.has_option('main', 'PHOTOMETRIC CATALOGUE')
        has_spec_indices = config.has_option('main', 'SPECTRAL INDICES CATALOGUE')
        file_list, IDs = get_files_list(suffix=args.suffix)
        if len(file_list) == 0:
            raise ValueError('No Beagle results files are present in the directory ' + BeagleDirectories.results_dir)
        regex = None
        if args.regex_ignore is not None:
            regex = re.compile(args.regex_ignore, re.IGNORECASE)
        for i, (ID, file) in enumerate(zip(IDs, file_list)):
            if args.ID_list is not None:
                if ID not in args.ID_list:
                    IDs.remove(ID)
                    file_list.remove(file)
                    continue
            if regex is not None:
                _ID = regex.sub('', ID)
                IDs[i] = _ID

    mock_catalogue = None
    if args.mock_file_name is not None:
        params_file = os.path.join(BeagleDirectories.results_dir, args.json_file_mock)
        mock_catalogue = BeagleMockCatalogue(params_file, ignore_string=regex, plot_title=args.plot_title)
        mock_catalogue.load(args.mock_file_name)
    params_file = os.path.join(BeagleDirectories.results_dir, args.json_file_triangle)
    summary_catalogue = BeagleSummaryCatalogue(credible_intervals=args.credible_interval, n_proc=args.n_proc)
    if args.compute_summary:
        if not summary_catalogue.exists():
            summary_catalogue.compute(file_list)
    if args.latex_table_params is not None:
        if not summary_catalogue.exists():
            summary_catalogue.compute(file_list)
        summary_catalogue.load()
        summary_catalogue.make_latex_table(args.latex_table_params, IDs=args.ID_list)
    if args.extract_MAP:
        summary_catalogue.extract_MAP_solution(file_list)
    if args.mock_file_name is not None:
        if not summary_catalogue.exists():
            summary_catalogue.compute(file_list)
        summary_catalogue.load()
        mock_catalogue.compare_hist(summary_catalogue, overwrite=True)
        mock_catalogue.compare(summary_catalogue, overwrite=True)
    if has_photometry:
        my_photometry = Photometry(**args_dict)
        try:
            filters_file = os.path.expandvars(config.get('main', 'FILTERS FILE'))
            filters_throughputs = None
        except:
            filters_file = os.path.expandvars(config.get('main', 'FILTERS CONFIGURATION'))
            try:
                filters_throughputs = os.path.expandvars(config.get('main', 'FILTERS THROUGHPUTS'))
            except:
                filters_throughputs = None

        my_photometry.filters.load(filters_file, filters_folder=args.filters_folder, filters_throughputs=filters_throughputs)
        file_name = os.path.expandvars(config.get('main', 'PHOTOMETRIC CATALOGUE'))
        my_photometry.observed_catalogue.load(file_name)
    if has_spec_indices and args.line_labels_json:
        my_spec_indices = SpectralIndices(**args_dict)
        file_name = os.path.expandvars(config.get('main', 'SPECTRAL INDICES CONFIGURATION'))
        my_spec_indices.observed_catalogue.configure(file_name)
        file_name = os.path.expandvars(config.get('main', 'SPECTRAL INDICES CATALOGUE'))
        my_spec_indices.observed_catalogue.load(file_name)
    if has_spectra:
        my_spectrum = Spectrum(params_file, **args_dict)
        my_spectrum.observed_spectrum.configure(config=config)
        inputSpectraFileName = os.path.expandvars(config.get('main', 'LIST OF SPECTRA'))
        lines = list()
        with open(inputSpectraFileName, 'r') as (f):
            for line in f:
                line = line.strip()
                line = os.path.join(os.path.dirname(inputSpectraFileName), line)
                lines.append(line)

        file_names = list()
        for ID in IDs:
            _ID = ID
            if regex is not None:
                _ID = regex.sub('', _ID)
            for line in lines:
                _line = trimFitsSuffix(os.path.basename(line))
                if regex is not None:
                    _line = regex.sub('', _line)
                _line = _line.split('_BEAGLE')[0]
                if _ID == _line:
                    file_names.append(line)
                    break

    if args.n_proc > 1:
        pool = ProcessingPool(nodes=args.n_proc)
    if args.plot_marginal:
        if args.n_proc > 1:
            if has_spectra:
                pool.map(my_spectrum.plot_marginal, IDs, file_names)
            if has_photometry:
                pool.map(my_photometry.plot_marginal, IDs)
            if has_spec_indices and args.line_labels_json:
                pool.map(my_spec_indices.plot_line_fluxes, IDs)
        else:
            for i, ID in enumerate(IDs):
                if has_spectra:
                    my_spectrum.plot_marginal(ID, file_names[i])
                if has_photometry:
                    my_photometry.plot_marginal(ID)
                if has_spec_indices and args.line_labels_json:
                    my_spec_indices.plot_line_fluxes(ID)

    if args.plot_triangle:
        my_PDF = PDF(params_file, mock_catalogue=mock_catalogue, **args_dict)
        if args.n_proc > 1:
            pool.map(my_PDF.plot_triangle, IDs)
        else:
            for ID in IDs:
                my_PDF.plot_triangle(ID)

    return
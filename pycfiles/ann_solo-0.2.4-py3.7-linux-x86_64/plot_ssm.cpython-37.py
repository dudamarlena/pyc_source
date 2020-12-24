# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ann_solo/plot_ssm.py
# Compiled at: 2019-11-12 16:23:45
# Size of source mod 2**32: 5957 bytes
import argparse, os
import urllib.parse as urlparse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from spectrum_utils import plot
from spectrum_utils.spectrum import PeptideFragmentAnnotation
from ann_solo import reader
from ann_solo import spectrum_match
import ann_solo.config as config
from ann_solo.spectrum import process_spectrum

def set_matching_peaks(library_spectrum, query_spectrum):
    peak_matches = spectrum_match.get_best_match(query_spectrum, [library_spectrum], config.fragment_mz_tolerance, config.allow_peak_shifts)[2]
    query_spectrum.annotation = np.full_like(query_spectrum.mz, None, object)
    for peak_match in peak_matches:
        library_annotation = library_spectrum.annotation[peak_match[1]]
        if library_annotation is not None:
            query_spectrum.annotation[peak_match[0]] = library_annotation
        else:
            fragment_annotation = PeptideFragmentAnnotation(1, 1, 'z', 0)
            fragment_annotation.ion_type = 'unknown'
            query_spectrum.annotation[peak_match[0]] = library_spectrum.annotation[peak_match[1]] = fragment_annotation


def main():
    parser = argparse.ArgumentParser(description='Visualize spectrum–spectrum matches from your ANN-SoLo identification results')
    parser.add_argument('mztab_filename',
      help='Identifications in mzTab format')
    parser.add_argument('query_id',
      help='The identifier of the query to visualize')
    args = parser.parse_args()
    metadata = {}
    with open(args.mztab_filename) as (f_mztab):
        for line in f_mztab:
            line_split = line.strip().split('\t')
            if line_split[0] == 'MTD':
                metadata[line_split[1]] = line_split[2]
            else:
                break

    ssms = reader.read_mztab_ssms(args.mztab_filename)
    ssms.index = ssms.index.map(str)
    settings = []
    for key in metadata:
        if 'software[1]-setting' in key:
            param = metadata[key][:metadata[key].find(' ')]
            value = metadata[key][metadata[key].rfind(' ') + 1:]
            if value != 'None':
                if value != 'False':
                    settings.append('--{}'.format(param))
                if value not in ('False', 'True'):
                    settings.append(value)

    settings.append('dummy_spectral_library_filename')
    settings.append('dummy_query_filename')
    settings.append('dummy_output_filename')
    config.parse(' '.join(settings))
    query_id = args.query_id
    query_uri = urlparse.urlparse(urlparse.unquote(metadata['ms_run[1]-location']))
    query_filename = os.path.abspath(os.path.join(query_uri.netloc, query_uri.path))
    ssm = ssms.loc[query_id]
    library_id = ssm['accession']
    library_uri = urlparse.urlparse(urlparse.unquote(ssm['database']))
    library_filename = os.path.abspath(os.path.join(library_uri.netloc, library_uri.path))
    score = ssm['search_engine_score[1]']
    with reader.SpectralLibraryReader(library_filename) as (lib_reader):
        library_spectrum = lib_reader.get_spectrum(library_id, True)
    query_spectrum = None
    for spec in reader.read_mgf(query_filename):
        if spec.identifier == query_id:
            query_spectrum = process_spectrum(spec, False)
            query_spectrum.precursor_charge = library_spectrum.precursor_charge
            break

    if query_spectrum is None:
        raise ValueError('Could not find the specified query spectrum')
    set_matching_peaks(library_spectrum, query_spectrum)
    plot.colors[None] = '#757575'
    fig, ax = plt.subplots(figsize=(20, 10))
    plot.mirror(query_spectrum, library_spectrum, {'color_ions':True, 
     'annotate_ions':False}, ax)
    max_intensity = library_spectrum.intensity.max()
    for i, annotation in enumerate(library_spectrum.annotation):
        if annotation is not None and annotation.ion_type != 'unknown':
            x = library_spectrum.mz[i]
            y = -library_spectrum.intensity[i] / max_intensity
            ax.text(x, y, (str(annotation)), color=(plot.colors[annotation.ion_type]),
              zorder=5,
              horizontalalignment='right',
              verticalalignment='center',
              rotation=90,
              rotation_mode='anchor')

    ax.set_ylim(-1.1, 1.05)
    ax.text(0.5, 1.06, f"{library_spectrum.peptide}, Score: {score:.3f}", horizontalalignment='center',
      verticalalignment='bottom',
      fontsize='x-large',
      fontweight='bold',
      transform=(ax.transAxes))
    ax.text(0.5, 1.02, f"File: {os.path.basename(query_filename)}, Scan: {query_spectrum.identifier}, Precursor m/z: {query_spectrum.precursor_mz:.4f}, Library m/z: {library_spectrum.precursor_mz:.4f}, Charge: {query_spectrum.precursor_charge}", horizontalalignment='center',
      verticalalignment='bottom',
      fontsize='large',
      transform=(ax.transAxes))
    plt.savefig(f"{query_id}.png", dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    main()
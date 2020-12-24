# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/jwql_monitors/generate_preview_images.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 25442 bytes
"""Generate preview images for all files in the ``jwql`` filesystem.

Execution of this script will generate preview images and thumbnail
images for each file in the ``jwql`` filesystem.  Preview images have
axes labels, titles, and colorbars, wheras thumbnail images are
smaller and contain no labels.  Images are saved into the
``preview_image_filesystem`` and ``thumbnail_filesystem``, organized
by subdirectories pertaining to the ``program_id`` in the filenames.

Authors
-------

    - Matthew Bourque
    - Bryan Hilbert

Use
---

    This script is intended to be executed as such:

    ::

        python generate_preview_images.py
"""
import glob, logging, multiprocessing, os, re, numpy as np
from jwql.utils import permissions
from jwql.utils.constants import NIRCAM_LONGWAVE_DETECTORS, NIRCAM_SHORTWAVE_DETECTORS
from jwql.utils.logging_functions import configure_logging, log_info, log_fail
from jwql.utils.preview_image import PreviewImage
from jwql.utils.utils import get_config, filename_parser
SW_MOD_GAP = 1387
LW_MOD_GAP = 741
SW_DET_GAP = 145
FULLX = 2048
FULLY = 2048

def array_coordinates(channelmod, detector_list, lowerleft_list):
    """Create an appropriately sized ``numpy`` array to contain the
    mosaic image given the channel and module of the data.

    Parameters
    ----------
    channelmod : str
        Indicator of the NIRCam channel/module of the data.
        Options are:
        ``LW`` - for longwave channel data
        ``SWA`` - for shortwave A module only (4 detectors) data
        ``SWB`` - for shortwave B module only (4 detectors) data
        ``SW`` - for shortwave both module data (8 detectors)

    detector_list : list
        List of detectors used in data to be simulated

    lowerleft_list : list
        Each element is a tuple giving the (x, y) coordinates
        corresponding to the lower left corner of the aperture within
        the full frame detector. These values come from the
        ``SUBSTRT1`` and 2 values in the file headers.

    Returns
    -------
    xdim : int
        Length of the output array needed to contain all detectors' data

    ydim : int
        Height of the output array needed to contain all detectors' data

    module_lowerlefts : dict
        Dictionary giving the ``(x, y)`` coordinate in the coordinate
        system of the full module(s) where the lower left corner of the
        data from a given detector will be placed. (e.g.
        ``NRCA1: (1888, 1888)`` means that the data from detector
        ``NRCA1`` should be placed into
        ``[1888: 1888+y_dim_of_data, 1888: 1888+x_dim_of_data]`` within
        the final array (which has total dimensions of ``(xdim, ydim)``
    """
    ashort = [
     'NRCA1', 'NRCA2', 'NRCA3', 'NRCA4']
    bshort = ['NRCB1', 'NRCB2', 'NRCB3', 'NRCB4']
    module_lowerlefts = {'NRCA1':(0, 0),  'NRCA2':(
      0, FULLY + SW_DET_GAP), 
     'NRCA3':(
      FULLX + SW_DET_GAP, 0), 
     'NRCA4':(
      FULLX + SW_DET_GAP, FULLY + SW_DET_GAP), 
     'NRCB1':(
      FULLX + SW_DET_GAP, FULLY + SW_DET_GAP), 
     'NRCB2':(
      FULLX + SW_DET_GAP, 0), 
     'NRCB3':(
      0, FULLY + SW_DET_GAP), 
     'NRCB4':(0, 0), 
     'NRCA5':(0, 0), 
     'NRCB5':(
      FULLX + LW_MOD_GAP, 0)}
    if channelmod == 'SW':
        mod_delta = (
         FULLX * 2 + SW_DET_GAP + SW_MOD_GAP, 0)
        for b_detector in bshort:
            module_lowerlefts[b_detector] = tuple([sum(x) for x in zip(module_lowerlefts[b_detector], mod_delta)])

    subx = 1
    suby = 1
    if 'SW' in channelmod:
        detector_list = np.array(detector_list)
        a1 = detector_list == 'NRCA1'
        b4 = detector_list == 'NRCB4'
        lowerleft_list = np.array(lowerleft_list)
        if np.sum(a1) == 1:
            subx, suby = lowerleft_list[a1][0]
        else:
            if np.sum(b4) == 1:
                subx, suby = lowerleft_list[b4][0]
            else:
                missing_a14 = 'SW data provided, but neither NRCA1 nor NRCB4 are present.'
                logging.error(missing_a14)
                raise ValueError(missing_a14)
    if (subx != 1) | (suby != 1):
        subarr_delta = {'NRCA1':(0, 0), 
         'NRCA2':(
          0, 0 - suby), 
         'NRCA3':(
          0 - subx, 0), 
         'NRCA4':(
          0 - subx, 0 - suby), 
         'NRCB1':(
          0 - subx, 0 - suby), 
         'NRCB2':(
          0 - subx, 0), 
         'NRCB3':(
          0, 0 - suby), 
         'NRCB4':(0, 0)}
        for det in ashort + bshort:
            module_lowerlefts[det] = tuple([sum(x) for x in zip(module_lowerlefts[det], subarr_delta[det])])

    aperturex = FULLX - (subx - 1)
    aperturey = FULLY - (suby - 1)
    if channelmod in ('SWA', 'SWB'):
        xdim = 2 * aperturex + SW_DET_GAP
        ydim = 2 * aperturey + SW_DET_GAP
    else:
        if channelmod == 'SW':
            xdim = 4 * aperturex + 2 * SW_DET_GAP + SW_MOD_GAP
            ydim = 2 * aperturey + SW_DET_GAP
        else:
            if channelmod == 'LW':
                xdim = 2 * aperturex + LW_MOD_GAP
                ydim = aperturey
    return (
     xdim, ydim, module_lowerlefts)


def check_existence(file_list, outdir):
    """Given a list of fits files, determine if a preview image has
    already been created in ``outdir``.

    Parameters
    ----------
    file_list : list
        List of fits filenames from which preview image will be
        generated

    outdir : str
        Directory that will contain the preview image if it exists

    Returns
    -------
    exists : bool
        ``True`` if preview image exists, ``False`` if it does not
    """
    if len(file_list) == 1:
        filename = os.path.split(file_list[0])[1]
        search_string = filename.split('.fits')[0] + '_*.jpg'
    else:
        file_parts = filename_parser(file_list[0])
    if file_parts['detector'].upper() in NIRCAM_SHORTWAVE_DETECTORS:
        mosaic_str = 'NRC_SW*_MOSAIC_'
    else:
        if file_parts['detector'].upper() in NIRCAM_LONGWAVE_DETECTORS:
            mosaic_str = 'NRC_LW*_MOSAIC_'
        search_string = 'jw{}{}{}_{}{}{}_{}_{}{}*.jpg'.format(file_parts['program_id'], file_parts['observation'], file_parts['visit'], file_parts['visit_group'], file_parts['parallel_seq_id'], file_parts['activity'], file_parts['exposure_id'], mosaic_str, file_parts['suffix'])
    current_files = glob.glob(os.path.join(outdir, search_string))
    if len(current_files) > 0:
        return True
    else:
        return False


def create_dummy_filename(filelist):
    """Create a dummy filename indicating the detectors used to create
    the mosaic. Check the list of detectors used to determine the proper
    text to substitute into the initial filename.

    Parameters
    ----------
    filelist : list
        List of filenames containing the data used to create the mosaic.
        It is assumed these filenames follow JWST filenaming
        conventions.

    Returns
    -------
    dummy_name : str
        The first filename in ``filelist`` is modified, such that the
        detector name is replaced with text indicating the source of the
        mosaic data.
    """
    det_string_list = []
    modules = []
    for filename in filelist:
        indir, infile = os.path.split(filename)
        det_string = filename_parser(infile)['detector']
        det_string_list.append(det_string)
        modules.append(det_string[3].upper())

    if '5' in det_string_list[0]:
        suffix = 'NRC_LW_MOSAIC'
    else:
        moda = modules.count('A')
        modb = modules.count('B')
        if moda > 0:
            if modb > 0:
                suffix = 'NRC_SWALL_MOSAIC'
            else:
                suffix = 'NRC_SWA_MOSAIC'
        else:
            if modb > 0:
                suffix = 'NRC_SWB_MOSAIC'
    dummy_name = filelist[0].replace(det_string_list[0], suffix)
    return dummy_name


def create_mosaic(filenames):
    """If an exposure comprises data from multiple detectors read in all
    the appropriate files and create a mosaic so that the preview image
    will show all the data together.

    Parameters
    ----------
    filenames : list
        List of filenames to be combined into a mosaic

    Returns
    -------
    mosaic_filename : str
        Name of fits file containing the mosaicked data
    """
    data = []
    detector = []
    data_lower_left = []
    for filename in filenames:
        image = PreviewImage(filename, 'SCI')
        data_dim = len(image.data.shape)
        if data_dim == 4:
            diff_im = image.difference_image(image.data)
        else:
            diff_im = image.data
        data.append(diff_im)
        detector.append(filename_parser(filename)['detector'].upper())
        data_lower_left.append((image.xstart, image.ystart))

    mosaic_channel = find_data_channel(detector)
    full_xdim, full_ydim, full_lower_left = array_coordinates(mosaic_channel, detector, data_lower_left)
    datashape = data[0].shape
    datadim = len(datashape)
    if datadim == 2:
        full_array = np.zeros((1, full_ydim, full_xdim)) * np.nan
    else:
        if datadim == 3:
            full_array = np.zeros((datashape[0], full_ydim, full_xdim)) * np.nan
        else:
            raise ValueError('Difference image for {} must be either 2D or 3D.'.format(filenames[0]))
    for pixdata, detect in zip(data, detector):
        x0, y0 = full_lower_left[detect]
        if datadim == 2:
            yd, xd = pixdata.shape
            full_array[0, y0:y0 + yd, x0:x0 + xd] = pixdata
        elif datadim == 3:
            ints, yd, xd = pixdata.shape
            full_array[:, y0:y0 + yd, x0:x0 + xd] = pixdata

    full_dq = create_dq_array(full_xdim, full_ydim, full_array[0, :, :], mosaic_channel)
    return (
     full_array, full_dq)


def create_dq_array(xd, yd, mosaic, module):
    """Create DQ array that goes with the mosaic image. Set unpopulated
    pixels to be skipped in preview image scaling. Same for the
    reference pixels for all detectors

    Parameters
    ----------
    xd : int
        X-coordinate dimension of the DQ array

    yd : int
        Y-coordinate dimension of the DQ array

    mosaic : obj
        2D ``numpy`` array containing the mosaic image

    module : str
        Module used for mosaic. Options are ``LW``,`` SW``, ``SWA``,
        ``SWB``

    Returns
    -------
    dq : obj
        2D ``numpy`` array containing the DQ array. Pixels that are
        ``True`` are considered science pixels and are used when
        scaling the preview image. Pixels that are ``False`` are
        skipped.
    """
    dq = np.ones((yd, xd), dtype='bool')
    dq[np.isnan(mosaic)] = 0
    if xd >= FULLX:
        dq[0:4, :] = 0
        dq[:, 0:4] = 0
        dq[2044:2048, :] = 0
        dq[:, 2044:2048] = 0
        if module == 'LW':
            lwb_lower = FULLX + LW_MOD_GAP
            dq[:, lwb_lower:lwb_lower + 4] = 0
            dq[:, lwb_lower + 2044:lwb_lower + 2048] = 0
        if module in ('SWA', 'SWB', 'SW'):
            lowerval = FULLX + SW_DET_GAP
            dq[lowerval:lowerval + 4, :] = 0
            dq[lowerval + 2044:, :] = 0
            dq[:, lowerval:lowerval + 4] = 0
            dq[:, lowerval + 2044:lowerval + 2048] = 0
        if module == 'SW':
            modb_lower = lowerval + FULLX + SW_MOD_GAP
            dq[:, modb_lower:modb_lower + 4] = 0
            dq[:, modb_lower + 2044:modb_lower + 2048] = 0
            modb_upper = modb_lower + FULLX + SW_DET_GAP
            dq[:, modb_upper:modb_upper + 4] = 0
            dq[:, modb_upper + 2044:modb_upper + 2048] = 0
    else:
        nan_indexes = np.where(np.isnan(mosaic))
        match = nan_indexes[0] == yd - 1
        vert_xmin = np.min(nan_indexes[1][match])
        vert_xmax = vert_xmin + SW_DET_GAP - 1
        match2 = nan_indexes[1] == xd - 1
        horiz_ymin = np.min(nan_indexes[0][match2])
        horiz_ymax = horiz_ymin + SW_DET_GAP - 1
        dq[:, vert_xmin - 4:vert_xmin] = 0
        dq[:, vert_xmax + 1:vert_xmax + 5] = 0
        dq[horiz_ymin - 4:horiz_ymin, :] = 0
        dq[horiz_ymax + 1:horiz_ymax + 5, :] = 0
    return dq


def detector_check(detector_list, search_string):
    """Search a given list of detector names for the provided regular
    expression sting.

    Parameters
    ----------
    detector_list : list
        List of detector names (e.g. ``NRCA5``)

    search_string : str
        Regular expression string to use for search

    Returns
    -------
    total : int
        Number of detectors in ``detector_list`` that match
        ``search_string``
    """
    pattern = re.compile(search_string, re.IGNORECASE)
    match = [pattern.match(detector) for detector in detector_list]
    total = np.sum(np.array([m is not None for m in match]))
    return total


def find_data_channel(detectors):
    """Using a list of detectors, identify the channel(s) that the data
    are from.

    Parameters
    ----------
    detectors : list
        List of detector names

    Returns
    -------
    channel : str
        Identifier noting which channels the given detectors are in.
        Can be ``SWA`` for shortwave, module A only, ``SWB`` for
        shortwave, module B only, ``SW``, for shortwave modules A and B,
        and ``LW`` for longwave.
    """
    nrc_swa_total = detector_check(detectors, 'NRCA[1-4]')
    nrc_swb_total = detector_check(detectors, 'NRCB[1-4]')
    nrc_lw_total = detector_check(detectors, 'NRC[AB]5')
    both_channels = "Can't mix NIRCam SW and LW data in same mosaic."
    if nrc_swa_total != 0:
        if nrc_lw_total != 0:
            raise ValueError(both_channels)
        else:
            if nrc_swb_total != 0:
                channel = 'SW'
            else:
                channel = 'SWA'
    else:
        if nrc_swb_total != 0:
            if nrc_lw_total != 0:
                raise ValueError(both_channels)
            else:
                channel = 'SWB'
        else:
            if nrc_lw_total != 0:
                channel = 'LW'
            else:
                raise ValueError('No NIRCam SW nor LW data')
    return channel


def get_base_output_name(filename_dict):
    """Returns the base output name used for preview images and
    thumbnails.

    Parameters
    ----------
    filename_dict : dict
        A dictionary containing parsed filename parts via
        ``filename_parser``

    Returns
    -------
    base_output_name : str
        The base output name, e.g. ``jw96090001002_03101_00001_nrca2_rate``
    """
    base_output_name = 'jw{}{}{}_{}{}{}_{}_'.format(filename_dict['program_id'], filename_dict['observation'], filename_dict['visit'], filename_dict['visit_group'], filename_dict['parallel_seq_id'], filename_dict['activity'], filename_dict['exposure_id'])
    return base_output_name


@log_fail
@log_info
def generate_preview_images():
    """The main function of the ``generate_preview_image`` module.
    See module docstring for further details."""
    logging.info('Beginning the script run')
    program_list = [os.path.basename(item) for item in glob.glob(os.path.join(get_config()['filesystem'], '*'))]
    pool = multiprocessing.Pool(processes=(int(get_config()['cores'])))
    pool.map(process_program, program_list)
    pool.close()
    pool.join()
    logging.info('Completed.')


def group_filenames(filenames):
    """Given a list of JWST filenames, group together files from the
    same exposure. These files will share the same ``program_id``,
    ``observation``, ``visit``, ``visit_group``, ``parallel_seq_id``,
    ``activity``, ``exposure``, and ``suffix``. Only the ``detector``
    will be different. Currently only NIRCam files for a given exposure
    will be grouped together. For other instruments multiple files for
    a given exposure will be kept separate from one another and no
    mosaic will be made.  Stage 3 files will remain as individual
    files, and will not be grouped together with any other files.

    Parameters
    ----------
    filenames : list
        list of filenames

    Returns
    -------
    grouped : list
        grouped list of filenames where each element is a list and
        contains the names of filenames with matching exposure
        information.
    """
    grouped, matched_names = [], []
    filenames.sort()
    for filename in filenames:
        subgroup = []
        filename_dict = filename_parser(os.path.basename(filename))
        if filename not in matched_names:
            if 'stage_3' in filename_dict['filename_type']:
                matched_names.append(filename)
                subgroup.append(filename)
            else:
                if filename_dict['filename_type'] == 'stage_1_and_2':
                    if filename_dict['detector'].upper() in NIRCAM_SHORTWAVE_DETECTORS:
                        detector_str = 'NRC[AB][1234]'
                    else:
                        if filename_dict['detector'].upper() in NIRCAM_LONGWAVE_DETECTORS:
                            detector_str = 'NRC[AB]5'
                        else:
                            detector_str = filename_dict['detector'].upper()
                        base_output_name = get_base_output_name(filename_dict)
                        match_str = '{}{}_{}.fits'.format(base_output_name, detector_str, filename_dict['suffix'])
                        match_str = os.path.join(os.path.dirname(filename), match_str)
                        pattern = re.compile(match_str, re.IGNORECASE)
                        for file_to_match in filenames:
                            if pattern.match(file_to_match) is not None:
                                matched_names.append(file_to_match)
                                subgroup.append(file_to_match)

            if len(subgroup) > 0:
                grouped.append(subgroup)

    return grouped


def process_program(program):
    """Generate preview images and thumbnails for the given program.

    Parameters
    ----------
    program : str
        The program identifier (e.g. ``88600``)
    """
    filenames = glob.glob(os.path.join(get_config()['filesystem'], program, '*.fits'))
    grouped_filenames = group_filenames(filenames)
    logging.info('Found {} filenames'.format(len(filenames)))
    for file_list in grouped_filenames:
        filename = file_list[0]
        try:
            identifier = 'jw{}'.format(filename_parser(filename)['program_id'])
        except ValueError:
            identifier = os.path.basename(filename).split('.fits')[0]

        preview_output_directory = os.path.join(get_config()['preview_image_filesystem'], identifier)
        thumbnail_output_directory = os.path.join(get_config()['thumbnail_filesystem'], identifier)
        file_exists = check_existence(file_list, preview_output_directory)
        if file_exists:
            logging.info('JPG already exists for {}, skipping.'.format(filename))
        else:
            if not os.path.exists(preview_output_directory):
                os.makedirs(preview_output_directory)
                permissions.set_permissions(preview_output_directory)
                logging.info('Created directory {}'.format(preview_output_directory))
            else:
                if not os.path.exists(thumbnail_output_directory):
                    os.makedirs(thumbnail_output_directory)
                    permissions.set_permissions(thumbnail_output_directory)
                    logging.info('Created directory {}'.format(thumbnail_output_directory))
                max_size = 8
                numfiles = len(file_list)
                if numfiles > 1:
                    try:
                        mosaic_image, mosaic_dq = create_mosaic(file_list)
                        logging.info('Created mosiac for:')
                        for item in file_list:
                            logging.info('\t{}'.format(item))

                    except (ValueError, FileNotFoundError) as error:
                        logging.error(error)

                    dummy_file = create_dummy_filename(file_list)
                    if numfiles in (2, 4):
                        max_size = 16
                    elif numfiles in (8, ):
                        max_size = 32
            try:
                im = PreviewImage(filename, 'SCI')
                im.clip_percent = 0.01
                im.scaling = 'log'
                im.cmap = 'viridis'
                im.output_format = 'jpg'
                im.preview_output_directory = preview_output_directory
                im.thumbnail_output_directory = thumbnail_output_directory
                if numfiles != 1:
                    im.data = mosaic_image
                    im.dq = mosaic_dq
                    im.file = dummy_file
                im.make_image(max_img_size=max_size)
                logging.info('Created preview image and thumbnail for: {}'.format(filename))
            except ValueError as error:
                logging.warning(error)


if __name__ == '__main__':
    module = os.path.basename(__file__).strip('.py')
    configure_logging(module)
    generate_preview_images()
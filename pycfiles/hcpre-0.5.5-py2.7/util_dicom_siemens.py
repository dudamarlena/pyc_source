# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hcpre/duke_siemens/util_dicom_siemens.py
# Compiled at: 2014-05-12 17:01:30
"""
Routines for extracting data from Siemens DICOM files.

The simplest way to read a file is to call read(filename). If you like you
can also call lower level functions like read_data().

Except for the map of internal data types to numpy type strings (which
doesn't require an import of numpy), this code is deliberately ignorant of
numpy. It returns native Python types that are easy to convert into
numpy types.
"""
from __future__ import division
import struct, exceptions, math, dicom, util_mrs_file, constants
TYPE_NONE = 0
TYPE_IMAGE = 1
TYPE_SPECTROSCOPY = 2
ASSERTIONS_ENABLED = False
TAG_CONTENT_TYPE = (
 41, 4104)
TAG_SPECTROSCOPY_DATA = (32737, 4112)

def read(filename, ignore_data=False):
    """ This is the simplest (and recommended) way for our code to read a
    Siemens DICOM file.
    
    It returns a tuple of (parameters, data). The parameters are a dict.
    The data is in a Python list.
    """
    defer_size = 4096 if ignore_data else 0
    dataset = dicom.read_file(filename)
    params = read_parameters_from_dataset(dataset)
    data = read_data_from_dataset(dataset)
    return (
     params, data)


def read_parameters(filename):
    return read_parameters_from_dataset(dicom.read_file(filename))


def read_data(filename):
    return read_data_from_dataset(dicom.read_file(filename))


def read_data_from_dataset(dataset):
    """Given a PyDicom dataset, returns the data in the Siemens DICOM 
    spectroscopy data tag (0x7fe1, 0x1010) as a list of complex numbers.    
    """
    data = _get(dataset, TAG_SPECTROSCOPY_DATA)
    if data:
        data = struct.unpack('<%df' % (len(data) / 4), data)
        data = util_mrs_file.collapse_complexes(data)
    else:
        data = []
    return data


def read_parameters_from_dataset(dataset):
    """Given a PyDicom dataset, returns a fairly extensive subset of the
    parameters therein as a dictionary.
    """
    params = {}
    slice_index = 1
    ptag_img = {}
    ptag_ser = {}
    for tag in ((41, 4112), (41, 4624), (41, 4368)):
        tag_data = dataset.get(tag, None)
        if tag_data:
            break

    if tag_data:
        ptag_img = _parse_csa_header(tag_data.value)
    for tag in ((41, 4128), (41, 4640), (41, 4384)):
        tag_data = dataset.get(tag, None)
        if tag_data:
            break

    if tag_data:
        ptag_ser = _parse_csa_header(tag_data.value)
    if ptag_ser.get('MrProtocol', ''):
        prot_ser = _parse_protocol_data(ptag_ser['MrProtocol'])
    if ptag_ser.get('MrPhoenixProtocol', ''):
        prot_ser = _parse_protocol_data(ptag_ser['MrPhoenixProtocol'])
    is_epsi = False
    is_svs = False
    is_csi = False
    is_jpress = False
    is_svslip2 = False
    parameter_filename = _extract_from_quotes(prot_ser.get('tProtocolName', ''))
    parameter_filename = parameter_filename.strip()
    sequence_filename = _extract_from_quotes(prot_ser.get('tSequenceFileName', ''))
    sequence_filename = sequence_filename.strip()
    sequence_filename2 = ptag_img.get('SequenceName', '')
    sequence_filename2 = sequence_filename2.strip()
    parameter_filename_lower = parameter_filename.lower()
    sequence_filename_lower = sequence_filename.lower()
    sequence_filename2_lower = sequence_filename2.lower()
    is_epsi = 'epsi' in (parameter_filename_lower, sequence_filename_lower)
    is_svs = 'svs' in (parameter_filename_lower, sequence_filename_lower,
     sequence_filename2_lower)
    if 'fid' in (parameter_filename_lower, sequence_filename_lower):
        if 'csi' in (parameter_filename_lower, sequence_filename_lower):
            is_csi = True
        else:
            is_svs = True
    if 'csi' in (parameter_filename_lower, sequence_filename_lower):
        is_csi = True
    is_jpress = 'jpress' in (parameter_filename_lower,
     sequence_filename_lower)
    is_svslip2 = 'svs_li2' in (parameter_filename_lower,
     sequence_filename2_lower)
    params['patient_name'] = _get(dataset, (16, 16), '')
    params['patient_id'] = _get(dataset, (16, 32))
    params['patient_birthdate'] = _get(dataset, (16, 48))
    params['patient_sex'] = _get(dataset, (16, 64), '')
    params['patient_age'] = int(_get(dataset, (16, 4112), '000Y')[:3])
    params['patient_weight'] = round(_get(dataset, (16, 4144), 0))
    params['study_code'] = _get(dataset, (8, 4144), '')
    params['bed_move_fraction'] = 0.0
    s = _get(dataset, (8, 128), '')
    if s:
        s = ' ' + s
    s += _get(dataset, (8, 4240), '')
    params['institution_id'] = s
    params['parameter_filename'] = parameter_filename
    params['study_type'] = 'spec'
    params['bed_move_date'] = _get(dataset, (8, 32), '')
    params['measure_date'] = params['bed_move_date']
    params['bed_move_time'] = _get(dataset, (8, 48), '')
    params['comment_1'] = _get(dataset, (8, 49), '')
    if not params['comment_1']:
        params['comment_1'] = _get(dataset, (32, 16384), '')
    params['measure_time'] = _get(dataset, (8, 50), '')
    params['sequence_filename'] = ptag_img.get('SequenceName', '')
    params['sequence_type'] = ptag_img.get('SequenceName', '')
    params['echo_position'] = '0.0'
    params['image_contrast_mode'] = 'unknown'
    params['kspace_mode'] = 'unknown'
    params['measured_slices'] = '1'
    params['saturation_bands'] = '0'
    params['averages'] = int(_float(ptag_img.get('NumberOfAverages', '')))
    params['flip_angle'] = _float(ptag_img.get('FlipAngle', ''))
    params['frequency'] = float(ptag_img.get('ImagingFrequency', 0)) * 1000000.0
    inversion_time = float(ptag_img.get('InversionTime', 0))
    params['inversion_time_1'] = inversion_time
    params['number_inversions'] = 1 if inversion_time else 0
    params['measured_echoes'] = ptag_img.get('EchoTrainLength', '1')
    params['nucleus'] = ptag_img.get('ImagedNucleus', '')
    params['prescans'] = prot_ser.get('sSpecPara.lPreparingScans', 0)
    gain = prot_ser.get('sRXSPEC.lGain', None)
    if gain == 0:
        gain = '-20.0'
    else:
        if gain == 1:
            gain = '0.0'
        else:
            gain = ''
        params['receiver_gain'] = gain
        params['ft_scale_factor'] = float(prot_ser.get('sRXSPEC.aFFT_SCALE[0].flFactor', 0))
        coil = prot_ser.get('sCOIL_SELECT_MEAS.asList[0].sCoilElementID.tCoilID', '')
        params['receiver_coil'] = _extract_from_quotes(coil)
        params['repetition_time_1'] = float(prot_ser.get('alTR[0]', 0)) * 0.001
        sweep_width = ''
        remove_oversample_flag = prot_ser.get('sSpecPara.ucRemoveOversampling', '')
        remove_oversample_flag = remove_oversample_flag.strip() == '0x1'
        readout_os = float(ptag_ser.get('ReadoutOS', 1.0))
        dwelltime = float(ptag_img.get('RealDwellTime', 1.0)) * 1e-09
        if dwelltime:
            sweep_width = 1 / dwelltime
            if not remove_oversample_flag:
                sweep_width *= readout_os
            sweep_width = str(sweep_width)
        params['transmitter_voltage'] = prot_ser.get('sTXSPEC.asNucleusInfo[0].flReferenceAmplitude', '0.0')
        params['total_duration'] = prot_ser.get('lTotalScanTimeSec', '0.0')
        prefix = 'sSliceArray.asSlice[%d].' % slice_index
        image_parameters = (
         ('image_dimension_line', 'dPhaseFOV'),
         ('image_dimension_column', 'dReadoutFOV'),
         ('image_dimension_partition', 'dThickness'),
         ('image_position_sagittal', 'sPosition.dSag'),
         ('image_position_coronal', 'sPosition.dCor'),
         ('image_position_transverse', 'sPosition.dTra'))
        for key, name in image_parameters:
            params[key] = float(prot_ser.get(prefix + name, '0.0'))

        image_orientation = ptag_img.get('ImageOrientationPatient', '')
        if not image_orientation:
            slice_orientation_pitch = ''
            slice_distance = ''
        else:
            if is_svs:
                image_orientation = image_orientation[3:] + image_orientation[:3]
            f = lambda value: 0.0 if abs(value) < 0.0001 else value
            image_orientation = [ f(float(value)) for value in image_orientation ]
            row = image_orientation[:3]
            column = image_orientation[3:6]
            normal = (row[1] * column[2] - row[2] * column[1],
             row[2] * column[0] - row[0] * column[2],
             row[0] * column[1] - row[1] * column[0])
            params['image_normal_sagittal'] = normal[0]
            params['image_normal_coronal'] = normal[1]
            params['image_normal_transverse'] = normal[2]
            params['image_column_sagittal'] = column[0]
            params['image_column_coronal'] = column[0]
            params['image_column_transverse'] = column[0]
            slice_orientation_pitch, _ = _dicom_orientation_string(normal)
            keys = ('image_position_sagittal', 'image_position_coronal', 'image_position_transverse')
            a = [ params[key] for key in keys ]
            b = normal
            bb = math.sqrt(sum([ value ** 2 for value in normal ]))
            slice_distance = (a[0] * b[0] + a[1] * b[1] + a[2] * b[2]) / bb
        params['slice_orientation_pitch'] = slice_orientation_pitch
        params['slice_distance'] = slice_distance
        regions = (
         ('region_dimension_line', 'dPhaseFOV'),
         ('region_dimension_column', 'dReadoutFOV'),
         ('region_dimension_partition', 'dThickness'),
         ('region_position_sagittal', 'sPosition.dSag'),
         ('region_position_coronal', 'sPosition.dCor'),
         ('region_position_transverse', 'sPosition.dTra'))
        for key, name in regions:
            name = 'sSpecPara.sVoI.' + name
            params[key] = float(prot_ser.get(name, 0))

    params['measure_size_spectral'] = long(prot_ser.get('sSpecPara.lVectorSize', 0))
    params['slice_thickness'] = _float(ptag_img.get('SliceThickness', 0))
    params['current_slice'] = '1'
    params['number_echoes'] = '1'
    params['number_slices'] = '1'
    params['data_size_spectral'] = params['measure_size_spectral']
    if not is_epsi:
        echo_time = 0.0
        if is_jpress:
            keys = prot_ser.keys()
            for key in keys:
                if key.upper() == 'ECHOTIME':
                    echo_time = float(prot_ser[key])

        if is_svslip2:
            keys = ptag_img.keys()
            for key in keys:
                if key.upper() == 'ECHOTIME':
                    echo_time = float(ptag_img[key])

        if not echo_time:
            echo_time = float(prot_ser.get('alTE[0]', 0.0))
            echo_time /= 1000
        params['echo_time'] = echo_time
        params['data_size_line'] = int(prot_ser.get('sSpecPara.lFinalMatrixSizePhase', 1))
        params['data_size_column'] = int(prot_ser.get('sSpecPara.lFinalMatrixSizeRead', 1))
        params['data_size_partition'] = int(prot_ser.get('sSpecPara.lFinalMatrixSizeSlice', 1))
        if is_svs:
            params['image_dimension_line'] = params['region_dimension_line']
            params['image_dimension_column'] = params['region_dimension_column']
            params['image_dimension_partition'] = params['region_dimension_partition']
            params['measure_size_line'] = 1
            params['measure_size_column'] = 1
            params['measure_size_partition'] = 1
        else:
            measure_size_line = int(prot_ser.get('sKSpace.lPhaseEncodingLines', 1))
            params['measure_size_line'] = str(measure_size_line)
            measure_size_column = int(prot_ser.get('sKSpace.lPhaseEncodingLines', 0))
            params['measure_size_column'] = str(measure_size_column)
            measure_size_partition = int(prot_ser.get('sKSpace.lPartitions', '0'))
            kspace_dimension = prot_ser.get('sKSpace.ucDimension', '')
            if kspace_dimension.strip() == '0x2':
                measure_size_partition = 1
                params['data_size_partition'] = 1
                data_size_partition = 1
            params['measure_size_partition'] = measure_size_partition
    if sequence_filename in ('svs_cp_press', 'svs_se_ir', 'svs_tavg'):
        s = prot_ser.get('SPREPPULSES.UCINVERSION', '')
        if s == '0x1':
            params['number_inversions'] = 1
        elif s == '0x2':
            params['number_inversions'] = 0
    if sequence_filename in ('svs_se', 'svs_st', 'fid', 'fid3', 'fid_var', 'csi_se',
                             'csi_st', 'csi_fid', 'csi_fidvar', 'epsi'):
        params['region_dimension_line'] = params['image_dimension_line']
        params['region_dimension_column'] = params['image_dimension_column']
        params['ft_scale_factor'] = '1.0'
        params['data_size_line'] = int(prot_ser.get('sKSpace.lPhaseEncodingLines', 0))
        params['data_size_column'] = int(prot_ser.get('sKSpace.lBaseResolution', 0)) * readout_os
        params['data_size_partition'] = int(prot_ser.get('sKSpace.lPartitions', 0))
        params['measure_size_line'] = params['data_size_line']
        measure_size_column = params['data_size_column']
        measure_size_partition = params['data_size_partition']
        index = 0 if int(dataset.get('InstanceNumber', 0)) % 2 == 1 else 1
        echo_time = float(prot_ser.get('alTE[%d]' % index, 0)) / 1000
        repetition_time_1 = float(prot_ser.get('alTR[%d]' % index, 0)) / 1000
        params['echo_time'] = str(echo_time)
        params['repetition_time_1'] = str(repetition_time_1)
        dwelltime = float(ptag_img.get('RealDwellTime', 0.0))
        if dwelltime and base_resolution:
            sweep_width = 1 / (dwelltime * base_resolution * readout_os)
        else:
            sweep_width = ''
        params['sweep_width'] = sweep_width
    ip_rot = prot_ser.get('sSliceArray.asSlice[0].dInPlaneRot', None)
    pol_swap = prot_ser.get('sWipMemBlock.alFree[40]', None)
    if ip_rot:
        try:
            ip_rot = float(ip_rot)
            params['in_plane_rotation'] = ip_rot
        except Exception as e:
            pass

    if pol_swap:
        try:
            pol_swap = int(pol_swap)
            params['polarity_swap'] = pol_swap
        except Exception as e:
            raise e

    return params


def _my_assert(expression):
    assert ASSERTIONS_ENABLED and expression


def _dicom_orientation_string(normal):
    """Given a 3-item list (or other iterable) that represents a normal vector
    to the "imaging" plane, this function determines the orientation of the
    vector in 3-dimensional space. It returns a tuple of (angle, orientation)
    in which angle is e.g. "Tra" or "Tra>Cor -6" or "Tra>Sag 14.1 >Cor 9.3"
    and orientation is e.g. "Sag" or "Cor-Tra".

    For double angulation, errors in secondary angle occur that may be due to
    rounding errors in internal Siemens software, which calculates row and
    column vectors.
    """
    TOLERANCE = 0.0001
    orientations = ('Sag', 'Cor', 'Tra')
    final_angle = ''
    final_orientation = ''
    sorted_normal = sorted(normal)
    for i, value in enumerate(normal):
        if value == sorted_normal[2]:
            principal = i
        if value == sorted_normal[1]:
            secondary = i
        if value == sorted_normal[0]:
            ternary = i

    angle_1 = math.atan2(normal[secondary], normal[principal]) * constants.RADIANS_TO_DEGREES
    new_normal_ip = math.sqrt(normal[principal] ** 2 + normal[secondary] ** 2)
    angle_2 = math.atan2(normal[ternary], new_normal_ip) * constants.RADIANS_TO_DEGREES
    if not principal:
        if abs(angle_1) > 0:
            sign1 = angle_1 / abs(angle_1)
        else:
            sign1 = 1.0
        angle_1 -= sign1 * 180.0
        angle_2 *= -1
    if abs(angle_2) < TOLERANCE or abs(abs(angle_2) - 180) < TOLERANCE:
        if abs(angle_1) < TOLERANCE or abs(abs(angle_1) - 180) < TOLERANCE:
            final_angle = orientations[principal]
            final_orientation = ang
        else:
            final_angle = '%s>%s %.3f' % (
             orientations[principal], orientations[secondary],
             -1 * angle_1)
            final_orientation = orientations[principal] + '-' + orientations[secondary]
    else:
        final_angle = '%s>%s %.3f >%s %f' % (
         orientations[principal], orientations[secondary],
         -1 * angle_1, orientations[ternary], -1 * angle_2)
        final_orientation = '%s-%s-%s' % (
         orientations[principal], orientations[secondary],
         orientations[ternary])
    return (final_angle, final_orientation)


def _float(value):
    """Attempts to return value as a float. No different from Python's 
    built-in float(), except that it accepts None and "" (for which it 
    returns 0.0).
    """
    if value:
        return float(value)
    return 0.0


def _extract_from_quotes(s):
    """Given a string, returns the portion between the first and last
    double quote (ASCII 34). If there aren't at least two quote characters,
    the original string is returned."""
    start = s.find('"')
    end = s.rfind('"')
    if start != -1 and end != -1:
        s = s[start + 1:end]
    return s


def _null_truncate(s):
    """Given a string, returns a version truncated at the first '\x00' if
    there is one. If not, the original string is returned."""
    i = s.find(chr(0))
    if i != -1:
        s = s[:i]
    return s


def _scrub(item):
    """Given a string, returns a version truncated at the first '\x00' and
    stripped of leading/trailing whitespace. If the param is not a string,
    it is returned unchanged."""
    if isinstance(item, basestring):
        return _null_truncate(item).strip()
    else:
        return item


def _get_chunks(tag, index, format, little_endian=True):
    """Given a CSA tag string, an index into that string, and a format
    specifier compatible with Python's struct module, returns a tuple
    of (size, chunks) where size is the number of bytes read and
    chunks are the data items returned by struct.unpack(). Strings in the
    list of chunks have been run through _scrub().
    """
    format = ('<' if little_endian else '>') + format
    size = struct.calcsize(format)
    chunks = struct.unpack(format, tag[index:index + size])
    chunks = [ _scrub(item) for item in chunks ]
    return (
     size, chunks)


def _parse_protocol_data(protocol_data):
    """Returns a dictionary containing the name/value pairs inside the
    "ASCCONV" section of the MrProtocol or MrPhoenixProtocol elements
    of a Siemens CSA Header tag.
    """
    start = protocol_data.find('### ASCCONV BEGIN ###')
    end = protocol_data.find('### ASCCONV END ###')
    _my_assert(start != -1)
    _my_assert(end != -1)
    start += len('### ASCCONV BEGIN ###')
    protocol_data = protocol_data[start:end]
    lines = protocol_data.split('\n')
    f = lambda pair: (
     pair[0].strip(), pair[1].strip())
    lines = [ f(line.split('=')) for line in lines if '=' in line ]
    return dict(lines)


def _get(dataset, tag, default=None):
    """Returns the value of a dataset tag, or the default if the tag isn't
    in the dataset.
    PyDicom datasets already have a .get() method, but it returns a
    dicom.DataElement object. In practice it's awkward to call dataset.get()
    and then figure out if the result is the default or a DataElement,
    and if it is the latter _get the .value attribute. This function allows
    me to avoid all that mess.
    It is also a workaround for this bug (which I submitted) which should be
    fixed in PyDicom > 0.9.3:
    http://code.google.com/p/pydicom/issues/detail?id=72
    """
    if tag not in dataset:
        return default
    return dataset[tag].value


def _parse_csa_header(tag, little_endian=True):
    """The CSA header is a Siemens private tag that should be passed as
    a string. Any of the following tags should work: (0x0029, 0x1010),
    (0x0029, 0x1210), (0x0029, 0x1110), (0x0029, 0x1020), (0x0029, 0x1220),
    (0x0029, 0x1120).

    The function returns a dictionary keyed by element name.
    """
    DELIMITERS = ('M', b'\xcd', 77, 205)
    elements = {}
    current = 0
    size, chunks = _get_chunks(tag, current, '4s4s')
    current += size
    _my_assert(chunks[0] == 'SV10')
    _my_assert(chunks[1] == '\x04\x03\x02\x01')
    size, chunks = _get_chunks(tag, current, 'L')
    current += size
    element_count = chunks[0]
    size, chunks = _get_chunks(tag, current, '4s')
    current += size
    _my_assert(chunks[0] in DELIMITERS)
    for i in range(element_count):
        size, chunks = _get_chunks(tag, current, '64s4s4s4sL4s')
        current += size
        name, vm, vr, syngo_dt, subelement_count, delimiter = chunks
        _my_assert(delimiter in DELIMITERS)
        values = []
        for j in range(subelement_count):
            size, chunks = _get_chunks(tag, current, '4L')
            current += size
            _my_assert(chunks[0] == chunks[1])
            _my_assert(chunks[1] == chunks[3])
            _my_assert(chunks[2] in DELIMITERS)
            length = chunks[0]
            size, chunks = _get_chunks(tag, current, '%ds' % length)
            current += size
            if chunks[0]:
                values.append(chunks[0])
            current += (4 - length % 4) % 4

        if len(values) == 0:
            values = ''
        if len(values) == 1:
            values = values[0]
        _my_assert(name not in elements)
        elements[name] = values

    return elements
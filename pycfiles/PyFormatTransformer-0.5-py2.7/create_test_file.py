# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/FormatTransformer/create_test_file.py
# Compiled at: 2015-11-15 19:21:34
import CifFile

def prepare_block(in_block):
    """Make sure all necessary elements are present in block"""
    dnames = [
     [
      '_diffrn_scan_frame.scan_id',
      '_diffrn_scan_frame.frame_id',
      '_diffrn_scan_frame.frame_number',
      '_diffrn_scan_frame.integration_time'],
     [
      '_diffrn_data_frame.id',
      '_diffrn_data_frame.detector_element_id',
      '_diffrn_data_frame.detector_id',
      '_diffrn_data_frame.array_id',
      '_diffrn_data_frame.binary_id',
      '_diffrn_data_frame.details'],
     [
      '_array_intensities.array_id',
      '_array_intensities.binary_id',
      '_array_intensities.linearity',
      '_array_intensities.gain',
      '_array_intensities.overload',
      '_array_intensities.undefined_value',
      '_array_intensities.pixel_slow_bin_size',
      '_array_intensities.pixel_fast_bin_size'],
     [
      '_array_data.binary_id', '_array_data.array_id', '_array_data.data'],
     [
      '_diffrn_radiation.wavelength_id',
      '_diffrn_radiation.diffrn_id',
      '_diffrn_radiation_wavelength.wavelength',
      '_diffrn_radiation_wavelength.wt'],
     [
      '_diffrn_scan.id',
      '_diffrn_scan.frame_id_start',
      '_diffrn_scan.frame_id_end',
      '_diffrn_scan.frames'],
     [
      '_diffrn_measurement.diffrn_id',
      '_diffrn_measurement.id',
      '_diffrn_measurement.method',
      '_diffrn_measurement.number_of_axes',
      '_diffrn_measurement.sample_detector_distance'],
     [
      '_diffrn_detector.id',
      '_diffrn_detector.diffrn_id',
      '_diffrn_detector.type',
      '_diffrn_detector.details',
      '_diffrn_detector.number_of_axes',
      '_diffrn_detector.layer_thickness'],
     [
      '_diffrn_detector_element.id',
      '_diffrn_detector_element.detector_id']]
    in_block.overwrite = True
    for loopnames in dnames:
        for d in loopnames:
            in_block[d] = [
             in_block[d]]

        in_block.CreateLoop(loopnames)

    for one_name in ['_axis.vector', '_axis.offset']:
        for direction in ['[1]', '[2]', '[3]']:
            full_name = one_name + direction
            for index in range(len(in_block[full_name])):
                if in_block[full_name][index] == '.':
                    in_block[full_name][index] = '0'

    in_block.overwrite = False


def add_image(out_block, in_block):
    """Merge image from [[in_block]] into [[out_block]], changing identifiers as
    necessary"""
    from copy import copy
    out_block.overwrite = True
    out_block['_array_data.data'].append(in_block['_array_data.data'])
    array_id = out_block['_array_data.array_id']
    array_id.append(array_id[0])
    binary_id = '%d' % (len(out_block['_array_data.binary_id']) + 1)
    out_block['_array_data.binary_id'].append(binary_id)
    int_loop = out_block.GetLoop('_array_intensities.array_id')
    new_packet = copy(int_loop.GetPacket(0))
    setattr(new_packet, '_array_intensities.binary_id', binary_id)
    int_loop.AddPacket(new_packet)
    new_frame_id = 'Frame' + binary_id
    frame_loop = out_block.GetLoop('_diffrn_data_frame.id')
    f_pack = frame_loop.GetPacket(0)
    new_packet = copy(f_pack)
    setattr(new_packet, '_diffrn_data_frame.binary_id', binary_id)
    setattr(new_packet, '_diffrn_data_frame.id', new_frame_id)
    frame_loop.AddPacket(new_packet)
    out_block['_diffrn_scan.frame_id_end'] = [
     new_frame_id]
    out_block['_diffrn_scan.frames'] = [len(out_block['_array_data.array_id'])]
    frame_number = len(out_block['_diffrn_scan_frame.frame_number']) + 1
    fnloop = out_block.GetLoop('_diffrn_scan_frame.frame_number')
    new_pack = copy(fnloop.GetPacket(0))
    setattr(new_pack, '_diffrn_scan_frame.frame_number', frame_number)
    setattr(new_pack, '_diffrn_scan_frame.frame_id', new_frame_id)
    fnloop.AddPacket(new_pack)
    axis_loop = in_block.GetLoop('_diffrn_scan_frame_axis.axis_id')
    new_axis_loop = out_block.GetLoop('_diffrn_scan_frame_axis.axis_id')
    for one_pack in axis_loop:
        setattr(one_pack, '_diffrn_scan_frame_axis.frame_id', new_frame_id)
        new_axis_loop.AddPacket(one_pack)

    out_block.overwrite = False


def process(template, start, finish):
    """Process a set of files"""
    import time
    print 'Processing from %s to %s' % (template % start, template % finish)
    out_name = template % 0 + '.merged'
    full_name = template % start
    start_time = time.time()
    print 'Reading in first file at ' + time.ctime()
    out_block = CifFile.CifFile(full_name).first_block()
    prepare_block(out_block)
    for file_no in range(start + 1, finish + 1):
        full_name = template % file_no
        print 'Reading in file %d' % file_no
        next_block = CifFile.CifFile(full_name).first_block()
        add_image(out_block, next_block)

    out_file = open(out_name, 'w')
    print 'Finished in %d seconds' % (time.time() - start_time)
    print 'Writing out %s' % out_name
    out_cif = CifFile.CifFile()
    out_cif['Merged_scans'] = out_block
    out_file.write(str(out_cif))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print 'Usage: create_test_file template start_no finish_no'
        exit
    infile = sys.argv[1]
    start_no = int(sys.argv[2])
    finish_no = int(sys.argv[3])
    process(infile, start_no, finish_no)
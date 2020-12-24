# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/io/io.py
# Compiled at: 2020-03-12 11:17:48
# Size of source mod 2**32: 13307 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/12/2019'
import logging
from datetime import datetime
import h5py, numpy
from silx.io import utils
from silx.io.dictdump import dicttoh5
from silx.io.url import DataUrl
from silx.utils.enum import Enum
try:
    import est.io.utils.pymca as pymca_read_spectrum
except ImportError:
    has_pymca = False
else:
    has_pymca = True
try:
    import est.io.utils.larch as larch_read_ascii
except ImportError:
    has_larch = False
else:
    has_larch = True
_logger = logging.getLogger(__name__)

class InputType(Enum):
    dat_spectrum = '*.dat'
    hdf5_spectra = '*.h5'
    xmu_spectrum = '*.xmu'


def read_xas(spectra_url, channel_url, config_url=None):
    """
    Read the given spectra url and the config url if any
    
    :param Union[DataUrl, str] spectra_url: 
    :param DataUrl config_url: 
    :return: spectra, energy, configuration
    """

    def get_url(original_url, name):
        url_ = original_url
        if type(url_) is str:
            try:
                url_ = DataUrl(path=url_)
            except:
                url_ = DataUrl(file_path=url_, scheme='PyMca')

        if not isinstance(url_, DataUrl):
            raise TypeError('given input for, ', name, 'is invalid')
        return url_

    _spectra_url = get_url(original_url=spectra_url, name='spectra')
    _energy_url = get_url(original_url=channel_url, name='energy')
    _config_url = config_url
    if type(_config_url) is str:
        if _config_url == '':
            _config_url = None
    if not _config_url is None:
        if not isinstance(_config_url, DataUrl):
            raise TypeError('given input for configuration is invalid')

    def load_data(data_url, name):
        if data_url is None:
            return
        if data_url.scheme() in ('PyMca', 'PyMca5'):
            if has_pymca is False:
                _logger.warning('Requires PyMca to load data from %s' % data_url.path())
                return
            assert name in ('spectra', 'energy')
            energy, mu = pymca_read_spectrum(data_url.file_path())
            if name == 'spectra':
                return mu.reshape(mu.shape[0], 1, 1)
            return energy
        else:
            if data_url.scheme() in ('larch', 'xraylarch'):
                if has_larch is False:
                    _logger.warning('Requires larch to load data from %s' % data_url.path())
                    return
                assert name in ('spectra', 'energy')
                energy, mu = larch_read_ascii(xmu_file=(data_url.file_path()))
                if name == 'spectra':
                    return mu.reshape(mu.shape[0], 1, 1)
                return energy
            else:
                if data_url.is_valid():
                    try:
                        data = utils.get_data(data_url)
                    except ValueError as e:
                        try:
                            _logger.error(e)
                        finally:
                            e = None
                            del e

                    else:
                        if name == 'spectra':
                            if data.ndim == 1:
                                return data.reshape(data.shape[0], 1, 1)
                        return data
                        return
                _logger.warning('invalid url for', name, ',  will not load it')

    spectra = load_data(_spectra_url, name='spectra')
    energy = load_data(_energy_url, name='energy')
    configuration = load_data(_config_url, name='configuration')
    return (
     spectra, energy, configuration)


def write_xas_proc(h5_file, entry, process, data, processing_order, data_path='/', overwrite=True):
    """
    Write a xas :class:`.Process` into .h5

    :param str h5_file: path to the hdf5 file
    :param str entry: entry name
    :param process: process executed
    :type: :class:`.Process`
    :param data: process result data
    :type: numpy.ndarray
    :param processing_order: processing order of treatment
    :type: int
    :param data_path: path to store the data
    :type: str
    """
    process_name = 'xas_process_' + str(processing_order)
    with h5py.File(h5_file, 'w') as (h5f):
        nx_entry = h5f.require_group('/'.join((data_path, entry)))
        nx_entry.attrs['NX_class'] = 'NXentry'
        nx_process = nx_entry.require_group(process_name)
        nx_process.attrs['NX_class'] = 'NXprocess'
        if overwrite:
            for key in ('program', 'version', 'date', 'processing_order', 'class_instance'):
                if key in nx_process:
                    del nx_process[key]

        else:
            nx_process['program'] = process.program_name()
            nx_process['version'] = process.program_version()
            nx_process['date'] = datetime.now().replace(microsecond=0).isoformat()
            nx_process['processing_order'] = numpy.int32(processing_order)
            _class = process.__class__
            nx_process['class_instance'] = '.'.join((_class.__module__,
             _class.__name__))
            nx_data = nx_entry.require_group('data')
            nx_data.attrs['NX_class'] = 'NXdata'
            nx_data.attrs['signal'] = 'data'

            def get_interpretation(mydata):
                if isinstance(mydata, numpy.ndarray):
                    if mydata.ndim is 1:
                        return 'spectrum'
                    if mydata.ndim in (2, 3):
                        return 'image'

            if isinstance(data, numpy.ndarray):
                data_ = {'data': data}
            else:
                data_ = data
        for key, value in data_.items():
            nx_process[key] = value
            interpretation = get_interpretation(value)
            if interpretation:
                nx_process[key].attrs['interpretation'] = interpretation

        nx_process_path = str(nx_process.name)
    if process.getConfiguration() is not None:
        dicttoh5((process.getConfiguration()), h5file=h5_file,
          h5path=('/'.join((nx_process_path, 'configuration'))),
          overwrite_data=True,
          mode='a')


def write_xas(h5_file, entry, energy, mu, sample=None, start_time=None, data_path='/', title=None, definition=None, overwrite=True):
    """
    Write raw date in nexus format

    :param str h5_file: path to the hdf5 file
    :param str entry: entry name
    :param sample: definition of the sample
    :type: :class:`.Sample`
    :param energy: beam energy (1D)
    :type: numpy.ndarray
    :param mu: beam absorption (2D)
    :type: numpy.ndarray
    :param start_time:
    :param str data_path:
    :param str title: experiment title
    :param str definition: experiment definition
    """
    with h5py.File(h5_file, 'w') as (h5f):
        nx_entry = h5f.require_group('/'.join((data_path, entry)))
        nx_entry.attrs['NX_class'] = 'NXentry'
        nx_monochromator = nx_entry.require_group('monochromator')
        nx_monochromator.attrs['NX_class'] = 'NXmonochromator'
        if overwrite:
            if 'energy' in nx_monochromator:
                del nx_monochromator['energy']
        nx_monochromator['energy'] = energy
        nx_monochromator['energy'].attrs['interpretation'] = 'spectrum'
        nx_monochromator['energy'].attrs['NX_class'] = 'NXdata'
        nx_absorbed_beam = nx_entry.require_group('absorbed_beam')
        nx_absorbed_beam.attrs['NX_class'] = 'NXdetector'
        if overwrite:
            if 'data' in nx_absorbed_beam:
                del nx_absorbed_beam['data']
        nx_absorbed_beam['data'] = mu
        nx_absorbed_beam['data'].attrs['interpretation'] = 'image'
        nx_absorbed_beam['data'].attrs['NX_class'] = 'NXdata'
        if sample:
            nx_sample = nx_entry.require_group('sample')
            nx_sample.attrs['NX_class'] = 'NXsample'
            if overwrite:
                if 'name' in nx_sample:
                    del nx_sample['name']
            nx_sample['name'] = sample.name
        nx_data = nx_entry.require_group('data')
        nx_data.attrs['NX_class'] = 'NXdata'
        if overwrite:
            if 'energy' in nx_data:
                del nx_data['energy']
        nx_data['energy'] = h5py.SoftLink(nx_monochromator['energy'].name)
        if overwrite:
            if 'absorbed_beam' in nx_data:
                del nx_data['absorbed_beam']
        nx_data['absorbed_beam'] = h5py.SoftLink(nx_absorbed_beam['data'].name)
        if start_time is not None:
            if overwrite:
                if 'start_time' in nx_entry:
                    del nx_entry['start_time']
            nx_entry['start_time'] = start_time
        if title is not None:
            if overwrite:
                if 'title' in nx_entry:
                    del nx_entry['title']
            nx_entry['title'] = title
        if definition is not None:
            if overwrite:
                if 'definition' in nx_entry:
                    del nx_entry['definition']
            nx_entry['definition'] = definition


def get_xasproc(h5_file, entry):
    """
    Return the list of all NXxasproc existing at the data_path level
    
    :param str h5_file: hdf5 file
    :param str entry: data location
     
    :return: 
    :rtype: list
    """

    def copy_nx_xas_process(h5_group):
        res = {}
        res['_h5py_path'] = h5_group.name
        relevant_keys = ('program', 'version', 'data', 'parameters', 'processing_order',
                         'configuration', 'class_instance')
        from silx.io.dictdump import h5todict
        for key in h5_group.keys():
            if key in relevant_keys:
                if key == 'configuration':
                    config_path = '/'.join((h5_group.name, 'configuration'))
                    res[key] = h5todict(h5_file, config_path)
                else:
                    res[key] = h5_group[key][...]

        return res

    res = []
    with h5py.File(h5_file, 'w') as (h5f):
        try:
            root_group = h5f[entry]
        except KeyError:
            _logger.warning(entry + ' does not exist in ' + h5_file)
        else:
            for key in root_group.keys():
                elmt = root_group[key]
                if hasattr(elmt, 'attrs') and 'NX_class' in elmt.attrs and elmt.attrs['NX_class'] == 'NXprocess':
                    nx_xas_proc = copy_nx_xas_process(elmt)
                    if len(nx_xas_proc) == 0:
                        _logger.warning('one xas process was not readable from the hdf5 file at:' + key)
                    else:
                        res.append(nx_xas_proc)

    return res


if __name__ == '__main__':
    import os
    from est.core.process.pymca.normalization import PyMca_normalization
    from est.core.process.pymca.exafs import PyMca_exafs
    from est.core.types import Sample
    h5_file = 'test_xas_123.h5'
    if os.path.exists(h5_file):
        os.remove(h5_file)
    sample = Sample(name='mysample')
    data = numpy.random.rand(51200)
    data = data.reshape((256, 20, 10))
    process_data = numpy.random.rand(51200).reshape((256, 20, 10))
    energy = numpy.linspace(start=3.25, stop=3.69, num=256)
    write_xas(h5_file=h5_file, entry='scan1', sample=sample, energy=energy, mu=data)
    process_norm = PyMca_normalization()
    write_xas_proc(h5_file=h5_file, entry='scan1', process=process_norm, data=process_data,
      processing_order=1)
    process_exafs = PyMca_exafs()
    process_data2 = numpy.random.rand(51200).reshape((256, 20, 10))
    write_xas_proc(h5_file=h5_file, entry='scan1', process=process_exafs, data=process_data2,
      processing_order=2)
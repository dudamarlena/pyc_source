# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/brk_brml_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 13113 bytes
import os, types
from zipfile import ZipFile
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import not_none
from ..base_parser import BaseParser
from ..xml_parser_mixin import XMLParserMixin
from .xrd_parser_mixin import XRDParserMixin
from .namespace import xrd_parsers

@xrd_parsers.register_parser()
class BrkBRMLParser(XRDParserMixin, XMLParserMixin, BaseParser):
    __doc__ = '\n        Bruker *.BRML format parser\n    '
    description = 'Bruker BRML files *.BRML'
    extensions = get_case_insensitive_glob('*.BRML')
    mimetypes = ['application/zip']
    __file_mode__ = 'r'

    @classmethod
    def _get_file(cls, fp, close=None):
        """
            Returns a three-tuple:
            filename, zipfile-object, close
        """
        if isinstance(fp, str):
            return (fp, ZipFile(fp, cls.__file_mode__), True if close is None else close)
        else:
            return (
             getattr(fp, 'name', None), ZipFile(fp, cls.__file_mode__), False if close is None else close)

    @classmethod
    def _get_raw_data_files(cls, f, folder):
        """
            Processes DataContainer.xml and returns a list of xml raw data
            filepaths and the sample name
        """
        contf = f.open('%s/DataContainer.xml' % folder, cls.__file_mode__)
        data = contf.read()
        contf.close()
        _, root = cls.get_xml_for_string(data)
        sample_name = root.find('./MeasurementInfo').get('SampleName')
        raw_data_files = []
        for child in root.find('./RawDataReferenceList'):
            raw_data_files.append(child.text)

        return (raw_data_files, sample_name)

    @classmethod
    def _get_header_dict(cls, f, folder):
        header_d = {}
        contf = f.open('%s/MeasurementContainer.xml' % folder, cls.__file_mode__)
        data = contf.read()
        contf.close()
        _, root = cls.get_xml_for_string(data)
        radius_path = "./HardwareLogicExt/Instrument/BeamPathContainers/BeamPathContainerAbc[@VisibleName='PrimaryTrack']/%s"
        tube_path = "./HardwareLogicExt/Instrument/BeamPathContainers/BeamPathContainerAbc[@VisibleName='PrimaryTrack']/BankPositions/BankPosition/MountedComponent/MountedTube/%s"
        soller1_path = "./HardwareLogicExt/Instrument/BeamPathContainers/BeamPathContainerAbc[@VisibleName='PrimaryTrack']/BankPositions/BankPosition/MountedComponent[@VisibleName='SollerMount']/%s"
        soller2_path = "./HardwareLogicExt/Instrument/BeamPathContainers/BeamPathContainerAbc[@VisibleName='SecondaryTrack']/BankPositions/BankPosition/MountedComponent[@VisibleName='SollerMount']/%s"
        divergence_path = "./HardwareLogicExt/Instrument/BeamPathContainers/BeamPathContainerAbc[@VisibleName='PrimaryTrack']/BankPositions/BankPosition/MountedComponent/Restrictions[@FieldName='OpeningDegree']/%s"
        header_d.update(alpha1=(float(cls.get_val(root, tube_path % 'WaveLengthAlpha1', 'Value')) / 10),
          alpha2=(float(cls.get_val(root, tube_path % 'WaveLengthAlpha2', 'Value')) / 10),
          alpha_average=(float(cls.get_val(root, tube_path % 'WaveLengthAverage', 'Value')) / 10),
          beta=(float(cls.get_val(root, tube_path % 'WaveLengthBeta', 'Value')) / 10),
          alpha_factor=(cls.get_val(root, tube_path % 'WaveLengthRatio', 'Value')),
          target_type=(cls.get_val(root, tube_path % 'TubeMaterial', 'Value')),
          soller1=(cls.get_val(root, soller1_path % 'Deflection', 'Value')),
          soller2=(cls.get_val(root, soller2_path % 'Deflection', 'Value')),
          radius=(float(cls.get_val(root, radius_path % 'Radius', 'Value', 0)) / 10.0),
          divergence=(cls.get_val(root, divergence_path % 'Data', 'Value')))
        return header_d

    @classmethod
    def parse(cls, fp, data_objects=None, close=False):
        filename, fp, close = cls._get_file(fp, close=close)
        try:
            basename = os.path.basename(filename)
        except AttributeError:
            basename = None

        num_samples = 0
        zipinfos = fp.infolist()
        processed_folders = []
        data_objects = not_none(data_objects, [])
        for zipinfo in zipinfos:
            if zipinfo.filename.count('/') == 1 and 'DataContainer.xml' in zipinfo.filename:
                folder = os.path.dirname(zipinfo.filename)
                if folder not in processed_folders:
                    processed_folders.append(folder)
                    header_d = cls._get_header_dict(fp, folder)
                    raw_data_files, sample_name = cls._get_raw_data_files(fp, folder)
                    for raw_data_filename in raw_data_files:
                        contf = fp.open(raw_data_filename)
                        _, root = cls.get_xml_for_file(contf)
                        isScan = 'NonAmbientModeData' not in root.find('./DataRoutes/DataRoute/ScanInformation').get('ScanName')
                        if isScan:
                            for route in root.findall('./DataRoutes/DataRoute'):
                                data_objects = cls._adapt_data_object_list(data_objects,
                                  num_samples=(num_samples + 1),
                                  only_extend=True)
                                data_object = data_objects[num_samples]
                                datums = route.findall('Datum')
                                data = []
                                enabled_datum_index = None
                                twotheta_datum_index = None
                                intensity_datum_index = None
                                steptime_datum_index = None
                                relative_humidity_data, relative_humidity_index = (None,
                                                                                   None)
                                temperature_data, temperature_index = (None, None)
                                temperature_index = None
                                for dataview in route.findall('./DataViews/RawDataView'):
                                    index = int(dataview.get('Start', 0))
                                    name = dataview.get('LogicName') or 'Undefined'
                                    xsi_type = dataview.get('{http://www.w3.org/2001/XMLSchema-instance}type') or 'Undefined'
                                    if name == 'MeasuredTime':
                                        steptime_datum_index = index
                                    else:
                                        if name == 'AbsorptionFactor':
                                            enabled_datum_index = index
                                        else:
                                            if name == 'Undefined':
                                                if xsi_type == 'VaryingRawDataView':
                                                    for i, definition in enumerate(dataview.findall('./Varying/FieldDefinitions')):
                                                        if definition.get('TwoTheta'):
                                                            index += i
                                                            break

                                                    twotheta_datum_index = index
                                    if name == 'Undefined':
                                        if xsi_type == 'RecordedRawDataView':
                                            logic_name = dataview.find('Recording').get('LogicName')
                                            if logic_name == 'ScanCounter':
                                                intensity_datum_index = index
                                            else:
                                                if logic_name == 'modeActualHum':
                                                    relative_humidity_index = index
                                                    relative_humidity_data = []
                                                elif logic_name == 'modeActualTemp':
                                                    temperature_index = index
                                                    temperature_data = []

                                twotheta_min = None
                                twotheta_max = None
                                twotheta_count = 0
                                for subscan in route.findall('./SubScans/SubScanInfo'):
                                    steps = int(subscan.get('MeasuredSteps'))
                                    start = int(subscan.get('StartStepNo'))
                                    steptime = float(subscan.get('PlannedTimePerStep'))
                                    for datum in datums[start:start + steps]:
                                        values = datum.text.split(',')
                                        if values[enabled_datum_index] == '1':
                                            datum_steptime = float(values[steptime_datum_index])
                                            intensity = float(values[intensity_datum_index])
                                            intensity /= float(steptime * datum_steptime)
                                            twotheta = float(values[twotheta_datum_index])
                                            if temperature_index is not None:
                                                temperature = float(values[temperature_index])
                                                temperature_data.append(temperature)
                                            if relative_humidity_index is not None:
                                                relative_humidity = float(values[relative_humidity_index])
                                                relative_humidity_data.append(relative_humidity)
                                            if twotheta_min is None:
                                                twotheta_min = twotheta
                                            else:
                                                twotheta_min = min(twotheta_min, twotheta)
                                            if twotheta_max is None:
                                                twotheta_max = twotheta
                                            else:
                                                twotheta_max = min(twotheta_max, twotheta)
                                            data.append([twotheta, intensity])
                                            twotheta_count += 1

                                (data_object.update)(filename=basename, 
                                 name=sample_name, 
                                 time_step=1, 
                                 twotheta_min=twotheta_min, 
                                 twotheta_max=twotheta_max, 
                                 twotheta_count=twotheta_count, **header_d)
                                data_object.data = data
                                data_object.temperature_data = temperature_data
                                data_object.relative_humidity_data = relative_humidity_data
                                num_samples += 1

                        contf.close()

        if close:
            fp.close()
        return data_objects
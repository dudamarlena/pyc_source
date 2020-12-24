# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/meta_file.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 7302 bytes
from pesummary.utils.utils import logger
from pesummary.core.file.meta_file import _MetaFile, recursively_save_dictionary_to_hdf5_file, DEFAULT_HDF5_KEYS as CORE_HDF5_KEYS
from pesummary.gw.inputs import GWPostProcessing
DEFAULT_HDF5_KEYS = CORE_HDF5_KEYS

class _GWMetaFile(_MetaFile):
    __doc__ = 'This class handles the creation of a meta file storing all information\n    from the analysis\n\n    Attributes\n    ----------\n    meta_file: str\n        name of the meta file storing all information\n    '

    def __init__(self, samples, labels, config, injection_data, file_versions, file_kwargs, calibration=None, psd=None, approximant=None, webdir=None, result_files=None, hdf5=False, existing_version=None, existing_label=None, existing_samples=None, existing_psd=None, existing_calibration=None, existing_approximant=None, existing_config=None, existing_injection=None, existing_metadata=None, priors={}, outdir=None, existing=None, existing_priors={}, existing_metafile=None, package_information={}, mcmc_samples=False):
        self.calibration = calibration
        self.psds = psd
        self.approximant = approximant
        self.existing_psd = existing_psd
        self.existing_calibration = existing_calibration
        self.existing_approximant = existing_approximant
        super(_GWMetaFile, self).__init__(samples,
          labels, config, injection_data, file_versions, file_kwargs,
          webdir=webdir, result_files=result_files, hdf5=hdf5, priors=priors,
          existing_version=existing_version,
          existing_label=existing_label,
          existing_samples=existing_samples,
          existing_injection=existing_injection,
          existing_metadata=existing_metadata,
          existing_config=existing_config,
          existing_priors=existing_priors,
          outdir=outdir,
          package_information=package_information,
          existing=existing,
          existing_metafile=existing_metafile,
          mcmc_samples=mcmc_samples)

    def _make_dictionary(self):
        super(_GWMetaFile, self)._make_dictionary()
        for num, label in enumerate(self.labels):
            cond = all(self.calibration[label] != j for j in [{}, None])
            if self.calibration != {}:
                if cond:
                    self.data[label]['calibration_envelope'] = {key:item for key, item in self.calibration[label].items() if item is not None if item is not None}
                else:
                    self.data[label]['calibration_envelope'] = {}
            elif self.psds != {} and all(self.psds[label] != j for j in [{}, None]):
                self.data[label]['psds'] = {key:item for key, item in self.psds[label].items() if item is not None if item is not None}
            else:
                self.data[label]['psds'] = {}
            if self.approximant is not None and self.approximant[label] is not None:
                self.data[label]['approximant'] = self.approximant[label]
            else:
                self.data[label]['approximant'] = {}

    @staticmethod
    def save_to_hdf5(data, labels, samples, meta_file, no_convert=False, mcmc_samples=False):
        """Save the metafile as a hdf5 file
        """
        _MetaFile.save_to_hdf5(data,
          labels, samples, meta_file, no_convert=no_convert, extra_keys=CORE_HDF5_KEYS,
          mcmc_samples=mcmc_samples)


class GWMetaFile(GWPostProcessing):
    __doc__ = 'This class handles the creation of a metafile storing all information\n    from the analysis\n    '

    def __init__(self, inputs):
        super(GWMetaFile, self).__init__(inputs)
        logger.info('Starting to generate the meta file')
        if self.add_to_existing:
            existing = self.existing
            existing_metafile = self.existing_metafile
            existing_samples = self.existing_samples
            existing_labels = self.existing_labels
            existing_psd = self.existing_psd
            existing_calibration = self.existing_calibration
            existing_config = self.existing_config
            existing_approximant = self.existing_approximant
            existing_injection = self.existing_injection_data
            existing_version = self.existing_file_version
            existing_metadata = self.existing_file_kwargs
            existing_priors = self.existing_priors
        else:
            existing_metafile = None
            existing_samples = None
            existing_labels = None
            existing_psd = None
            existing_calibration = None
            existing_config = None
            existing_approximant = None
            existing_injection = None
            existing_version = None
            existing_metadata = None
            existing = None
            existing_priors = {}
        meta_file = _GWMetaFile((self.samples),
          (self.labels), (self.config), (self.injection_data), (self.file_version),
          (self.file_kwargs), calibration=(self.calibration), psd=(self.psd),
          hdf5=(self.hdf5),
          webdir=(self.webdir),
          result_files=(self.result_files),
          existing_version=existing_version,
          existing_label=existing_labels,
          existing_samples=existing_samples,
          existing_psd=existing_psd,
          existing_calibration=existing_calibration,
          existing_approximant=existing_approximant,
          existing_injection=existing_injection,
          existing_metadata=existing_metadata,
          existing_config=existing_config,
          priors=(self.priors),
          existing_priors=existing_priors,
          existing=existing,
          existing_metafile=existing_metafile,
          approximant=(self.approximant),
          package_information=(self.package_information),
          mcmc_samples=(self.mcmc_samples))
        meta_file.make_dictionary()
        if not self.hdf5:
            meta_file.save_to_json(meta_file.data, meta_file.meta_file)
        else:
            meta_file.save_to_hdf5((meta_file.data),
              (meta_file.labels), (meta_file.samples), (meta_file.meta_file),
              mcmc_samples=(meta_file.mcmc_samples))
        meta_file.save_to_dat()
        meta_file.write_marginalized_posterior_to_dat()
        logger.info('Finishing generating the meta file. The meta file can be viewed here: {}'.format(meta_file.meta_file))
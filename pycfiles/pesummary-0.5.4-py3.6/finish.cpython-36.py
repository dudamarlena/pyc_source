# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/finish.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 4038 bytes
import subprocess, os, time, numpy as np
from pesummary.core.finish import FinishingTouches
from pesummary.gw.inputs import PostProcessing
from pesummary.utils.utils import logger

class GWFinishingTouches(FinishingTouches):
    __doc__ = 'Class to handle the finishing touches\n\n    Parameters\n    ----------\n    ligo_skymap_PID: dict\n        dictionary containing the process ID for the ligo.skymap subprocess\n        for each analysis\n    '

    def __init__(self, inputs, ligo_skymap_PID=None):
        super(GWFinishingTouches, self).__init__(inputs)
        self.ligo_skymap_PID = ligo_skymap_PID
        self.generate_ligo_skymap_statistics()

    def generate_ligo_skymap_statistics(self):
        """Extract key statistics from the ligo.skymap fits file
        """
        FAILURE = False
        if self.ligo_skymap_PID is None:
            return
        samples_dir = os.path.join(self.webdir, 'samples')
        for label in self.labels:
            _path = os.path.join(samples_dir, '{}_skymap.fits'.format(label))
            while not os.path.isfile(_path):
                try:
                    output = subprocess.check_output([
                     'ps -p {}'.format(self.ligo_skymap_PID[label])],
                      shell=True)
                    cond1 = 'summarypages' not in str(output)
                    cond2 = 'defunct' in str(output)
                    if cond1 or cond2:
                        if not os.path.isfile(_path):
                            FAILURE = True
                        break
                except (subprocess.CalledProcessError, KeyError):
                    FAILURE = True
                    break

                time.sleep(60)

            if FAILURE:
                pass
            else:
                ess = subprocess.Popen(('ligo-skymap-stats {} -p 50 90 -o {}'.format(os.path.join(samples_dir, '{}_skymap.fits'.format(label)), os.path.join(samples_dir, '{}_skymap_stats.dat'.format(label)))),
                  shell=True)
                ess.wait()
                self.save_skymap_data_to_metafile(label, os.path.join(samples_dir, '{}_skymap_stats.dat'.format(label)))

    def save_skymap_data_to_metafile(self, label, filename):
        """Save the skymap data to the PESummary metafile

        Parameters
        ----------
        label: str
            the label of the analysis that the skymap statistics corresponds to
        filename: str
            name of the file that contains the skymap statistics for label
        """
        logger.info('Adding ligo.skymap statistics to the metafile')
        skymap_data = np.genfromtxt(filename, names=True, skip_header=True)
        keys = skymap_data.dtype.names
        command_line = 'summarymodify --webdir {} --samples {} --delimiter / --kwargs {} --overwrite'.format(self.webdir, os.path.join(self.webdir, 'samples', 'posterior_samples.h5'), ' '.join(['{}/{}:{}'.format(label, key, skymap_data[key]) for key in keys]))
        ess = subprocess.Popen(command_line, shell=True)
        ess.wait()
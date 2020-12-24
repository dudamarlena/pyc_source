# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marrabld/Projects/planarradpy/gui/gui_batch.py
# Compiled at: 2015-05-30 03:03:17
import os

class BatchFile:
    """
    This class creates the batch file which will be used by planarRad.
    The constructor receives data that the user typed and transmitted thanks to files, concerning the environment.
    """

    def __init__(self, batch_name, p_values, x_value, y_value, g_value, s_value, z_value, wavelength_values, verbose_value, phytoplankton_path, bottom_path, nb_cpu, executive_path, saa_values, sza_values, report_parameter_value):
        self.batch_name = batch_name
        self.p_values = p_values
        self.x_value = x_value
        self.y_value = y_value
        self.g_value = g_value
        self.s_value = s_value
        self.z_value = z_value
        self.wavelength_values = wavelength_values
        self.verbose_value = verbose_value
        self.phytoplankton_path = phytoplankton_path
        self.bottom_path = bottom_path
        self.nb_cpu = nb_cpu
        self.executive_path = executive_path
        self.report_parameter_value = report_parameter_value
        self.saa_values = saa_values
        self.sza_values = sza_values

    def write_batch_to_file(self, filename='batch_test_default.txt'):
        """
        This function creates a new file if he doesn't exist already, moves it to 'inputs/batch_file' folder
        and writes data and comments associated to them.
        Inputs: saa_values : <list> Sun Azimuth Angle (deg)
                sza_values : <list> Sun Zenith Angle (deg)
                batch_name : Name of the batch file.
                p_values : <list> Phytoplankton linear scaling factor
                x_value : <list> Scattering scaling factor
                y_value : <list> Scattering slope factor
                g_value : <list> CDOM absorption scaling factor
                s_value : <list> CDOM absorption slope factor
                s_value : <list> depth (m)
                waveL_values : Wavelength values used to test.
                verbose_value : Number concerning if the software explains a lot or not what it does.
                phytoplankton_path : The path to the file containing phytoplankton data.
                bottom_path : The path to the file containing bottom data.
                nb_cpu : The number of CPU we want to allowed to the software.
                executive_path : The path to the file where there is executive files using by PlanarRad.
                report_parameter :
        """
        self.batch_file = open(str(filename), 'w')
        self.batch_file.write('#----------------------------------------#\n# Name of the batch run\n#----------------------------------------#\nbatch_name = ')
        self.batch_file.write(str(self.batch_name))
        self.batch_file.write('\n\n#----------------------------------------#\n# Bio-optical parameters list\n#----------------------------------------#\nsaa_list = ')
        self.batch_file.write(str(self.saa_values))
        self.batch_file.write('\nsza_list = ')
        self.batch_file.write(str(self.sza_values))
        self.batch_file.write('\np_list = ')
        self.batch_file.write(str(self.p_values))
        self.batch_file.write('\nx_list = ')
        self.batch_file.write(str(self.x_value))
        self.batch_file.write('\ny_list = ')
        self.batch_file.write(str(self.y_value))
        self.batch_file.write('\ng_list = ')
        self.batch_file.write(str(self.g_value))
        self.batch_file.write('\ns_list = ')
        self.batch_file.write(str(self.s_value))
        self.batch_file.write('\nz_list = ')
        self.batch_file.write(str(self.z_value))
        self.batch_file.write('\n\n#----------------------------------------#\n# Wavelengths\n# All IOPs are interpolated to these \n# Wavelengths\n#----------------------------------------#\nwavelengths = ')
        self.batch_file.write(str(self.wavelength_values))
        self.batch_file.write('\n\n#----------------------------------------#\n# Number of CPUs\n# -1 means query the number of CPUs\n#----------------------------------------#\nnum_cpus = ')
        self.batch_file.write(str(self.nb_cpu))
        self.batch_file.write('\n\n#----------------------------------------#\n# Path of Planarrad\n#----------------------------------------#\nexec_path = ')
        self.batch_file.write(self.executive_path)
        self.batch_file.write('\n\n#----------------------------------------#\n# Logging level\n#----------------------------------------#\nverbose = ')
        self.batch_file.write(str(self.verbose_value))
        self.batch_file.write('\n\n#----------------------------------------#\n# File paths\n# Using absolute paths\n#----------------------------------------#\nphytoplankton_absorption_file =')
        self.batch_file.write(self.phytoplankton_path)
        self.batch_file.write('\nbottom_reflectance_file = ')
        self.batch_file.write(self.bottom_path)
        self.batch_file.write('\n\n#----------------------------------------#\n# Set the parameter to report\n#----------------------------------------#\nreport_parameter = ')
        self.batch_file.write(str(self.report_parameter_value))
        self.batch_file.write('\n\n')
        self.batch_file.close()
        src = './' + filename
        dst = './inputs/batch_files'
        os.system('mv ' + src + ' ' + dst)
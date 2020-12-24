# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\siglent_parser\siglent_parser\parser.py
# Compiled at: 2019-08-07 11:11:25
# Size of source mod 2**32: 13467 bytes
"""parser.py

Copyright 2019 Matt Trzcinski

This file is part of siglent_parser.

siglent_parser is free software: you can redistribute it and/or
modify- it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

siglent_parser is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with siglent_parser.  If not, see
<https://www.gnu.org/licenses/>.

"""
import numpy as np, warnings

class DataType:
    analog = 'analog'
    digital = 'digital'
    analog_digital = 'analog_digital'


TABLE2 = {0:1e-09, 
 1:2e-09, 
 2:5e-09, 
 3:1e-08, 
 4:2e-08, 
 5:5e-08, 
 6:1e-07, 
 7:2e-07, 
 8:5e-07, 
 9:1e-06, 
 10:2e-06, 
 11:5e-06, 
 12:1e-05, 
 13:2e-05, 
 14:5e-05, 
 15:0.0001, 
 16:0.0002, 
 17:0.0005, 
 18:0.001, 
 19:0.002, 
 20:0.005, 
 21:0.01, 
 22:0.02, 
 23:0.05, 
 24:0.1, 
 25:0.2, 
 26:0.5, 
 27:1, 
 28:2, 
 29:5, 
 30:10, 
 31:20, 
 32:50}
TABLE3 = {0:0.001, 
 1:0.002, 
 2:0.005, 
 3:0.01, 
 4:0.02, 
 5:0.05, 
 6:0.1, 
 7:0.2, 
 8:0.5, 
 9:1, 
 10:2, 
 11:5, 
 12:10}

class SiglentParser:
    __doc__ = 'Siglent SDS1000X/2000X Parser.'

    def __init__(self):
        super().__init__()
        self.file = None
        self.raw_bytes = None
        self.wave_length = None
        self.mso_wave_length = None
        self.mso_ch_open_num = None
        self.mso_ch_open_state = []
        self.ch1_volt_div_val = None
        self.ch2_volt_div_val = None
        self.ch3_volt_div_val = None
        self.ch4_volt_div_val = None
        self.ch1_vert_offset = None
        self.ch2_vert_offset = None
        self.ch3_vert_offset = None
        self.ch4_vert_offset = None
        self.ch1_volt_div = None
        self.ch2_volt_div = None
        self.ch3_volt_div = None
        self.ch4_volt_div = None
        self.ch1_on = None
        self.ch2_on = None
        self.ch3_on = None
        self.ch4_on = None
        self.time_div = None
        self.time_delay = None
        self.data = None
        self.sample_rate = None
        self.time = None
        self.analog = None
        self.digital = None

    def read_file(self, file):
        """Read in the raw binary data.

        Args:
            file (str/Path): Raw binary data output from Siglent unit

        Returns:
            bytes: Python bytes object of all the binary data

        """
        self.file = file
        with open(file, 'rb') as (f):
            self.raw_bytes = f.read()
        return self.raw_bytes

    def parse_file(self, byts):
        """Parse binary data.

        Args:
            byts (bytes): Binary data

        Returns:
            Nothing

        """
        self.ba_mso_wave_length = byts[4:8]
        self.ba_mso_ch_open_num = byts[16:20]
        self.ba_mso_ch_open_state = byts[20:36]
        self.ba_ch1_volt_div_val = byts[188:192]
        self.ba_ch2_volt_div_val = byts[192:196]
        self.ba_ch3_volt_div_val = byts[196:200]
        self.ba_ch4_volt_div_val = byts[200:204]
        self.ba_ch1_vert_offset = byts[220:224]
        self.ba_ch2_vert_offset = byts[224:228]
        self.ba_ch3_vert_offset = byts[228:232]
        self.ba_ch4_vert_offset = byts[232:236]
        self.ba_ch1_volt_div = byts[240:244]
        self.ba_ch2_volt_div = byts[244:248]
        self.ba_ch3_volt_div = byts[248:252]
        self.ba_ch4_volt_div = byts[252:256]
        self.ba_ch1_on = byts[256:260]
        self.ba_ch2_on = byts[260:264]
        self.ba_ch3_on = byts[264:268]
        self.ba_ch4_on = byts[268:272]
        self.ba_time_div = byts[584:588]
        self.ba_time_delay = byts[592:596]
        self.mso_wave_length = np.frombuffer((self.ba_mso_wave_length), dtype='<i4')[0]
        self.mso_ch_open_num = np.frombuffer((self.ba_mso_ch_open_num), dtype='<i4')[0]
        self.mso_ch_open_state = [np.uint8(b) for b in self.ba_mso_ch_open_state]
        self.ch1_volt_div_val = np.frombuffer((self.ba_ch1_volt_div_val), dtype='<f4')[0]
        self.ch2_volt_div_val = np.frombuffer((self.ba_ch2_volt_div_val), dtype='<f4')[0]
        self.ch3_volt_div_val = np.frombuffer((self.ba_ch3_volt_div_val), dtype='<f4')[0]
        self.ch4_volt_div_val = np.frombuffer((self.ba_ch4_volt_div_val), dtype='<f4')[0]
        self.ch1_vert_offset = np.frombuffer((self.ba_ch1_vert_offset), dtype='<i4')[0]
        self.ch2_vert_offset = np.frombuffer((self.ba_ch2_vert_offset), dtype='<i4')[0]
        self.ch3_vert_offset = np.frombuffer((self.ba_ch3_vert_offset), dtype='<i4')[0]
        self.ch4_vert_offset = np.frombuffer((self.ba_ch4_vert_offset), dtype='<i4')[0]
        self.ch1_volt_div = np.frombuffer((self.ba_ch1_volt_div), dtype='<i4')[0]
        self.ch2_volt_div = np.frombuffer((self.ba_ch2_volt_div), dtype='<i4')[0]
        self.ch3_volt_div = np.frombuffer((self.ba_ch3_volt_div), dtype='<i4')[0]
        self.ch4_volt_div = np.frombuffer((self.ba_ch4_volt_div), dtype='<i4')[0]
        self.ch1_on = np.frombuffer((self.ba_ch1_on), dtype='<i4')[0]
        self.ch2_on = np.frombuffer((self.ba_ch2_on), dtype='<i4')[0]
        self.ch3_on = np.frombuffer((self.ba_ch3_on), dtype='<i4')[0]
        self.ch4_on = np.frombuffer((self.ba_ch4_on), dtype='<i4')[0]
        self.time_div = np.frombuffer((self.ba_time_div), dtype='<i4')[0]
        self.time_delay = np.frombuffer((self.ba_time_delay), dtype='<i4')[0]
        self.data = np.frombuffer((byts[5232:]), dtype='<u1')
        self.real_ch1_volt_div_val = self.ch1_volt_div_val / (TABLE3[self.ch1_volt_div] * 1000000.0)
        self.real_ch1_vert_offset = self.calc_vertical_offset(self.ch1_vert_offset, self.real_ch1_volt_div_val)
        self.real_ch2_volt_div_val = self.ch2_volt_div_val / (TABLE3[self.ch2_volt_div] * 1000000.0)
        self.real_ch2_vert_offset = self.calc_vertical_offset(self.ch2_vert_offset, self.real_ch2_volt_div_val)
        self.real_ch3_volt_div_val = self.ch3_volt_div_val / (TABLE3[self.ch3_volt_div] * 1000000.0)
        self.real_ch3_vert_offset = self.calc_vertical_offset(self.ch3_vert_offset, self.real_ch3_volt_div_val)
        self.real_ch4_volt_div_val = self.ch4_volt_div_val / (TABLE3[self.ch4_volt_div] * 1000000.0)
        self.real_ch4_vert_offset = self.calc_vertical_offset(self.ch4_vert_offset, self.real_ch4_volt_div_val)
        self.data_type = self.get_data_type()
        try:
            if self.data_type == DataType.analog:
                self.wave_length = np.int32(len(self.data))
                self.sample_rate = self.wave_length / (14 * TABLE2[self.time_div])
                self.analog = self.calc_data_to_volt(self.data, self.real_ch1_volt_div_val, self.real_ch1_vert_offset)
                self.time = np.arange(len(self.analog)) / self.sample_rate
            else:
                warnings.warn('Parsing of digital data not currently implemented.')
        except:
            warnings.warn('Unable to identify data as analog or digital.')

    def calc_vertical_offset(self, ch_vert_offset, ch_volt_div_val, pixels_per_div=50):
        """Calculate the vertical offset.

        The comments state, "pixels_per_div = 50 # total display
        pixels in a vertical division, on SDS2000X is 50"

        """
        return (ch_vert_offset - 220) * (ch_volt_div_val / pixels_per_div)

    def calc_data_to_volt(self, data, ch_volt_div_val, ch_vert_offset, code_per_div=25):
        """Convert the data to voltage.

        The comments state, "code_per_div = 50 # total data code in a
        horizontal division, on SDS2000X is 25"

        """
        try:
            data = data.astype(np.float32)
        except:
            pass

        return (data - 128) * ch_volt_div_val / 1000 / code_per_div + ch_vert_offset

    def parse_binary(self, file):
        """Read in binary Siglent data and return well-formatted numpy array.

        Args:
            file (str/Path): Path to binary file

        Returns:
            numpy.array: Parsed data

        """
        byts = self.read_file(file)
        self.parse_file(byts)
        my_descr = [
         ('time', '<f8'), ('volts', '<f4')]
        my_df = np.empty(shape=(len(self.data)), dtype=my_descr)
        my_df['time'] = self.time
        my_df['volts'] = self.analog
        return my_df

    def get_data_type(self):
        """Return whether the data is analog-only, digital-only, or
        analog-digital.

        Returns:
            DataType (str): String describing data type

        """
        if self.mso_ch_open_num == 0:
            return DataType.analog
        else:
            if self.wave_length == self.mso_wave_length:
                return DataType.analog_digital
            return DataType.digital
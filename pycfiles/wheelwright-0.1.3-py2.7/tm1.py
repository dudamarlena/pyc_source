# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/wheelwright/tm1.py
# Compiled at: 2012-01-14 10:55:34
"""Park TM-1 tension meter data library and parameter fitting."""
__author__ = 'Kris Andersen'
__email__ = 'kris@biciworks.com'
__copyright__ = 'Copyright © 2012 Kris Andersen'
__license__ = 'GPLv3'
import numpy as np
spoke_codes = [
 'Steel Round 2.6 mm',
 'Steel Round 2.55 mm',
 'Steel Round 2.3 mm',
 'Steel Round 2.0 mm',
 'Steel Round 1.8 mm',
 'Steel Round 1.7 mm',
 'Steel Round 1.6 mm',
 'Steel Round 1.5 mm',
 'Steel Round 1.4 mm',
 'SPO Spinnergy Round 2.6 mm',
 'Titanium Round 2.0 mm',
 'Aluminum Round 3.3 mm',
 'Aluminum Round 2.8 mm',
 'Aluminum Round 2.54 mm',
 'Aluminum Round 2.28 mm',
 'Steel Blade 1.7 x 2.3 mm',
 'Steel Blade 1.5 x 2.4-2.6 mm',
 'Steel Blade 1.4 x 2.9 mm',
 'Steel Blade 1.4 x 2.6 mm',
 'Steel Blade 1.4 x 2.3 mm',
 'Steel Blade 1.3 x 2.7 mm',
 'Steel Blade 1.3 x 2.2-2.5 mm',
 'Steel Blade 1.3 x 2.1 mm',
 'Steel Blade 1.2 x 2.6 mm',
 'Steel Blade 1.2 x 1.9 mm',
 'Steel Blade 1.1 x 3.0-3.6 mm',
 'Steel Blade 1.1 x 1.9-2.0 mm',
 'Steel Blade 1.0 x 3.2 mm',
 'Steel Blade 1.0 x 2.5-2.7 mm',
 'Steel Blade 1.0 x 2.0-2.2 mm',
 'Steel Blade 0.9 x 3.6 mm',
 'Steel Blade 0.9 x 2.2 mm',
 'Steel Blade 0.8 x 2.0 mm',
 'Titanium Blade 1.4 x 2.6 mm',
 'Aluminum Blade 2.1 x 4.3 mm',
 'Aluminum Blade 1.8 x 5.3 mm',
 'Aluminum Blade 1.5 x 3.9 mm',
 'Mavic R2R Carbon Blade']

class TM1(object):
    """TM-1 instrument object."""

    def __init__(self, code):
        """
        Instrument constructor.

        :Parameters:
          - `code`: TM-1 spoke code index
        """
        self.code = code
        self.tm1_x, self.tm1_y = data_table(code)
        self.fit(order=4)

    def convert_to_kgf(self, x):
        """
        Convert TM-1 reading to tension [kgf].

        :Parameters:
          - `x`: TM-1 reading

        :Returns:
          Tension [kgf].
        """
        return np.polyval(self.p, x)

    def fit(self, order):
        """
        Polynomial fit of TM-1 tension data.

        :Parameters:
          - `order`: Polynomial order

        :Returns:
          Polynomial coefficients and relative error.
        """
        self.p = np.polyfit(self.tm1_x, self.tm1_y, order)
        self.err = np.abs(np.polyval(self.p, self.tm1_x) - self.tm1_y) / self.tm1_y

    def tm1_target(self, target, accuracy):
        """
        Determine valid range of TM-1 readings around tension target.

        :Parameters:
          - `target`: Target tension [kgf]
          - `accuracy`: Target accuracy [0.0, 1.0]

        :Returns:
          TM-1 target, minimum, and maximum readings.
        """

        def find_root(ro, roots):
            """Find root closet to ro."""
            R = []
            for r in roots:
                if abs(np.imag(r)) > 0.1:
                    continue
                R.append((abs(r - ro), r))

            return np.real(min(R)[1])

        ro = 0.5 * (max(self.tm1_x) + min(self.tm1_x))
        p0 = np.poly1d([target])
        t = find_root(ro, np.roots(np.polysub(self.p, p0)))
        tmin = find_root(ro, np.roots(np.polysub(self.p, p0 * (1.0 - accuracy))))
        tmax = find_root(ro, np.roots(np.polysub(self.p, p0 * (1.0 + accuracy))))
        return (
         t, tmin, tmax)

    def plot(self, axes, target, accuracy):
        """
        Plot TM-1 data and polynomial fit.

        :Parameters:
          - `axes`: Matplotlib axes
          - `target`: Target tension [kgf]
          - `accuracy`: Target accuracy [0.0, 1.0]
        """
        x = np.linspace(np.min(self.tm1_x), np.max(self.tm1_x))
        y = np.polyval(self.p, x)
        axes.plot(self.tm1_x, self.tm1_y, 'bo')
        axes.plot(x, y, 'b--')
        t, tmin, tmax = self.tm1_target(target, accuracy)
        axes.axvline(t, color='g')
        axes.bar(tmin, axes.axis()[3], tmax - tmin, color='g', alpha=0.25)
        axes.text(t + 0.1, 30.0, '%.1f' % t, color='g')
        axes.text(tmin + 0.1, 20.0, '%.1f' % tmin, color='g')
        axes.text(tmax + 0.1, 20.0, '%.1f' % tmax, color='g')
        axes.set_xlabel('TM-1 Reading')
        axes.set_ylabel('Spoke Tension (kgf)')
        axes.grid()


def data_table(code):
    """
    Data from TM-1 Tension Meter Conversion Table.

    :Parameters:
      - `code`: TM-1 spoke code index

    :Returns:
      TM-1 reading and corresponding tension [kgf].

    :See:
      http://www.parktool.com/documents/ee5fb98f0f91e4f6be32f7b1e0b9f12b10a74bf0.pdf
    """
    if code == 0:
        x = range(27, 37)
        y = [55, 62, 69, 78, 88, 100, 114, 130, 150, 172]
    elif code == 1:
        x = range(26, 36)
        y = [54, 60, 67, 76, 85, 97, 110, 125, 143, 164]
    elif code == 2:
        x = range(22, 33)
        y = [54, 59, 66, 73, 82, 92, 104, 117, 133, 151, 172]
    elif code == 3:
        x = range(17, 29)
        y = [53, 58, 63, 70, 77, 86, 96, 107, 120, 135, 153, 173]
    elif code == 4:
        x = range(14, 26)
        y = [53, 58, 64, 70, 77, 85, 94, 105, 117, 131, 148, 167]
    elif code == 5:
        x = np.arange(12, 25)
        y = [51, 56, 61, 67, 73, 81, 89, 99, 110, 122, 137, 154, 174]
    elif code == 6:
        x = range(11, 23)
        y = [54, 58, 64, 70, 76, 84, 93, 103, 114, 128, 143, 160]
    elif code == 7:
        x = range(9, 22)
        y = [52, 56, 61, 66, 73, 80, 88, 97, 107, 119, 133, 148, 166]
    elif code == 8:
        x = range(8, 21)
        y = [54, 58, 63, 69, 75, 83, 91, 100, 111, 123, 137, 154, 172]
    elif code == 9:
        x = range(10, 29)
        y = [51, 54, 57, 61, 64, 68, 73, 77, 83, 88, 95, 102, 109, 118, 127, 137, 148, 160, 174]
    elif code == 10:
        x = range(15, 28)
        y = [52, 56, 61, 66, 73, 80, 88, 97, 109, 121, 136, 154, 174]
    elif code == 11:
        x = range(33, 41)
        y = [56, 65, 76, 89, 105, 123, 146, 174]
    elif code == 12:
        x = range(23, 33)
        y = [51, 58, 65, 74, 83, 95, 108, 123, 141, 162]
    elif code == 13:
        x = range(15, 25)
        y = [50, 57, 64, 73, 82, 94, 107, 122, 140, 160]
    elif code == 14:
        x = range(13, 24)
        y = [55, 61, 68, 77, 86, 96, 108, 121, 137, 154, 175]
    elif code == 15:
        x = range(16, 28)
        y = [54, 59, 65, 72, 79, 88, 98, 109, 123, 138, 156, 176]
    elif code == 16:
        x = range(14, 26)
        y = [54, 59, 65, 71, 78, 87, 96, 107, 120, 134, 151, 170]
    elif code == 17:
        x = range(12, 24)
        y = [53, 58, 63, 69, 76, 83, 92, 102, 114, 127, 142, 160]
    elif code == 18:
        x = range(13, 25)
        y = [53, 58, 63, 69, 76, 84, 93, 103, 115, 129, 144, 163]
    elif code == 19:
        x = range(11, 24)
        y = [50, 54, 59, 65, 71, 78, 86, 95, 105, 117, 131, 146, 165]
    elif code == 20:
        x = range(12, 25)
        y = [51, 56, 61, 66, 73, 80, 89, 98, 109, 122, 137, 153, 173]
    elif code == 21:
        x = range(11, 24)
        y = [53, 57, 62, 68, 74, 82, 90, 100, 111, 124, 138, 155, 175]
    elif code == 22:
        x = range(9, 22)
        y = [51, 55, 60, 66, 72, 79, 86, 95, 106, 117, 131, 146, 164]
    elif code == 23:
        x = range(9, 22)
        y = [51, 55, 59, 65, 71, 77, 85, 94, 104, 116, 129, 144, 161]
    elif code == 24:
        x = range(8, 21)
        y = [53, 58, 63, 68, 74, 82, 90, 99, 110, 122, 136, 152, 170]
    elif code == 25:
        x = range(8, 22)
        y = [51, 55, 59, 65, 71, 77, 85, 94, 103, 115, 128, 142, 160, 179]
    elif code == 26:
        x = range(7, 21)
        y = [51, 56, 60, 65, 71, 78, 86, 94, 104, 115, 128, 143, 160, 180]
    elif code == 27:
        x = range(7, 20)
        y = [53, 57, 62, 67, 73, 80, 88, 97, 107, 119, 132, 148, 165]
    elif code == 28:
        x = range(6, 20)
        y = [50, 54, 59, 64, 69, 76, 83, 91, 100, 111, 123, 137, 153, 171]
    elif code == 29:
        x = range(6, 19)
        y = [53, 57, 62, 68, 74, 81, 89, 98, 108, 119, 133, 148, 165]
    elif code == 30:
        x = range(5, 19)
        y = [52, 56, 60, 65, 71, 78, 85, 93, 103, 114, 126, 141, 157, 176]
    elif code == 31:
        x = range(5, 18)
        y = [53, 57, 62, 67, 73, 80, 88, 97, 107, 118, 131, 146, 163]
    elif code == 32:
        x = range(3, 16)
        y = [53, 57, 62, 67, 73, 80, 88, 96, 106, 117, 130, 145, 161]
    elif code == 33:
        x = range(9, 22)
        y = [53, 57, 62, 67, 72, 79, 86, 95, 105, 116, 129, 143, 160]
    elif code == 34:
        x = range(21, 31)
        y = [56, 63, 71, 81, 92, 104, 118, 134, 153, 174]
    elif code == 35:
        x = range(14, 26)
        y = [51, 56, 61, 68, 75, 83, 92, 103, 115, 130, 146, 165]
    elif code == 36:
        x = range(7, 18)
        y = [52, 58, 65, 72, 81, 91, 103, 116, 130, 147, 166]
    elif code == 37:
        x = range(6, 19)
        y = [59, 63, 67, 72, 77, 82, 89, 96, 105, 119, 125, 137, 151]
    else:
        raise IndexError, 'Spoke code %d is not valid' % code
    return (x, np.array(y))
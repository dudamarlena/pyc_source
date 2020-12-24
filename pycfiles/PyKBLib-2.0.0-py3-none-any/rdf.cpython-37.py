# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/rdf.py
# Compiled at: 2019-01-10 08:39:12
# Size of source mod 2**32: 12269 bytes
__doc__ = '\nA set of tools to work with Radial distribution functions, and Kirkwood-Buff integrals.\n\nRadial distribution functions are regularly obtained from molecular simulations, and\ncan be used to.\n\n'
import scipy.integrate, scipy.stats, numpy as np, json
__all__ = [
 'RDF']

def default(o):
    if isinstance(o, np.int64):
        return int(o)
    print(type(o))
    raise TypeError


class RDF:
    """RDF"""

    def __init__(self, radial_dist, radial_dist_func, closed=True, npart=None, box_size=None, eqint=None, name=None):
        self.npart = npart
        if isinstance(radial_dist_func, np.ndarray):
            self.gr = radial_dist_func
        else:
            raise TypeError("RDF: 'radial_dist_func' must be numpy.ndarray")
        if isinstance(radial_dist, np.ndarray):
            self.r = radial_dist
        else:
            raise TypeError("RDF: 'radial_dist' must be numpy.ndarray")
        if closed:
            self.integral_type = 'closed'
        else:
            self.integral_type = 'open'
        self.eqint = eqint
        if box_size is not None:
            self.AddBoxSize(box_size)
        else:
            self.lt = None
            self.volume = None
        if name is None:
            self.name = 'None'
        else:
            self.name = name
        self.rint = None
        self.kbi = None
        self.integral_value = None

    def PrintState(self):
        """
        Print the state of this current system.
        """
        print('RDF-system with name: {}'.format(self.name))
        print('g(r) and r of length {} and {}'.format(len(self.gr), len(self.r)))
        if self.eqint is None:
            print('No information if rdf is between equal or non-equal particles.')
        elif self.eqint:
            print('This rdf is between particles of the same type')
        else:
            print('This rdf is between particles of different type')
        if self.lt is None:
            print('No box-size information present.')
        else:
            if self.kbi is None:
                print('This rdf has not been integrated yet.')
            if self.integral_type is None:
                print('No integral type has been set yet.')
            else:
                print("For this object we are using the '{}' integration method".format(self.integral_type))
        print('Kirkwood-Buff integral: {}'.format(self.ReturnKBI()))
        if self.integral_value is None:
            return
        if 'rint_value' in self.integral_value.keys():
            print('Radial value at readout: {}'.format(self.integral_value['rint_value']))
        if 'index' in self.integral_value.keys():
            print('Index: {}'.format(self.integral_value['index']))
        if 'slope' in self.integral_value.keys():
            print('Line has slope: {}'.format(self.integral_value['slope']))
        if 'r_value' in self.integral_value.keys():
            print('R-squared value: {}'.format(self.integral_value['r_value'] ** 2))
        if 'p_value' in self.integral_value.keys():
            print('p-value: {}'.format(self.integral_value['p_value']))
        if 'std_error' in self.integral_value.keys():
            print('Std. error of slope: {}'.format(self.integral_value['std_error']))
        if 'value_limit' in self.integral_value.keys():
            print('Integral was extrapolated between {}\xa0and {}'.format(self.integral_value['value_limit'][0], self.integral_value['value_limit'][1]))
        if 'index_limit' in self.integral_value.keys():
            print('Indexes for extrapolation {}\xa0and {}'.format(self.integral_value['index_limit'][0], self.integral_value['index_limit'][1]))

    def AddBoxSize(self, lt):
        """
        Add the boxsize and volume to the rdf
        """
        self.lt = lt
        self.volume = lt ** 3

    def Integrate(self):
        """
        Integrate the rdf-data, use either open or closed integration method
        """
        if self.integral_type == 'open':
            self._IntegrateOpenSystem()
        elif self.integral_type == 'closed':
            self._IntegrateClosedSystem()
        else:
            print("'{}' is unknown integration type.".format(self.integral_type))

    def _IntegrateOpenSystem(self):
        """
        Kirkwood-Buff integration of an open system. This only converges if the
        g(r) has been sampled in an grand-canonical or open ensemble. In most
        cases, this is not the case, and the integration should be performed
        using the Kruger-integration. (IntegratedClosedSystem)
        """
        self.rint = np.zeros(len(self.r) - 1)
        self.rint[:] = self.r[1:]
        h = self.gr - 1.0
        self.kbi = 4.0 * np.pi * scipy.integrate.cumtrapz(h * self.r ** 2, self.r)

    def _IntegrateClosedSystem(self):
        """
        Kirkwood-Buff integration of a closed system. This is typically from a
        system in the NVT/NPT/NVE simulation.
        This integration is done using the modification from
        Kruger et al. J. Phys. Chem. Lett. 2013, 4, 235-238 (dx.doi.org/10.1021/jz301992u)
        """
        elems = len(self.r)
        self.rint = np.zeros(elems - 1)
        self.rint[:] = self.r[1:]
        self.kbi = np.zeros(elems - 1)
        h = self.gr - 1.0
        for i in range(1, elems):
            self.kbi[i - 1] = scipy.integrate.trapz(h[:i] * self.r[:i] ** 2 * (1.0 - 1.5 * (self.r[:i] / self.r[i]) + 0.5 * (self.r[:i] / self.r[i]) ** 3), self.r[:i])

        self.kbi *= 4.0 * np.pi

    def FindValues(self, position=None):
        """
        Extract the values from the integral.

        If the system was integrated as an open system, we read it directly
        from the KBI-vector, while if it is a closed system, we have to do
        extrapolation.

        param: position: (first, [last])

        If the position tuple has a None-variable first, it will be set to the
        last value, and the last index.

        """
        self.integral_value = {}
        if self.integral_type == 'open':
            if position is None:
                index = len(self.kbi) - 1
            else:
                if position[0] > self.rint[(-1)] or position[0] < 0.0:
                    print('Trying to read values outside the range of the array')
                    return
                index = np.argmax(self.rint > position[0])
            self.integral_value['G'] = self.kbi[index]
            self.integral_value['rint_value'] = self.rint[index]
            self.integral_value['index'] = index
        elif self.integral_type == 'closed':
            if position is None:
                print('\n We have to set the postions to extrapolate a closed system.\n')
                self.integral_value = None
                return
                if len(position) != 2:
                    print('\n We integrated a closed system, we must supply ranges to extract values\n')
                    self.integral_value = None
                    return
                r_inverse = 1.0 / self.rint
                index = [
                 None, None]
                if position[0] is None:
                    index[1] = len(self.kbi) - 1
            else:
                if position[0] < r_inverse[(-1)]:
                    print('\n Lower limit is outside of the acceptable range.\n')
                    self.integral_value = None
                    return
                index[1] = np.argmax(r_inverse < position[0])
            if position[1] is None:
                print('\n Upper limit has to be set when we read out values from closed system.\n ')
                self.integral_value = None
                return
            if position[1] > r_inverse[0]:
                print('\n Upper limit is outside of the acceptable range.\n')
                self.integral_value = None
                return
            index[0] = np.argmax(r_inverse < position[1])
            slope, intercept, r_value, p_value, std_error = scipy.stats.linregress(r_inverse[index], self.kbi[index])
            self.integral_value['G'] = intercept
            self.integral_value['slope'] = slope
            self.integral_value['p_value'] = p_value
            self.integral_value['std_error'] = std_error
            self.integral_value['r_value'] = r_value
            self.integral_value['index_limit'] = index
            self.integral_value['value_limit'] = r_inverse[index]

    def ReturnKBI(self):
        """
        Return the KBI value
        """
        if self.integral_value is not None:
            if 'G' in self.integral_value.keys():
                return self.integral_value['G']
        return

    def PlotRDF(self, axhandle, kwargs={}):
        """
        Function to plot the rdf

        """
        (axhandle.plot)((self.r), (self.gr), **kwargs)

    def PlotKBI(self, axhandle, kwargs={}):
        """
        Function to plot the KB
        """
        if self.kbi is None:
            print('No integral present in this dataset')
        (axhandle.plot)((self.rint), (self.kbi), **kwargs)

    def PlotKBIInverse(self, axhandle, kwargs={}):
        """
        Plot the inverse of the KB-integral
        """
        if self.kbi is None:
            print('No integral present in this dataset')
        (axhandle.plot)((1.0 / self.rint), (self.kbi), **kwargs)

    def PlotReadout(self, axhandle, kwargs={}):
        """
        Plot the positions where the data extrapolated or readout was done
        """
        if self.integral_value is None:
            print('\nNo data has been read from this data.\n')
            return
        elif self.integral_type == 'open':
            (axhandle.plot)((self.integral_value['rint_value']), (self.ReturnKBI()), 'o', **kwargs)
        elif self.integral_type == 'closed':
            index = self.integral_value['index_limit']
            r_inverse = 1.0 / self.rint
            (axhandle.plot)((r_inverse[index]), (self.kbi[index]), 'o-', **kwargs)
            (axhandle.plot)(0.0, (self.ReturnKBI()), 's', **kwargs)

    def SaveToJSON(self, fname):
        """
        Save the result from the self.integral data-structure to a json-file.
        """
        if '.json' not in fname:
            fname += '.json'
        if self.integral_value == None:
            print('No integral data yet.')
            print('Use FindValues function to read out values.')
            return
        json_data = self.integral_value.copy()
        json_data['gr'] = self.gr.tolist()
        json_data['r'] = self.r.tolist()
        json_data['rint'] = self.rint.tolist()
        json_data['kbi'] = self.kbi.tolist()
        json_data['value_limit'] = json_data['value_limit'].tolist()
        with open(fname, 'w') as (outfile):
            json.dump(json_data, outfile, indent=2, default=default)
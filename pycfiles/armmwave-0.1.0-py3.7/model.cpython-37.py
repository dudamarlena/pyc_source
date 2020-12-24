# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/armmwave/model.py
# Compiled at: 2019-11-15 15:45:08
# Size of source mod 2**32: 12144 bytes
"""
Contains the methods and attributes of a ``Model``.
"""
import sys, numpy as np, armmwave.layer, armmwave.core

class Model:
    __doc__ = 'The ``Model`` class is the framework used to assemble the simulation\n    ``Layer`` objects. It serves as an entry-point to the main calculation.\n\n    Attributes\n    ----------\n    struct : list\n        A collection of ``Layer`` objects as assembled by the ``Model.set_up()``\n        class method.\n    low_freq : float\n        The low-frequency (Hz) bound for the calculation. May be set directly or\n        through the ``Model.set_freq_range()`` class method. Defaults to 500 MHz\n        if not set before ``Model.run()`` is called.\n    high_freq : float\n        The high-frequency (Hz) bound for the calculation. May be set directly or\n        through the ``Model.set_freq_range()`` class method. Defaults to 500 GHz if\n        not set before ``Model.run()`` is called.\n    freq_range : array_like\n        The frequencies (Hz) at which to run the calculation. Defaults to\n        [500e6, 500e9] with 1000 evenly-spaced samples if not set before\n        ``Model.run()`` is called.\n    pol : str\n        The target polarization, either `s` or `p`. Defaults to `s` if not\n        set before ``Model.run()`` is called.\n    incident_angle : float\n        The initial angle (in radians; with respect to normal) at which the\n        wave should strike the model. Defaults to 0 if not set before\n        ``Model.run()`` is called.\n    rinds : array_like\n        A collection of refractive indices for each ``Layer`` in the model,\n        ordered from ``Layer.Source`` to ``Layer.Terminator``.\n    tands : array_like\n        A collection of loss tangents for each ``Layer`` in the model,\n        ordered from ``Layer.Source`` to ``Layer.Terminator``.\n    halpern_layers : dict\n        A dictionary, keyed by ``Layer`` position (specifically, the index into\n        `tands`) containing Halpern `a` and `b` coefficients, if they exist.\n        These coefficients are used to calculate a frequency-dependent loss\n        term, and override the loss tangent for the corresponding layer.\n    thicks : array_like\n        A collection of thicknesses (in meters) for each ``Layer`` in the model,\n        ordered from ``Layer.Source`` to ``Layer.Terminator``.\n\n    '

    def __init__(self):
        self.struct = None
        self.low_freq = None
        self.high_freq = None
        self.freq_range = None
        self.pol = None
        self.incident_angle = None
        self.rinds = None
        self.tands = None
        self.halpern_layers = None
        self.thicks = None
        self._sim_params = None
        self._sim_results = None

    def set_freq_range(self, freq1, freq2, nsample=1000):
        """Set ``Model.freq_range``, the frequency range over which the model's
        response will be calculated.

        Parameters
        ----------
        freq1 : float
            The lower frequency bound (in Hz).
        freq2 : float
            The upper frequency bound (in Hz).
        nsample : int, optional
            The number of evenly-spaced samples between `freq1` and `freq2`.
            Default is 1000.

        Returns
        -------
        freq_range : numpy array

        Raises
        ------
        ValueError
            Raised if `nsample` < 0.

        """
        if nsample <= 0:
            raise ValueError('nsample must be a positive number')
        else:
            self.low_freq = min(freq1, freq2)
            self.high_freq = max(freq1, freq2)
            if freq1 == freq2:
                self.freq_range = np.array([freq1])
            else:
                self.freq_range = np.linspace(freq1, freq2, num=nsample)
        return self.freq_range

    def set_angle_range(self, angle1, angle2, nsample=50):
        """Not implemented.

        Will implement once pi/2 is handled more carefully.

        Raises
        ------
        NotImplementedError
            This function is not implemented.
        """
        raise NotImplementedError('Coming soon! Maybe!')

    def set_up(self, layers, low_freq=500000000.0, high_freq=500000000000.0, theta0=0.0, pol='s'):
        """Assemble the necessary model components.

        This is a convenience function to get all the model bits and pieces
        in one place. Call this before calling ``Model.run()``.

        Parameters
        ----------
        layers : list
            A list containing ``Layer`` objects ordered from ``Layer.Source``
            to ``Layer.Terminator``. Note that the ``Layer.Source`` and
            ``Layer.Terminator`` layers should be the first and last entries of
            the list, respectively.
        low_freq : float, optional
            The lower frequency bound (in Hz). Default is 500e6 (500 MHz).
        high_freq : float, optional
            The upper frequency bound (in Hz). Default is 500e9 (500 GHz).
        theta0 : float, optional
            The initial angle (radians; with respect to normal) at which the
            wave should strike the model. Default is 0.
        pol : str, optional
            The target polarization for the calculation. Must be either `s`,
            or `p`. Default is `s`.

        Raises
        ------
        IndexError
            Raised if there are fewer than three ``Layer`` elements in the
            ``Model``. There must be **at least** a ``Layer.Source``, a
            user-defined ``Layer``, and a ``Layer.Terminator``.
        TypeError
            Raised if the first layer element is not a ``Layer.Source`` or the
            final layer element is not a ``Layer.Terminator``.

        """
        if len(layers) < 3:
            raise IndexError('Must pass a Source layer, at least one material layer, and a Terminator layer.')
        else:
            if not isinstance(layers[0], armmwave.layer.Source):
                raise TypeError('The first layer must be a Source layer.')
            if not isinstance(layers[(-1)], armmwave.layer.Terminator):
                raise TypeError('The last layer must be a Terminator layer.')
            self.struct = layers
            term_layer = self.struct[(-1)]
            last_material = self.struct[(-2)]
            if term_layer.rind == 1.0:
                term_layer.rind = term_layer.vac or last_material.rind
        self.halpern_layers = {}
        for index, l in enumerate(self.struct):
            if l.desc != 'Source layer' and l.desc != 'Terminator layer' and isinstance(l.halperna, float) and isinstance(l.halpernb, float):
                self.halpern_layers[index] = {'a':l.halperna, 
                 'b':l.halpernb,  'n':l.rind}

        self.rinds = [l.rind for l in self.struct]
        self.tands = [l.tand for l in self.struct]
        self.thicks = [l.thick for l in self.struct]
        if self.freq_range is None:
            self.set_freq_range(freq1=low_freq, freq2=high_freq)
        if np.isclose(theta0, np.pi / 2):
            raise ValueError('Incident angle is too close to pi/2. Maximum allowed angle is 89.999 degrees ~= 1.5707788735023767 radians.')
        self.incident_angle = theta0
        self.pol = pol
        self._sim_params = self._set_up_sim(self.rinds, self.tands, self.thicks, self.freq_range, self.incident_angle, self.pol, self.halpern_layers)

    def _set_up_sim(self, rinds, tands, thicks, freq_range, theta0, pol, halpern_layers):
        """Ensure the user-supplied parameters are in a form that the core
        calculation functions expect.

        It is not recommended to call this function directly. Call
        ``Model().set_up()`` instead.

        Parameters
        ----------
        rinds : array_like
        tands : array_like
        thicks : array_like
        freq_range : array_like
        theta0 : float
        pol : str
        halpern_layers : dict

        Returns
        -------
        simargs : dict

        """
        sim_args = {'rind':rinds, 
         'tand':tands,  'thick':thicks,  'freq':freq_range}
        for key, val in sim_args.items():
            if not isinstance(val, np.ndarray):
                sim_args[key] = np.asarray(val)

        sim_args['theta0'] = theta0
        sim_args['pol'] = pol
        sim_args['halpern_layers'] = halpern_layers
        return sim_args

    def reset_model(self):
        """Reinitialize the ``Model`` with its default attribute values: `None`."""
        for key, val in self.__dict__.items():
            self.__dict__[key] = None

    def run(self):
        """Calculate transmittance and reflectance for the given model.

        This function is the primary entry-point to the main calculations.

        Returns
        -------
        results : dict
            A dictionary with three keys:
             * `frequency` : numpy array of frequencies corresponding
               to `T` and `R`
             * `transmittance` : numpy array of transmittances (`T`) for each
               frequency
             * `reflectance` : numpy array of reflectances (`R`) for each
               frequency

        """
        try:
            assert bool(self._sim_params)
        except AssertionError:
            raise KeyError('Did not find calculation-ready parameters. Must call `set_up()` before calling `run()`')

        results = armmwave.core.main(self._sim_params)
        self._sim_results = results
        return results

    def save(self, dest):
        """Write calculation results to a file.

        Write the simulated transmittance and reflectance to a file at `dest`.
        The output includes a header describing the simulation parameters.

        Parameters
        ----------
        dest : str
            The path to the output file.

        """
        fs = self._sim_results['frequency']
        rs = self._sim_results['reflectance']
        ts = self._sim_results['transmittance']
        header = [
         'Structure: {}'.format(self.struct),
         'Frequency lower bound (Hz): {}'.format(self.low_freq),
         'Frequency upper bound (Hz): {}'.format(self.high_freq),
         'Incident angle (rad): {}'.format(self.incident_angle),
         'Polarization: {}'.format(self.pol),
         'Refractive indices: {}'.format(self.rinds),
         'Loss tangents: {}'.format(self.tands),
         'Thicknesses (m): {}'.format(self.thicks),
         '\n',
         'Frequency\t\t\tTransmittance\t\t\tReflectance']
        np.savetxt(dest, (np.c_[(fs, ts, rs)]), delimiter='\t', header=('\n'.join(header)))
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/PyBigDFT/BigDFT/Inputfiles.py
# Compiled at: 2019-12-11 11:59:52
__doc__ = 'Handling of the input options\n\nThis module contains the useful quantities to deal with the preparation and\nthe usage of inputfiles for BigDFT code. The main object is the\n:class:`Inputfile` class, which inherits from a python dictionary. Such\ninheritance is made possible by the internal representation of the BigDFT\ninputfile, which employs the YAML syntax. This means that there is a one-to-one\ncorrespondence between a python dictionary and a BigDFT inputfile.\n\n'

class Inputfile(dict):
    """ The BigDFT inputfile.

    Principal object needed to run a  BigDFT calculation.
    Might be initialized either from a dictionary, a
    :py:class:`~BigDFT.Logfiles.Logfile` instance
    or a (yaml-compliant) filename path

    Note:

       Each of the actions of the module :py:mod:`~BigDFT.InputActions`, which
       is defined on a generic dictionary, also corresponds to a method of of
       the `Inputfile` class, and it is applied to the class instance.
       Therefore also the first argument of the corresponding action is
       implicitly the class instance. For the
       :py:func:`~BigDFT.InputActions.remove` method, the action has to be
       invoked should come from the :py:mod:`~BigDFT.InputActions` module.

    .. _input_action_example:
    Example:

       >>> import InputActions as A, Inputfiles as I
       >>> inp=I.Inputfile()
       >>> inp.set_hgrids(0.3) # equivalent to A.set_hgrids(inp,0.3)
       >>> inp
       {'dft': {'hgrids': 0.3}}
       >>> inp.optimize_geometry() # equivalent to A.optimize_geometry(inp)
       >>> inp
       {'dft': {'hgrids': 0.3},'geopt': {'method': 'FIRE',
                                         'ncount_cluster_x': 50} }
       >>> # equivalent to A.remove(inp,A.optimize_geometry)
       >>> inp.remove(A.optimize_geometry)
       >>> inp
       {'dft': {'hgrids': 0.3}}

     .. todo ::

         Consider the possiblity of initializing an `Inputfile` instance
         from a ``yaml`` file. And also from a
         :py:class:`~BigDFT.Logfiles.Logfile` class

    """

    def __init__(self, *args, **kwargs):
        import BigDFT.InputActions as A
        dict.__init__(self, *args, **kwargs)
        functions = dir(A)
        for action in functions:
            if '__' in action:
                continue
            from functools import partial
            func = getattr(A, action)
            setattr(self, action, partial(func, self))
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/curvedb.py
# Compiled at: 2017-08-29 09:44:06
import numpy as np, pandas as pd, os, logging, pickle as file_backend
try:
    from . import global_config
    CurveDB = __import__(global_config.general.curvedb).CurveDB
except:
    from . import user_curve_dir

    class CurveDB(object):
        _dirname = user_curve_dir
        file_extension = '.dat'
        if not os.path.exists(_dirname):
            os.mkdir(_dirname)

        def __init__(self, name='some_curve'):
            """
            A CurveDB object has
            - name   = string to give the curve a name
            - pk     = integer to uniquely identify the curve (the database primary key)
            - data   = pandas.Series() object to hold any data
            - params = dict() with all kinds of parameters
            """
            self.logger = logging.getLogger(name=__name__)
            self.params = dict()
            x, y = np.array([], dtype=np.float), np.array([], dtype=np.float)
            self.data = (x, y)
            self.name = name

        @property
        def name(self):
            return self.params['name']

        @name.setter
        def name(self, val):
            self.params['name'] = val
            return val

        @classmethod
        def create(cls, *args, **kwds):
            """
            Creates a new curve, first arguments should be either
            Series(y, index=x) or x, y.
            kwds will be passed to self.params
            """
            if len(args) == 0:
                ser = (
                 np.array([], dtype=np.float), np.array([], dtype=np.float))
            if len(args) == 1:
                if isinstance(args[0], pd.Series):
                    x, y = args[0].index.values, args[0].values
                    ser = (x, y)
                elif isinstance(args[0], (np.array, list, tuple)):
                    ser = args[0]
                else:
                    raise ValueError('cannot recognize argument %s as numpy.array or pandas.Series.', args[0])
            elif len(args) == 2:
                x = np.array(args[0])
                y = np.array(args[1])
                ser = (x, y)
            else:
                raise ValueError('first arguments should be either x or x, y')
            obj = cls()
            obj.data = ser
            obj.params = kwds
            if 'name' not in obj.params:
                obj.params['name'] = 'new_curve'
            pk = obj.pk
            if 'childs' not in obj.params:
                obj.params['childs'] = None
            if 'autosave' not in kwds or kwds['autosave']:
                obj.save()
            return obj

        def plot(self):
            self.data.plot()

        @classmethod
        def get(cls, curve):
            if isinstance(curve, CurveDB):
                return curve
            else:
                if isinstance(curve, list):
                    return [ CurveDB.get(c) for c in curve ]
                with open(os.path.join(CurveDB._dirname, str(curve) + cls.file_extension), 'rb' if file_backend.__name__ == 'pickle' else 'r') as (f):
                    curve = CurveDB()
                    curve._pk, curve.params, data = file_backend.load(f)
                    curve.data = tuple([ np.asarray(a) for a in data ])
                if isinstance(curve.data, pd.Series):
                    x, y = curve.data.index.values, curve.data.values
                    curve.data = (x, y)
                return curve

        def save(self):
            with open(os.path.join(self._dirname, str(self.pk) + self.file_extension), 'wb' if file_backend.__name__ == 'pickle' else 'w') as (f):
                data = [ a.tolist() for a in self.data ]
                file_backend.dump([self.pk, self.params, data], f)

        def delete(self):
            delpk = self.pk
            parent = self.parent
            childs = self.childs
            if isinstance(childs, list) and len(childs) > 0:
                self.logger.debug('Deleting all childs of curve %d' % delpk)
                for child in childs:
                    child.delete()

            self.logger.debug('Deleting curve %d' % delpk)
            try:
                filename = os.path.join(self._dirname, str(self.pk) + self.file_extension)
                os.remove(filename)
            except OSError:
                self.logger.warning('Could not find and remove the file %s. ', filename)

            if parent:
                parentchilds = parent.childs
                parentchilds.remove(delpk)
                parent.childs = parentchilds
                parent.save()

        @property
        def childs(self):
            try:
                childs = self.params['childs']
            except KeyError:
                return []

            if childs is None:
                return []
            else:
                try:
                    return CurveDB.get(childs)
                except KeyError:
                    return []

                return

        @property
        def parent(self):
            try:
                parentid = self.params['parent']
            except KeyError:
                self.logger.debug('No parent found.')
                return

            return CurveDB.get(parentid)
            return

        def add_child(self, child_curve):
            child = CurveDB.get(child_curve)
            child.params['parent'] = self.pk
            child.save()
            childs = self.params['childs'] or []
            self.params['childs'] = list(childs + [child.pk])
            self.save()

        @classmethod
        def all_pks(cls):
            """
            Returns:
                list of int: A list of the primary keys of all CurveDB objects on the computer.
            """
            pks = [ int(f.split('.dat')[0]) for f in os.listdir(cls._dirname) if f.endswith('.dat')
                  ]
            return sorted(pks, reverse=True)

        @classmethod
        def all(cls):
            """
            Returns:
                list of CurveDB: A list of all CurveDB objects on the computer.
            """
            return [ cls.get(pk) for pk in cls.all_pks() ]

        @property
        def pk(self):
            """
            (int): The primary Key of the
            """
            if hasattr(self, '_pk'):
                return self._pk
            else:
                pks = self.all_pks()
                if len(pks) == 0:
                    self._pk = 1
                else:
                    self._pk = max(pks) + 1
                with open(os.path.join(self._dirname, str(self._pk) + '.dat'), 'w') as (f):
                    f.close()
                return self._pk

            return -1

        def sort(self):
            """numerically sorts the data series so that indexing can be used"""
            X, Y = self.data
            xs = np.array([ x for x, y in sorted(zip(X, Y)) ], dtype=np.float64)
            ys = np.array([ y for x, y in sorted(zip(X, Y)) ], dtype=np.float64)
            self.data = (xs, ys)

        def fit(self):
            """ prototype for fitting a curve """
            self.logger.warning('Not implemented')

        def get_child(self, name):
            """
            Returns the child of the curve with name 'name'

            Arguments:
                name (str): Name of the child curve to be retrieved. If
                    several childs have the same name, the first one is
                    returned.

            Returns:
                CurveDB: the child curve
            """
            for c in self.childs:
                if c.name == name:
                    return c
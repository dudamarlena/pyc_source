# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/data/roles.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 7291 bytes
"""A :class:`~getml.data.role` determines if and how
:mod:`~getml.data.columns` are handled during the construction of the
data model (see :ref:`data_model`) and used by the feature engineering
(FE) algorithm (see :ref:`feature_engineering`).

Upon construction (via :func:`~getml.data.DataFrame.from_csv`,
:func:`~getml.data.DataFrame.from_pandas`,
:func:`~getml.data.DataFrame.from_db`, and
:func:`~getml.data.DataFrame.from_json`) a
:class:`~getml.data.DataFrame` will only consist of
:mod:`~getml.data.columns` holding either the role
:const:`~getml.data.role.unused_float` or
:const:`~getml.data.role.unused_string` depending on the underlying
data type. This tells the getML software to neither use these columns
during the creation of the data model, the feature engineering, or the
training of the machine learning (ML) algorithms.

To make use of the uploaded data, you have to tell the getML suite how
you intend to use it by assigning another
:class:`~getml.data.role`. This can be done by either using the
:meth:`~getml.data.DataFrame.set_role` method of the
:class:`~getml.data.DataFrame` containing the particular column or by
providing a dictionary in the constructor function.

Each column must have at have a single role. But what if you e.g. want
to use a column to both create relations in your data model and to be
the basis of new features? You have to add it twice and assign
each of them a different role.
"""
categorical = 'categorical'
join_key = 'join_key'
numerical = 'numerical'
target = 'target'
time_stamp = 'time_stamp'
unused_float = 'unused_float'
unused_string = 'unused_string'
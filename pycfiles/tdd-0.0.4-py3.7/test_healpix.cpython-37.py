# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/test_healpix.py
# Compiled at: 2019-04-16 05:35:19
# Size of source mod 2**32: 5989 bytes
"""
Tests associated with the `opsimsummary/healpix.py` module
"""
from __future__ import division, print_function, absolute_import
import opsimsummary as oss, os, pytest, numpy as np, pandas as pd
from sqlalchemy import create_engine
import unittest, healpy as hp, sqlite3

class Test_obsHistIDsFortileID(unittest.TestCase):
    __doc__ = '\n    Tests associated with obtaining obsHistID values for tileIDs using healpix\n    in  the nest scheme.\n    '

    @classmethod
    def setUpClass(cls):
        pkgDir = os.path.abspath(os.path.split(oss.__file__)[0])
        dbname = os.path.join(pkgDir, 'example_data', 'enigma_1189_micro.db')
        engineFile = 'sqlite:///' + dbname
        engine = create_engine(engineFile)
        sql_query = 'SELECT * FROM Summary WHERE PropID == 364'
        print(sql_query)
        opsimdf = pd.read_sql_query(sql_query, con=engine,
          index_col='obsHistID')
        cls.nside = 4
        stdDBname = os.path.join(pkgDir, 'example_data', 'healpixels_micro.db')
        cls.stdDBConn = sqlite3.Connection(stdDBname)
        cls.newDB = 'healpix_micro_new.db'
        if os.path.exists(cls.newDB):
            os.remove(cls.newDB)
        cls.newconn = sqlite3.Connection(cls.newDB)
        h = oss.HealPixelizedOpSim(opsimDF=opsimdf, NSIDE=(cls.nside), source=dbname)
        h.doPreCalcs()
        try:
            version = oss.__version__
            h.writeToDB((cls.newDB), version=version)
        except:
            cls.tearDownClass()
            raise Warning('Had to erase teardown the class to set it up')

        cls.hpOps = h

    def test_obsHistIDsForfields(self):
        """
        Check that a healpix ID p is in the list of hids associated with 
        each of the pointings intersecting with it.
        """
        h = self.hpOps
        hids = np.arange(hp.nside2npix(self.nside))
        l = list((all(h.opsimdf.query('obsHistID in @h.obsHistIdsForTile(@p)').hids.apply(lambda x: p in x).values) for p in hids))
        assert all(l)

    def test_writemethod(self):
        """
        Sanity checks on the output database from writing out ipix, obsHistID database
        """
        newcursor = self.newconn.cursor()
        newcursor.execute('SELECT COUNT(*) FROM simlib')
        x = newcursor.fetchone()[0]
        self.assertEqual(x, 159608)
        newcursor.execute('SELECT MIN(ipix) FROM simlib')
        y = newcursor.fetchone()
        self.assertEqual(y[0], 0)
        x = newcursor.execute('SELECT MAX(ipix) FROM simlib')
        y = x.fetchone()
        self.assertEqual(y[0], 191)
        x = newcursor.execute('SELECT MIN(ipix) FROM simlib')
        y = x.fetchone()
        self.assertEqual(y[0], 0)
        newcursor = self.newconn.cursor()
        x = newcursor.execute('SELECT * FROM metadata')
        y = x.fetchall()
        self.assertEqual(len(y), 1)
        self.assertEqual(len(y[0]), 10)
        version = oss.__version__
        self.assertEqual(y[0][4], version)
        self.assertEqual(np.int(y[0][5]), self.nside)
        self.assertEqual(np.int(y[0][6]), 4)

    @pytest.mark.skip(reason='skipped before')
    def test_compareWithOldDB(self):
        """
        Compare any new database with a stored version of the old database
        """
        newcursor = self.newconn.cursor()
        npix = hp.nside2npix(1)
        ipixvalues = np.arange(npix)
        stdCursor = self.stdDBConn.cursor()
        for hid in ipixvalues[:11]:
            newcursor.execute('SELECT obsHistID FROM simlib WHERE ipix == {}'.format(hid))
            _new = newcursor.fetchall()
            new = np.asarray(list((xx[0] for xx in _new)))
            stdCursor.execute('SELECT obsHistID FROM simlib WHERE ipix == {}'.format(hid))
            _std = stdCursor.fetchall()
            std = np.asarray(list((xx[0] for xx in _std)))
            np.testing.assert_equal(std, new, verbose=True, err_msg=('std = {0} and new ={1}'.format(std, new)))

    def test_compareFunctionWithDB(self):
        """
        Test comparing values in written database to values calculated in-situ
        for 12 values of ipix
        """
        newcursor = self.newconn.cursor()
        npix = hp.nside2npix(self.nside)
        ipixvalues = np.arange(npix)
        for hid in ipixvalues[:11]:
            newcursor.execute('SELECT obsHistID FROM simlib WHERE ipix == {}'.format(hid))
            x = newcursor.fetchall()
            y = np.asarray(list((xx[0] for xx in x)))
            h = self.hpOps
            z = h.obsHistIdsForTile(hid)
            np.testing.assert_equal(y, z, verbose=True, err_msg=('x = {0} and y ={1}'.format(y, z)))

    @classmethod
    def tearDownClass(cls):
        import os
        if os.path.exists(cls.newDB):
            os.remove(cls.newDB)
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rasmus/src/pytc/lib/tc/test/hdb.py
# Compiled at: 2009-03-01 17:58:06
import os, sys, unittest, tc, struct
DBNAME = 'test.hdb'
DBNAME2 = 'test.hdb.copy'

class TestHDB(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DBNAME):
            os.remove(DBNAME)

    def tearDown(self):
        if os.path.exists(DBNAME):
            os.remove(DBNAME)

    def testAll(self):
        db = tc.HDB()
        db.tune(100, 32, 64, tc.HDBTTCBS)
        db.open(DBNAME2, tc.HDBOWRITER | tc.HDBOCREAT)
        db.copy(DBNAME)
        db.close
        os.remove(DBNAME2)
        db = tc.HDB(DBNAME, tc.HDBOWRITER)
        db.put('hamu', 'ju')
        db.put('moru', 'pui')
        db.put('kiki', 'nya-')
        self.assertEqual(db.get('hamu'), 'ju')
        self.assertEqual(db.vsiz('hamu'), len('ju'))
        self.assertRaises(tc.Error, db.putkeep, 'moru', 'puipui')
        db.putkeep('moruta', 'puipui')
        self.assertEqual(db.get('moruta'), 'puipui')
        db.putcat('kiki', 'nya-nya-')
        self.assertEqual(db.get('kiki'), 'nya-nya-nya-')
        db.putasync('gunya', 'darari')
        db.sync
        self.assertEqual(db.get('gunya'), 'darari')
        db.out('gunya')
        self.assertRaises(KeyError, db.get, 'gunya')
        db.optimize(100, 32, 64, tc.HDBTTCBS)
        self.assertEqual(db.path(), DBNAME)
        self.assertEqual(db.rnum(), 4)
        self.assertNotEqual(db.fsiz(), 0)
        db.iterinit()
        self.assertEqual(db.iternext(), 'hamu')
        db.iterinit()
        self.assertEqual(db.iternext(), 'hamu')
        result = []
        for key in db:
            result.append(key)

        self.assertEqual(sorted(result), ['hamu', 'kiki', 'moru', 'moruta'])
        self.assertEqual(sorted(db.keys()), ['hamu', 'kiki', 'moru', 'moruta'])
        self.assertEqual(sorted(db.values()), ['ju', 'nya-nya-nya-', 'pui', 'puipui'])
        self.assertEqual(sorted(db.items()), [
         ('hamu', 'ju'), ('kiki', 'nya-nya-nya-'), ('moru', 'pui'), ('moruta', 'puipui')])
        result = []
        for key in db.iterkeys():
            result.append(key)

        self.assertEqual(sorted(result), ['hamu', 'kiki', 'moru', 'moruta'])
        result = []
        for value in db.itervalues():
            result.append(value)

        self.assertEqual(sorted(result), ['ju', 'nya-nya-nya-', 'pui', 'puipui'])
        result = []
        for (key, value) in db.iteritems():
            result.append((key, value))

        self.assertEqual(sorted(result), [
         ('hamu', 'ju'), ('kiki', 'nya-nya-nya-'), ('moru', 'pui'), ('moruta', 'puipui')])
        self.assertRaises(TypeError, eval, 'db[:]', globals(), locals())
        db['gunya'] = 'tekito'
        self.assertEqual(db['gunya'], 'tekito')
        del db['gunya']
        self.assertRaises(KeyError, db.get, 'gunya')
        self.assert_('hamu' in db)
        self.assert_('python' not in db)
        db.vanish()
        self.assertEqual(db.rnum(), 0)
        db['int'] = struct.pack('i', 0)
        db.addint('int', 1)
        self.assertEqual(struct.unpack('i', db['int'])[0], 1)
        db['double'] = struct.pack('d', 0.0)
        db.adddouble('double', 1.0)
        self.assertEqual(struct.unpack('d', db['double'])[0], 1.0)
        try:
            db['absence']
        except Exception, e:
            self.assertEqual(type(e), KeyError)

        os.remove(DBNAME)


def suite():
    return unittest.TestSuite([
     unittest.makeSuite(TestHDB)])


if __name__ == '__main__':
    unittest.main()
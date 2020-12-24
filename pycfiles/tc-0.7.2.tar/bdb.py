# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rasmus/src/pytc/lib/tc/test/bdb.py
# Compiled at: 2009-03-01 17:59:10
import os, sys, unittest, tc, struct
DBNAME = 'test.bdb'
DBNAME2 = 'test.bdb.copy'

class TestBDB(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DBNAME):
            os.remove(DBNAME)

    def tearDown(self):
        if os.path.exists(DBNAME):
            os.remove(DBNAME)

    def testAll(self):
        db = tc.BDB()
        db.tune(2, 4, 19, 4, 5, tc.BDBTTCBS)
        db.setcache(1, 1)
        db.open(DBNAME2, tc.BDBOWRITER | tc.BDBOCREAT)
        db.copy(DBNAME)
        db.close
        os.remove(DBNAME2)
        db = tc.BDB(DBNAME, tc.BDBOWRITER)
        db.put('hamu', 'ju')
        db.put('moru', 'pui')
        db.put('kiki', 'nya-')
        db.put('gunya', 'gorori')
        self.assertEqual(db.get('hamu'), 'ju')
        self.assertEqual(db.vsiz('hamu'), len('ju'))
        self.assertRaises(tc.Error, db.putkeep, 'moru', 'puipui')
        db.putkeep('moruta', 'puipui')
        self.assertEqual(db.get('moruta'), 'puipui')
        db.putcat('kiki', 'nya-nya-')
        self.assertEqual(db.get('kiki'), 'nya-nya-nya-')
        db.putdup('kiki', 'unya-n')
        self.assertEqual(db.getlist('kiki'), ['nya-nya-nya-', 'unya-n'])
        self.assertEqual(db.vnum('kiki'), 2)
        db.out('gunya')
        self.assertRaises(KeyError, db.get, 'gunya')
        db.putlist('gunya', ['gorori', 'harahetta', 'nikutabetai'])
        self.assertEqual(db.getlist('gunya'), ['gorori', 'harahetta', 'nikutabetai'])
        db.outlist('gunya')
        self.assertEqual(db.vnum('gunya'), 0)
        db.optimize(2, 4, 19, 4, 5, tc.BDBTTCBS)
        self.assertEqual(db.path(), DBNAME)
        self.assertEqual(db.rnum(), 5)
        self.assertNotEqual(db.fsiz(), 0)
        result = []
        for key in db:
            result.append(key)

        self.assertEqual(sorted(result), ['hamu', 'kiki', 'kiki', 'moru', 'moruta'])
        self.assertEqual(sorted(db.keys()), [
         'hamu', 'kiki', 'kiki', 'moru', 'moruta'])
        self.assertEqual(sorted(db.values()), [
         'ju', 'nya-nya-nya-', 'pui', 'puipui', 'unya-n'])
        self.assertEqual(sorted(db.items()), [
         ('hamu', 'ju'), ('kiki', 'nya-nya-nya-'), ('kiki', 'unya-n'),
         ('moru', 'pui'), ('moruta', 'puipui')])
        result = []
        for key in db.iterkeys():
            result.append(key)

        self.assertEqual(sorted(result), ['hamu', 'kiki', 'kiki', 'moru', 'moruta'])
        result = []
        for value in db.itervalues():
            result.append(value)

        self.assertEqual(sorted(result), [
         'ju', 'nya-nya-nya-', 'pui', 'puipui', 'unya-n'])
        result = []
        for (key, value) in db.iteritems():
            result.append((key, value))

        self.assertEqual(sorted(result), [
         ('hamu', 'ju'), ('kiki', 'nya-nya-nya-'), ('kiki', 'unya-n'),
         ('moru', 'pui'), ('moruta', 'puipui')])
        self.assertRaises(TypeError, eval, 'db[:]', globals(), locals())
        db['gunya'] = 'tekito'
        self.assertEqual(db['gunya'], 'tekito')
        del db['gunya']
        self.assertRaises(KeyError, db.get, 'gunya')
        self.assert_('hamu' in db)
        self.assert_('python' not in db)
        cur = db.curnew()
        cur.first()
        self.assertEqual(cur.key(), 'hamu')
        self.assertEqual(cur.val(), 'ju')
        self.assertEqual(cur.rec(), ('hamu', 'ju'))
        cur.next()
        self.assertEqual(cur.rec(), ('kiki', 'nya-nya-nya-'))
        cur.put('fungofungo', tc.BDBCPCURRENT)
        self.assertEqual(cur.rec(), ('kiki', 'fungofungo'))
        cur.out()
        self.assertEqual(db.vnum('kiki'), 1)
        cur.prev()
        self.assertEqual(cur.rec(), ('hamu', 'ju'))
        cur.jump('moru')
        self.assertEqual(cur.rec(), ('moru', 'pui'))
        cur.last()
        self.assertEqual(cur.rec(), ('moruta', 'puipui'))
        db.tranbegin()
        db.put('moru', 'pupupu')
        self.assertEqual(db.get('moru'), 'pupupu')
        db.tranabort()
        self.assertEqual(db.get('moru'), 'pui')
        db.tranbegin()
        db.put('moru', 'pupupu')
        db.trancommit()
        self.assertEqual(db.get('moru'), 'pupupu')
        db['nagasaki'] = 'ichiban'
        db['nagasaki-higashi'] = 'toh'
        db['nagasaki-nishi'] = 'zai'
        db['nagasaki-minami'] = 'nan'
        db['nagasaki-kita'] = 'boku'
        db['nagasaki-hokuyodai'] = 'hokuyodai'
        self.assertEqual(db.range('nagasaki', False, 'nagasaki-kita', True, 3), [
         'nagasaki-higashi',
         'nagasaki-hokuyodai',
         'nagasaki-kita'])
        self.assertEqual(db.rangefwm('nagasaki', 5), [
         'nagasaki', 'nagasaki-higashi',
         'nagasaki-hokuyodai', 'nagasaki-kita',
         'nagasaki-minami'])
        db.vanish()
        self.assertRaises(KeyError, db.rnum)
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

    def testCmpFunc(self):
        db = tc.BDB()
        db.setcmpfunc(lambda x, y: len(x) == len(y), 1)
        db.open(DBNAME, tc.BDBOWRITER | tc.BDBOCREAT)
        db['kiki'] = 'nya-'
        db['moru'] = 'pui'
        self.assertEqual(db.get('kiki'), 'pui')
        os.remove(DBNAME)


def suite():
    return unittest.TestSuite([
     unittest.makeSuite(TestBDB)])


if __name__ == '__main__':
    unittest.main()
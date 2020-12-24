# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tests/test_m1.py
# Compiled at: 2019-12-05 17:01:18
# Size of source mod 2**32: 5841 bytes
import unittest
import nacc.uds3.m as m_builder
from nacc.uds3 import blanks
import nacc.uds3 as m_packet
import nacc.uds3.m as m_form

class TestM1(unittest.TestCase):

    def test_m1_death_date_accept(self):
        """ death date format interpreter accept correct dates """
        date = [
         '12/12/2012', '12-12-2012', '2012/12/12', '2012-12-12']
        date_parsed = ['12', '12', '2012', '12', '12', '2012', '12', '12', '2012', '12', '12', '2012']
        record = make_blank_m()
        out = []
        for x in date:
            record['DECEASED'] = '1'
            record['DEATHMO'] = m_builder.parse_date(x, 'M')
            record['DEATHDY'] = m_builder.parse_date(x, 'D')
            record['DEATHYR'] = m_builder.parse_date(x, 'Y')
            out += [str(record['DEATHMO']), str(record['DEATHDY']), str(record['DEATHYR'])]

        self.assertEqual(date_parsed, out)

    def test_m1_death_date_reject(self):
        """ death date format interpreter rejects wrong dates """
        date = [
         '12/12/2012', '12-1212', '12/2012/12', '2012-12-12']
        date_parsed = ['12', '12', '2012', '12', '12', '2012', '12', '12', '2012', '12', '12', '2012']
        record = make_blank_m()
        out = []
        with self.assertRaises(ValueError):
            for x in date:
                record['DECEASED'] = '1'
                record['DEATHMO'] = m_builder.parse_date(x, 'M')
                record['DEATHDY'] = m_builder.parse_date(x, 'D')
                record['DEATHYR'] = m_builder.parse_date(x, 'Y')
                out += [str(record['DEATHMO']), str(record['DEATHDY']), str(record['DEATHYR'])]

        self.assertNotEqual(date_parsed, out)

    @unittest.skip("'0' is outside of the inclusive_range for 'FTLDREAS', 'FTLDREAX' should be left blank if FTLDREAS is filled regardless of 'DECEASED' or 'DISCONT' status")
    def test_m1_blank_if_dead(self):
        """ If dead should be blank """
        packet = m_packet.Packet()
        m = m_form.FormM()
        m.DECEASED = '1'
        m.CHANGEMO = '02'
        m.CHANGEDY = '28'
        m.CHANGEYR = '2008'
        m.PROTOCOL = '2'
        m.ACONSENT = '0'
        m.RECOGIM = '0'
        m.REPHYILL = '0'
        m.REREFUSE = '0'
        m.RENAVAIL = '0'
        m.RENURSE = '0'
        m.REJOIN = '0'
        m.FTLDDISC = '0'
        m.FTLDREAS = '0'
        m.FTLDREAX = '0'
        m.DISCONT = '0'
        packet.append(m)
        blanks.set_zeros_to_blanks(packet)
        self.assertEqual(packet['RENURSE'], '')
        self.assertEqual(packet['RECOGIM'], '')
        self.assertEqual(packet['REPHYILL'], '')
        self.assertEqual(packet['REREFUSE'], '')
        self.assertEqual(packet['RENAVAIL'], '')
        self.assertEqual(packet['FTLDDISC'], '')
        self.assertEqual(packet['AUTOPSY'], '')
        self.assertEqual(packet['FTLDREAS'], '')

    @unittest.skip("'0' is outside of the inclusive_range for 'FTLDREAS', 'FTLDREAX' should be left blank if FTLDREAS is filled regardless of 'DECEASED' or 'DISCONT' status")
    def test_m1_blank_if_discont(self):
        """ If discontinued should be blank """
        packet = m_packet.Packet()
        m = m_form.FormM()
        m.DISCONT = '1'
        m.DECEASED = '0'
        m.CHANGEMO = '02'
        m.CHANGEDY = '28'
        m.CHANGEYR = '2008'
        m.PROTOCOL = '2'
        m.ACONSENT = '0'
        m.RECOGIM = '0'
        m.REPHYILL = '0'
        m.REREFUSE = '0'
        m.RENAVAIL = '0'
        m.RENURSE = '0'
        m.REJOIN = '0'
        m.FTLDDISC = '0'
        m.FTLDREAS = '0'
        m.FTLDREAX = '0'
        packet.append(m)
        blanks.set_zeros_to_blanks(packet)
        self.assertEqual(packet['RENURSE'], '')
        self.assertEqual(packet['RECOGIM'], '')
        self.assertEqual(packet['REPHYILL'], '')
        self.assertEqual(packet['REREFUSE'], '')
        self.assertEqual(packet['RENAVAIL'], '')
        self.assertEqual(packet['FTLDDISC'], '')
        self.assertEqual(packet['AUTOPSY'], '')
        self.assertEqual(packet['FTLDREAS'], '')


def make_blank_m():
    return {'visitmo':'', 
     'visitday':'', 
     'visityr':'', 
     'CHANGEMO':'', 
     'CHANGEDY':'', 
     'CHANGEYR':'', 
     'PROTOCOL':'', 
     'ACONSENT':'', 
     'RECOGIM':'', 
     'REPHYILL':'', 
     'REREFUSE':'', 
     'RENAVAIL':'', 
     'RENURSE':'', 
     'NURSEMO':'', 
     'NURSEDY':'', 
     'NURSEYR':'', 
     'REJOIN':'', 
     'FTLDDISC':'', 
     'FTLDREAS':'', 
     'FTLDREAx':'', 
     'DECEASED':'', 
     'DISCONT':'', 
     'DEATHMO':'', 
     'DEATHDY':'', 
     'DEATHYR':'', 
     'AUTOPSY':'', 
     'DISCMO':'', 
     'DISCDAY':'', 
     'DISCYR':'', 
     'DROPREAS':''}


if __name__ == '__main__':
    unittest.main()
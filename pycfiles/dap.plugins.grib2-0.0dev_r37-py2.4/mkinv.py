# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/plugins/grib2/mkinv.py
# Compiled at: 2007-04-02 15:10:13
import os, sys
from grib2 import Grib2Decode
from BeautifulSoup import *
from grib2.tobase import tobase
from dap.exceptions import ClientError

def load_pdt_table():
    pdt_table = {}
    pdt_table[1] = {'postfix': 'sfc', 'factor': 1}
    pdt_table[4] = {'postfix': '0deg', 'factor': 1}
    pdt_table[6] = {'postfix': 'mwl', 'factor': 1}
    pdt_table[7] = {'level': 'Tropopause', 'postfix': 'trp', 'factor': 1}
    pdt_table[8] = {'level': 'Nominal Top of the Atmosphere', 'postfix': 'toa', 'factor': 1}
    pdt_table[100] = {'postfix': 'mb', 'factor': 0.01}
    pdt_table[101] = {'postfix': 'msl', 'factor': 1}
    pdt_table[102] = {'postfix': 'm', 'factor': 1}
    pdt_table[103] = {'postfix': 'm', 'factor': 1}
    pdt_table[104] = {'postfix': 'sig', 'factor': 1}
    pdt_table[105] = {'postfix': 'hyb', 'factor': 1}
    pdt_table[106] = {'postfix': 'cm', 'factor': 0.1}
    pdt_table[108] = {'postfix': 'mb', 'factor': 0.01}
    pdt_table[109] = {'postfix': 'pvsfc', 'factor': 1}
    pdt_table[200] = {'level': 'Entire atmosphere', 'postfix': 'atmcol', 'factor': 1}
    pdt_table[204] = {'postfix': 'htfl', 'factor': 1}
    pdt_table[209] = {'postfix': 'blcbl', 'factor': 1}
    pdt_table[210] = {'postfix': 'blctl', 'factor': 1}
    pdt_table[211] = {'postfix': 'blcl', 'factor': 1}
    pdt_table[212] = {'postfix': 'lcbl', 'factor': 1}
    pdt_table[213] = {'postfix': 'lctl', 'factor': 1}
    pdt_table[214] = {'postfix': 'lcl', 'factor': 1}
    pdt_table[222] = {'postfix': 'mcbl', 'factor': 1}
    pdt_table[223] = {'postfix': 'mctl', 'factor': 1}
    pdt_table[224] = {'postfix': 'mcl', 'factor': 1}
    pdt_table[232] = {'postfix': 'hcbl', 'factor': 1}
    pdt_table[233] = {'postfix': 'hctl', 'factor': 1}
    pdt_table[234] = {'postfix': 'hcl', 'factor': 1}
    pdt_table[242] = {'postfix': 'ccbl', 'factor': 1}
    pdt_table[243] = {'postfix': 'cctl', 'factor': 1}
    pdt_table[244] = {'postfix': 'ccl', 'factor': 1}
    return pdt_table


def load_grib2_map(file):
    xml_file = file
    fp = open(xml_file, 'r')
    xml = BeautifulSoup(fp)
    fp.close()
    return xml


def get_grb_def(gpath, gxml):
    ele = gpath[0]
    gx = gxml.fetch(ele)
    if len(gx) == 0:
        return [
         None, None, None]
    if len(gpath[1:]) > 0:
        res = get_grb_def(gpath[1:], gx[0])
        return res
    gx = gx[0]
    return [
     gx.short_name.string, gx.long_name.string, gx.units.string]


def map_grib2_to_var(datafp, xml, pdt_table):
    inv = datafp.inventory
    used_var = {}
    grib2_map = {}
    for r in range(len(inv)):
        for sr in range(len(inv[r])):
            lev = datafp.level[r][sr]
            disc = 'd%d' % datafp.discipline[r]
            pdt = datafp.pdtmpl[r][sr]
            catg = 'c%d' % pdt[0]
            numb = 'n%d' % pdt[1]
            lvtype = pdt[9]
            parm = datafp.parameter[r][sr]
            unit = datafp.units[r][sr]
            (var, p, u) = get_grb_def([disc, catg, numb], xml)
            if p != Null:
                parm = str(p)
            if u != Null:
                unit = str(u)
            if var == None or unit == Null or parm == Null or parm == 'Reserved for local use':
                print disc, catg, numb, var, unit, parm
                raise ClientError('No definition found(%s %s %s) please update ncep.xml' % (disc, catg, numb))
            if var[0] >= '0' and var[0] <= '9':
                var = 'x%s' % var
            var = var.lower()
            try:
                pdt_conv = pdt_table[lvtype]
                pf = pdt_conv['postfix']
                if lev == '' and 'level' in pdt_conv:
                    lev = str(pdt_conv['level'])
            except:
                print disc, catg, numb, var, unit, parm
                raise ClientError('Undefined level type: %s' % lvtype)

            lv = ''
            if pdt[9] != 255:
                lv1 = int(pdt[11] * pdt_conv['factor'])
                if lv1 < 0:
                    lv1 = 'm%s' % abs(lv1)
                lv = '%s' % lv1
                if pdt[12] != 255:
                    lv2 = int(pdt[14] * pdt_conv['factor'])
                    if lv2 < 0:
                        lv2 = 'm%s' % abs(lv2)
                    lv = '%s_%s' % (lv1, lv2)
            if lv == '0':
                var = '%s_%s' % (var, pf)
            else:
                var = '%s_%s_%s' % (var, lv, pf)
            if var in used_var:
                num = used_var[var] + 1
                used_var[var] = num
                var = '%s_dup_%s' % (var, num)
                grib2_map[var] = {'rec': [r, sr], 'units': unit, 'parameter': parm, 'level': lev, 'tables': '%s %s %s' % (disc, catg, numb)}
            else:
                used_var[var] = 1
                grib2_map[var] = {'rec': [r, sr], 'units': unit, 'parameter': parm, 'level': lev, 'tables': '%s %s %s' % (disc, catg, numb)}

    return grib2_map


if __name__ == '__main__':
    pdt_table = load_pdt_table()
    xml = load_grib2_map('/home/cermak/howto/grib2/dap/plugins/grib2/ncep.xml')
    filepath = ['/space/pydap/data/F012_242_grib2_NAM_84.grb2']
    filepath = ['/space/pydap/data/242/20070301/1200/F006_242_grib2_NAM_84']
    filepath = ['/home/cermak/howto/data/fh.0012_tl.press_gr.0p5deg.grb2', '/home/cermak/howto/data/F012_242_grib2_NAM_84.grb2', '/home/cermak/howto/data/F012_160_grib2_GFS.grb2']
    for f in filepath:
        print f
        fp = Grib2Decode(f)
        grib2varmap = map_grib2_to_var(fp, xml, pdt_table)
        gtnum = fp.gdtnum[0]
        print fp.projection[0]
        print tobase(2, int(fp.gdtmpl[0][0][16]))[0]
        projinfo = fp.getgridinfo(0)
        (lats, lons) = fp.getlatlon(0)
        print projinfo
        print lats.shape, lons.shape
        fp.close()
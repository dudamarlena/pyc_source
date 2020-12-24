# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\csvwt.py
# Compiled at: 2019-11-25 16:46:05
# Size of source mod 2**32: 15209 bytes
"""
csvwt - write csv from various file types
===================================================
"""
import pdb, argparse, tempfile, collections, os
from collections import OrderedDict
import csv, xlrd, unicodecsv
from sqlalchemy.orm import class_mapper
from . import version

class invalidParameter(Exception):
    pass


class parameterError(Exception):
    pass


class _objdict(dict):
    __doc__ = '\n    subclass dict to make it work like an object\n\n    see http://goodcode.io/articles/python-dict-object/\n    '

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError('No such attribute: ' + name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError('No such attribute: ' + name)


def record2csv(inrecs, mapping, outfile=None):
    """
    convert list of dict or object records to a csv list or file based on a specified mapping
    
    :param inrecs: list of dicts or objects
    :param mapping: OrderedDict {'outfield1':'infield1', 'outfield2':outfunction(inrec), ...} or ['inoutfield1', 'inoutfield2', ...]
    :param outfile: optional output file
    :rtype: lines from output file
    """
    if isinstance(mapping, list):
        mappingtype = list
    else:
        if type(mapping) in [dict, OrderedDict]:
            mappingtype = dict
        else:
            raise invalidParameter('invalid mapping type {}. mapping type must be list, dict or OrderedDict').with_traceback(format(type(mapping)))
    outfields = []
    for outfield in mapping:
        invalue = mapping[outfield] if mappingtype == dict else outfield
        if not isinstance(invalue, str):
            if not callable(invalue):
                raise invalidParameter('invalid mapping {}. mapping values must be str or function'.format(invalue))
        outfields.append(outfield)

    outreclist = wlist()
    coutreclist = csv.DictWriter(outreclist, outfields)
    coutreclist.writeheader()
    for inrec in inrecs:
        if isinstance(inrec, dict):
            inrec = _objdict(inrec)
        outrow = {}
        for outfield in mapping:
            infield = mapping[outfield] if mappingtype == dict else outfield
            if isinstance(infield, str):
                outvalue = getattr(inrec, infield, None)
            else:
                outvalue = infield(inrec)
            outrow[outfield] = outvalue

        coutreclist.writerow(outrow)

    if outfile:
        with open(outfile, 'wb') as (out):
            out.writelines(outreclist)
    return outreclist


class Base2Csv:
    __doc__ = '\n    base class for any file to csv conversion\n    \n    :param outdir: directory to put output file(s) -- if None, temporary directory is used\n    '

    def __init__(self, filename, outdir=None, hdrmap=None):
        """
        """
        self.filename = filename
        self.tempdir = False
        if outdir is None:
            self.tempdir = True
            outdir = tempfile.mkdtemp(prefix='csvwt-')
        self.dir = outdir
        self.files = collections.OrderedDict()

    def __del__(self):
        """
        release resources
        """
        if self.tempdir:
            for name in self.files:
                os.remove(self.files[name])

            os.rmdir(self.dir)

    def getfiles(self):
        """
        get sheetnames and file pathnames produced
        
        :rtype: OrderedDict{sheet:pathname,...}
        """
        return self.files


class Xls2Csv(Base2Csv):
    __doc__ = '\n    create csv file(s) from xlsx (or xls) sheets\n    \n    :param filename: name of file to convert\n    :param outdir: directory to put output file(s) -- if None, temporary directory is used\n    :param hdrmap: maps input header to csv header -- if None, input header is used as csv header\n    '

    def __init__(self, filename, outdir=None, hdrmap=None):
        """
        """
        super().__init__(filename, outdir=outdir)
        wb = xlrd.open_workbook(filename)
        for name in wb.sheet_names():
            sheet = wb.sheet_by_name(name)
            if sheet.nrows == 0:
                pass
            else:
                inhdr = sheet.row_values(0)
                if hdrmap is not None:
                    outhdr = [hdrmap[k] for k in hdrmap]
                else:
                    hdrmap = dict(list(zip(inhdr, inhdr)))
                    outhdr = inhdr
                self.files[name] = '{0}/{1}.csv'.format(self.dir, name)
                OUT = open(self.files[name], 'wb')
                writer = unicodecsv.DictWriter(OUT, outhdr)
                writer.writeheader()
                for row in range(1, sheet.nrows):
                    inrow = dict(list(zip(inhdr, sheet.row_values(row))))
                    outrow = {}
                    for incol in inhdr:
                        if incol in hdrmap:
                            outrow[hdrmap[incol]] = inrow[incol]

                    writer.writerow(outrow)

                OUT.close()

        wb.release_resources()


class Db2Csv(Base2Csv):
    __doc__ = '\n    create csv file(s) from db tables\n        \n    :param outdir: directory to put output file(s) -- if None, temporary directory is used\n    '

    def __init__(self, outdir=None):
        """
        """
        super().__init__('', outdir=outdir)

    def addtable(self, name, session, model, hdrmap=None, **kwargs):
        """
        insert a new element or update an existing on based on kwargs query
        
        hdrmap may be of the form {infield1:{outfield:function,...},infield2:outfield2,...},
        
            where:
                
                outfield is the column name
                function is defined as function(session,value), session is database session and value is the value of the inrow[infield]
                
                this allows multiple output columns, each tranformed from the input by a different function
        
        :param name: 'sheet' name, used to name output file
        :param session: session within which update occurs
        :param model: table model
        :param hdrmap: maps input table column names to csv header -- if None, input table column names are used as csv header
        :param **kwargs: used for db filter
        """
        inhdr = []
        for col in class_mapper(model).columns:
            inhdr.append(col.key)

        if hdrmap is not None:
            outhndlr = [hdrmap[k] for k in hdrmap]
            outhdr = []
            for k in outhndlr:
                if isinstance(k, str):
                    outhdr.append(k)
                else:
                    if isinstance(k, dict):
                        for subk in k:
                            if not isinstance(subk, str):
                                raise parameterError('{0}: invalid hdrmap {1}'.format(self.filename, hdrmap))
                            outhdr.append(subk)

                    else:
                        raise parameterError('{0}: invalid hdrmap {1}'.format(self.filename, hdrmap))

        else:
            hdrmap = dict(list(zip(inhdr, inhdr)))
            outhdr = inhdr
        self.files[name] = '{0}/{1}.csv'.format(self.dir, name)
        OUT = open(self.files[name], 'wb')
        writer = unicodecsv.DictWriter(OUT, outhdr)
        writer.writeheader()
        for inrow in (session.query(model).filter_by)(**kwargs).all():
            outrow = {}
            for incol in inhdr:
                if incol in hdrmap:
                    outcol = hdrmap[incol]
                    if isinstance(outcol, str):
                        outrow[outcol] = getattr(inrow, incol)
                    else:
                        for subk in outcol:
                            outrow[subk] = outcol[subk](session, getattr(inrow, incol))

            writer.writerow(outrow)

        OUT.close()


class wlist(list):
    __doc__ = '\n    extends list to include a write method, in order to allow csv.writer to output to the list\n    '

    def write(self, line):
        """
        write method to be added to list object.  Appends line to the list
        
        :param line: line to append to the list
        """
        self.append(line)


def main():
    """
    unit tests
    """
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('-d', '--dbfilename', help='name of db file for testing')
    args = parser.parse_args()
    dbfilename = args.dbfilename
    from running import racedb
    racedb.setracedb(dbfilename)
    s = racedb.Session()
    dd = Db2Csv()
    hdrmap = {'dateofbirth':'DOB', 
     'gender':'Gender',  'name':{'First':lambda f: ' '.join(f.split(' ')[0:-1]), 
      'Last':lambda f: f.split(' ')[(-1)]}, 
     'hometown':{'City':lambda f: ','.join(f.split(',')[0:-1]), 
      'State':lambda f: f.split(',')[(-1)]}}
    dd.addtable('Sheet1', s, (racedb.Runner), hdrmap, active=True)
    files = dd.getfiles()
    pdb.set_trace()


if __name__ == '__main__':
    main()
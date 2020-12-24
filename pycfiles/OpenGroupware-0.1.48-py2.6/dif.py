# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/api_dif/dif.py
# Compiled at: 2012-10-12 07:02:39
"""dif.py -- Navy DIF file handler"""
__version__ = '1.1'

class DIFError(StandardError):
    pass


class DIF:

    def __init__(self, file):
        line = file.readline().rstrip().upper()
        header = 1
        self.data = []
        self.header = {}
        self.vectors = []
        while line:
            if header:
                if line == 'DATA':
                    header = 0
                    tup = None
                    file.readline()
                    file.readline()
                else:
                    line = line.lower()
                    n = map(int, file.readline().rstrip().split(','))
                    s = file.readline().strip()[1:-1]
                    n.append(s)
                    if self.header.has_key(line):
                        if type(self.header[line]) is type(()):
                            self.header[line] = [
                             self.header[line], tuple(n)]
                        else:
                            self.header[line].append(tuple(n))
                    else:
                        self.header[line] = tuple(n)
                    if line == 'vectors':
                        self.vectors = map(lambda x: 'FIELD%d' % x, range(n[1]))
                    elif line == 'label' and n[1] == 0:
                        self.vectors[n[0] - 1] = n[2]
            else:
                nums = map(int, line.split(','))
                strv = file.readline().rstrip()
                if nums[0] == -1:
                    if strv == 'BOT':
                        if tup:
                            self.data.append(tup)
                        tup = []
                    else:
                        if strv == 'EOD':
                            self.data.append(tup)
                            tup = []
                            return
                        raise DIFError, 'Invalid Special Data Value [%s]' % strv
                elif nums[0] == 0:
                    if strv == 'V' or strv == 'TRUE' or strv == 'FALSE':
                        tup.append(nums[1])
                    elif strv == 'NA' or strv == 'ERROR':
                        tup.append(None)
                    else:
                        raise DIFError, 'Invalid Numeric Data Type [%s]' % strv
                elif nums[0] == 1:
                    strv = strv.strip()
                    if strv[0:1] == '"':
                        strv = strv[1:-1]
                    tup.append(strv)
                else:
                    raise DIFError, 'Invalid Type Indicator [%d]' % nums[0]
            line = file.readline().rstrip().upper()

        return

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        row = self.data[key]
        rc = {}
        for i in range(len(row)):
            rc[self.vectors[i]] = row[i]

        return rc


if __name__ == '__main__':
    from distutils.core import setup, Extension
    setup(name='DIF', version=__version__, description='dif.py', long_description='Navy DIF file handler', author='Chris Gonnerman', author_email='chris.gonnerman@newcenturycomputers.net', url='http://newcenturycomputers.net/projects/dif.html', py_modules=[
     'dif'])
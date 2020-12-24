# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: krnet/kreaction.py
# Compiled at: 2015-07-17 10:50:12
# Size of source mod 2**32: 1910 bytes


class KReaction:

    def __init__(self, re=None):
        self._id = ''
        self.subs = []
        self.subcoef = []
        self.prods = []
        self.procoef = []
        self.enzs = []
        if re[0].startswith('ENTRY'):
            if re[(len(re) - 1)].startswith('//'):
                self._id = re[0][12:20].strip()
                for ln in re[1:]:
                    if ln.startswith('EQUATION'):
                        temp = ln[12:].split('<=>')
                        if len(temp) > 2 and len(temp) < 2:
                            print('File not compatible with KEGG REACTION format specifications!! Please check!!')
                        else:
                            tp = temp[0].split('+')
                            for c in tp:
                                c = c.strip()
                                cco = c.split(' ')
                                if len(cco) > 1:
                                    self.subcoef.append(int(cco[0]))
                                    self.subs.append(cco[1])
                                else:
                                    self.subcoef.append(1)
                                    self.subs.append(c)

                            tp = temp[1].split('+')
                            for c in tp:
                                c = c.strip()
                                cco = c.split(' ')
                                if len(cco) > 1:
                                    self.procoef.append(int(cco[0]))
                                    self.prods.append(cco[1])
                                else:
                                    self.procoef.append(1)
                                    self.prods.append(c)

                    elif ln.startswith('ENZYME'):
                        temp = ln[12:].split(' ')
                        if temp.count('') > 0:
                            while temp.count('') > 0:
                                temp.remove('')

                        for e in temp:
                            self.enzs.append(e)

                        continue

    def number_of_substrates(self):
        return len(self.subs)

    def number_of_products(self):
        return len(self.prods)

    def number_of_enzymes(self):
        return len(self.enzs)

    def id(self):
        return self._id

    def enzymes(self):
        return self.enzs

    def enzyme(self, i):
        return self.enzs[i]

    def substrates(self):
        return self.subs

    def substrate(self, i):
        return self.subs[i]

    def products(self):
        return self.prods

    def product(self, i):
        return self.prods[i]
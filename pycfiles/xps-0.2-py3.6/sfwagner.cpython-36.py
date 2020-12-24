# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-6.5-amd64/egg/xps/sfwagner.py
# Compiled at: 2019-10-13 09:08:45
# Size of source mod 2**32: 3627 bytes
"""
sfwagner.py

X-Ray photoelectron spectroscopy (XPS) Wagner sensitivity factors (sf), this
is required for any corrections on any XPS machine.

The xps/data/sfwagner.db contains Wagner sensitivity factors from

"Practical Surface Analysis by Auger and X-ray Photoelectron Spectroscopy",
D. Briggs and M. P. Seah,
Appendix 5, p511-514,
Published by J. Wiley and Sons in 1983, ISBN 0-471-26279

Appendix 5: Empirically derived set of atomic sensitivity factors for XPS

Copyright (c) 1983 by John Wiley & Sons Ltd.

The data in Appendix 5 is reproduced and provided here for non-profit use with
permission of the publisher John Wiley & Sons Ltd.

For non-profit use as framework system calls or as a reference.
This permission does not include the right to grant others permission to
photocopy or otherwise reproduce this material except for accessible versions
made by non-profit organizations serving the blind, visually impaired and other
persons with print disabilities (VIPs).

The original set of data first appeared in the following resource:
C. D. Wagner, L. E. Davis, M. V. Zeller, J. A. Taylor, R. M. Raymond and L. H. Gale,
Surf. Interface Anal., 3. 211 (1981)

Any use of this data must include the citations above in any work.
"""
import os.path as _path, sqlite3 as _sqlite3
ROOTPATH = _path.dirname(_path.abspath(__file__))
DATAPATH = _path.join(ROOTPATH, 'data')
SFWAGNER_DB = _path.join(DATAPATH, 'sfwagner.db')

class Shell:

    def __init__(self, elem):
        self.element = elem

    def __str__(self):
        s = 'Has the following attributes: '
        if hasattr(self, 'area'):
            s += '.area '
        if hasattr(self, 'height'):
            s += '.height '
        return s


class SensitivityFactors:

    def __init__(self):
        conn = _sqlite3.connect(SFWAGNER_DB)
        cur = conn.cursor()
        query = 'SELECT DISTINCT element FROM wagner'
        element = [row[0] for row in cur.execute(query)]
        for e in element:
            query = 'SELECT shell FROM wagner WHERE element=="{elem}"'
            shell = [row[0] for row in cur.execute(query.format(elem=e))]
            shell_dict = {}
            for s in shell:
                shell_dict[s] = dict()
                query = 'SELECT area, height FROM wagner WHERE element=="{elem}" AND shell=="{sh}"'
                res = cur.execute(query.format(elem=e, sh=s))
                area, height = res.fetchone()
                if area is not None:
                    shell_dict[s]['area'] = area
                if height is not None:
                    shell_dict[s]['height'] = height

            setattr(self, e, shell_dict)


if __name__ == '__main__':
    pass
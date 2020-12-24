# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/mail.py
# Compiled at: 2018-09-07 05:20:19
# Size of source mod 2**32: 356 bytes
"""A Wrapper for the mail command line"""
import subprocess as sbp

def sendmail(subject='objet', body=b'bit sting body'):
    """Sand the emal to Antoine Tavant"""
    adress = 'antoine.tavant@lpp.polytechnique.fr'
    iout = sbp.run(['mail', '-s', subject, adress], input=body)
    print(iout)


if __name__ == '__main__':
    sendmail('test', b'o\n')
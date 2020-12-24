# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazelleapi/__init__.py
# Compiled at: 2016-12-20 08:39:16
"""
We use this to store the constants for the program, as well as make a nice little shortcut
for importing GazelleAPI in third-party scripts (so you don't have to do gazelleapi.gazelleapi
"""
from .gazelleapi import GazelleAPI
__version__ = '0.1.4'
__author__ = 'itismadness'
__author_email__ = 'it.is.madness@gmail.com'
__url__ = 'https://github.com/itismadness/gazelleapi'
__description__ = "GazelleAPI is a handy interface for interacting with gazelle based\ntrackers. This should work on Python 2 and 3.\n\nIt is based on `whatapi <https://github.com/isaaczafuta/whatapi>`_ and `xanaxbetter <https://github.com/rguedes/xanaxbetter>`_.\n\n************\nInstallation\n************\n\nPip\n---\n\n.. code:: bash\n\n    pip install gazelleapi\n\nSource\n------\n.. code:: bash\n\n    git clone https://github.com/itismadness/gazelleapi\n    cd gazelleapi\n    python setup.py install\n\n*****\nUsage\n*****\n\n.. code:: bash\n\n    >>> from gazelleapi import GazelleAPI\n    >>> api = GazelleAPI(username='user', password='pass', hostname='example.com')\n    >>> api.request('index')\n\nTo avoid having to always login to the site, we suggest using cookies in the following manner:\n\n.. code:: bash\n\n    >>> from gazelleapi import GazelleAPI\n    >>> import pickle\n    >>> cookies = pickle.load(open('cookies.dat', 'rb'))\n    >>> api = GazelleAPI(username='user', password='pass', hostname='example.com', cookies=cookies)\n\nand to save the cookie on an open session:\n\n.. code:: bash\n\n    >>> pickle.dump(api.session.cookies, open('cookies.dat', 'wb'))\n"
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/__init__.py
# Compiled at: 2013-04-04 15:36:36
"""The Muntjac base package. Contains the Application class, the
starting point of any application that uses Muntjac.

Contains all Muntjac core classes. A Muntjac application is based
on the L{Application} class and deployed as a servlet
using L{ApplicationServlet} or L{GaeApplicationServlet}
(for Google App Engine).

All classes in Muntjac are pickleable unless otherwise noted.
This allows Muntjac applications to run in cluster and cloud
environments.
"""
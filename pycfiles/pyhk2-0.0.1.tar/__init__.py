# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/__init__.py
# Compiled at: 2006-06-21 07:37:34
__doc__ = "\nPyHJB is a python client library for accessing JMS 1.1 (Java Message\nService) messaging providers via HJB, the HTTP JMS bridge.\n\n`HJB`_ provides access to JMS resources via HTTP.  It acts as an HTTP\ngateway server for any JMS messaging provider, and provides a RESTful\nequivalent for most of the non-optional portions of the JMS API.\n\n.. _HJB: http://hjb.berlios.de\n\nPyHJB is a pure python package which, via HJB, allows python programs\nto:\n\n* send/receive messages from **any** Enterprise Messaging System that\n  supports JMS.  It is distributed with a few demo scripts showing it\n  being used with a selection of well-known messaging providers:\n  WebSphere MQ, Swift MQ, Active MQ and JBoss Messaging.\n\n* register JMS administrable objects via JMS, e.g, queues, topics and\n  connection factories.\n\n* configure JMS runtime objects, e.g, connections, sessions, message\n  consumers, message producers, queue browsers and durable subscribers\n  etc.\n\nImportantly, python programs written using PyHJB are portable across\nJMS messaging providers.  The programs use the JMS API via HTTP rather\nthan a vendor's custom messaging API, and thus combine two important\nmaintainability traits:\n\n* the use of the JMS API\n\n* being written in python!\n\n"
__docformat__ = 'restructuredtext en'
__version__ = '0.5.1'
__author__ = 'Tim Emiola <tbetbe@users.berlios.de>'
__url__ = 'http://hjb.python-hosting.com'
__license__ = 'GNU Lesser General Public License (LGPL)'
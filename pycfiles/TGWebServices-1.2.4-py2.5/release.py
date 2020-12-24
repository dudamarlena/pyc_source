# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgwebservices/release.py
# Compiled at: 2010-08-30 04:29:56
version = '1.2.4'
description = 'Multiprotocol Web Services for TurboGears'
long_description = "TurboGears gives you a plain HTTP with JSON return\nvalues API for your application for free. This isn't always what you want,\nthough. Sometimes, you don't want to expose all of the data to the web\nthat you need to render your templates. Maybe you need to support a\nprotocol that names the function it's calling as part of what it POSTs\nsuch as SOAP or XML-RPC.\n\nTGWebServices provides a super simple API for creating web services that\nare available via SOAP, HTTP->XML, and HTTP->JSON. The SOAP API generates\nWSDL automatically for your Python and even generates enough type\ninformation for statically typed languages (Java and C#, for example) to\ngenerate good client code on their end.\n\nHow easy is it?\n\n::\n\n    class Multiplier(WebServicesRoot):\n\n        @wsexpose(int)\n        @wsvalidate(int, int)\n        def multiply(self, num1, num2):\n            return num1 * num2\n\nWith this at the root, SOAP clients can find the WSDL file at /soap/api.wsdl\nand POST SOAP requests to /soap/. HTTP requests to /multiply?num1=5&num2=20\nwill return an XML document with the result of 100. Add ?tg_format=json (or\nan HTTP Accept: text/javascript header) and you'll get JSON back.\n\nThe great thing about this is that the code above looks like a '''normal\nPython function''' and doesn't know a thing about web services.\n\nA more complete documentation can be found at\nhttp://wiki.tgws.googlecode.com/hg/index.html.\n\nFeatures\n--------\n\n* Easiest way to expose a web services API\n* Supports SOAP, HTTP+XML, HTTP+JSON\n* Outputs wrapped document/literal SOAP, which is the most widely\n  compatible format\n* Provides enough type information for statically typed languages\n  to generate conveniently usable interfaces\n* Can output instances of your own classes\n* Can also accept instances of your classes as input\n* Works with TurboGears 1.0 and 1.1\n* MIT license allows for unrestricted use"
author = 'Kevin Dangoor, Christophe de Vienne'
email = 'turbogears-web-services@googlegroups.com'
copyright = 'Copyright 2006, 2007 Kevin Dangoor, Arbor Networks. 2008-2010 The TGWebServices development team.'
url = 'http://code.google.com/p/tgws/'
license = 'MIT'
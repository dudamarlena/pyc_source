# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\basic.py
# Compiled at: 2017-03-24 09:14:35
from evgen.core import SessionTemplate, GenericEventTemplate
from evgen.writers import ConsoleWriter
session = SessionTemplate()
session.add_event(GenericEventTemplate('start'), probability=1, delay=5000)
session.add_event(GenericEventTemplate('stop'), probability=1)
session.add_writer(ConsoleWriter())
session.generate()
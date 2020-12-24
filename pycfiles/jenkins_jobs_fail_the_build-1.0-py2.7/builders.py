# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jenkins_jobs_fail_the_build/builders.py
# Compiled at: 2015-09-24 12:40:15
import xml.etree.ElementTree as XML, logging
logger = logging.getLogger(__name__)

def set_build_result(parser, xml_parent, data):
    t = XML.SubElement(xml_parent, 'org.jenkins_ci.plugins.fail_the_build.FixResultBuilder')
    XML.SubElement(t, 'defaultResultName').text = data.upper()
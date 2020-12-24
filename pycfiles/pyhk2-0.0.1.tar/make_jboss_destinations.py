# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/scripts/make_jboss_destinations.py
# Compiled at: 2006-06-04 05:57:12
__doc__ = '\nSimple script for automatically creating a xxx-service.xml file that adds the\nHJB demo queues to a JBoss Messaging server.\n\nShould be invoked as follows:\n\n  make_jboss_destinations.py [jboss-service-filename]\n\n  e.g. python make_jboss_destinations.py C:\\jboss4xx\\server\\messaging\\deploy\\hjb-demo-service.xml\n  \njboss-service-filename is optional, if its not supplied, generated service file\nis dumped to stdout\n\n'
from os.path import isfile
import sys
from xml.dom.minidom import parseString
from hjbjboss import topic_aliases, queue_aliases
__docformat__ = 'restructuredtext en'
service_xml_template = '<?xml version="1.0" encoding="UTF-8"?>\n<server>\n  <loader-repository>jboss.messaging:loader=ScopedLoaderRepository\n    <loader-repository-config>java2ParentDelegation=false</loader-repository-config>\n  </loader-repository>\n  %s\n</server>\n'
queue_mbean_template = '\n  <mbean code="org.jboss.jms.server.destination.Queue"\n         name="jboss.messaging.destination:service=Queue,name=%s"\n         xmbean-dd="xmdesc/Queue-xmbean.xml">\n    <depends optional-attribute-name="ServerPeer">jboss.messaging:service=ServerPeer</depends>\n      <attribute name="SecurityConfig">\n        <security>\n          <role name="guest" read="true" write="true"/>\n          <role name="publisher" read="true" write="true" create="false"/>\n          <role name="noacc" read="false" write="false" create="false"/>\n        </security>\n      </attribute>\n  </mbean>\n'
topic_mbean_template = '\n  <mbean code="org.jboss.jms.server.destination.Topic"\n         name="jboss.messaging.destination:service=Topic,name=%s"\n         xmbean-dd="xmdesc/Topic-xmbean.xml">\n     <depends optional-attribute-name="ServerPeer">jboss.messaging:service=ServerPeer</depends>\n     <attribute name="SecurityConfig">\n        <security>\n           <role name="guest" read="true" write="true" create="true"/>\n           <role name="publisher" read="true" write="true" create="false"/>\n           <role name="durpublisher" read="true" write="true" create="true"/>\n        </security>\n     </attribute>\n  </mbean>\n'

def write_service_xml_text(queues=None, topics=None, fd=None):
    """Create a jboss service_xml file and write it to file-like object `fd`
       
    Creates a jboss service.xml file that contains topic and queue
    configuration for a JBoss messaging server.  
    
    `queues` should be a list containing queue names.  Each queue will
    be configured using `queue_mbean_template` as a template.

    `topics` should be a list cointaining topic names.  Each topic
    will be configured using `topic_mbean_template` as a template.

    `fd` is a file-like object to which the configuration XML  will be written.

    """
    if not queues:
        queues = [
         'testQueue']
    if not topics:
        topics = [
         'testTopic']
    if not fd:
        fd = sys.stdout
    queue_text = ('').join([ queue_mbean_template % s.replace('/queue/', '') for s in queues ])
    topic_text = ('').join([ topic_mbean_template % s.replace('/topic/', '') for s in topics ])
    all_text = service_xml_template % (queue_text + topic_text)
    parseString(all_text)
    fd.write(all_text)


def open_file_if_specified():
    """Attempts to open sys.argv[1] as file and return the opened file.

    Returns `None` if file operation fails or if sys.argv[1] is not present.  

    """
    if len(sys.argv) > 1:
        try:
            return file(sys.argv[1], 'w')
        except:
            print '[** Error ***] could not open file ', sys.argv[1]
            return

    return


def main():
    fd = open_file_if_specified()
    write_service_xml_text(queues=queue_aliases.values(), topics=topic_aliases.values(), fd=fd)
    if fd:
        fd.close()


if __name__ == '__main__':
    main()
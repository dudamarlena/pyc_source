# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/websetup.py
# Compiled at: 2010-08-26 11:01:50
"""Setup the pyf.services application"""
import logging, sys, transaction
from tg import config
from pyf.services.config.environment import load_environment
__all__ = [
 'setup_app_command',
 'setup_app']
log = logging.getLogger(__name__)

def setup_app_command():
    if len(sys.argv) < 2:
        raise ValueError, 'Please provide a .ini file'
    ini_file = sys.argv[1]
    from paste.deploy import appconfig
    conf = appconfig('config:%s' % ini_file, relative_to='./')
    setup_app(sys.argv[0], conf, sys.argv[2:])


def setup_app(command, conf, vars):
    """Place any commands to setup pyf.services here"""
    load_environment(conf.global_conf, conf.local_conf)
    from pyf.services import model
    from pyf.services.model import DBSession
    print 'Creating tables'
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)
    if not DBSession.query(model.User).filter(model.User.email_address == 'manager@somedomain.com').first():
        manager = model.User()
        manager.user_name = 'manager'
        manager.display_name = 'Example manager'
        manager.email_address = 'manager@somedomain.com'
        manager.password = 'managepass'
        model.DBSession.add(manager)
    if not DBSession.query(model.Group).filter(model.Group.group_name == 'managers').first():
        group = model.Group()
        group.group_name = 'managers'
        group.display_name = 'Managers Group'
        group.users.append(manager)
        model.DBSession.add(group)
    if not DBSession.query(model.Permission).filter(model.Permission.permission_name == 'manage').first():
        permission = model.Permission()
        permission.permission_name = 'manage'
        permission.description = 'This permission give an administrative right to the bearer'
        permission.groups.append(group)
        model.DBSession.add(permission)
    if not DBSession.query(model.User).filter(model.User.email_address == 'editor@somedomain.com').first():
        editor = model.User()
        editor.user_name = 'editor'
        editor.display_name = 'Example editor'
        editor.email_address = 'editor@somedomain.com'
        editor.password = 'editpass'
        model.DBSession.add(editor)
    model.DBSession.flush()
    desc = setup_sample_descriptor(model)
    if desc is not None:
        (tube, tubelayer) = setup_sample_tube(model)
        dispatch = setup_dispatch(model, '3 col csv dispatcher', tube, desc, tubelayer.variant_name)
    transaction.commit()
    print 'Successfully setup'
    return


def setup_sample_descriptor(model):
    from pyf.services.model import DBSession
    if not DBSession.query(model.Descriptor).filter(model.Descriptor.name == 'simple_csv').first():
        print 'creating descriptor'
        desc = model.Descriptor(display_name='Simple CSV descriptor', default_encoding='UTF-8', name='simple_csv', description='', payload_xml='<descriptor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="descriptor.xsd">\n        <header>\n            <format name="csv">\n                <startline>1</startline>\n                <delimiter>;</delimiter>\n            </format>\n        </header>\n        <fields>\n            <field name="Field1" mandatory="true">\n                <source>1</source>\n                <type>int</type>\n            </field>\n            <field mandatory="false" name="Field2">\n                <source>2</source>\n                <type>string</type>\n            </field>\n            <field mandatory="false" name="Field3">\n                <source>3</source>\n                <type>string</type>\n            </field>\n            <field mandatory="false" name="Field4">\n                <source>4</source>\n                <type>string</type>\n            </field>\n        </fields>\n    </descriptor>\n            ')
        model.DBSession.add(desc)
        model.DBSession.flush()
        return desc
    else:
        return
        return


def setup_sample_tube(model):
    tube = model.Tube(name='simple', display_name='Simple tube for 3 fields parsing', description='- Encloses the XML Writer in a new node that adds a Field4 column\n- Modifies the XML Writer template to show that column\n- Removes the CSV writer', payload='<config>\n  <process name="ledger">\n    <node type="producer" pluginname="descriptorsource" name="source">\n      <children>\n        <node type="consumer" pluginname="csvwriter" name="writer_csv">\n          <columns>\n            <column>Field1</column>\n            <column>Field2</column>\n            <column>Field3</column>\n          </columns>\n          <encoding>UTF-8</encoding>\n          <delimiter>;</delimiter>\n          <target_filename>test_file_%Y%m%d_%H%M%S.csv</target_filename>\n        </node>\n        <node type="consumer" pluginname="xmlwriter" name="writer_xml">\n          <encoding>UTF-8</encoding>\n          <target_filename>test_file_%Y%m%d_%H%M%S.xml</target_filename>\n          <template type="embedded">\n            <![CDATA[\n<?xml version="1.0" encoding="UTF-8"?>\n<records xmlns:py="http://genshi.edgewall.org/"\nxmlns:xi="http://www.w3.org/2001/XInclude">\n  <record py:for="record in datas">\n    <FieldA py:content="record.Field1" />\n    <FieldB py:content="record.Field2" />\n    <FieldC py:content="record.Field3" />\n  </record>\n</records>\n            ]]>\n          </template>\n        </node>\n      </children>\n    </node>\n  </process>\n</config>')
    model.DBSession.add(tube)
    model.DBSession.flush()
    tubelayer = model.TubeLayer(tube_id=tube.id, name='recap_adder', variant_name='sample', display_name='Adds a recapitulative column', description='', active=True, payload='<modifiers>\n  <modifier target="writer_xml" action="enclose">\n    <node type="adapter" from="code" name="field4_adder">\n      <code type="function">\n        <![CDATA[\ndef iterator(input):\n    for i, value in enumerate(input):\n        setattr(value, \'Field4\', str(i*2))\n        yield value\n]]>\n      </code>\n    </node>\n  </modifier>\n  <modifier target="writer_xml" action="modify">\n    <template type="embedded">\n      <![CDATA[\n<?xml version="1.0" encoding="UTF-8"?>\n<records xmlns:py="http://genshi.edgewall.org/"\nxmlns:xi="http://www.w3.org/2001/XInclude">\n  <record py:for="record in datas">\n    <FieldA py:content="record.Field1" />\n    <FieldB py:content="record.Field2" />\n    <FieldC py:content="record.Field3" />\n    <FieldD py:content="record.Field4" />\n  </record>\n</records>\n            ]]>\n    </template>\n  </modifier>\n  <modifier target="writer_csv" action="remove" />\n</modifiers>')
    model.DBSession.add(tubelayer)
    model.DBSession.flush()
    return (
     tube, tubelayer)


def setup_dispatch(model, display_name, tube, descriptor, variant_name):
    dispatch = model.Dispatch(display_name=display_name, name=display_name.lower().replace(' ', '_'), description='', tube_id=tube.id, descriptor_id=descriptor.id, variant_name=variant_name)
    model.DBSession.add(dispatch)
    model.DBSession.flush()
    return dispatch
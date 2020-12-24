# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/tool/functions.py
# Compiled at: 2019-11-09 06:47:30
# Size of source mod 2**32: 6259 bytes
from __future__ import print_function
import atexit
from dataclay.api import init_connection
from jinja2 import Template
import os, sys
from uuid import UUID
from dataclay.communication.grpc.messages.common.common_messages_pb2 import LANG_PYTHON
from dataclay.util.StubUtils import deploy_stubs
from dataclay.util.StubUtils import prepare_storage
from dataclay.util.YamlParser import dataclay_yaml_dump, dataclay_yaml_load
from dataclay.util.tools.python.PythonMetaClassFactory import MetaClassFactory

def _establish_client():
    client = init_connection(os.getenv('DATACLAYCLIENTCONFIG', './cfgfiles/client.properties'))
    atexit.register(lambda : client.close())
    return client


def register_model(username, password, namespace, python_path):
    client = _establish_client()
    credential = (
     None, password)
    user_id = client.get_account_id(username)
    mfc = MetaClassFactory(namespace=namespace, responsible_account=username)
    full_python_path = os.path.abspath(python_path)
    if full_python_path not in sys.path:
        added_to_path = True
        sys.path.insert(0, full_python_path)
    else:
        added_to_path = False
    n_base_skip = len(full_python_path.split(os.sep))
    for dirpath, dirnames, filenames in os.walk(full_python_path):
        base_import = '.'.join(dirpath.split(os.sep)[n_base_skip:])
        for f in filenames:
            if not f.endswith('.py'):
                continue
            elif f == '__init__.py':
                if not base_import:
                    print('Ignoring `__init__.py` at the root of the model folder (do not put classes there!)', file=(sys.stderr))
                    continue
                import_str = base_import
            else:
                if not base_import:
                    import_str = os.path.splitext(f)[0]
                else:
                    import_str = '%s.%s' % (base_import, os.path.splitext(f)[0])
            mfc.import_and_add(import_str)

    result = client.new_class(user_id, credential, LANG_PYTHON, mfc.classes)
    print(('Was gonna register: %s\nEventually registered: %s' % (mfc.classes, result.keys())), file=(sys.stderr))
    if len(result.keys()) == 0:
        print('No classes registered, exiting', file=(sys.stderr))
        return
    interfaces = list()
    interfaces_in_contract = list()
    for class_name, class_info in result.items():
        ref_class_name = class_name.replace('.', '')
        interfaces.append(Template('\n{{ class_name }}interface: &{{ ref_class_name }}iface !!es.bsc.dataclay.util.management.interfacemgr.Interface\n  providerAccountName: {{ username }}\n  namespace: {{ namespace }}\n  classNamespace: {{ namespace }}\n  className: {{ class_name }}\n  propertiesInIface: !!set {% if class_info.properties|length == 0 %} { } {% endif %}\n  {% for property in class_info.properties %}\n     ? {{ property.name }}\n  {% endfor %}\n  operationsSignatureInIface: !!set {% if class_info.operations|length == 0 %} { } {% endif %}\n  {% for operation in class_info.operations %} \n    ? {{ operation.nameAndDescriptor }}\n  {% endfor %}\n').render(class_name=class_name,
          ref_class_name=ref_class_name,
          username=username,
          namespace=namespace,
          class_info=class_info))
        interfaces_in_contract.append(Template('\n    - !!es.bsc.dataclay.util.management.contractmgr.InterfaceInContract\n      iface: *{{ ref_class_name }}iface\n      implementationsSpecPerOperation: !!set {% if class_info.operations|length == 0 %} { } {% endif %}\n        {% for operation in class_info.operations %}\n          ? !!es.bsc.dataclay.util.management.contractmgr.OpImplementations\n            operationSignature: {{ operation.nameAndDescriptor }}\n            numLocalImpl: 0\n            numRemoteImpl: 0\n        {% endfor %}\n').render(class_name=class_name,
          ref_class_name=ref_class_name,
          class_info=class_info))

    contract = Template('\n{{ namespace }}contract: !!es.bsc.dataclay.util.management.contractmgr.Contract\n  beginDate: 1980-01-01T00:00:01\n  endDate: 2055-12-31T23:59:58\n  namespace: {{ namespace }}\n  providerAccountID: {{ user_id }}\n  applicantsAccountsIDs:\n    ? {{ user_id }}\n  interfacesInContractSpecs:\n{{ interfaces_in_contract }}\n  publicAvailable: True\n').render(user_id=user_id,
      namespace=namespace,
      interfaces_in_contract=('\n'.join(interfaces_in_contract)))
    yaml_request = '\n'.join(interfaces) + contract
    yaml_response = client.perform_set_of_operations(user_id, credential, yaml_request)
    response = dataclay_yaml_load(yaml_response)
    print(' ===> The ContractID for the registered classes is:', file=(sys.stderr))
    print(response['contracts'][('%scontract' % namespace)])
    if added_to_path:
        sys.path.remove(full_python_path)
    return str(response['contracts'][('%scontract' % namespace)])


def get_stubs(username, password, contract_ids_str, path):
    client = _establish_client()
    try:
        contracts = list(map(UUID, contract_ids_str.split(',')))
    except ValueError:
        raise ValueError('This is not a valid list of contracts: %s' % contract_ids_str)

    credential = (
     None, password)
    user_id = client.get_account_id(username)
    prepare_storage(path)
    babel_data = client.get_babel_stubs(user_id, credential, contracts)
    with open(os.path.join(path, 'babelstubs.yml'), 'wb') as (f):
        f.write(babel_data)
    all_stubs = client.get_stubs(user_id, credential, LANG_PYTHON, contracts)
    for key, value in all_stubs.items():
        with open(os.path.join(path, key), 'wb') as (f):
            f.write(value)

    deploy_stubs(path)
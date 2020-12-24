# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyazure\pyazure.py
# Compiled at: 2012-01-28 13:53:21
__doc__ = '\nPython wrapper around Windows Azure storage and management APIs\n\nAuthors:\n    Sriram Krishnan <sriramk@microsoft.com>\n    Steve Marx <steve.marx@microsoft.com>\n    Tihomir Petkov <tpetkov@gmail.com>\n    Blair Bethwaite <blair.bethwaite@gmail.com>\n\nLicense:\n    GNU General Public Licence (GPL)\n    \n    This file is part of pyazure.\n    \n    pyazure is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyazure is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with pyazure. If not, see <http://www.gnu.org/licenses/>.\n'
import sys
from util import *
from storage import *

class PyAzure(object):
    """Class exposing Windows Azure storage and, if initialised appropriately,
    service management operations.    
    """

    def __init__(self, storage_account_name=None, storage_account_key=None, use_path_style_uris=False, management_cert_path=None, management_key_path=None, subscription_id=None):
        self.storage_account = storage_account_name
        if management_cert_path and subscription_id:
            self.wasm = WASM(management_cert_path, subscription_id, management_key_path)
        else:
            self.wasm = None
        if not storage_account_key:
            if not self.wasm:
                raise WAError('Windows Azure Service Management API not available.')
            storage_account_key, _, _ = self.wasm.get_storage_account_keys(storage_account_name)
        self.blobs = BlobStorage(storage_account_name, storage_account_key, use_path_style_uris)
        self.tables = TableStorage(storage_account_name, storage_account_key, use_path_style_uris)
        self.queues = QueueStorage(storage_account_name, storage_account_key, use_path_style_uris)
        self.WAError = WAError
        self.data_connection_string = self.blobs.create_data_connection_string()
        return

    def set_storage_account(self, storage_account_name, create=False, location_or_affinity_group='Anywhere US'):
        """Set the storage account used by storage API objects.

        Setting to DEVSTORE_ACCOUNT will switch to the local storage
        emulator.
        For anything except switching to dev storage this requires the API
        to have been initialised with an appropriate management Windows
        Azure Service Mangement certificate.
        If the create flag is True and the storage account does not exist
        it will be created in the specified location or affinity group.
        May produce WAError exceptions due to authentication issues or when
        the storage account limit is reached.
        """
        if self.storage_account == storage_account_name:
            return
        else:
            storage_account_key = None
            if storage_account_name == DEVSTORE_ACCOUNT:
                self.blobs = BlobStorage(DEVSTORE_BLOB_HOST, DEVSTORE_ACCOUNT, DEVSTORE_SECRET_KEY)
                self.tables = TableStorage(DEVSTORE_BLOB_HOST, DEVSTORE_ACCOUNT, DEVSTORE_SECRET_KEY)
                self.queues = QueueStorage(DEVSTORE_BLOB_HOST, DEVSTORE_ACCOUNT, DEVSTORE_SECRET_KEY)
                self.data_connection_string = create_data_connection_string(DEVSTORE_ACCOUNT, DEVSTORE_SECRET_KEY)
                self.storage_account = storage_account_name
                return
            if not self.wasm:
                raise WAError('Windows Azure Service Management API not available.')
            if storage_account_name not in self.wasm.list_storage_accounts():
                if create:
                    request = self.wasm.create_storage_account(storage_account_name, 'PyAzure storage: %s' % get_azure_time(), location_or_affinity_group, 'Storage account created by PyAzure')
                    self.wasm.wait_for_request(request)
                else:
                    raise WAError('Unknown storage account')
            storage_account_key, _, _ = self.wasm.get_storage_account_keys(storage_account_name)
            self.blobs = BlobStorage(CLOUD_BLOB_HOST, storage_account_name, storage_account_key)
            self.tables = TableStorage(CLOUD_TABLE_HOST, storage_account_name, storage_account_key)
            self.queues = QueueStorage(CLOUD_QUEUE_HOST, storage_account_name, storage_account_key)
            self.storage_account = storage_account_name
            self.data_connection_string = create_data_connection_string(storage_account_name, storage_account_key)
            return


class WASM(object):
    """Single class that conveniently exposes Windows Azure Service Management
    operations from those implemented and explicitly exposed by the individual
    service wrappers.
    
    Using WASM
    ----------
    >>> import pyazure
    >>> pa = pyazure.PyAzure(management_cert_path=MANAGEMENT_CERT, 
    ... subscription_id=SUBSCRIPTION_ID, management_key_path=MANAGEMENT_KEY)
    >>> 'Anywhere Asia' in pa.wasm.list_locations()
    True
    >>> request_id = pa.wasm.create_storage_account('pyazuretest','doctest',
    ... 'anywhere us', 'Here is my description, not great is it?')
    >>> pa.wasm.wait_for_request(request_id)
    True
    >>> (pa.wasm.get_operation_status(request_id) == 
    ... {'HttpStatusCode': 200, 'Status': 'Succeeded'})
    True
    >>> request_id = pa.wasm.create_storage_account(
    ... 'pyazuretestwithaverylongname','doctest','anywhere us')
    Traceback (most recent call last):
        ...
    ValueError: ('pyazuretestwithaverylongname', 'name must be between 3 and 24 characters in length and use numbers and lower-case letters only.')
    >>> 'pyazuretest' in pa.wasm.list_storage_accounts()
    True
    >>> pa.wasm.create_service('pyazuretest','create service doctest',
    ... 'anywhere europe')
    True
    >>> 'pyazuretest' in pa.wasm.list_services()
    True
    >>> pa.wasm.create_service('pyazuretest','create service doctest',
    ... 'anywhere europe')
    Traceback (most recent call last):
        ...
    WASMError: (409, 'ConflictError', 'The specified DNS name is already taken.')
    >>> pa.wasm.create_service('pyazuretest','create service doctest' * 10,
    ... 'anywhere europe') # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ('create service doctest...', 'label exceeds 100 char limit')
    >>> pa.wasm.get_service_properties('pyazuretest') # doctest: +ELLIPSIS
    ...                                   # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([('Url', 'http...'),
                 ('ServiceName', 'pyazuretest'),
                 ('HostedServiceProperties',
                     OrderedDict([('Description', ''),
                                  ('Location', 'Anywhere Europe'),
                                  ('Label', 'create service doctest')]))])
    >>> pa.wasm.delete_service('pyazuretest')
    True
    >>> pa.wasm.delete_storage_account('pyazuretest')
    True
    >>> pa.wasm.delete_storage_account('pyazuretest')
    Traceback (most recent call last):
        ...
    WASMError: (404, 'ResourceNotFound', 'The requested storage account was not found.')
    """

    def __init__(self, management_cert_path, subscription_id, management_key_path=None):
        """Initialise the various API interfaces.
        
        Note that management_key_path is not required (except for Python 2.5),
        as the key can be included in the certificate chain file. The OpenSSL
        command line can create an appropriate PEM file like so:
        openssl pkcs12 -in azure.pfx -out azure.pem -nodes
        """
        from hostedservices import HostedServices, ServiceConfiguration
        from storageaccounts import StorageAccounts
        from locations import Locations
        self.service_api = HostedServices(management_cert_path, subscription_id, management_key_path)
        self.ServiceConfiguration = ServiceConfiguration
        self.storage_api = StorageAccounts(management_cert_path, subscription_id, management_key_path)
        self.location_api = Locations(management_cert_path, subscription_id, management_key_path)
        self._sme = ServiceManagementEndpoint(management_cert_path, subscription_id, management_key_path)
        self.WASMError = WASMError
        self.get_operation_status = self._sme.get_operation_status
        self.request_done = self._sme.request_done
        self.wait_for_request = self._sme.wait_for_request
        for op in self.service_api.get_wasm_ops():
            setattr(self, op.__name__, op)

        for op in self.storage_api.get_wasm_ops():
            setattr(self, op.__name__, op)

        for op in self.location_api.get_wasm_ops():
            setattr(self, op.__name__, op)


def usage():
    print '\nThis module is an API, and as such is not designed to be run directly.\nHowever, there are embedded doctests which can executed by running pyazure.py\nand providing a Windows Azure subscription id and management certificate path\nas arguments, e.g., pyazure.py -s <subscription_id> -c <management_cert>\n\nAvailable docstrings for the top-level API follow:\nService Management:\n%s\nStorage:\n%s\n' % (PyAzure.__doc__, WASM.__doc__)
    print usage.func_doc


if __name__ == '__main__':
    import doctest, getopt
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'hvs:c:k:', [
         'help', 'verbose', 'subscription_id', 'management_cert',
         'management_key'])
    except getopt.GetoptError as e:
        print str(e)
        sys.exit(2)

    sub_id = cert = key = None
    loud = False
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-s', '--subscription_id'):
            sub_id = arg
        elif opt in ('-c', '--management_cert'):
            cert = arg
        elif opt in ('-k', '--management_key'):
            key = arg
        elif opt in ('-v', '--verbose'):
            loud = True

    if sub_id is None or cert is None:
        usage()
        sys.exit(2)
    doctest.testmod(extraglobs={'SUBSCRIPTION_ID': sub_id, 'MANAGEMENT_CERT': cert, 'MANAGEMENT_KEY': key}, verbose=loud)
    sys.exit()
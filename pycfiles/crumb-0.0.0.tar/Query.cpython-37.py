# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/Query.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 1751 bytes
from cruisecontrolclient.client.Endpoint import AbstractEndpoint
import warnings

def generate_url_from_cc_socket_address(cc_socket_address: str, endpoint: AbstractEndpoint) -> str:
    """
    Given a cruise-control hostname[:port] and an Endpoint, return the correct URL
    for this cruise-control operation.

    Note that this URL _includes_ parameters.

    :param cc_socket_address: like hostname[:port], ip-address[:port]
    :param endpoint:
    :return: URL, the correct URL to perform the Endpoint's operation
             on the given cruise-control host, _including parameters_.
    """
    warnings.warn('This function is deprecated as of 0.2.0. It may be removed entirely in future versions.', DeprecationWarning,
      stacklevel=2)
    url = f"http://{cc_socket_address}/kafkacruisecontrol/{endpoint.compose_endpoint()}"
    return url


def generate_base_url_from_cc_socket_address(cc_socket_address: str, endpoint: AbstractEndpoint) -> str:
    """
    Given a cruise-control hostname[:port] and an Endpoint, return the correct URL
    for this cruise-control operation.

    Note that this URL _excludes_ parameters.

    :param cc_socket_address: like hostname[:port], ip-address[:port]
    :param endpoint:
    :return: URL, the correct URL to perform the Endpoint's operation
             on the given cruise-control host, _excluding parameters_.
    """
    url = f"http://{cc_socket_address}/kafkacruisecontrol/{endpoint.name}"
    return url
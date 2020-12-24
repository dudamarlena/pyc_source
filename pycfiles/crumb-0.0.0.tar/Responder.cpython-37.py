# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/Responder.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 6406 bytes
from cruisecontrolclient.util.print import print_error
from cruisecontrolclient.client.Endpoint import AbstractEndpoint
from cruisecontrolclient.client.Query import generate_base_url_from_cc_socket_address
import requests
from urllib.parse import urlencode
import warnings, re

class CruiseControlResponder(requests.Session):
    """CruiseControlResponder"""

    def retrieve_response(self, method, url, **kwargs) -> requests.Response:
        """
        Returns a final requests.Response object from cruise-control
        where Response.text is JSON-formatted.

        :return: requests.Response
        """
        if 'params' in kwargs:
            url_with_params = f"{url}?{urlencode(kwargs['params'])}"
        else:
            url_with_params = url
        print_error(f"Starting long-running poll of {url_with_params}")
        for key, value in kwargs.items():
            if key == 'params':
                continue
            else:
                print_error(f"{key}: {value}")

        def inner_request_helper():
            return (self.request)(method, url, **kwargs)

        def is_response_final(response: requests.Response):

            def json_or_text_guesser():
                try:
                    return 'progress' not in response.json().keys()
                except ValueError:
                    cc_version = response.headers.get('Cruise-Control-Version')
                    if cc_version is not None:
                        warnings.warn(f"json=False received from cruise-control version ({cc_version}) that does not support 202 response codes. Please upgrade cruise-control to >=2.0.61, or use json=True with cruise-control-client. Returning a potentially non-final response.")
                    elif response.status_code == 414:
                        pass
                    else:
                        warnings.warn('Unable to determine cruise-control version. Returning a potentially non-final response.')
                    return True

            if response.status_code == 202:
                return False
                if 'Cruise-Control-Version' in response.headers:
                    non_decimal = re.compile('[^\\d.]+')
                    integer_semver = lambda x: [int(elem) for elem in x.split('.')]
                    cc_version = integer_semver(non_decimal.sub('', response.headers['Cruise-Control-Version']))
                    if cc_version >= [2, 0, 61]:
                        return True
                    return json_or_text_guesser()
            else:
                return json_or_text_guesser()

        response = inner_request_helper()
        final_response = is_response_final(response)
        while not final_response:
            print_error(response.text)
            response = inner_request_helper()
            final_response = is_response_final(response)

        return response

    def retrieve_response_from_Endpoint(self, cc_socket_address: str, endpoint: AbstractEndpoint, **kwargs):
        """
        Returns a final requests.Response object from cruise-control
        where Response.text is JSON-formatted.

        This method is a convenience wrapper around the more-general retrieve_response.

        :return: requests.Response
        :param cc_socket_address: like someCruiseControlAddress:9090
        :param endpoint: an instance of an Endpoint
        :return:
        """
        return (self.retrieve_response)(method=endpoint.http_method, 
         url=generate_base_url_from_cc_socket_address(cc_socket_address, endpoint), 
         params=endpoint.get_composed_params(), **kwargs)
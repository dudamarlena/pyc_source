# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/test/REST/attestationendpoint/peer_communication.py
# Compiled at: 2019-05-16 09:27:10
from abc import abstractmethod

class IPostStyleRequestsAE(object):
    """
    Defines an interface for the POST requests which are accepted by the Attestation Endpoint
    """

    @abstractmethod
    def make_attestation_request(self, param_dict):
        """
        Generate an attestation request

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_attest(self, param_dict):
        """
        Generate an attestation

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_verify(self, param_dict):
        """
        Generate an attestation verification request

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_allow_verify(self, param_dict):
        """
        Generate an allow verification request

        :param param_dict: the request's arguments
        :return: None
        """
        pass


class IGetStyleRequestsAE(object):
    """
    Defines an interface for the GET requests which are accepted by the Attestation Endpoint
    """

    @abstractmethod
    def make_outstanding(self, param_dict):
        """
        Generate a request asking for the outstanding attestation requests

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_verification_output(self, param_dict):
        """
        Generate a request asking for the outputs of the verification processes

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_peers(self, param_dict):
        """
        Generate a request asking for the known peers in the network

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_attributes(self, param_dict):
        """
        Generate a request asking for the known peers in the network

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_drop_identity(self, param_dict):
        """
        Generate a request for dropping an identity

        :param param_dict: the request's arguments
        :return: None
        """
        pass

    @abstractmethod
    def make_outstanding_verify(self, param_dict):
        """
        Generate a request for retrieving the outstanding verification requests

        :param param_dict: the request's arguments
        :return: None
        """
        pass
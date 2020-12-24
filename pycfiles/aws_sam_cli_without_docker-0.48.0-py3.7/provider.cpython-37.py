# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/providers/provider.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 8216 bytes
"""
A provider class that can parse and return Lambda Functions from a variety of sources. A SAM template is one such
source
"""
import hashlib
from collections import namedtuple
from samcli.commands.local.cli_common.user_exceptions import InvalidLayerVersionArn, UnsupportedIntrinsic
Function = namedtuple('Function', [
 'name',
 'functionname',
 'runtime',
 'memory',
 'timeout',
 'handler',
 'codeuri',
 'environment',
 'rolearn',
 'layers'])

class LayerVersion:
    __doc__ = '\n    Represents the LayerVersion Resource for AWS Lambda\n    '
    LAYER_NAME_DELIMETER = '-'

    def __init__(self, arn, codeuri):
        """

        Parameters
        ----------
        name str
            Name of the layer, this can be the ARN or Logical Id in the template
        codeuri str
            CodeURI of the layer. This should contain the path to the layer code
        """
        if not isinstance(arn, str):
            raise UnsupportedIntrinsic('{} is an Unsupported Intrinsic'.format(arn))
        self._arn = arn
        self._codeuri = codeuri
        self.is_defined_within_template = bool(codeuri)
        self._name = LayerVersion._compute_layer_name(self.is_defined_within_template, arn)
        self._version = LayerVersion._compute_layer_version(self.is_defined_within_template, arn)

    @staticmethod
    def _compute_layer_version(is_defined_within_template, arn):
        """
        Parses out the Layer version from the arn

        Parameters
        ----------
        is_defined_within_template bool
            True if the resource is a Ref to a resource otherwise False
        arn str
            ARN of the Resource

        Returns
        -------
        int
            The Version of the LayerVersion

        """
        if is_defined_within_template:
            return
        try:
            _, layer_version = arn.rsplit(':', 1)
            layer_version = int(layer_version)
        except ValueError:
            raise InvalidLayerVersionArn(arn + ' is an Invalid Layer Arn.')

        return layer_version

    @staticmethod
    def _compute_layer_name(is_defined_within_template, arn):
        """
        Computes a unique name based on the LayerVersion Arn

        Format:
        <Name of the LayerVersion>-<Version of the LayerVersion>-<sha256 of the arn>

        Parameters
        ----------
        is_defined_within_template bool
            True if the resource is a Ref to a resource otherwise False
        arn str
            ARN of the Resource

        Returns
        -------
        str
            A unique name that represents the LayerVersion
        """
        if is_defined_within_template:
            return arn
        try:
            _, layer_name, layer_version = arn.rsplit(':', 2)
        except ValueError:
            raise InvalidLayerVersionArn(arn + ' is an Invalid Layer Arn.')

        return LayerVersion.LAYER_NAME_DELIMETER.join([
         layer_name, layer_version, hashlib.sha256(arn.encode('utf-8')).hexdigest()[0:10]])

    @property
    def arn(self):
        return self._arn

    @property
    def name(self):
        """
        A unique name from the arn or logical id of the Layer

        A LayerVersion Arn example:
        arn:aws:lambda:region:account-id:layer:layer-name:version

        Returns
        -------
        str
            A name of the Layer that is used on the system to uniquely identify the layer
        """
        return self._name

    @property
    def codeuri(self):
        return self._codeuri

    @property
    def version(self):
        return self._version

    @property
    def layer_arn(self):
        layer_arn, _ = self.arn.rsplit(':', 1)
        return layer_arn

    @codeuri.setter
    def codeuri(self, codeuri):
        self._codeuri = codeuri

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__dict__ == other.__dict__
        return False


class FunctionProvider:
    __doc__ = '\n    Abstract base class of the function provider.\n    '

    def get(self, name):
        """
        Given name of the function, this method must return the Function object

        :param string name: Name of the function
        :return Function: namedtuple containing the Function information
        """
        raise NotImplementedError('not implemented')

    def get_all(self):
        """
        Yields all the Lambda functions available in the provider.

        :yields Function: namedtuple containing the function information
        """
        raise NotImplementedError('not implemented')


class Api:

    def __init__(self, routes=None):
        if routes is None:
            routes = []
        self.routes = routes
        self.cors = None
        self.binary_media_types_set = set()
        self.stage_name = None
        self.stage_variables = None

    def __hash__(self):
        return hash(self.routes) * hash(self.cors) * hash(self.binary_media_types_set)

    @property
    def binary_media_types(self):
        return list(self.binary_media_types_set)


_CorsTuple = namedtuple('Cors', ['allow_origin', 'allow_methods', 'allow_headers', 'max_age'])
_CorsTuple.__new__.__defaults__ = (None, None, None, None)

class Cors(_CorsTuple):

    @staticmethod
    def cors_to_headers(cors):
        """
        Convert CORS object to headers dictionary
        Parameters
        ----------
        cors list(samcli.commands.local.lib.provider.Cors)
            CORS configuration objcet
        Returns
        -------
            Dictionary with CORS headers
        """
        if not cors:
            return {}
        headers = {'Access-Control-Allow-Origin':cors.allow_origin, 
         'Access-Control-Allow-Methods':cors.allow_methods, 
         'Access-Control-Allow-Headers':cors.allow_headers, 
         'Access-Control-Max-Age':cors.max_age}
        return {h_key:h_value for h_key, h_value in headers.items() if h_value is not None if h_value is not None}


class AbstractApiProvider:
    __doc__ = '\n    Abstract base class to return APIs and the functions they route to\n    '

    def get_all(self):
        """
        Yields all the APIs available.

        :yields Api: namedtuple containing the API information
        """
        raise NotImplementedError('not implemented')
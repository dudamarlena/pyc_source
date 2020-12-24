# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/samlib/wrapper.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5447 bytes
"""
Wrapper for the SAM Translator and Parser classes.

##### NOTE #####
This module uses internal packages of SAM Translator library in order to provide a nice interface for the CLI. This is
a tech debt that we have decided to take on. This will be eventually thrown away when SAM Translator exposes a
rich public interface.
"""
import copy, os, json, functools, boto3
from samtranslator.model.exceptions import InvalidDocumentException, InvalidTemplateException, InvalidResourceException, InvalidEventException
from samtranslator.validator.validator import SamTemplateValidator
from samtranslator.model import ResourceTypeResolver, sam_resources
from samtranslator.plugins import LifeCycleEvents
from samtranslator.translator.translator import prepare_plugins, Translator
from samtranslator.translator.managed_policy_translator import ManagedPolicyLoader
from samtranslator.parser.parser import Parser
from samcli.commands.validate.lib.exceptions import InvalidSamDocumentException
from .local_uri_plugin import SupportLocalUriPlugin

class SamTranslatorWrapper:
    _thisdir = os.path.dirname(os.path.abspath(__file__))
    _DEFAULT_MANAGED_POLICIES_FILE = os.path.join(_thisdir, 'default_managed_policies.json')

    def __init__(self, sam_template, offline_fallback=True):
        """

        Parameters
        ----------
        sam_template dict:
            SAM Template dictionary
        offline_fallback bool:
            Set it to True to make the translator work entirely offline, if internet is not available
        """
        self.local_uri_plugin = SupportLocalUriPlugin()
        self.extra_plugins = [
         self.local_uri_plugin]
        self._sam_template = sam_template
        self._offline_fallback = offline_fallback

    def run_plugins(self, convert_local_uris=True):
        template_copy = self.template
        additional_plugins = []
        if convert_local_uris:
            additional_plugins.append(self.local_uri_plugin)
        parser = _SamParserReimplemented()
        all_plugins = prepare_plugins(additional_plugins)
        try:
            parser.parse(template_copy, all_plugins)
        except InvalidDocumentException as e:
            try:
                raise InvalidSamDocumentException(functools.reduce(lambda message, error: message + ' ' + str(error), e.causes, str(e)))
            finally:
                e = None
                del e

        return template_copy

    def __translate(self, parameter_values):
        """
        This method is unused and a Work In Progress
        """
        template_copy = self.template
        sam_parser = Parser()
        sam_translator = Translator(managed_policy_map=(self._SamTranslatorWrapper__managed_policy_map()),
          sam_parser=sam_parser,
          plugins=(self.extra_plugins))
        return sam_translator.translate(sam_template=template_copy, parameter_values=parameter_values)

    @property
    def template(self):
        return copy.deepcopy(self._sam_template)

    def __managed_policy_map(self):
        """
        This method is unused and a Work In Progress
        """
        try:
            iam_client = boto3.client('iam')
            return ManagedPolicyLoader(iam_client).load()
        except Exception as ex:
            try:
                if self._offline_fallback:
                    with open(self._DEFAULT_MANAGED_POLICIES_FILE, 'r') as (fp):
                        return json.load(fp)
                raise ex
            finally:
                ex = None
                del ex


class _SamParserReimplemented:
    __doc__ = '\n    Re-implementation (almost copy) of Parser class from SAM Translator\n    '

    def parse(self, sam_template, sam_plugins):
        self._validate(sam_template)
        sam_plugins.act(LifeCycleEvents.before_transform_template, sam_template)
        macro_resolver = ResourceTypeResolver(sam_resources)
        document_errors = []
        for logical_id, resource in sam_template['Resources'].items():
            try:
                if macro_resolver.can_resolve(resource):
                    macro_resolver.resolve_resource_type(resource).from_dict(logical_id,
                      resource, sam_plugins=sam_plugins)
            except (InvalidResourceException, InvalidEventException) as e:
                try:
                    document_errors.append(e)
                finally:
                    e = None
                    del e

        if document_errors:
            raise InvalidDocumentException(document_errors)

    def _validate(self, sam_template):
        """ Validates the template and parameter values and raises exceptions if there's an issue

        :param dict sam_template: SAM template
        """
        if not (('Resources' not in sam_template or isinstance)(sam_template['Resources'], dict) and sam_template['Resources']):
            raise InvalidDocumentException([InvalidTemplateException("'Resources' section is required")])
        SamTemplateValidator.validate(sam_template)
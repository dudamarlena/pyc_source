# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/gcp_field_validator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 22823 bytes
__doc__ = 'Validator for body fields sent via GCP API.\n\nThe validator performs validation of the body (being dictionary of fields) that\nis sent in the API request to Google Cloud (via googleclient API usually).\n\nContext\n-------\nThe specification mostly focuses on helping Airflow DAG developers in the development\nphase. You can build your own GCP operator (such as GcfDeployOperator for example) which\ncan have built-in validation specification for the particular API. It\'s super helpful\nwhen developer plays with different fields and their values at the initial phase of\nDAG development. Most of the Google Cloud APIs perform their own validation on the\nserver side, but most of the requests are asynchronous and you need to wait for result\nof the operation. This takes precious times and slows\ndown iteration over the API. BodyFieldValidator is meant to be used on the client side\nand it should therefore provide an instant feedback to the developer on misspelled or\nwrong type of parameters.\n\nThe validation should be performed in "execute()" method call in order to allow\ntemplate parameters to be expanded before validation is performed.\n\nTypes of fields\n---------------\n\nSpecification is an array of dictionaries - each dictionary describes field, its type,\nvalidation, optionality, api_version supported and nested fields (for unions and dicts).\n\nTypically (for clarity and in order to aid syntax highlighting) the array of\ndicts should be defined as series of dict() executions. Fragment of example\nspecification might look as follows::\n\n    SPECIFICATION =[\n       dict(name="an_union", type="union", optional=True, fields=[\n           dict(name="variant_1", type="dict"),\n           dict(name="variant_2", regexp=r\'^.+$\', api_version=\'v1beta2\'),\n       ),\n       dict(name="an_union", type="dict", fields=[\n           dict(name="field_1", type="dict"),\n           dict(name="field_2", regexp=r\'^.+$\'),\n       ),\n       ...\n    ]\n\n\nEach field should have key = "name" indicating field name. The field can be of one of the\nfollowing types:\n\n* Dict fields: (key = "type", value="dict"):\n  Field of this type should contain nested fields in form of an array of dicts.\n  Each of the fields in the array is then expected (unless marked as optional)\n  and validated recursively. If an extra field is present in the dictionary, warning is\n  printed in log file (but the validation succeeds - see the Forward-compatibility notes)\n* List fields: (key = "type", value="list"):\n  Field of this type should be a list. Only the type correctness is validated.\n  The contents of a list are not subject to validation.\n* Union fields (key = "type", value="union"): field of this type should contain nested\n  fields in form of an array of dicts. One of the fields (and only one) should be\n  present (unless the union is marked as optional). If more than one union field is\n  present, FieldValidationException is raised. If none of the union fields is\n  present - warning is printed in the log (see below Forward-compatibility notes).\n* Fields validated for non-emptiness: (key = "allow_empty") - this applies only to\n  fields the value of which is a string, and it allows to check for non-emptiness of\n  the field (allow_empty=False).\n* Regexp-validated fields: (key = "regexp") - fields of this type are assumed to be\n  strings and they are validated with the regexp specified. Remember that the regexps\n  should ideally contain ^ at the beginning and $ at the end to make sure that\n  the whole field content is validated. Typically such regexp\n  validations should be used carefully and sparingly (see Forward-compatibility\n  notes below).\n* Custom-validated fields: (key = "custom_validation") - fields of this type are validated\n  using method specified via custom_validation field. Any exception thrown in the custom\n  validation will be turned into FieldValidationException and will cause validation to\n  fail. Such custom validations might be used to check numeric fields (including\n  ranges of values), booleans or any other types of fields.\n* API version: (key="api_version") if API version is specified, then the field will only\n  be validated when api_version used at field validator initialization matches exactly the\n  the version specified. If you want to declare fields that are available in several\n  versions of the APIs, you should specify the field as many times as many API versions\n  should be supported (each time with different API version).\n* if none of the keys ("type", "regexp", "custom_validation" - the field is not validated\n\nYou can see some of the field examples in EXAMPLE_VALIDATION_SPECIFICATION.\n\n\nForward-compatibility notes\n---------------------------\nCertain decisions are crucial to allow the client APIs to work also with future API\nversions. Since body attached is passed to the API’s call, this is entirely\npossible to pass-through any new fields in the body (for future API versions) -\nalbeit without validation on the client side - they can and will still be validated\non the server side usually.\n\nHere are the guidelines that you should follow to make validation forward-compatible:\n\n* most of the fields are not validated for their content. It\'s possible to use regexp\n  in some specific cases that are guaranteed not to change in the future, but for most\n  fields regexp validation should be r\'^.+$\' indicating check for non-emptiness\n* api_version is not validated - user can pass any future version of the api here. The API\n  version is only used to filter parameters that are marked as present in this api version\n  any new (not present in the specification) fields in the body are allowed (not verified)\n  For dictionaries, new fields can be added to dictionaries by future calls. However if an\n  unknown field in dictionary is added, a warning is logged by the client (but validation\n  remains successful). This is very nice feature to protect against typos in names.\n* For unions, newly added union variants can be added by future calls and they will\n  pass validation, however the content or presence of those fields will not be validated.\n  This means that it’s possible to send a new non-validated union field together with an\n  old validated field and this problem will not be detected by the client. In such case\n  warning will be printed.\n* When you add validator to an operator, you should also add ``validate_body`` parameter\n  (default = True) to __init__ of such operators - when it is set to False,\n  no validation should be performed. This is a safeguard for totally unpredicted and\n  backwards-incompatible changes that might sometimes occur in the APIs.\n\n'
import re
from typing import Sequence, Dict, Callable
from airflow import LoggingMixin, AirflowException
COMPOSITE_FIELD_TYPES = [
 'union', 'dict', 'list']

class GcpFieldValidationException(AirflowException):
    """GcpFieldValidationException"""

    def __init__(self, message):
        super(GcpFieldValidationException, self).__init__(message)


class GcpValidationSpecificationException(AirflowException):
    """GcpValidationSpecificationException"""

    def __init__(self, message):
        super(GcpValidationSpecificationException, self).__init__(message)


def _int_greater_than_zero(value):
    if int(value) <= 0:
        raise GcpFieldValidationException('The available memory has to be greater than 0')


EXAMPLE_VALIDATION_SPECIFICATION = [
 dict(name='name', allow_empty=False),
 dict(name='description', allow_empty=False, optional=True),
 dict(name='availableMemoryMb', custom_validation=_int_greater_than_zero, optional=True),
 dict(name='labels', optional=True, type='dict'),
 dict(name='an_union', type='union', fields=[
  dict(name='variant_1', regexp='^.+$'),
  dict(name='variant_2', regexp='^.+$', api_version='v1beta2'),
  dict(name='variant_3', type='dict', fields=[
   dict(name='url', regexp='^.+$')]),
  dict(name='variant_4')])]

class GcpBodyFieldValidator(LoggingMixin):
    """GcpBodyFieldValidator"""

    def __init__(self, validation_specs, api_version):
        super(GcpBodyFieldValidator, self).__init__()
        self._validation_specs = validation_specs
        self._api_version = api_version

    @staticmethod
    def _get_field_name_with_parent(field_name, parent):
        if parent:
            return parent + '.' + field_name
        else:
            return field_name

    @staticmethod
    def _sanity_checks(children_validation_specs, field_type, full_field_path, regexp, allow_empty, custom_validation, value):
        if value is None:
            if field_type != 'union':
                raise GcpFieldValidationException("The required body field '{}' is missing. Please add it.".format(full_field_path))
            else:
                if regexp:
                    if field_type:
                        raise GcpValidationSpecificationException("The validation specification entry '{}' has both type and regexp. The regexp is only allowed without type (i.e. assume type is 'str' that can be validated with regexp)".format(full_field_path))
                if allow_empty is not None:
                    if field_type:
                        raise GcpValidationSpecificationException("The validation specification entry '{}' has both type and allow_empty. The allow_empty is only allowed without type (i.e. assume type is 'str' that can be validated with allow_empty)".format(full_field_path))
                if children_validation_specs:
                    if field_type not in COMPOSITE_FIELD_TYPES:
                        raise GcpValidationSpecificationException("Nested fields are specified in field '{}' of type '{}'. Nested fields are only allowed for fields of those types: ('{}').".format(full_field_path, field_type, COMPOSITE_FIELD_TYPES))
        else:
            if custom_validation:
                if field_type:
                    raise GcpValidationSpecificationException("The validation specification field '{}' has both type and custom_validation. Custom validation is only allowed without type.".format(full_field_path))

    @staticmethod
    def _validate_regexp(full_field_path, regexp, value):
        if not re.match(regexp, value):
            raise GcpFieldValidationException("The body field '{}' of value '{}' does not match the field specification regexp: '{}'.".format(full_field_path, value, regexp))

    @staticmethod
    def _validate_is_empty(full_field_path, value):
        if not value:
            raise GcpFieldValidationException("The body field '{}' can't be empty. Please provide a value.".format(full_field_path, value))

    def _validate_dict(self, children_validation_specs, full_field_path, value):
        for child_validation_spec in children_validation_specs:
            self._validate_field(validation_spec=child_validation_spec, dictionary_to_validate=value,
              parent=full_field_path)

        all_dict_keys = [spec['name'] for spec in children_validation_specs]
        for field_name in value.keys():
            if field_name not in all_dict_keys:
                self.log.warning("The field '%s' is in the body, but is not specified in the validation specification '%s'. This might be because you are using newer API version and new field names defined for that version. Then the warning can be safely ignored, or you might want to upgrade the operatorto the version that supports the new API version.", self._get_field_name_with_parent(field_name, full_field_path), children_validation_specs)

    def _validate_union(self, children_validation_specs, full_field_path, dictionary_to_validate):
        field_found = False
        found_field_name = None
        for child_validation_spec in children_validation_specs:
            new_field_found = self._validate_field(validation_spec=child_validation_spec,
              dictionary_to_validate=dictionary_to_validate,
              parent=full_field_path,
              force_optional=True)
            field_name = child_validation_spec['name']
            if new_field_found:
                if field_found:
                    raise GcpFieldValidationException("The mutually exclusive fields '{}' and '{}' belonging to the union '{}' are both present. Please remove one".format(field_name, found_field_name, full_field_path))
                if new_field_found:
                    field_found = True
                    found_field_name = field_name

        if not field_found:
            self.log.warning("There is no '%s' union defined in the body %s. Validation expected one of '%s' but could not find any. It's possible that you are using newer API version and there is another union variant defined for that version. Then the warning can be safely ignored, or you might want to upgrade the operator to the version that supports the new API version.", full_field_path, dictionary_to_validate, [field['name'] for field in children_validation_specs])

    def _validate_field(self, validation_spec, dictionary_to_validate, parent=None, force_optional=False):
        """
        Validates if field is OK.

        :param validation_spec: specification of the field
        :type validation_spec: dict
        :param dictionary_to_validate: dictionary where the field should be present
        :type dictionary_to_validate: dict
        :param parent: full path of parent field
        :type parent: str
        :param force_optional: forces the field to be optional
            (all union fields have force_optional set to True)
        :type force_optional: bool
        :return: True if the field is present
        """
        field_name = validation_spec['name']
        field_type = validation_spec.get('type')
        optional = validation_spec.get('optional')
        regexp = validation_spec.get('regexp')
        allow_empty = validation_spec.get('allow_empty')
        children_validation_specs = validation_spec.get('fields')
        required_api_version = validation_spec.get('api_version')
        custom_validation = validation_spec.get('custom_validation')
        full_field_path = self._get_field_name_with_parent(field_name=field_name, parent=parent)
        if required_api_version:
            if required_api_version != self._api_version:
                self.log.debug("Skipping validation of the field '%s' for API version '%s' as it is only valid for API version '%s'", field_name, self._api_version, required_api_version)
                return False
        value = dictionary_to_validate.get(field_name)
        if (optional or force_optional) and value is None:
            self.log.debug("The optional field '%s' is missing. That's perfectly OK.", full_field_path)
            return False
        else:
            self._sanity_checks(children_validation_specs=children_validation_specs, field_type=field_type,
              full_field_path=full_field_path,
              regexp=regexp,
              allow_empty=allow_empty,
              custom_validation=custom_validation,
              value=value)
            if allow_empty is False:
                self._validate_is_empty(full_field_path, value)
            if regexp:
                self._validate_regexp(full_field_path, regexp, value)
            else:
                if field_type == 'dict':
                    if not isinstance(value, dict):
                        raise GcpFieldValidationException("The field '{}' should be of dictionary type according to the specification '{}' but it is '{}'".format(full_field_path, validation_spec, value))
                    else:
                        if children_validation_specs is None:
                            self.log.debug("The dict field '%s' has no nested fields defined in the specification '%s'. That's perfectly ok - it's content will not be validated.", full_field_path, validation_spec)
                        else:
                            self._validate_dict(children_validation_specs, full_field_path, value)
                else:
                    if field_type == 'union':
                        if not children_validation_specs:
                            raise GcpValidationSpecificationException("The union field '%s' has no nested fields defined in specification '%s'. Unions should have at least one nested field defined.", full_field_path, validation_spec)
                        self._validate_union(children_validation_specs, full_field_path, dictionary_to_validate)
                    else:
                        if field_type == 'list':
                            if not isinstance(value, list):
                                raise GcpFieldValidationException("The field '{}' should be of list type according to the specification '{}' but it is '{}'".format(full_field_path, validation_spec, value))
                        else:
                            if custom_validation:
                                try:
                                    custom_validation(value)
                                except Exception as e:
                                    raise GcpFieldValidationException("Error while validating custom field '{}' specified by '{}': '{}'".format(full_field_path, validation_spec, e))

                            else:
                                if field_type is None:
                                    self.log.debug("The type of field '%s' is not specified in '%s'. Not validating its content.", full_field_path, validation_spec)
                                else:
                                    raise GcpValidationSpecificationException("The field '{}' is of type '{}' in specification '{}'.This type is unknown to validation!".format(full_field_path, field_type, validation_spec))
            return True

    def validate(self, body_to_validate):
        """
        Validates if the body (dictionary) follows specification that the validator was
        instantiated with. Raises ValidationSpecificationException or
        ValidationFieldException in case of problems with specification or the
        body not conforming to the specification respectively.

        :param body_to_validate: body that must follow the specification
        :type body_to_validate: dict
        :return: None
        """
        try:
            for validation_spec in self._validation_specs:
                self._validate_field(validation_spec=validation_spec, dictionary_to_validate=body_to_validate)

        except GcpFieldValidationException as e:
            raise GcpFieldValidationException("There was an error when validating: body '{}': '{}'".format(body_to_validate, e))

        all_field_names = [spec['name'] for spec in self._validation_specs if spec.get('type') != 'union' if spec.get('api_version') != self._api_version]
        all_union_fields = [spec for spec in self._validation_specs if spec.get('type') == 'union']
        for union_field in all_union_fields:
            all_field_names.extend([nested_union_spec['name'] for nested_union_spec in union_field['fields'] if nested_union_spec.get('type') != 'union' if nested_union_spec.get('api_version') != self._api_version])

        for field_name in body_to_validate.keys():
            if field_name not in all_field_names:
                self.log.warning("The field '%s' is in the body, but is not specified in the validation specification '%s'. This might be because you are using newer API version and new field names defined for that version. Then the warning can be safely ignored, or you might want to upgrade the operatorto the version that supports the new API version.", field_name, self._validation_specs)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pypermedia/siren.py
# Compiled at: 2016-02-16 21:11:04
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json, logging, re, six
from requests import Response, Session, Request

def _check_and_decode_response(response):
    """
    Checks if the response is valid.  If it is, it returns the response body.  Otherwise it raises an exception or
    returns None if the status_code is 404.

    :param Response response: The response to check
    :return: The response body if appropriate.
    :rtype: unicode
    """
    if response.status_code == 404:
        return None
    else:
        if response.status_code > 299 or response.status_code < 200:
            raise UnexpectedStatusError(message=(b'Received an unexpected status code of "{0}"! Unable to construct siren objects.').format(response.status_code))
        response = response.text
        if not response:
            raise MalformedSirenError(message=b'Parameter "response" object had empty response content. Unable to construct siren objects.')
        return response


class RequestMixin(object):
    """Values for any request creating object."""

    def __init__(self, request_factory=Request, verify=False):
        """
        :param type|function request_factory: constructor for request objects
        :param bool verify: whether ssl certificate validation should occur
        """
        self.request_factory = request_factory
        self.verify = verify


class SirenBuilder(RequestMixin):
    """Responsible for constructing Siren hierarchy objects."""

    def from_api_response(self, response):
        """
        Creates a SirenEntity and related siren object graph.

        :param response: response item containing siren construction information
        :type response: str or unicode or requests.Response
        :return: siren entity graph
        :rtype: SirenEntity
        :raises: MalformedSirenError
        :raises: TypeError
        """
        if isinstance(response, Response):
            response = _check_and_decode_response(response)
            if response is None:
                return
        if isinstance(response, six.string_types):
            try:
                response = json.loads(response)
            except ValueError as e:
                raise MalformedSirenError(message=b'Parameter "response" must be valid json. Unable to construct siren objects.', errors=e)

        if type(response) is not dict:
            raise TypeError(b'Siren object construction requires a valid response, json, or dict object.')
        try:
            return self._construct_entity(response)
        except Exception as e:
            raise MalformedSirenError(message=b'Siren response is malformed and is missing one or more required values. Unable to create python object representation.', errors=e)

        return

    def _construct_entity(self, entity_dict):
        """
        Constructs an entity from a dictionary. Used
        for both entities and embedded sub-entities.

        :param dict entity_dict:
        :return: The SirenEntity representing the object
        :rtype: SirenEntity
        :raises KeyError
        """
        classname = entity_dict[b'class']
        properties = entity_dict.get(b'properties', {})
        rel = entity_dict.get(b'rel', [])
        actions = []
        for action_dict in entity_dict.get(b'actions', []):
            siren_action = SirenAction(request_factory=self.request_factory, verify=self.verify, **action_dict)
            actions.append(siren_action)

        links = []
        for links_dict in entity_dict.get(b'links', []):
            link = self._construct_link(links_dict)
            links.append(link)

        entities = []
        for entities_dict in entity_dict.get(b'entities', []):
            try:
                entity = self._construct_link(entities_dict)
            except KeyError:
                entity = self._construct_entity(entities_dict)

            entities.append(entity)

        siren_entity = SirenEntity(classnames=classname, properties=properties, actions=actions, links=links, entities=entities, rel=rel, verify=self.verify, request_factory=self.request_factory)
        return siren_entity

    def _construct_link(self, links_dict):
        """
        Constructs a link from the links dictionary.

        :param dict links_dict: A dictionary include a {key: list, href: unicode}
        :return: A SirenLink representing the link
        :rtype: SirenLink
        :raises: KeyError
        """
        rel = links_dict[b'rel']
        href = links_dict[b'href']
        link = SirenLink(rel=rel, href=href, verify=self.verify, request_factory=self.request_factory)
        return link


class SirenEntity(RequestMixin):
    """
    Represents a siren-entity object. This is the highest-level/root item used by Siren. These represent
    instances/classes.
    """
    log = logging.getLogger(__name__)

    def __init__(self, classnames, links, properties=None, actions=None, entities=None, rel=None, **kwargs):
        """
        Constructor.

        :param classnames: root classnames of the response, currently these do nothing, in the future they will be used
            to add expanded functionality to an object.
        :type classnames: str or list[str]
        :param links: link relations to self and related but non owned items
        :type links: str or list[str]
        :param properties: fields/properties of the instance
        :type properties:
        :param actions: actions that can be performed on an instance or object class
        :type actions:
        :raises: ValueError
        """
        super(SirenEntity, self).__init__(**kwargs)
        if not classnames or len(classnames) == 0:
            raise ValueError(b'Parameter "classnames" must have at least one element.')
        self.classnames = classnames
        self.rel = rel
        self.properties = properties if properties else {}
        self.actions = actions if actions else []
        self.links = links or []
        self.entities = entities or []

    def get_links(self, rel):
        """
        Obtains a link based upon relationship value.

        :param rel: relationship between this entity and the linked resource
        :type rel: str
        :return: link to the resource with the specified relationship
        :rtype: SirenEntity
        """
        if not self.links:
            return None
        else:
            return [ x for x in self.links if rel in x.rel ]

    def get_entities(self, rel):
        """
        Obtains an entity based upon the relationship value.

        :param rel: relationship between this entity and the linked resource
        :type rel: str
        :return: link to the resource with the specified relationship
        :rtype: list
        """
        if not self.entities:
            return []
        return [ x for x in self.entities if rel in x.rel ]

    def get_primary_classname(self):
        """
        Obtains the primary classname associated with this entity. This is assumed to be the first classname in the list
        of classnames associated with this entity.

        :return: primary classname
        :rtype: str
        """
        return self.classnames[0]

    def get_base_classnames(self):
        """
        Obtains the base classnames associated with this entity. This is assumed to be all values following the
        first/primary classname.

        :return: base classnames
        :rtype: str
        """
        if len(self.classnames) > 1:
            return self.classnames[1:]
        return []

    def as_siren(self):
        """
        Python dictionary/array representation of this entity graph.

        :return: dictionary representation of this siren entity
        :rtype: dict[str]
        """
        new_dict = {b'class': self.classnames, b'properties': self.properties}
        new_dict[b'actions'] = [ action.as_siren() for action in self.actions ]
        new_dict[b'entities'] = [ entity.as_siren() for entity in self.entities ]
        new_dict[b'links'] = [ link.as_siren() for link in self.links ]
        return new_dict

    def as_json(self):
        """
        Json-string representation of this entity graph.

        :return: json-string representation of this siren entity
        :rtype: str
        """
        new_dict = self.as_siren()
        return json.dumps(new_dict)

    def as_python_object(self):
        """
        Programmatically create a python object for this siren entity.

        :return: dynamically created object based upon the siren response, type is based upon the classname(s) of this
        siren entity
        :rtype: object
        """
        ModelClass = type(str(self.get_primary_classname()), (), self.properties)
        siren_builder = SirenBuilder(verify=self.verify, request_factory=self.request_factory)
        for action in self.actions:
            method_name = SirenEntity._create_python_method_name(action.name)
            method_def = _create_action_fn(action, siren_builder)
            setattr(ModelClass, method_name, method_def)

        for link in self.links:
            for rel in link.rel:
                method_name = SirenEntity._create_python_method_name(rel)
                siren_builder = SirenBuilder(verify=self.verify, request_factory=self.request_factory)
                method_def = _create_action_fn(link, siren_builder)
                setattr(ModelClass, method_name, method_def)

        def get_entity(obj, rel):
            matching_entities = self.get_entities(rel) or []
            for x in matching_entities:
                yield x.as_python_object()

        setattr(ModelClass, b'get_entities', get_entity)
        return ModelClass()

    @staticmethod
    def _create_python_method_name(base_name):
        """
        Creates a valid python method name from a non-normalized base name.

        :param base_name: base string/name
        :type base_name: str
        :return: valid python method name
        :rtype: str|unicode
        """
        name = six.text_type(base_name)
        name = name.lower()
        name = re.sub(b'-', b'_', name)
        name = re.sub(b'[^a-zA-Z0-9_]', b'', name)
        matcher = re.compile(b'[a-zA-Z_][a-zA-Z0-9_]*')
        if matcher.match(name):
            return name
        raise ValueError((b'Unable to create normalized python method name! Base method name="{}". Attempted normalized name="{}"').format(base_name, name))


class SirenAction(RequestMixin):
    """Representation of a Siren Action element. Actions are operations on a hypermedia instance or class level."""

    def __init__(self, name, href, type=b'application/json', fields=None, title=None, method=b'GET', verify=False, request_factory=Request, **kwargs):
        """
        Constructor.

        :param name: method name for this action
        :type name: str|unicode
        :param href: url associated with the method
        :type href: str|unicode
        :param type: content-type of the payload
        :type type: str|unicode
        :param fields: list of fields to send with this action/request (parameters, either post or query)
        :type fields: list[dict]
        :param title: descriptive title/in-line documentation for the method
        :type title: str|unicode
        :param method: HTTP verb to use for this action (GET, PUT, POST, PATCH, HEAD, etc.)
        :type method: str|unicode
        :param request_factory: constructor for request objects
        :type type or function
        :param dict kwargs:  Extra stuff to ignore for now.
        """
        self.name = name
        self.title = title
        self.method = method
        self.href = href
        self.type = type
        self.fields = fields if fields else []
        super(SirenAction, self).__init__(request_factory=request_factory, verify=verify, **kwargs)

    @staticmethod
    def create_field(name, type=None, value=None):
        """
        Convenience method for creating a field dictionary.

        :param name: name of the field/property for this method
        :type name: str
        :param type: object type for the field (optional)
        :type type: str
        :param value: value assigned to the field (optional)
        :type value: object
        :return: dictionary with field definition
        :rtype: dict
        """
        return {b'name': name, b'type': type, b'value': value}

    def add_field(self, name, type=None, value=None):
        """
        Convenience method for adding a field.

        :param name: name of the field/property for this method
        :type name: str
        :param type: object type for the field (optional)
        :type type: str
        :param value: value assigned to the field (optional)
        :type value: object
        """
        field = self.create_field(name, type, value)
        self.fields.append(field)

    def get_fields_as_dict(self):
        """
        Gets the fields of this object as a dictionary of key/value pairs.

        :return: dictionary of field key/value pairs that will be sent with this action.
        :rtype: dict[str, object]
        """
        fields_dict = {}
        for f in self.fields:
            fields_dict[f[b'name']] = f.get(b'value', None)

        return fields_dict

    def _get_bound_href(self, template_class, **kwfields):
        """
        Gets the bound href and the
        remaining variables

        :param dict kwargs:
        :return: The templated string representing
            the href and the remaining variables
            to place in the query or request body.
        :rtype: str|unicode, dict
        """
        templated_href = template_class(self.href)
        url_params = dict(kwfields)
        bound_href = templated_href.bind(**url_params)
        if bound_href.has_unbound_variables():
            raise ValueError((b'Unbound template parameters in url detected! All variables must be specified! Unbound variables: {}').format(bound_href.unbound_variables()))
        bound_href = bound_href.as_string()
        url_variables = templated_href.unbound_variables()
        request_fields = {}
        for k, v in kwfields.items():
            if k not in url_variables:
                request_fields[k] = v

        return (
         bound_href, request_fields)

    def as_siren(self):
        """
        Returns a siren-compatible dictionary representation of this object.

        :return: siren dictionary representation of the action
        :rtype: dict
        """
        new_dict = dict(name=self.name, title=self.name, method=self.method, href=self.href, type=self.type, fields=self.fields)
        return new_dict

    def as_json(self):
        """
        Returns as a json string a siren-compatible representation of this object.

        :return: json-siren
        :rtype: str
        """
        new_dict = self.as_siren()
        return json.dumps(new_dict)

    def as_request(self, **kwfields):
        """
        Creates a Request object from this action. This Request object may be used to call-out and retrieve data from an external source.

        :param kwfields: query/post parameters to add to the request, parameter type depends upon HTTP verb in use  # limitation of siren
        :return: Request object representation of this action
        :rtype: Request
        """
        bound_href, request_fields = self._get_bound_href(TemplatedString, **kwfields)
        fields = self.get_fields_as_dict()
        fields.update(request_fields)
        fields = self.prepare_payload_parameters(**fields)
        if self.method == b'GET':
            req = self.request_factory(self.method, bound_href, params=fields)
        elif self.method in ('PUT', 'POST', 'PATCH'):
            req = self.request_factory(self.method, bound_href, data=fields)
        else:
            req = self.request_factory(self.method, bound_href)
        return req.prepare()

    def make_request(self, _session=None, **kwfields):
        """
        Performs the request.

        :param kwfields: additional items to add to the underlying request object
        :return: response from the server
        :rtype: Response
        """
        s = _session or Session()
        return s.send(self.as_request(**kwfields), verify=self.verify)

    @staticmethod
    def prepare_payload_parameters(**params):
        """
        Prepares parameters for their serialized json representation.

        :param params: query/post parameters
        :return: dictionary of prepared parameters
        :rtype: dict[str, str]
        """
        result = {}
        for k, v in params.items():
            if not v:
                continue
            if not isinstance(v, six.string_types):
                v = json.dumps(v)
            result[k] = v

        return result


class SirenLink(SirenBuilder):
    """
    Representation of a Link in Siren. Links are traversals to related objects that exist outside of normal entity
    (parent-child) ownership.
    """

    def __init__(self, rel, href, verify=False, request_factory=Request):
        """
        Constructor.

        :param rel: relationship or list relationships associated with the link
        :type rel: list[str] or str
        :param href: href
        :type href: str
        :param request_factory: constructor for request objects
        :type type or function
        :raises: ValueError
        """
        if not rel:
            raise ValueError(b'Parameter "rel" is required and must be a string or list of at least one element..')
        if isinstance(rel, six.string_types):
            rel = [
             rel]
        self.rel = list(rel)
        if not href or not isinstance(href, six.string_types):
            raise ValueError(b'Parameter "href" must be a string.')
        self.href = href
        self.verify = verify
        self.request_factory = request_factory

    def add_rel(self, new_rel):
        """
        Adds a new relationship to this link.

        :param new_rel: additional relationship to assign to this link (note that duplicate relationships will not be added)
        :type new_rel: str
        """
        if new_rel not in self.rel:
            self.rel.append(new_rel)

    def rem_rel(self, cur_rel):
        """
        Removes a relationship from this link.

        :param cur_rel: pre-existing relationship to remove (note that removing relationships not assigned to this link is a no-op)
        :type cur_rel: str|unicode
        """
        if cur_rel in self.rel:
            self.rel.remove(cur_rel)

    def as_siren(self):
        """
        Returns a siren-compatible dictionary representation of this object.

        :return: siren dictionary representation of the link
        :rtype: dict
        """
        return dict(rel=self.rel, href=self.href)

    def as_json(self):
        """
        Returns as a json string a siren-compatible representation of this object.

        :return: json-siren
        :rtype: unicode
        """
        new_dict = self.as_siren()
        return json.dumps(new_dict)

    def as_request(self, **kwfields):
        """
        Returns this link as a request.

        :param kwfields: optional and not currently used for standard links, retained for method-signature compatibility with actions
        :return: request object representing the link
        :rtype: Request
        """
        req = self.request_factory(b'GET', self.href)
        return req.prepare()

    def as_python_object(self, _session=None, **kwargs):
        """
        Constructs the link as a python object by
        first making a request and then constructing the
        corresponding object.

        :param kwfields: query/post parameters to add to the request, parameter type depends upon HTTP verb in use  # limitation of siren
        :return: The SirenEntity constructed from the respons from the api.
        :rtype: SirenEntity
        """
        resp = self.make_request(_session=_session)
        siren_entity = self.from_api_response(resp)
        return siren_entity.as_python_object()

    def make_request(self, _session=None, **kwfields):
        """
        Performs retrieval of the link from the external server.

        :param kwfields: query/post parameters to add to the request, parameter type depends upon HTTP verb in use  # limitation of siren
        :return: Request object representation of this action
        :rtype: Request
        """
        s = _session or Session()
        return s.send(self.as_request(**kwfields), verify=self.verify)


class MalformedSirenError(Exception):
    """
    siren-json representation is errant.
    """

    def __init__(self, message, errors=None):
        Exception.__init__(self, message)


class UnexpectedStatusError(Exception):
    """
    Unexpected status was returned from the service. These are errant statuses from which the library cannot recover to
    create an object.
    """

    def __init__(self, message, errors=None):
        Exception.__init__(self, message)


class TemplatedString(object):
    """
    Helper class for handling templated strings and allows for partial templating.
    """

    def __init__(self, base):
        """
        Constructor. Creates template dict.

        :param base: base string which template placeholders
        :type base: str or unicode
        """
        self.base = str(base)
        param_locator = re.compile(b'\\{[^}]+\\}')
        params = param_locator.findall(self.base)
        self.param_dict = {}
        for p in params:
            self.param_dict[p.replace(b'{', b'').replace(b'}', b'')] = p

    def items(self):
        """
        Unbound template variables and their literal string value in the list.

        :return: iterator on template dictionary
        :rtype: dict[str, str]
        """
        return self.param_dict.items()

    def unbound_variables(self):
        """
        Gets the unbound template variables.

        :return: unbound variables
        :rtype: list[str]
        """
        return self.param_dict.keys()

    def bind(self, **kwargs):
        """
        Binds the keyword arguments against the template variables. Partial binding is permitted. Later rebinding is not
        possible.

        :param kwargs: parameters and binding values
        :type kwargs: dict[str, str]
        :return: templated string with bound variables
        :rtype: TemplatedString
        """
        bound_string = self.base
        for param_key, param_val in kwargs.items():
            template = self.param_dict.get(param_key, None)
            if not template:
                continue
            bound_string = bound_string.replace(template, six.text_type(param_val))

        return TemplatedString(bound_string)

    def has_unbound_variables(self):
        """
        Checks whether there are unmet variable assignments.

        :return: True if there are unbound variables, False otherwise
        :rtype: bool
        """
        return len(self.param_dict) != 0

    def as_string(self):
        """
        Provides the string representation.

        :return: string representation.
        :rtype: str
        """
        return self.base


def _create_action_fn(action, siren_builder, **kwargs):
    """Creates an action function which will make a web request, retrieve content, and create a python object.

    :param action: action object capable of making a request
    :type action: SirenAction or SirenLink
    :param kwargs: keyword arguments for passage into the underlying requests library object
    :return: action function capable of requesting data from the server and creating a new proxy object
    :rtype: function
    """

    def _action_fn(self, **kwargs):
        response = action.make_request(verify=siren_builder.verify, **kwargs)
        siren = siren_builder.from_api_response(response=response)
        if not siren:
            return None
        else:
            return siren.as_python_object()

    return _action_fn
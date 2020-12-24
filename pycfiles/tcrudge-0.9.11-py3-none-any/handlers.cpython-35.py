# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/handlers.py
# Compiled at: 2017-01-07 12:43:01
# Size of source mod 2**32: 30127 bytes
"""
Module contains basic handlers:

* BaseHandler - to be used for custom handlers. For instance - RPC, if you wish.
* ApiHandler - Abstract for API handlers above.
* ApiListHandler - Create (POST), List view (GET).
* ApiItemHandler - detailed view (GET), Update (PUT), Delete (DELETE).
"""
import json, operator, traceback
from abc import ABCMeta, abstractmethod
import peewee
from jsonschema.validators import validator_for
from playhouse.shortcuts import model_to_dict
from tornado import web
from tornado.gen import multi
from tcrudge.exceptions import HTTPError
from tcrudge.models import FILTER_MAP
from tcrudge.response import response_json, response_msgpack
from tcrudge.utils.validation import validate_integer

class BaseHandler(web.RequestHandler):
    __doc__ = "\n    Base helper class. Provides basic handy responses.\n\n    To be used for customized handlers that don't fit REST API recommendations.\n\n    Defines response types in relation to Accept header. Response interface is\n    described in corresponding module.\n\n    By default, inherited handlers have callback functions for JSON and\n    MessagePack responses.\n    "
    response_callbacks = {'application/json': response_json, 
     'application/x-msgpack': response_msgpack}

    def get_response(self, result=None, errors=None, **kwargs):
        """
        Method returns conventional formatted byte answer.

        It gets Accept header, returns answer processed by callback.

        :param result: contains result if succeeded
        :param errors: contains errors if any
        :param kwargs: other answer attributes
        :return: byte answer of appropriate content type
        :rtype: bytes

        """
        _errors = errors or []
        success = not _errors
        answer = {'result': result, 
         'errors': _errors, 
         'success': success}
        accept = self.request.headers.get('Accept', 'application/json')
        callback = self.response_callbacks.get(accept, response_json)
        return callback(self, {**answer, **kwargs})

    def response(self, result=None, errors=None, **kwargs):
        """
        Method writes the response and finishes the request.

        :param result: contains result if succeeded
        :param errors: contains errors if any
        :param kwargs: other answer attributes
        """
        self.write(self.get_response(result, errors, **kwargs))
        self.finish()

    def write_error(self, status_code, **kwargs):
        """
        Method gets traceback, writes it into response, finishes response.

        :param status_code: tornado parameter to format html, we don't use it.
        :type status_code: int
        :param kwargs: in debug mode must contain exc_info.
        :type kwargs: dict
        """
        exc_info = kwargs.get('exc_info')
        if self.settings.get('serve_traceback') and exc_info:
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*exc_info):
                self.write(line)

        else:
            self.write(getattr(exc_info[1], 'body', self._reason))
        self.finish()

    async def validate(self, data, schema, **kwargs):
        """
        Method to validate parameters.
        Raises HTTPError(400) with error info for invalid data.

        :param data: bytes or dict
        :param schema: dict, valid JSON schema
          (http://json-schema.org/latest/json-schema-validation.html)
        :return: None if data is not valid. Else dict(data)
        """
        if isinstance(data, dict):
            _data = data
        else:
            try:
                _data = json.loads(data.decode())
            except ValueError as e:
                raise HTTPError(400, body=self.get_response(errors=[
                 {'code': '', 
                  'message': 'Request body is not a valid json object', 
                  'detail': str(e)}]))

        v = validator_for(schema)(schema)
        errors = []
        for error in v.iter_errors(_data):
            errors.append({'code': '', 'message': 'Validation failed', 'detail': error.message})

        if errors:
            raise HTTPError(400, body=self.get_response(errors=errors))
        return _data

    async def bad_permissions(self):
        """
        Returns answer of access denied.

        :raises: HTTPError 401
        """
        raise HTTPError(401, body=self.get_response(errors=[
         {'code': '', 
          'message': 'Access denied'}]))

    async def is_auth(self):
        """
        Validate user authorized. Abstract. Auth logic is up to user.
        """
        return True

    async def get_roles(self):
        """
        Gets roles. Abstract. Auth logic is up to user.
        """
        return []


class ApiHandler(BaseHandler, metaclass=ABCMeta):
    __doc__ = '\n    Base helper class for API functions.\n    model_cls MUST be defined.\n    '
    exclude_fields = ()
    recurse = False
    max_depth = None

    @property
    @abstractmethod
    def model_cls(self):
        """
        Model class must be defined. Otherwise it'll crash a little later even
        if nothing seems to be accessing a model class. If you think you don't
        need a model class, consider the architecture. Maybe it doesn't
        fit REST. In that case use BaseHandler.

        https://github.com/CodeTeam/tcrudge/issues/6
        """
        raise NotImplementedError('Model class must be defined.')

    @property
    def get_schema_output(self):
        """
        Maybe you'd ask: "What's a get-schema?"

        The answer is that we wanted to check input of every request method
        in a homologous way. So we decided to describe any input and output
        using JSON schema.

        Schema must be a dict.
        """
        return {}

    async def serialize(self, model):
        """
        Method to serialize a model.

        By default all fields are serialized by model_to_dict.
        The model can be any model instance to pass through this method. It
        MUST be a Model instance, it won't work for basic types containing
        such instances.

        User have to handle it by their own hands.

        :param model: Model instance to serialize.
        :type model: Model instance.
        :return: serialized model.
        :rtype: dict
        """
        return model_to_dict(model, recurse=self.recurse, exclude=self.exclude_fields, max_depth=self.max_depth)


class ApiListHandler(ApiHandler):
    __doc__ = '\n    Base List API Handler. Supports C, L from CRUDL.\n    Handles pagination,\n\n    * default limit is defined\n    * maximum limit is defined\n\n    One can redefine that in their code.\n\n    Other pagination parameters are:\n\n    * limit - a positive number of items to show on a single page, int.\n    * offset - a positive int to define the position in result set to start with.\n    * total - A boolean to define total amount of items to be put in result set or not. 1 or 0.\n\n    Those parameters can be sent as either GET parameters or HTTP headers.\n    HTTP headers are more significant during parameters processing, but GET\n    parameters are preferable to use as conservative way of pagination.\n    HTTP headers are:\n\n    * X-Limit\n    * X-Offset\n    * X-Total\n\n    "exclude" filter args are for pagination, you must not redefine them ever.\n    Otherwise you\'d have to also redefine the prepare method.\n\n    Some fieldnames can be added to that list. Those are fields one wishes not\n    to be included to filters.\n    '
    default_limit = 50
    max_limit = 100
    exclude_filter_args = [
     'limit', 'offset', 'total']

    def __init__(self, *args, **kwargs):
        super(ApiListHandler, self).__init__(*args, **kwargs)
        self.limit = None
        self.offset = None
        self.total = False
        self.prefetch_queries = []

    @property
    def get_schema_input(self):
        """
        JSON Schema to validate GET Url parameters.
        By default it contains pagination parameters as required fields.
        If you wish to use query filters via GET parameters, you need to
        redefine get_schema_input so that request with filter parameters
        would be valid.

        In schema you must define every possible way to filter a field,
        you wish to be filtered, in every manner it should be filtered.
        For example, if you wish to filter by a field "name" so that the query
        returns you every object with name like given string::

          {
              "type": "object",
              "additionalProperties": False,
              "properties": {
                "name__like": {"type": "string"},
                "total": {"type": "string"},
                "limit": {"type": "string"},
                "offset": {"type": "string"},
                "order_by": {"type": "string"},
              },
          }

        If you wish to filter by a field "created_dt" by given range::

          {
              "type": "object",
              "additionalProperties": False,
              "properties": {
                "created_dt__gte": {"type": "string"},
                "created_dt__lte": {"type": "string"},
                "total": {"type": "string"},
                "limit": {"type": "string"},
                "offset": {"type": "string"},
                "order_by": {"type": "string"},
              },
          }

        To cut it short, you need to add parameters like "field__operator"
        for every field you wish to be filtered and for every operator you
        wish to be used.

        Every schema must be a dict.

        :return: returns schema.
        :rtype: dict
        """
        return {'type': 'object', 
         'additionalProperties': False, 
         'properties': {'total': {'type': 'string'}, 
                        'limit': {'type': 'string'}, 
                        'offset': {'type': 'string'}, 
                        'order_by': {'type': 'string'}}}

    @property
    def post_schema_input(self):
        """
        JSON Schema to validate POST request body. Abstract.

        Every schema must be a dict.

        :return: dict
        """
        return {}

    @property
    def post_schema_output(self):
        """
        JSON schema of our model is generated here. Basically it is used for
        Create method - list handler, method POST.

        Hint: Modified version of this schema can be used for Update (PUT,
        detail view).

        :return: JSON schema of given model_cls Model.
        :rtype: dict
        """
        return self.model_cls.to_schema(excluded=['id'])

    @property
    def default_filter(self):
        """
        Default queryset WHERE clause. Used for list queries first.
        One must redefine it to customize filters.

        :return: dict
        """
        return {}

    @property
    def default_order_by(self):
        """
        Default queryset ORDER BY clause. Used for list queries.
        Order by must contain a string with a model field name.
        """
        return ()

    def prepare(self):
        """
        Method to get and validate offset and limit params for GET REST request.
        Total is boolean 1 or 0.

        Works for GET method only.
        """
        if self.request.method == 'GET':
            limit = self.request.headers.get('X-Limit', self.get_query_argument('limit', self.default_limit))
            self.limit = validate_integer(limit, 1, self.max_limit, self.default_limit)
            offset = self.request.headers.get('X-Offset', self.get_query_argument('offset', 0))
            self.offset = validate_integer(offset, 0, None, 0)
            self.total = 'X-Total' in self.request.headers or self.get_query_argument('total', None) == '1'

    @classmethod
    def qs_filter(cls, qs, flt, value, process_value=True):
        """
        Private method to set WHERE part of query.
        If required, Django-style filter is available via qs.filter()
        and peewee.DQ - this method provides joins.

        Filter relational operators are:
        * NOT - '-', not operator, should be user as prefix
        * < - 'lt', less than
        * > - 'gt', greater than
        * <= - 'lte', less than or equal
        * >= - 'gte', greater than or equal
        * != - 'ne', not equal
        * LIKE - 'like', classic like operator
        * ILIKE - 'ilike', case-insensitive like operator
        * IN - 'in', classic in. Values should be separated by comma
        * ISNULL - 'isnull', operator to know if smth is equal to null. Use -<fieldname>__isnull for IS NOT NULL
        """
        neg = False
        if flt[0] in '-':
            neg = True
            flt = flt[1:]
        fld_name, _, k = flt.rpartition('__')
        if not fld_name:
            fld_name, k = k, ''
        op = FILTER_MAP.get(k, operator.eq)
        if neg:
            _op = op
            op = lambda f, x: operator.inv(_op(f, x))
        fld = getattr(cls.model_cls, fld_name)
        if process_value:
            _v = value.decode()
            if isinstance(fld, peewee.BooleanField) and _v in ('0', 'f'):
                _v = False
            else:
                if k == 'in':
                    _v = _v.split(',')
                elif k == 'isnull':
                    _v = None
        else:
            _v = value
        return qs.where(op(fld, _v))

    @classmethod
    def qs_order_by(cls, qs, value, process_value=True):
        """
        Set ORDER BY part of response.

        Fields are passed in a string with commas to separate values.
        '-' prefix means descending order, otherwise it is ascending order.

        :return: orderbyed queryset
        :rtype: queryset
        """
        if process_value:
            _v = (_ for _ in value.decode().split(',') if _)
        else:
            _v = (
             value,)
        for ordr in _v:
            if ordr[0] == '-':
                fld = getattr(cls.model_cls, ordr[1:])
                qs = qs.order_by(fld.desc(), extend=True)
            else:
                fld = getattr(cls.model_cls, ordr)
                qs = qs.order_by(fld, extend=True)

        return qs

    def get_queryset(self, paginate=True):
        """
        Get queryset for model.
        Override this method to change logic.

        By default it uses qs_filter and qs_order_by.
        All arguments for WHERE clause are passed with AND condition.
        """
        qs = self.model_cls.select()
        if paginate:
            qs = qs.limit(self.limit).offset(self.offset)
        for k, v in self.default_filter.items():
            qs = self.qs_filter(qs, k, v, process_value=False)

        for v in self.default_order_by:
            qs = self.qs_order_by(qs, v, process_value=False)

        for k, v in self.request.arguments.items():
            if k in self.exclude_filter_args:
                continue
            else:
                if k == 'order_by':
                    qs = self.qs_order_by(qs, v[0])
                else:
                    qs = self.qs_filter(qs, k, v[0])

        return qs

    async def _get_items(self, qs):
        """
        Gets queryset and paginates it.
        It executes database query. If total amount of items should be
        received (self.total = True), queries are executed in parallel.

        :param qs: peewee queryset
        :return: tuple: executed query, pagination info (dict)
        :raises: In case of bad query parameters - HTTP 400.
        """
        pagination = {'offset': self.offset}
        try:
            if self.total:
                awaitables = []
                qs_total = self.get_queryset(paginate=False)
                if self.prefetch_queries:
                    awaitables.append(self.application.objects.prefetch(qs, *self.prefetch_queries))
                else:
                    awaitables.append(self.application.objects.execute(qs))
                awaitables.append(self.application.objects.count(qs_total))
                items, total = await multi(awaitables)
                pagination['total'] = total
            else:
                if self.prefetch_queries:
                    items = await self.application.objects.prefetch(qs, *self.prefetch_queries)
                else:
                    items = await self.application.objects.execute(qs)
        except (peewee.DataError, ValueError) as e:
            raise HTTPError(400, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Bad query arguments', 
              'detail': str(e)}]))

        pagination['limit'] = len(items)
        return (
         items, pagination)

    async def get(self):
        """
        Handles GET request.

        1. Validates GET parameters using GET input schema and validator.
        2. Executes query using given query parameters.
        3. Paginates.
        4. Serializes result.
        5. Writes to response, not finishing it.

        :raises: In case of bad query parameters - HTTP 400.
        """
        await self.validate({k:self.get_argument(k) for k in self.request.query_arguments.keys()}, self.get_schema_input)
        try:
            qs = self.get_queryset()
        except AttributeError as e:
            raise HTTPError(400, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Bad query arguments', 
              'detail': str(e)}]))

        items, pagination = await self._get_items(qs)
        result = []
        for m in items:
            result.append(await self.serialize(m))

        self.response(result={'items': result}, pagination=pagination)

    async def head(self):
        """
        Handles HEAD request.

        1. Validates GET parameters using GET input schema and validator.
        2. Fetches total amount of items and returns it in X-Total header.
        3. Finishes response.

        :raises: In case of bad query parameters - HTTPError 400.
        """
        await self.validate({k:self.get_argument(k) for k in self.request.query_arguments.keys()}, self.get_schema_input)
        try:
            qs = self.get_queryset(paginate=False)
        except AttributeError as e:
            raise HTTPError(400)

        try:
            total_num = await self.application.objects.count(qs)
        except (peewee.DataError, peewee.ProgrammingError, ValueError) as e:
            raise HTTPError(400)

        self.set_header('X-Total', total_num)
        self.finish()

    async def post(self):
        """
        Handles POST request.
        Validates data and creates new item.
        Returns serialized object written to response.

        HTTPError 405 is raised in case of not creatable model (there must be
        _create method implemented in model class).

        HTTPError 400 is raised in case of violated constraints, invalid
        parameters and other data and integrity errors.

        :raises: HTTPError 405, 400
        """
        data = await self.validate(self.request.body, self.post_schema_input)
        try:
            item = await self.model_cls._create(self.application, data)
        except AttributeError as e:
            raise HTTPError(405, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Method not allowed', 
              'detail': str(e)}]))
        except (peewee.IntegrityError, peewee.DataError) as e:
            raise HTTPError(400, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Invalid parameters', 
              'detail': str(e)}]))

        self.response(result=await self.serialize(item))


class ApiItemHandler(ApiHandler):
    __doc__ = '\n    Base Item API Handler.\n    Supports R, U, D from CRUDL.\n    '

    def __init__(self, *args, **kwargs):
        super(ApiItemHandler, self).__init__(*args, **kwargs)
        self._instance = None

    @property
    def get_schema_input(self):
        """
        JSON Schema to validate DELETE request body.

        :returns: GET JSON schema
        :rtype: dict
        """
        return {'type': 'object', 
         'additionalProperties': False, 
         'properties': {}}

    @property
    def put_schema_input(self):
        """
        JSON Schema to validate PUT request body.

        :return: JSON schema of PUT
        :rtype: dict
        """
        return self.model_cls.to_schema(excluded=['id'])

    @property
    def delete_schema_input(self):
        """
        JSON Schema to validate DELETE request body.

        :returns: JSON schema for DELETE.
        :rtype: dict
        """
        return {'type': 'object', 
         'additionalProperties': False, 
         'properties': {}}

    @property
    def put_schema_output(self):
        """
        Returns PUT Schema, empty be default.

        :rtype: dict
        """
        return {}

    @property
    def delete_schema_output(self):
        """
        Returns DELETE Schema, empty be default.

        :rtype: dict
        """
        return {}

    async def get_item(self, item_id):
        """
        Fetches item from database by PK.
        Result is cached in self._instance for multiple calls

        :raises: HTTP 404 if no item found.
        :returns: raw object if exists.
        :rtype: ORM model instance.
        """
        if not self._instance:
            try:
                self._instance = await self.application.objects.get(self.model_cls, **{self.model_cls._meta.primary_key.name: item_id})
            except (self.model_cls.DoesNotExist, ValueError) as e:
                raise HTTPError(404, body=self.get_response(errors=[
                 {'code': '', 
                  'message': 'Item not found', 
                  'detail': str(e)}]))

            return self._instance

    async def get(self, item_id):
        """
        Handles GET request.

        1. Validates request.
        2. Writes serialized object of ORM model instance to response.
        """
        await self.validate({k:self.get_argument(k) for k in self.request.query_arguments.keys()}, self.get_schema_input, item_id=item_id)
        item = await self.get_item(item_id)
        self.response(result=await self.serialize(item))

    async def put(self, item_id):
        """
        Handles PUT request.
        Validates data and updates given item.

        Returns serialized model.

        Raises 405 in case of not updatable model (there must be
        _update method implemented in model class).

        Raises 400 in case of violated constraints, invalid parameters and other
        data and integrity errors.

        :raises: HTTP 405, HTTP 400.
        """
        item = await self.get_item(item_id)
        data = await self.validate(self.request.body, self.put_schema_input, item_id=item_id)
        try:
            item = await item._update(self.application, data)
        except AttributeError as e:
            raise HTTPError(405, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Method not allowed', 
              'detail': str(e)}]))
        except (peewee.IntegrityError, peewee.DataError) as e:
            raise HTTPError(400, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Invalid parameters', 
              'detail': str(e)}]))

        self.response(result=await self.serialize(item))

    async def delete(self, item_id):
        """
        Handles DELETE request.

        _delete method must be defined to handle delete logic. If method
        is not defined, HTTP 405 is raised.

        If deletion is finished, writes to response HTTP code 200 and
        a message 'Item deleted'.

        :raises: HTTPError 405 if model object is not deletable.
        """
        await self.validate(self.request.body or {}, self.delete_schema_input, item_id=item_id)
        item = await self.get_item(item_id)
        try:
            await item._delete(self.application)
        except AttributeError as e:
            raise HTTPError(405, body=self.get_response(errors=[
             {'code': '', 
              'message': 'Method not allowed', 
              'detail': str(e)}]))

        self.response(result='Item deleted')
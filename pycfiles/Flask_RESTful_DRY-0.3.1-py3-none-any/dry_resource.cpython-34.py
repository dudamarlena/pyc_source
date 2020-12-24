# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bruce/GoTonight/restful_poc/Flask-RESTful-DRY/build/lib/flask_dry/api/dry_resource.py
# Compiled at: 2015-04-13 11:30:26
# Size of source mod 2**32: 15106 bytes
import types
from functools import partial
from copy import deepcopy
import re
from flask import request, current_app
from flask.views import MethodViewType
from flask.ext.restful import Resource, abort
from .class_init import declarative
from .step_utils import generate_steps
from .steps import QuitSteps
from .links import register_link
from .column_auth import action_column_auth, Get_column_suffixes, List_column_suffixes, Update_column_suffixes, Insert_column_suffixes
from .query_categories import query_category, get_query_category
from .allow import Deny
from ..model.utils import transaction, now_truncated
Debug_header = 'X-DRY-Debug'

class DRY_Resource(metaclass=declarative):
    __doc__ = 'Base class for all DRY_Resources.\n\n    This class is subclassed for each desired resource.  The subclasses may be\n    further subclassed to nest the subclass resource under the parent class\n    resource in terms of the url path.\n    '
    url_classes = ()
    url = '/api'
    get_method = None
    put_method = None
    post_method = None
    delete_method = None
    cache_public = True
    cache_max_age = 3600
    debug = 0
    trace = False
    trace_final = False
    show_unused_steps = False
    step_fns = ()
    query_categories = ()
    queries = ()
    no_query_parameters_ok = True
    get_column_suffixes = ('columns', )
    list_column_suffixes = ('list_columns', ) + get_column_suffixes
    update_column_suffixes = ('update_columns', ) + get_column_suffixes
    insert_column_suffixes = ('insert_columns', ) + update_column_suffixes
    columns = Deny('created_by', 'created_timestamp', 'last_modified_by', 'last_modified_timestamp', 'etag', 'admin_notes')
    update_columns = columns.denying('id').allowing('admin_notes')
    authorization_requirements = ()
    output_bytes = None
    last_modified = None
    provided_attributes = ('top_model', 'method', 'url_parameters', 'headers', 'output',
                           'now')

    @classmethod
    def resource_init(cls, api):
        """Sets url and creates subordinate url classes.

        Returns {relation: {method: dummy, relation: ...}}.
        """
        if getattr(cls, 'relation_category', None) is None:
            cls.relation_category = cls.__name__.lower()
        if getattr(cls, 'resource_extension', None) is None:
            cls.resource_extension = '/' + cls.relation_category
        if getattr(cls, 'auth_model', None) is None:
            if getattr(cls, 'model', None) is not None:
                cls.auth_model = cls.model
        cls.relations = {}
        cls.url = cls.url.rstrip('/') + cls.resource_extension
        url_dummies = {}
        cls.create_url_classes(cls, api, url_dummies)
        return url_dummies

    @classmethod
    def create_url_classes(cls, resource_class, api, url_dummies, dummy_path=(), base_url_class=None):
        """Used by both resource_init and url_init.

        Resource_init doesn't pass a base_url_class, while url_init does.

        Adds {method: dummy, relation: ...} to dummy_path in url_dummies.
        """
        for relation in cls.url_classes:
            if isinstance(relation, str):
                relation_name, url_base_class = relation, None
            else:
                relation_name, url_base_class = relation
            if url_base_class is None:
                if base_url_class is None:
                    bases = (url, resource_class)
                else:
                    bases = (
                     base_url_class,)
            else:
                if base_url_class is None:
                    bases = (url_base_class, resource_class)
                else:
                    bases = (
                     url_base_class, base_url_class)
            url_class = types.new_class('{}_{}'.format(resource_class.__name__, relation_name), bases)
            resource_class.relations[relation_name] = url_class
            url_class.url_init(resource_class, relation, api, getattr(cls, relation_name), url_dummies, dummy_path + (relation_name,))

    def column_auth_for_get(self, prefix=''):
        return action_column_auth(self, Get_column_suffixes, prefix)

    def column_auth_for_list(self, prefix=''):
        return action_column_auth(self, List_column_suffixes, prefix)

    def column_auth_for_update(self, prefix=''):
        return action_column_auth(self, Update_column_suffixes, prefix)

    def column_auth_for_insert(self, prefix=''):
        return action_column_auth(self, Insert_column_suffixes, prefix)


werkzeug_to_format = partial(re.compile('<(?:[^:>]*:)?([^>]*)>').sub, '{\\1}')
format_to_keys = re.compile('{([^}]*)}').findall

class url_metaclass(declarative, MethodViewType):
    pass


class url(Resource, metaclass=url_metaclass):
    __doc__ = 'This is a Flask-RESTful Resource.\n\n    This is subclassed for each url path, and is what the Flask http request\n    dispatching lands on.  Each of these subclasses is also a subclass of\n    :class:`.DRY_Resource`.\n\n    The various http methods are generalized here into a single :method:`._run`\n    method.  The self object acts as a request context, storing all values\n    relating to that one request.\n\n    Since different http methods require different contexts, the context\n    related to the http method invoked is added to self by _run.  This\n    default context values may be assigned as class variables to either the\n    url class or the parent DRY_Resource class; and then be overridden, as\n    needed, for each http method.\n\n    This context includes the list of `steps` to run to process the http\n    method.  Each step is simply a function taking this url object as a\n    parameter for its context.  It may reference, as well as modify, the\n    context; which then gets passed to subsequent steps.  Setting up the steps\n    to processing an http method as a simple context value makes it much\n    easier to use many different combinations of a set of simple steps to\n    accomplish whatever the various kinds of http methods need to be done.\n\n    The alternative, using subclassing, would be unmanageable and end up\n    requiring repeating the same code sequences many times.\n    '

    @classmethod
    def url_init(cls, resource_class, relation, api, initial_context, url_dummies, dummy_path):
        """Initializes the url class (not the objects).

        Adds {method: dummy} to the dummy_path of url_dummies.

        First, let's check out our regular expressions:

            >>> werkzeug_to_format('/api/members/<int:member_id>')
            '/api/members/{member_id}'
            >>> werkzeug_to_format('/api/members/<member_id>')
            '/api/members/{member_id}'
            >>> format_to_keys('/api/members/{member_id}/{bogus_id}')
            ['member_id', 'bogus_id']
        """
        cls.resource_class = resource_class
        cls.url_classes = ()
        cls.init_fn = None
        initial_context.copy_into(cls)
        if not hasattr(cls, 'relation') or cls.relation == getattr(super(cls, cls), 'relation', None):
            cls.relation = relation
        if not hasattr(cls, 'url_extension'):
            cls.url_extension = '/' + cls.relation
        cls.url = cls.url.rstrip('/') + cls.url_extension
        cls.url_format = werkzeug_to_format(cls.url)
        cls.keys = tuple(sorted(format_to_keys(cls.url_format)))
        cls.provided_attributes += cls.keys
        bottom_dummy = url_dummies
        for p in dummy_path[:-1]:
            bottom_dummy = bottom_dummy[p]

        method_dummies = bottom_dummy[dummy_path[(-1)]] = {}
        if cls.init_fn is not None:
            cls.init_fn(cls, url_dummies, dummy_path)
        needs_link = False
        authorization_requirements = ()
        no_authorization_needed = False
        for method in ('get_method', 'put_method', 'delete_method', 'post_method'):
            nl, dummy = cls.compile_method(api.app, method)
            if nl:
                needs_link = True
            if dummy is not None:
                method_dummies[method] = dummy
                auth_requirements = dummy.authorization_requirements
                if auth_requirements:
                    authorization_requirements += auth_requirements
                else:
                    no_authorization_needed = True
                    continue

        if needs_link:
            register_link(api.app, cls.keys, cls.relation_category, cls.relation, cls.url_format, () if no_authorization_needed else authorization_requirements)
        api.add_resource(cls, cls.url)
        cls.create_url_classes(cls.resource_class, api, url_dummies, dummy_path, cls)

    @classmethod
    def compile_method(cls, app, method):
        """Returns needs_link, dummy.

        Needs_link is True iff this method can be called without any query
        parameters (in which case, it needs a link registered for it,
        otherwise, the queries will register their links).

        Dummy is None if this method is None.
        """
        method_attrs = getattr(cls, method, None)
        if method_attrs is not None:
            method_attrs = deepcopy(method_attrs)
            needs_link, dummy = cls.compile_method_attrs(app, method, method_attrs)
            setattr(cls, method, method_attrs)
            return (
             needs_link, dummy)
        return (False, None)

    @classmethod
    def compile_method_attrs(cls, app, method, method_attrs):

        def make_dummy_context():
            dummy = cls()
            dummy.url_class_name = cls.__name__
            dummy.location = method
            method_attrs.copy_into(dummy)
            return dummy

        dummy = make_dummy_context()
        trace = dummy.trace
        trace_final = dummy.trace_final
        show_unused_steps = dummy.show_unused_steps
        if trace:
            print('compiling', dummy.url_class_name, dummy.location)
        if dummy.queries:
            if dummy.query_categories:
                raise AssertionError('{}.{}: has both query_categories and queries'.format(dummy.url_class_name, dummy.location))
            else:
                dummy.query_categories = (
                 query_category(dummy.queries),)
        method_attrs.query_categories = tuple(deepcopy(qc) for qc in dummy.query_categories)
        for qc in method_attrs.query_categories:
            qc.compile(app, make_dummy_context())

        needs_link = False
        if dummy.no_query_parameters_ok:
            method_attrs.steps = dummy.compile_steps(trace, trace_final, show_unused_steps)
            needs_link = True
        return (needs_link, dummy)

    def compile_steps(self, trace, trace_final, show_unused_steps):
        """Creates the tuple of steps to execute in the order of execution.
        """
        ans = tuple(generate_steps(self, trace, show_unused_steps))
        if trace or trace_final:
            print('{}.{} steps:'.format(self.url_class_name, self.location), tuple([s.__name__ for s in ans]))
            print()
        return ans

    def post(self, **url_parameters):
        return self._run('post', url_parameters)

    def get(self, **url_parameters):
        return self._run('get', url_parameters)

    def put(self, **url_parameters):
        return self._run('put', url_parameters)

    def delete(self, **url_parameters):
        return self._run('delete', url_parameters)

    def _run(self, method, url_parameters):
        if current_app.debug:
            if Debug_header in request.headers:
                self.debug = int(request.headers[Debug_header])
        method_attrs_name = method + '_method'
        method_attrs = getattr(self, method_attrs_name, None)
        if method_attrs is None:
            abort(405)
        method_attrs.copy_into(self)
        self.top_model = getattr(self, 'model', None)
        self.method = method
        self.url_parameters = url_parameters
        for k, v in url_parameters.items():
            setattr(self, k, v)

        self.headers = {}
        self.output = {}
        self.now = now_truncated()
        args = request.args
        qc = get_query_category(self.query_categories, frozenset(args.keys()))
        if qc is None:
            if not self.no_query_parameters_ok:
                abort(400, message='missing query parameter(s)')
        else:
            qc.prepare_context(self, args)
        with transaction():
            try:
                for step in self.steps:
                    step(context=self)

            except QuitSteps:
                pass

        return self.response
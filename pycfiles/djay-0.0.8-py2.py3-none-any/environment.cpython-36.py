# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/jinja2/jinja2/environment.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 50849 bytes
"""
    jinja2.environment
    ~~~~~~~~~~~~~~~~~~

    Provides a class that holds runtime and parsing time options.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
import os, sys, weakref
from functools import reduce, partial
from jinja2 import nodes
from jinja2.defaults import BLOCK_START_STRING, BLOCK_END_STRING, VARIABLE_START_STRING, VARIABLE_END_STRING, COMMENT_START_STRING, COMMENT_END_STRING, LINE_STATEMENT_PREFIX, LINE_COMMENT_PREFIX, TRIM_BLOCKS, NEWLINE_SEQUENCE, DEFAULT_FILTERS, DEFAULT_TESTS, DEFAULT_NAMESPACE, DEFAULT_POLICIES, KEEP_TRAILING_NEWLINE, LSTRIP_BLOCKS
from jinja2.lexer import get_lexer, TokenStream
from jinja2.parser import Parser
from jinja2.nodes import EvalContext
from jinja2.compiler import generate, CodeGenerator
from jinja2.runtime import Undefined, new_context, Context
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound, TemplatesNotFound, TemplateRuntimeError
from jinja2.utils import import_string, LRUCache, Markup, missing, concat, consume, internalcode, have_async_gen
from jinja2._compat import imap, ifilter, string_types, iteritems, text_type, reraise, implements_iterator, implements_to_string, encode_filename, PY2, PYPY
_spontaneous_environments = LRUCache(10)
_make_traceback = None

def get_spontaneous_environment(*args):
    """Return a new spontaneous environment.  A spontaneous environment is an
    unnamed and unaccessible (in theory) environment that is used for
    templates generated from a string and not from the file system.
    """
    try:
        env = _spontaneous_environments.get(args)
    except TypeError:
        return Environment(*args)
    else:
        if env is not None:
            return env
        else:
            _spontaneous_environments[args] = env = Environment(*args)
            env.shared = True
            return env


def create_cache(size):
    """Return the cache class for the given size."""
    if size == 0:
        return
    else:
        if size < 0:
            return {}
        return LRUCache(size)


def copy_cache(cache):
    """Create an empty copy of the given cache."""
    if cache is None:
        return
    else:
        if type(cache) is dict:
            return {}
        return LRUCache(cache.capacity)


def load_extensions(environment, extensions):
    """Load the extensions from the list and bind it to the environment.
    Returns a dict of instantiated environments.
    """
    result = {}
    for extension in extensions:
        if isinstance(extension, string_types):
            extension = import_string(extension)
        result[extension.identifier] = extension(environment)

    return result


def fail_for_missing_callable(string, name):
    msg = string % name
    if isinstance(name, Undefined):
        try:
            name._fail_with_undefined_error()
        except Exception as e:
            msg = '%s (%s; did you forget to quote the callable name?)' % (msg, e)

    raise TemplateRuntimeError(msg)


def _environment_sanity_check(environment):
    """Perform a sanity check on the environment."""
    if not issubclass(environment.undefined, Undefined):
        raise AssertionError('undefined must be a subclass of undefined because filters depend on it.')
    else:
        assert environment.block_start_string != environment.variable_start_string != environment.comment_start_string, 'block, variable and comment start strings must be different'
        assert environment.newline_sequence in ('\r', '\r\n', '\n'), 'newline_sequence set to unknown line ending string.'
    return environment


class Environment(object):
    __doc__ = "The core component of Jinja is the `Environment`.  It contains\n    important shared variables like configuration, filters, tests,\n    globals and others.  Instances of this class may be modified if\n    they are not shared and if no template was loaded so far.\n    Modifications on environments after the first template was loaded\n    will lead to surprising effects and undefined behavior.\n\n    Here are the possible initialization parameters:\n\n        `block_start_string`\n            The string marking the beginning of a block.  Defaults to ``'{%'``.\n\n        `block_end_string`\n            The string marking the end of a block.  Defaults to ``'%}'``.\n\n        `variable_start_string`\n            The string marking the beginning of a print statement.\n            Defaults to ``'{{'``.\n\n        `variable_end_string`\n            The string marking the end of a print statement.  Defaults to\n            ``'}}'``.\n\n        `comment_start_string`\n            The string marking the beginning of a comment.  Defaults to ``'{#'``.\n\n        `comment_end_string`\n            The string marking the end of a comment.  Defaults to ``'#}'``.\n\n        `line_statement_prefix`\n            If given and a string, this will be used as prefix for line based\n            statements.  See also :ref:`line-statements`.\n\n        `line_comment_prefix`\n            If given and a string, this will be used as prefix for line based\n            comments.  See also :ref:`line-statements`.\n\n            .. versionadded:: 2.2\n\n        `trim_blocks`\n            If this is set to ``True`` the first newline after a block is\n            removed (block, not variable tag!).  Defaults to `False`.\n\n        `lstrip_blocks`\n            If this is set to ``True`` leading spaces and tabs are stripped\n            from the start of a line to a block.  Defaults to `False`.\n\n        `newline_sequence`\n            The sequence that starts a newline.  Must be one of ``'\\r'``,\n            ``'\\n'`` or ``'\\r\\n'``.  The default is ``'\\n'`` which is a\n            useful default for Linux and OS X systems as well as web\n            applications.\n\n        `keep_trailing_newline`\n            Preserve the trailing newline when rendering templates.\n            The default is ``False``, which causes a single newline,\n            if present, to be stripped from the end of the template.\n\n            .. versionadded:: 2.7\n\n        `extensions`\n            List of Jinja extensions to use.  This can either be import paths\n            as strings or extension classes.  For more information have a\n            look at :ref:`the extensions documentation <jinja-extensions>`.\n\n        `optimized`\n            should the optimizer be enabled?  Default is ``True``.\n\n        `undefined`\n            :class:`Undefined` or a subclass of it that is used to represent\n            undefined values in the template.\n\n        `finalize`\n            A callable that can be used to process the result of a variable\n            expression before it is output.  For example one can convert\n            ``None`` implicitly into an empty string here.\n\n        `autoescape`\n            If set to ``True`` the XML/HTML autoescaping feature is enabled by\n            default.  For more details about autoescaping see\n            :class:`~jinja2.utils.Markup`.  As of Jinja 2.4 this can also\n            be a callable that is passed the template name and has to\n            return ``True`` or ``False`` depending on autoescape should be\n            enabled by default.\n\n            .. versionchanged:: 2.4\n               `autoescape` can now be a function\n\n        `loader`\n            The template loader for this environment.\n\n        `cache_size`\n            The size of the cache.  Per default this is ``400`` which means\n            that if more than 400 templates are loaded the loader will clean\n            out the least recently used template.  If the cache size is set to\n            ``0`` templates are recompiled all the time, if the cache size is\n            ``-1`` the cache will not be cleaned.\n\n            .. versionchanged:: 2.8\n               The cache size was increased to 400 from a low 50.\n\n        `auto_reload`\n            Some loaders load templates from locations where the template\n            sources may change (ie: file system or database).  If\n            ``auto_reload`` is set to ``True`` (default) every time a template is\n            requested the loader checks if the source changed and if yes, it\n            will reload the template.  For higher performance it's possible to\n            disable that.\n\n        `bytecode_cache`\n            If set to a bytecode cache object, this object will provide a\n            cache for the internal Jinja bytecode so that templates don't\n            have to be parsed if they were not changed.\n\n            See :ref:`bytecode-cache` for more information.\n\n        `enable_async`\n            If set to true this enables async template execution which allows\n            you to take advantage of newer Python features.  This requires\n            Python 3.6 or later.\n    "
    sandboxed = False
    overlayed = False
    linked_to = None
    shared = False
    exception_handler = None
    exception_formatter = None
    code_generator_class = CodeGenerator
    context_class = Context

    def __init__(self, block_start_string=BLOCK_START_STRING, block_end_string=BLOCK_END_STRING, variable_start_string=VARIABLE_START_STRING, variable_end_string=VARIABLE_END_STRING, comment_start_string=COMMENT_START_STRING, comment_end_string=COMMENT_END_STRING, line_statement_prefix=LINE_STATEMENT_PREFIX, line_comment_prefix=LINE_COMMENT_PREFIX, trim_blocks=TRIM_BLOCKS, lstrip_blocks=LSTRIP_BLOCKS, newline_sequence=NEWLINE_SEQUENCE, keep_trailing_newline=KEEP_TRAILING_NEWLINE, extensions=(), optimized=True, undefined=Undefined, finalize=None, autoescape=False, loader=None, cache_size=400, auto_reload=True, bytecode_cache=None, enable_async=False):
        self.block_start_string = block_start_string
        self.block_end_string = block_end_string
        self.variable_start_string = variable_start_string
        self.variable_end_string = variable_end_string
        self.comment_start_string = comment_start_string
        self.comment_end_string = comment_end_string
        self.line_statement_prefix = line_statement_prefix
        self.line_comment_prefix = line_comment_prefix
        self.trim_blocks = trim_blocks
        self.lstrip_blocks = lstrip_blocks
        self.newline_sequence = newline_sequence
        self.keep_trailing_newline = keep_trailing_newline
        self.undefined = undefined
        self.optimized = optimized
        self.finalize = finalize
        self.autoescape = autoescape
        self.filters = DEFAULT_FILTERS.copy()
        self.tests = DEFAULT_TESTS.copy()
        self.globals = DEFAULT_NAMESPACE.copy()
        self.loader = loader
        self.cache = create_cache(cache_size)
        self.bytecode_cache = bytecode_cache
        self.auto_reload = auto_reload
        self.policies = DEFAULT_POLICIES.copy()
        self.extensions = load_extensions(self, extensions)
        self.enable_async = enable_async
        self.is_async = self.enable_async and have_async_gen
        _environment_sanity_check(self)

    def add_extension(self, extension):
        """Adds an extension after the environment was created.

        .. versionadded:: 2.5
        """
        self.extensions.update(load_extensions(self, [extension]))

    def extend(self, **attributes):
        """Add the items to the instance of the environment if they do not exist
        yet.  This is used by :ref:`extensions <writing-extensions>` to register
        callbacks and configuration values without breaking inheritance.
        """
        for key, value in iteritems(attributes):
            if not hasattr(self, key):
                setattr(self, key, value)

    def overlay(self, block_start_string=missing, block_end_string=missing, variable_start_string=missing, variable_end_string=missing, comment_start_string=missing, comment_end_string=missing, line_statement_prefix=missing, line_comment_prefix=missing, trim_blocks=missing, lstrip_blocks=missing, extensions=missing, optimized=missing, undefined=missing, finalize=missing, autoescape=missing, loader=missing, cache_size=missing, auto_reload=missing, bytecode_cache=missing):
        """Create a new overlay environment that shares all the data with the
        current environment except for cache and the overridden attributes.
        Extensions cannot be removed for an overlayed environment.  An overlayed
        environment automatically gets all the extensions of the environment it
        is linked to plus optional extra extensions.

        Creating overlays should happen after the initial environment was set
        up completely.  Not all attributes are truly linked, some are just
        copied over so modifications on the original environment may not shine
        through.
        """
        args = dict(locals())
        del args['self']
        del args['cache_size']
        del args['extensions']
        rv = object.__new__(self.__class__)
        rv.__dict__.update(self.__dict__)
        rv.overlayed = True
        rv.linked_to = self
        for key, value in iteritems(args):
            if value is not missing:
                setattr(rv, key, value)

        if cache_size is not missing:
            rv.cache = create_cache(cache_size)
        else:
            rv.cache = copy_cache(self.cache)
        rv.extensions = {}
        for key, value in iteritems(self.extensions):
            rv.extensions[key] = value.bind(rv)

        if extensions is not missing:
            rv.extensions.update(load_extensions(rv, extensions))
        return _environment_sanity_check(rv)

    lexer = property(get_lexer, doc='The lexer for this environment.')

    def iter_extensions(self):
        """Iterates over the extensions by priority."""
        return iter(sorted((self.extensions.values()), key=(lambda x: x.priority)))

    def getitem(self, obj, argument):
        """Get an item or attribute of an object but prefer the item."""
        try:
            return obj[argument]
        except (AttributeError, TypeError, LookupError):
            if isinstance(argument, string_types):
                try:
                    attr = str(argument)
                except Exception:
                    pass
                else:
                    try:
                        return getattr(obj, attr)
                    except AttributeError:
                        pass

            return self.undefined(obj=obj, name=argument)

    def getattr(self, obj, attribute):
        """Get an item or attribute of an object but prefer the attribute.
        Unlike :meth:`getitem` the attribute *must* be a bytestring.
        """
        try:
            return getattr(obj, attribute)
        except AttributeError:
            pass

        try:
            return obj[attribute]
        except (TypeError, LookupError, AttributeError):
            return self.undefined(obj=obj, name=attribute)

    def call_filter(self, name, value, args=None, kwargs=None, context=None, eval_ctx=None):
        """Invokes a filter on a value the same way the compiler does it.

        Note that on Python 3 this might return a coroutine in case the
        filter is running from an environment in async mode and the filter
        supports async execution.  It's your responsibility to await this
        if needed.

        .. versionadded:: 2.7
        """
        func = self.filters.get(name)
        if func is None:
            fail_for_missing_callable('no filter named %r', name)
        args = [
         value] + list(args or ())
        if getattr(func, 'contextfilter', False):
            if context is None:
                raise TemplateRuntimeError('Attempted to invoke context filter without context')
            args.insert(0, context)
        else:
            if getattr(func, 'evalcontextfilter', False):
                if eval_ctx is None:
                    if context is not None:
                        eval_ctx = context.eval_ctx
                    else:
                        eval_ctx = EvalContext(self)
                args.insert(0, eval_ctx)
            else:
                if getattr(func, 'environmentfilter', False):
                    args.insert(0, self)
        return func(*args, **kwargs or {})

    def call_test(self, name, value, args=None, kwargs=None):
        """Invokes a test on a value the same way the compiler does it.

        .. versionadded:: 2.7
        """
        func = self.tests.get(name)
        if func is None:
            fail_for_missing_callable('no test named %r', name)
        return func(value, *(args or ()), **kwargs or {})

    @internalcode
    def parse(self, source, name=None, filename=None):
        """Parse the sourcecode and return the abstract syntax tree.  This
        tree of nodes is used by the compiler to convert the template into
        executable source- or bytecode.  This is useful for debugging or to
        extract information from templates.

        If you are :ref:`developing Jinja2 extensions <writing-extensions>`
        this gives you a good overview of the node tree generated.
        """
        try:
            return self._parse(source, name, filename)
        except TemplateSyntaxError:
            exc_info = sys.exc_info()

        self.handle_exception(exc_info, source_hint=source)

    def _parse(self, source, name, filename):
        """Internal parsing function used by `parse` and `compile`."""
        return Parser(self, source, name, encode_filename(filename)).parse()

    def lex(self, source, name=None, filename=None):
        """Lex the given sourcecode and return a generator that yields
        tokens as tuples in the form ``(lineno, token_type, value)``.
        This can be useful for :ref:`extension development <writing-extensions>`
        and debugging templates.

        This does not perform preprocessing.  If you want the preprocessing
        of the extensions to be applied you have to filter source through
        the :meth:`preprocess` method.
        """
        source = text_type(source)
        try:
            return self.lexer.tokeniter(source, name, filename)
        except TemplateSyntaxError:
            exc_info = sys.exc_info()

        self.handle_exception(exc_info, source_hint=source)

    def preprocess(self, source, name=None, filename=None):
        """Preprocesses the source with all extensions.  This is automatically
        called for all parsing and compiling methods but *not* for :meth:`lex`
        because there you usually only want the actual source tokenized.
        """
        return reduce(lambda s, e: e.preprocess(s, name, filename), self.iter_extensions(), text_type(source))

    def _tokenize(self, source, name, filename=None, state=None):
        """Called by the parser to do the preprocessing and filtering
        for all the extensions.  Returns a :class:`~jinja2.lexer.TokenStream`.
        """
        source = self.preprocess(source, name, filename)
        stream = self.lexer.tokenize(source, name, filename, state)
        for ext in self.iter_extensions():
            stream = ext.filter_stream(stream)
            if not isinstance(stream, TokenStream):
                stream = TokenStream(stream, name, filename)

        return stream

    def _generate(self, source, name, filename, defer_init=False):
        """Internal hook that can be overridden to hook a different generate
        method in.

        .. versionadded:: 2.5
        """
        return generate(source, self, name, filename, defer_init=defer_init, optimized=(self.optimized))

    def _compile(self, source, filename):
        """Internal hook that can be overridden to hook a different compile
        method in.

        .. versionadded:: 2.5
        """
        return compile(source, filename, 'exec')

    @internalcode
    def compile(self, source, name=None, filename=None, raw=False, defer_init=False):
        """Compile a node or template source code.  The `name` parameter is
        the load name of the template after it was joined using
        :meth:`join_path` if necessary, not the filename on the file system.
        the `filename` parameter is the estimated filename of the template on
        the file system.  If the template came from a database or memory this
        can be omitted.

        The return value of this method is a python code object.  If the `raw`
        parameter is `True` the return value will be a string with python
        code equivalent to the bytecode returned otherwise.  This method is
        mainly used internally.

        `defer_init` is use internally to aid the module code generator.  This
        causes the generated code to be able to import without the global
        environment variable to be set.

        .. versionadded:: 2.4
           `defer_init` parameter added.
        """
        source_hint = None
        try:
            if isinstance(source, string_types):
                source_hint = source
                source = self._parse(source, name, filename)
            else:
                source = self._generate(source, name, filename, defer_init=defer_init)
                if raw:
                    return source
                if filename is None:
                    filename = '<template>'
                else:
                    filename = encode_filename(filename)
            return self._compile(source, filename)
        except TemplateSyntaxError:
            exc_info = sys.exc_info()

        self.handle_exception(exc_info, source_hint=source_hint)

    def compile_expression(self, source, undefined_to_none=True):
        """A handy helper method that returns a callable that accepts keyword
        arguments that appear as variables in the expression.  If called it
        returns the result of the expression.

        This is useful if applications want to use the same rules as Jinja
        in template "configuration files" or similar situations.

        Example usage:

        >>> env = Environment()
        >>> expr = env.compile_expression('foo == 42')
        >>> expr(foo=23)
        False
        >>> expr(foo=42)
        True

        Per default the return value is converted to `None` if the
        expression returns an undefined value.  This can be changed
        by setting `undefined_to_none` to `False`.

        >>> env.compile_expression('var')() is None
        True
        >>> env.compile_expression('var', undefined_to_none=False)()
        Undefined

        .. versionadded:: 2.1
        """
        parser = Parser(self, source, state='variable')
        exc_info = None
        try:
            expr = parser.parse_expression()
            if not parser.stream.eos:
                raise TemplateSyntaxError('chunk after expression', parser.stream.current.lineno, None, None)
            expr.set_environment(self)
        except TemplateSyntaxError:
            exc_info = sys.exc_info()

        if exc_info is not None:
            self.handle_exception(exc_info, source_hint=source)
        body = [
         nodes.Assign((nodes.Name('result', 'store')), expr, lineno=1)]
        template = self.from_string(nodes.Template(body, lineno=1))
        return TemplateExpression(template, undefined_to_none)

    def compile_templates(self, target, extensions=None, filter_func=None, zip='deflated', log_function=None, ignore_errors=True, py_compile=False):
        """Finds all the templates the loader can find, compiles them
        and stores them in `target`.  If `zip` is `None`, instead of in a
        zipfile, the templates will be stored in a directory.
        By default a deflate zip algorithm is used. To switch to
        the stored algorithm, `zip` can be set to ``'stored'``.

        `extensions` and `filter_func` are passed to :meth:`list_templates`.
        Each template returned will be compiled to the target folder or
        zipfile.

        By default template compilation errors are ignored.  In case a
        log function is provided, errors are logged.  If you want template
        syntax errors to abort the compilation you can set `ignore_errors`
        to `False` and you will get an exception on syntax errors.

        If `py_compile` is set to `True` .pyc files will be written to the
        target instead of standard .py files.  This flag does not do anything
        on pypy and Python 3 where pyc files are not picked up by itself and
        don't give much benefit.

        .. versionadded:: 2.4
        """
        from jinja2.loaders import ModuleLoader
        if log_function is None:
            log_function = lambda x: None
        else:
            if py_compile:
                if not PY2 or PYPY:
                    from warnings import warn
                    warn(Warning('py_compile has no effect on pypy or Python 3'))
                    py_compile = False
                else:
                    import imp, marshal
                    py_header = imp.get_magic() + 'ÿÿÿÿ'.encode('iso-8859-15')
                    if sys.version_info >= (3, 3):
                        py_header += '\x00\x00\x00\x00'.encode('iso-8859-15')

            def write_file(filename, data, mode):
                if zip:
                    info = ZipInfo(filename)
                    info.external_attr = 32309248
                    zip_file.writestr(info, data)
                else:
                    f = open(os.path.join(target, filename), mode)
                    try:
                        f.write(data)
                    finally:
                        f.close()

            if zip is not None:
                from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, ZIP_STORED
                zip_file = ZipFile(target, 'w', dict(deflated=ZIP_DEFLATED, stored=ZIP_STORED)[zip])
                log_function('Compiling into Zip archive "%s"' % target)
            else:
                if not os.path.isdir(target):
                    os.makedirs(target)
                log_function('Compiling into folder "%s"' % target)
        try:
            for name in self.list_templates(extensions, filter_func):
                source, filename, _ = self.loader.get_source(self, name)
                try:
                    code = self.compile(source, name, filename, True, True)
                except TemplateSyntaxError as e:
                    if not ignore_errors:
                        raise
                    log_function('Could not compile "%s": %s' % (name, e))
                    continue

                filename = ModuleLoader.get_module_filename(name)
                if py_compile:
                    c = self._compile(code, encode_filename(filename))
                    write_file(filename + 'c', py_header + marshal.dumps(c), 'wb')
                    log_function('Byte-compiled "%s" as %s' % (
                     name, filename + 'c'))
                else:
                    write_file(filename, code, 'w')
                    log_function('Compiled "%s" as %s' % (name, filename))

        finally:
            if zip:
                zip_file.close()

        log_function('Finished compiling templates')

    def list_templates(self, extensions=None, filter_func=None):
        """Returns a list of templates for this environment.  This requires
        that the loader supports the loader's
        :meth:`~BaseLoader.list_templates` method.

        If there are other files in the template folder besides the
        actual templates, the returned list can be filtered.  There are two
        ways: either `extensions` is set to a list of file extensions for
        templates, or a `filter_func` can be provided which is a callable that
        is passed a template name and should return `True` if it should end up
        in the result list.

        If the loader does not support that, a :exc:`TypeError` is raised.

        .. versionadded:: 2.4
        """
        x = self.loader.list_templates()
        if extensions is not None:
            if filter_func is not None:
                raise TypeError('either extensions or filter_func can be passed, but not both')
            filter_func = lambda x: '.' in x and x.rsplit('.', 1)[1] in extensions
        if filter_func is not None:
            x = list(ifilter(filter_func, x))
        return x

    def handle_exception(self, exc_info=None, rendered=False, source_hint=None):
        """Exception handling helper.  This is used internally to either raise
        rewritten exceptions or return a rendered traceback for the template.
        """
        global _make_traceback
        if exc_info is None:
            exc_info = sys.exc_info()
        else:
            if _make_traceback is None:
                from jinja2.debug import make_traceback as _make_traceback
            traceback = _make_traceback(exc_info, source_hint)
            if rendered:
                if self.exception_formatter is not None:
                    return self.exception_formatter(traceback)
            if self.exception_handler is not None:
                self.exception_handler(traceback)
        exc_type, exc_value, tb = traceback.standard_exc_info
        reraise(exc_type, exc_value, tb)

    def join_path(self, template, parent):
        """Join a template with the parent.  By default all the lookups are
        relative to the loader root so this method returns the `template`
        parameter unchanged, but if the paths should be relative to the
        parent template, this function can be used to calculate the real
        template name.

        Subclasses may override this method and implement template path
        joining here.
        """
        return template

    @internalcode
    def _load_template(self, name, globals):
        if self.loader is None:
            raise TypeError('no loader for this environment specified')
        else:
            cache_key = (
             weakref.ref(self.loader), name)
            if self.cache is not None:
                template = self.cache.get(cache_key)
                if template is not None:
                    if not self.auto_reload or template.is_up_to_date:
                        return template
            template = self.loader.load(self, name, globals)
            if self.cache is not None:
                self.cache[cache_key] = template
        return template

    @internalcode
    def get_template(self, name, parent=None, globals=None):
        """Load a template from the loader.  If a loader is configured this
        method asks the loader for the template and returns a :class:`Template`.
        If the `parent` parameter is not `None`, :meth:`join_path` is called
        to get the real template name before loading.

        The `globals` parameter can be used to provide template wide globals.
        These variables are available in the context at render time.

        If the template does not exist a :exc:`TemplateNotFound` exception is
        raised.

        .. versionchanged:: 2.4
           If `name` is a :class:`Template` object it is returned from the
           function unchanged.
        """
        if isinstance(name, Template):
            return name
        else:
            if parent is not None:
                name = self.join_path(name, parent)
            return self._load_template(name, self.make_globals(globals))

    @internalcode
    def select_template(self, names, parent=None, globals=None):
        """Works like :meth:`get_template` but tries a number of templates
        before it fails.  If it cannot find any of the templates, it will
        raise a :exc:`TemplatesNotFound` exception.

        .. versionadded:: 2.3

        .. versionchanged:: 2.4
           If `names` contains a :class:`Template` object it is returned
           from the function unchanged.
        """
        if not names:
            raise TemplatesNotFound(message='Tried to select from an empty list of templates.')
        globals = self.make_globals(globals)
        for name in names:
            if isinstance(name, Template):
                return name
            if parent is not None:
                name = self.join_path(name, parent)
            try:
                return self._load_template(name, globals)
            except TemplateNotFound:
                pass

        raise TemplatesNotFound(names)

    @internalcode
    def get_or_select_template(self, template_name_or_list, parent=None, globals=None):
        """Does a typecheck and dispatches to :meth:`select_template`
        if an iterable of template names is given, otherwise to
        :meth:`get_template`.

        .. versionadded:: 2.3
        """
        if isinstance(template_name_or_list, string_types):
            return self.get_template(template_name_or_list, parent, globals)
        else:
            if isinstance(template_name_or_list, Template):
                return template_name_or_list
            return self.select_template(template_name_or_list, parent, globals)

    def from_string(self, source, globals=None, template_class=None):
        """Load a template from a string.  This parses the source given and
        returns a :class:`Template` object.
        """
        globals = self.make_globals(globals)
        cls = template_class or self.template_class
        return cls.from_code(self, self.compile(source), globals, None)

    def make_globals(self, d):
        """Return a dict for the globals."""
        if not d:
            return self.globals
        else:
            return dict((self.globals), **d)


class Template(object):
    __doc__ = "The central template object.  This class represents a compiled template\n    and is used to evaluate it.\n\n    Normally the template object is generated from an :class:`Environment` but\n    it also has a constructor that makes it possible to create a template\n    instance directly using the constructor.  It takes the same arguments as\n    the environment constructor but it's not possible to specify a loader.\n\n    Every template object has a few methods and members that are guaranteed\n    to exist.  However it's important that a template object should be\n    considered immutable.  Modifications on the object are not supported.\n\n    Template objects created from the constructor rather than an environment\n    do have an `environment` attribute that points to a temporary environment\n    that is probably shared with other templates created with the constructor\n    and compatible settings.\n\n    >>> template = Template('Hello {{ name }}!')\n    >>> template.render(name='John Doe') == u'Hello John Doe!'\n    True\n    >>> stream = template.stream(name='John Doe')\n    >>> next(stream) == u'Hello John Doe!'\n    True\n    >>> next(stream)\n    Traceback (most recent call last):\n        ...\n    StopIteration\n    "

    def __new__(cls, source, block_start_string=BLOCK_START_STRING, block_end_string=BLOCK_END_STRING, variable_start_string=VARIABLE_START_STRING, variable_end_string=VARIABLE_END_STRING, comment_start_string=COMMENT_START_STRING, comment_end_string=COMMENT_END_STRING, line_statement_prefix=LINE_STATEMENT_PREFIX, line_comment_prefix=LINE_COMMENT_PREFIX, trim_blocks=TRIM_BLOCKS, lstrip_blocks=LSTRIP_BLOCKS, newline_sequence=NEWLINE_SEQUENCE, keep_trailing_newline=KEEP_TRAILING_NEWLINE, extensions=(), optimized=True, undefined=Undefined, finalize=None, autoescape=False, enable_async=False):
        env = get_spontaneous_environment(block_start_string, block_end_string, variable_start_string, variable_end_string, comment_start_string, comment_end_string, line_statement_prefix, line_comment_prefix, trim_blocks, lstrip_blocks, newline_sequence, keep_trailing_newline, frozenset(extensions), optimized, undefined, finalize, autoescape, None, 0, False, None, enable_async)
        return env.from_string(source, template_class=cls)

    @classmethod
    def from_code(cls, environment, code, globals, uptodate=None):
        """Creates a template object from compiled code and the globals.  This
        is used by the loaders and environment to create a template object.
        """
        namespace = {'environment':environment, 
         '__file__':code.co_filename}
        exec(code, namespace)
        rv = cls._from_namespace(environment, namespace, globals)
        rv._uptodate = uptodate
        return rv

    @classmethod
    def from_module_dict(cls, environment, module_dict, globals):
        """Creates a template object from a module.  This is used by the
        module loader to create a template object.

        .. versionadded:: 2.4
        """
        return cls._from_namespace(environment, module_dict, globals)

    @classmethod
    def _from_namespace(cls, environment, namespace, globals):
        t = object.__new__(cls)
        t.environment = environment
        t.globals = globals
        t.name = namespace['name']
        t.filename = namespace['__file__']
        t.blocks = namespace['blocks']
        t.root_render_func = namespace['root']
        t._module = None
        t._debug_info = namespace['debug_info']
        t._uptodate = None
        namespace['environment'] = environment
        namespace['__jinja_template__'] = t
        return t

    def render(self, *args, **kwargs):
        """This method accepts the same arguments as the `dict` constructor:
        A dict, a dict subclass or some keyword arguments.  If no arguments
        are given the context will be empty.  These two calls do the same::

            template.render(knights='that say nih')
            template.render({'knights': 'that say nih'})

        This will return the rendered template as unicode string.
        """
        vars = dict(*args, **kwargs)
        try:
            return concat(self.root_render_func(self.new_context(vars)))
        except Exception:
            exc_info = sys.exc_info()

        return self.environment.handle_exception(exc_info, True)

    def render_async(self, *args, **kwargs):
        """This works similar to :meth:`render` but returns a coroutine
        that when awaited returns the entire rendered template string.  This
        requires the async feature to be enabled.

        Example usage::

            await template.render_async(knights='that say nih; asynchronously')
        """
        raise NotImplementedError('This feature is not available for this version of Python')

    def stream(self, *args, **kwargs):
        """Works exactly like :meth:`generate` but returns a
        :class:`TemplateStream`.
        """
        return TemplateStream((self.generate)(*args, **kwargs))

    def generate(self, *args, **kwargs):
        """For very large templates it can be useful to not render the whole
        template at once but evaluate each statement after another and yield
        piece for piece.  This method basically does exactly that and returns
        a generator that yields one item after another as unicode strings.

        It accepts the same arguments as :meth:`render`.
        """
        vars = dict(*args, **kwargs)
        try:
            for event in self.root_render_func(self.new_context(vars)):
                yield event

        except Exception:
            exc_info = sys.exc_info()
        else:
            return
            yield self.environment.handle_exception(exc_info, True)

    def generate_async(self, *args, **kwargs):
        """An async version of :meth:`generate`.  Works very similarly but
        returns an async iterator instead.
        """
        raise NotImplementedError('This feature is not available for this version of Python')

    def new_context(self, vars=None, shared=False, locals=None):
        """Create a new :class:`Context` for this template.  The vars
        provided will be passed to the template.  Per default the globals
        are added to the context.  If shared is set to `True` the data
        is passed as it to the context without adding the globals.

        `locals` can be a dict of local variables for internal usage.
        """
        return new_context(self.environment, self.name, self.blocks, vars, shared, self.globals, locals)

    def make_module(self, vars=None, shared=False, locals=None):
        """This method works like the :attr:`module` attribute when called
        without arguments but it will evaluate the template on every call
        rather than caching it.  It's also possible to provide
        a dict which is then used as context.  The arguments are the same
        as for the :meth:`new_context` method.
        """
        return TemplateModule(self, self.new_context(vars, shared, locals))

    def make_module_async(self, vars=None, shared=False, locals=None):
        """As template module creation can invoke template code for
        asynchronous exections this method must be used instead of the
        normal :meth:`make_module` one.  Likewise the module attribute
        becomes unavailable in async mode.
        """
        raise NotImplementedError('This feature is not available for this version of Python')

    @internalcode
    def _get_default_module(self):
        if self._module is not None:
            return self._module
        else:
            self._module = rv = self.make_module()
            return rv

    @property
    def module(self):
        """The template as module.  This is used for imports in the
        template runtime but is also useful if one wants to access
        exported template variables from the Python layer:

        >>> t = Template('{% macro foo() %}42{% endmacro %}23')
        >>> str(t.module)
        '23'
        >>> t.module.foo() == u'42'
        True

        This attribute is not available if async mode is enabled.
        """
        return self._get_default_module()

    def get_corresponding_lineno(self, lineno):
        """Return the source line number of a line number in the
        generated bytecode as they are not in sync.
        """
        for template_line, code_line in reversed(self.debug_info):
            if code_line <= lineno:
                return template_line

        return 1

    @property
    def is_up_to_date(self):
        """If this variable is `False` there is a newer version available."""
        if self._uptodate is None:
            return True
        else:
            return self._uptodate()

    @property
    def debug_info(self):
        """The debug info mapping."""
        return [tuple(imap(int, x.split('='))) for x in self._debug_info.split('&')]

    def __repr__(self):
        if self.name is None:
            name = 'memory:%x' % id(self)
        else:
            name = repr(self.name)
        return '<%s %s>' % (self.__class__.__name__, name)


@implements_to_string
class TemplateModule(object):
    __doc__ = 'Represents an imported template.  All the exported names of the\n    template are available as attributes on this object.  Additionally\n    converting it into an unicode- or bytestrings renders the contents.\n    '

    def __init__(self, template, context, body_stream=None):
        if body_stream is None:
            if context.environment.is_async:
                raise RuntimeError('Async mode requires a body stream to be passed to a template module.  Use the async methods of the API you are using.')
            body_stream = list(template.root_render_func(context))
        self._body_stream = body_stream
        self.__dict__.update(context.get_exported())
        self.__name__ = template.name

    def __html__(self):
        return Markup(concat(self._body_stream))

    def __str__(self):
        return concat(self._body_stream)

    def __repr__(self):
        if self.__name__ is None:
            name = 'memory:%x' % id(self)
        else:
            name = repr(self.__name__)
        return '<%s %s>' % (self.__class__.__name__, name)


class TemplateExpression(object):
    __doc__ = 'The :meth:`jinja2.Environment.compile_expression` method returns an\n    instance of this object.  It encapsulates the expression-like access\n    to the template with an expression it wraps.\n    '

    def __init__(self, template, undefined_to_none):
        self._template = template
        self._undefined_to_none = undefined_to_none

    def __call__(self, *args, **kwargs):
        context = self._template.new_context(dict(*args, **kwargs))
        consume(self._template.root_render_func(context))
        rv = context.vars['result']
        if self._undefined_to_none:
            if isinstance(rv, Undefined):
                rv = None
        return rv


@implements_iterator
class TemplateStream(object):
    __doc__ = 'A template stream works pretty much like an ordinary python generator\n    but it can buffer multiple items to reduce the number of total iterations.\n    Per default the output is unbuffered which means that for every unbuffered\n    instruction in the template one unicode string is yielded.\n\n    If buffering is enabled with a buffer size of 5, five items are combined\n    into a new unicode string.  This is mainly useful if you are streaming\n    big templates to a client via WSGI which flushes after each iteration.\n    '

    def __init__(self, gen):
        self._gen = gen
        self.disable_buffering()

    def dump(self, fp, encoding=None, errors='strict'):
        """Dump the complete stream into a file or file-like object.
        Per default unicode strings are written, if you want to encode
        before writing specify an `encoding`.

        Example usage::

            Template('Hello {{ name }}!').stream(name='foo').dump('hello.html')
        """
        close = False
        if isinstance(fp, string_types):
            if encoding is None:
                encoding = 'utf-8'
            fp = open(fp, 'wb')
            close = True
        try:
            if encoding is not None:
                iterable = (x.encode(encoding, errors) for x in self)
            else:
                iterable = self
            if hasattr(fp, 'writelines'):
                fp.writelines(iterable)
            else:
                for item in iterable:
                    fp.write(item)

        finally:
            if close:
                fp.close()

    def disable_buffering(self):
        """Disable the output buffering."""
        self._next = partial(next, self._gen)
        self.buffered = False

    def _buffered_generator(self, size):
        buf = []
        c_size = 0
        push = buf.append
        while True:
            try:
                while c_size < size:
                    c = next(self._gen)
                    push(c)
                    if c:
                        c_size += 1

            except StopIteration:
                if not c_size:
                    return

            yield concat(buf)
            del buf[:]
            c_size = 0

    def enable_buffering(self, size=5):
        """Enable buffering.  Buffer `size` items before yielding them."""
        if size <= 1:
            raise ValueError('buffer size too small')
        self.buffered = True
        self._next = partial(next, self._buffered_generator(size))

    def __iter__(self):
        return self

    def __next__(self):
        return self._next()


Environment.template_class = Template
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/config.py
# Compiled at: 2017-08-22 11:06:05
from __future__ import unicode_literals
from ..elements.elementbase import ElementBase, LogicElement, Attribute
from ..tags.context import DataSetter
from .. import logic
from .. import errors
from ..elements.attributetypes import *
from ..contextenum import ContextEnum
from ..compat import iteritems, text_type, reload
from .. import tools
from .. import timezone
from fs.path import join
from fs.opener import open_fs
from fs.errors import FSError, IllegalBackReference, ResourceNotFound
from os.path import dirname, abspath
import sys, textwrap
from time import time
import pytz, logging
log = logging.getLogger(b'moya.runtime')
startup_log = logging.getLogger(b'moya.startup')
runtime_log = logging.getLogger(b'moya.runtime')

class Moya(ElementBase):
    """This is the root element for Moya files."""
    version = Attribute(b'version number of this Moya file (currently ignored, if supplied use "1.0")', type=b'version', required=False)

    class Help:
        synopsis = b'begin a Moya file'
        example = b'\n        <moya xmlns="http://moyaproject.com">\n            <!-- Ready for take off -->\n        </moya>\n\n        '


class ConfigElement(ElementBase):

    class Help:
        undocumented = True

    def execute(self, archive, context, fs):
        pass


class Breakpoint(LogicElement):
    """Stops the execute of Moya code and drops in to the debugger."""

    class Help:
        synopsis = b'drop in to the debugger'
        example = b'\n\n        <!-- drop in to the debugger -->\n        <breakpoint/>\n\n        <for src="-100..100" dst="count">\n            <!-- Conditional breakpoint with \'if\' attribute -->\n            <breakpoint if="count==0"/>\n            <!-- This throws an exception when count is 0 -->\n            <echo>${1/count}<echo>\n        </for>\n\n        '

    def logic(self, context):
        raise logic.DebugBreak(self)


class Import(LogicElement):
    """Import a library. Importing reads the XML associated with a library and makes it available to be installed as an application. This tag must appear within a [tag]server[/tag] tag.

    Libraries can be installed either from a Python module, or directly from a path. For example, this installs a library from a Python module:

    [code xml]
    <import py="moya.libs.auth"/>
    [/code]

    And this installs a library from a a relative path:

    [code xml]
    <import location="./local/sushishop/" />
    [/code]

    The [c]priority[/c] attribute is used when two element have the same element reference. This is typically used to override an element in another library. For example, let's say we have the following [tag]macro[/tag] in a library called [c]sushifinder.shop[/c], which calculate tax on a shopping cart:

    [code xml]
    <macro libname="macro.get_tax">
        <!-- calculate tax for an order-->
    </macro>
    [/code]

    We could replace this by defining the following in another library:

    [code xml]
    <macro libname="sushifinder.shop#macro.get_tax">
        <!-- custom tax calculator -->
    </macro>
    [/code]

    Note the use of a full element reference (including library name) in the [c]libname[/c] attribute. This tells Moya that the macro should go in a library other than the one it was declared in. If the code above is in a library with a higher priority then it will replace the macro in the [c]sushifinder.shop[/c] library.

    The [c]templatepriority[/c] is used when there are conflicting template paths. The template from the library with the highest priority wins. This value takes precedence over the [c]priority[/c] defined in [link library#lib-section]lib.ini[/link].

    """

    class Help:
        synopsis = b'import a library'

    class Meta:
        oneof = [
         b'location', b'py', b'lib']

    name = Attribute(b'Name of the library')
    lib = Attribute(b'Library to import e.g. acme.blog==0.1.0')
    location = Attribute(b'A path to a Moya library')
    py = Attribute(b'Python import, e.g. widgets.moya.widgetapp')
    priority = Attribute(b'Priority for elements', type=b'integer', required=False, default=None)
    templatepriority = Attribute(b'Priority for templates', type=b'integer', required=False, default=None)
    datapriority = Attribute(b'Priority for library data', type=b'integer', required=False, default=None)

    def logic(self, context):
        start = time()
        name, _location, lib, py, priority, template_priority, data_priority = self.get_parameters(context, b'name', b'location', b'lib', b'py', b'priority', b'templatepriority', b'datapriority')
        if template_priority is None:
            template_priority = priority
        archive = self.document.archive
        absolute = False
        import_fs = None
        if lib is not None:
            import_fs = archive.find_lib(lib)
            if import_fs is None:
                self.throw(b'import.fail', (b"lib '{}' not found; searched {}").format(lib, tools.textual_list(archive.lib_paths, join_word=b'and')))
        else:
            if _location is not None:
                location = _location
            else:
                if py in sys.modules:
                    reload(sys.modules[py])
                try:
                    __import__(py)
                except ImportError as e:
                    raise errors.ElementError((b"unable to import Python module '{}'").format(py), element=self, diagnosis=text_type(e))

                module = sys.modules[py]
                location = dirname(abspath(module.__file__))
                absolute = True
            try:
                if import_fs is None:
                    if b'::/' in location:
                        import_fs = open_fs(location)
                    elif absolute:
                        import_fs = open_fs(location)
                    else:
                        project_fs = context[b'fs']
                        try:
                            if project_fs.hassyspath(b'/'):
                                project_path = project_fs.getsyspath(b'/')
                                import_path = join(project_path, location)
                                try:
                                    import_fs = open_fs(import_path)
                                except ResourceNotFound:
                                    self.throw(b'import.fail', (b"location '{}' was not found").format(import_path), diagnosis=b'Check the location is exists and is a directory.')

                            else:
                                import_fs = context[b'fs'].opendir(location)
                        except (IllegalBackReference, FSError) as e:
                            self.throw(b'import.fail', (b"unable to import location '{}' from {}").format(location, project_fs), diagnosis=text_type(e))

                lib = archive.load_library(import_fs, priority=priority, template_priority=template_priority, data_priority=data_priority, long_name=name, rebuild=context.root.get(b'_rebuild', False))
                if lib.failed_documents:
                    if _location is not None:
                        msg = b"Failed to load library '{}' from location '{}'"
                        raise errors.StartupFailedError(msg.format(name or lib.long_name, _location))
                    elif py:
                        msg = b"Failed to load library '{}' from Python module '{}'"
                        raise errors.StartupFailedError(msg.format(name or lib.long_name, py))
                    else:
                        raise errors.StartupFailedError((b"Failed to load library '{}'").format(name or lib.long_name))
                startup_log.debug(b'%s imported %.1fms', lib, (time() - start) * 1000.0)
                if lib.priority:
                    startup_log.debug(b'%s priority is %s', lib, lib.priority)
                if lib.template_priority:
                    startup_log.debug(b'%s template priority is %s', lib, lib.template_priority)
            except Exception as e:
                if not self.archive.test_build:
                    raise

        return


class Install(LogicElement):
    """
    Installs an [i]application[/i]. An application is effectively an [i]instance[/i] of a library, with its own settings and serving content from unique URL(s). An [tag]install[/tag] tag should appear within a [tag]server[/tag] tag. A library must first be [i]imported[/i] (with [tag]import[/tag]) prior to installing.

    """

    class Help:
        synopsis = b'create an application from a library'
        example = b'\n        <install name="auth" lib="moya.auth" mount="/auth/"/>\n        '

    lib = Attribute(b'Library long name (e.g. moya.auth)', required=True)
    name = Attribute(b'Name of the application (must not contain a dot), e.g. "auth"', required=True)
    mount = Attribute(b'URL component to mount, e.g. "auth"')
    mountpoint = Attribute(b'Name of the <mountpoint> tag', required=False, default=b'main')
    urlpriority = Attribute(b'Priority for URLs in mountpoint', type=b'integer', required=False, default=0)
    server = Attribute(b'Server object', type=b'expression', required=False, default=None)

    def logic(self, context):
        params = self.get_parameters(context)
        archive = self.document.archive
        try:
            self.archive.build_libs()
        except Exception as e:
            if not self.archive.test_build:
                raise

        try:
            try:
                app = archive.create_app(params.name, params.lib)
            except errors.ArchiveError as e:
                raise errors.ElementError(text_type(e))

            if app.lib.failed_documents:
                raise errors.StartupFailedError(b"Unable to import lib '%s'" % params.lib)
            if params.mount:
                server = params.server or self.get_ancestor(b'server')
                try:
                    mountpoint = app.lib.get_element_by_type_and_attribute(b'mountpoint', b'name', params.mountpoint)
                except errors.ElementNotFoundError:
                    return
                    raise errors.StartupFailedError((b"No mountpoint called '{0}' in {1}").format(params.mountpoint, app.lib))

                app.mounts.append((params.mountpoint, params.mount))
                server.urlmapper.mount(params.mount, mountpoint.urlmapper, defaults={b'app': app.name}, name=params.name, priority=params.urlpriority)
                for stage, urlmapper in iteritems(server.middleware):
                    urlmapper.mount(params.mount, mountpoint.middleware[stage], defaults={b'app': app.name}, name=params.name, priority=params.urlpriority)

                startup_log.debug(b'%s installed, mounted on %s', app, tools.normalize_url_path(params.mount))
            else:
                startup_log.debug(b'%s installed', app)
        except:
            if not self.archive.test_build:
                raise


class Log(LogicElement):
    """Write text to the logs. Every line of text can have a [i]level[/i] which indicates how significant the message is. Log levels can be filtered, so you only see relevant messages.

    You can control which log messages are written via [c]logging.ini[/c].
    """

    class Help:
        synopsis = b'write information to the log'
        example = b'\n\n        <log level="debug">This may help you track down errors</log>\n        <log>Something worth knowing happened</log> <!-- default log level is "info" -->\n        <log level="warning">Pay attention, this may be significant</log>\n        <log level="error">Something quite alarming happened</log>\n        <log level="fatal">Absolute disaster</log>\n\n        '

    _levels = {b'debug': 10, 
       b'info': 20, 
       b'warn': 30, 
       b'warning': 30, 
       b'error': 40, 
       b'fatal': 50}
    _default_level = b'info'
    level = Attribute(b'Logging level', required=False, default=None, choices=_levels.keys())
    logger = Attribute(b'Logger to write to', default=None, required=False)

    def logic(self, context):
        text = textwrap.dedent(context.sub(self.text))
        _level, _logger = self.get_parameters(context, b'level', b'logger')
        _level = _level or self._default_level
        if _level.isdigit():
            level = int(_level)
        else:
            level = self._levels.get(_level, logging.INFO)
        if _logger:
            log = logging.getLogger(_logger)
        else:
            app_name = context.get(b'.app.name', None)
            if app_name is None:
                log = runtime_log
            else:
                log = logging.getLogger((b'moya.app.{}').format(app_name))
            for line in text.splitlines():
                if line:
                    log.log(level, line)

        return


class LogDebug(Log):
    """See [tag]log[/tag]"""
    _default_level = b'debug'

    class Help:
        synopsis = b'write information to the log'


class LogInfo(Log):
    """See [tag]log[/tag]"""
    _default_level = b'info'

    class Help:
        synopsis = b'write information to the log'


class LogWarn(Log):
    """See [tag]log[/tag]"""
    _default_level = b'warn'

    class Help:
        synopsis = b'write information to the log'


class LogError(Log):
    """See [tag]log[/tag]"""
    _default_level = b'error'

    class Help:
        synopsis = b'write information to the log'


class LogFatal(Log):
    """See [tag]log[/tag]"""
    _default_level = b'fatal'

    class Help:
        synopsis = b'write information to the log'


class Choices(ElementBase):
    """
    Define choices, for use by select fields.

    Choices are a list of values and labels, that might be used by a select control. You can retrieve the data defined by this tag with [tag]get-choices[/tag].

    """

    class Help:
        synopsis = b'define choices'
        example = b'\n            <choices libname="choices.markup">\n                <choice value="text" label="Plain text"/>\n                <choice value="bbcode" label="BBCode markup"/>\n                <choice value="html" label="HTML"/>\n            </choices>\n            <get-choices choices="#choices.markup" dst="choices" />\n        '

    def finalize(self, context):
        self.choices = choices = []
        append = choices.append
        for choice in self.get_children(b'choice'):
            value, label = choice.get_parameters(context, b'value', b'label')
            if not label:
                label = context.sub(choice.text)
            append((value, label))


class Choice(ElementBase):
    """
    Define a choice in a [tag]choices[/tag] tag.

    """

    class Help:
        synopis = b'define a choice'

    value = Attribute(b'Choice value')
    label = Attribute(b'Label to display')


class GetChoices(DataSetter):
    """
    Get choice data from a [tag]choices[/tag] tag

    """
    choices = Attribute(b'Choices element', type=b'elementref', required=b'yes')
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    def get_value(self, context):
        app, choices = self.get_parameters(context, b'from', b'choices')
        app = app or context[b'.app']
        _app, choices_el = app.get_element(choices)
        return choices_el.choices


class Enum(ElementBase):
    """
    Define and [i]enumeration[/i] object. An enumeration is a collection of text identifiers with an integer value. This tag should contain [tag]value[/tag] tags that define the values.

    You can retrieve an enumeration object with the [tag]get-enum[/tag] tag.

    """
    name = Attribute(b'Identifier for enum', required=False, default=None)
    start = Attribute(b'Starting ID if not specified in <value>', type=b'integer', default=1)

    class Help:
        synopsis = b'map numbers on to identifiers'
        example = b'\n        <enum libname="enum.jsonrpc.errors">\n            <value id="1" name="not_logged_in" description="You must be logged in to do that" />\n            <value name="invalid_score" description="Score must be -1, 0 or +1"/>\n            <value name="unknown_link" description="Link object was not found"/>\n        </enum>\n        '

    def post_build(self, context):
        params = self.get_parameters(context)
        start = params.start
        name = params.name or self.libname
        enum = ContextEnum(name, start=start)
        self.archive.add_enum(self.libid, enum)


class Value(ElementBase):
    """Defines a single value in an enumeration object. Should be contained within an [tag]enum[/tag]."""

    class Help:
        synopsis = b'a value in an enumeration'

    id = Attribute(b'Enumeration ID', type=b'integer', default=None)
    name = Attribute(b'Value name', required=True)
    description = Attribute(b'Description of enumeration value', default=b'')
    group = Attribute(b'Group name', default=b'')

    def finalize(self, context):
        enum_parent = self.get_ancestor(b'enum')
        params = self.get_parameters(context)
        description = params.description
        if not description:
            description = context.sub(self.text)
        enum = self.archive.get_enum(enum_parent.libid)
        if description:
            description = description.strip()
        enum.add_value(params.name, enum_id=params.id, description=description, group=params.group)


class GetEnum(DataSetter):
    """Get an enumeration object (see [tag]enum[/tag])."""

    class Help:
        synopsis = b'get an enumeration'
        example = b'\n        <get-enum enum="sociallinks#enum.jsonrpc.errors" dst="errors" />\n        <return value="errors.unknown_link" />\n\n        '

    enum = Attribute(b'enumeration ref', type=b'elementref')
    _from = Attribute(b'from application', type=b'application', default=None, evaldefault=True)

    def logic(self, context):
        params = self.get_parameters(context)
        app = self.get_app(context)
        app, el = app.get_element(params.enum)
        enum = self.archive.get_enum(el.libid)
        self.set_context(context, params.dst, enum)


class GetTimezones(DataSetter):
    """Get a list of common timezones."""

    class Help:
        synopsis = b'get common timezones'
        example = b'\n        <get-timezones dst="timezones" />\n        <echo>Timezones: ${commalist:timezones}</echo>\n\n        '

    def logic(self, context):
        timezones = pytz.common_timezones[:]
        self.set_context(context, dst, timezones)


class GetTimezoneGroups(DataSetter):
    """Get timezone information, for use in select controls."""

    class Help:
        synopsis = b'get timezone choices'

    def get_value(self, context):
        return timezone.get_common_timezones_groups()


class Handle(LogicElement):
    """
    Handles a [i]signal[/i]. A signal is a way of broadcasting to other parts of the project that a particular event has occurred.

    See [doc signals] for more information.

    """

    class Help:
        synopsis = b'respond to a signal'
        example = b'\n\n        <!-- Moya fires a number of signals itself, for various system events -->\n        <handle signal="sys.startup">\n            <log>This code executes on startup, prior to any requests</log>\n        </handle>\n        <!-- Handle a custom signal -->\n        <handle signal="mordor.arrived">\n            <log>${hobbit} has arrived in Mordor!</log>\n        </handle>\n\n        '

    signal = Attribute(b'Signal name to handle. Multiple names may be specified to handle more than one signal.', type=b'commalist', required=True)
    sender = Attribute(b'Only handle the signal(s) if sent from this element(s).', type=b'commalist', default=None)

    def lib_finalize(self, context):
        sender, signals = self.get_parameters(context, b'sender', b'signal')
        senders = []
        if sender:
            for _sender in sender:
                sender = self.document.qualify_element_ref(_sender, lib=self.lib)
                app, element = self.get_element(sender)
                senders.append(element.libid)

        for signal in signals:
            if senders:
                for sender in senders:
                    self.archive.signals.add_handler(signal, self.libid, sender)

            else:
                self.archive.signals.add_handler(signal, self.libid, None)

        return


class Fire(LogicElement):
    """
    Fire (broadcast) a signal. Additional data may be provided to the signal handlers, by setting values in the [i]let map[/i]. Signals may be [i]handlers[/i] with the [tag]handle[/tag] tag.

    Moya will catch and log any exceptions raised by the signal handler(s).

    """
    signal = Attribute(b'Signal name, should be in a dotted notation. Names with no dots are reserved by Moya.', required=True)
    sender = Attribute(b'Optional element associated with the signal.', required=False, type=b'elementref', default=None)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    class Help:
        synopsis = b'fire a signal'
        example = b'\n        <fire signal="mordor.arrived" let:hobbit="Frodo"/>\n        '

    class Meta:
        trap_exceptions = True

    def logic(self, context):
        app = self.get_app(context)
        signal = self.signal(context)
        sender = self.sender(context)
        data = self.get_let_map(context)
        self.archive.fire(context, signal, app=app, sender=sender, data=data)
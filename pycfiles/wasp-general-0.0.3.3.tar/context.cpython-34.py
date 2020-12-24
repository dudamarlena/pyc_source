# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/command/context.py
# Compiled at: 2017-10-29 12:15:55
# Size of source mod 2**32: 8919 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
from wasp_general.verify import verify_type, verify_value
from wasp_general.command.command import WCommandProto
from wasp_general.composer import WComposerProto

class WContextProto(metaclass=ABCMeta):
    __doc__ = ' Represent context configuration\n\t'

    @abstractmethod
    def context_name(self):
        """ Return this context name

                :return: str
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def context_value(self):
        """ Return this context value (can be None)

                :return: str or None
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    def linked_context(self):
        """ Return link to 'parent'/'higher' context

                :return: WContextProto or None
                """
        raise NotImplementedError('This method is abstract')

    def __len__(self):
        """ Return linked context count

                :return: int
                """
        return len([x for x in self])

    def __iter__(self):
        """Iterate over

                :return:
                """
        context = self
        while context is not None:
            yield context
            context = context.linked_context()

    def __eq__(self, other):
        """ Compare two context. Two context are equal if they have the same context_name and each their own
                linked context are equal also.

                :param other: context to compare
                :return: bool
                """
        if isinstance(other, WContextProto) is False:
            return False
        context_a = self
        context_b = other
        while context_a is not None and context_b is not None:
            if context_a.context_name() != context_b.context_name():
                return False
            context_a = context_a.linked_context()
            context_b = context_b.linked_context()

        if context_b is not None:
            return False
        if context_a is not None:
            return False
        return True


class WContext(WContextProto):
    __doc__ = ' :class:`.WContextProto` implementation\n\t'

    @verify_type(context_name=str, context_value=(str, None), linked_context=(WContextProto, None))
    def __init__(self, context_name, context_value=None, linked_context=None):
        """ Create new context request

                :param context_name: context name
                :param context_value: context value
                :param linked_context: linked context
                """
        self._WContext__context_name = context_name
        self._WContext__context_value = context_value
        self._WContext__linked_context = linked_context

    def context_name(self):
        """ :meth:`.WContextProto.context_name` implementation
                """
        return self._WContext__context_name

    def context_value(self):
        """ :meth:`.WContextProto.context_value` implementation
                """
        return self._WContext__context_value

    def linked_context(self):
        """ :meth:`.WContextProto.linked_context` implementation
                """
        return self._WContext__linked_context

    @classmethod
    @verify_type(context=(WContextProto, None))
    def export_context(cls, context):
        """ Export the specified context to be capable context transferring

                :param context: context to export
                :return: tuple
                """
        if context is None:
            return
        result = [(x.context_name(), x.context_value()) for x in context]
        result.reverse()
        return tuple(result)

    @classmethod
    @verify_type(context=(tuple, list, None))
    def import_context(cls, context):
        """ Import context to corresponding WContextProto object (:meth:`WContext.export_context` reverse operation)

                :param context: context to import
                :return: WContext
                """
        if context is None or len(context) == 0:
            return
        result = WContext(context[0][0], context[0][1])
        for iter_context in context[1:]:
            result = WContext(iter_context[0], context_value=iter_context[1], linked_context=result)

        return result

    @classmethod
    @verify_type(context_specs=str)
    def specification(cls, *context_specs):
        """ Return linked context as adapter specification (is used by :class:`.WCommandContextAdapter`)

                :param context_specs: context names
                :return: WContext
                """
        import_data = []
        for name in context_specs:
            import_data.append((name, None))

        return cls.import_context(import_data)


class WContextComposer(WComposerProto):

    @verify_type('paranoid', obj_spec=(tuple, list, None))
    def compose(self, obj_spec):
        return WContext.import_context(obj_spec)

    @verify_type('paranoid', obj=(WContextProto, None))
    def decompose(self, obj):
        return WContext.export_context(obj)


class WCommandContextAdapter(metaclass=ABCMeta):
    __doc__ = ' Adapter is used for command tokens modification\n\t'

    @verify_type(context_specifications=(WContextProto, None))
    def __init__(self, context_specifications):
        """ Create adapter

                :param context_specifications: context for what this adapter works
                """
        self._WCommandContextAdapter__spec = context_specifications

    def specification(self):
        """ Return adapter specification

                :return: WContextProto or None
                """
        return self._WCommandContextAdapter__spec

    @verify_type(command_context=(WContextProto, None))
    def match(self, command_context=None, **command_env):
        """ Check if context request is compatible with adapters specification. True - if compatible,
                False - otherwise

                :param command_context: context to check
                :param command_env: command environment
                :return: bool
                """
        spec = self.specification()
        if command_context is None and spec is None:
            return True
        if command_context is not None and spec is not None:
            return command_context == spec
        return False

    @abstractmethod
    @verify_type(command_tokens=str, command_context=(WContextProto, None))
    def adapt(self, *command_tokens, command_context=None, **command_env):
        """ Adapt the given command tokens with this adapter

                :param command_tokens: command tokens to adapt
                :param command_context: context
                :param command_env: command environment
                :return: list of str
                """
        raise NotImplementedError('This method is abstract')


class WCommandContext(WCommandProto):
    __doc__ = ' Command that can be adapted by a context\n\t'

    @verify_type(command=WCommandProto, context_adapter=WCommandContextAdapter)
    def __init__(self, base_command, context_adapter):
        """ Create new command

                :param base_command: basic command that does real magic
                :param context_adapter: adapter for command tokens modification
                """
        WCommandProto.__init__(self)
        self._WCommandContext__command = base_command
        self._WCommandContext__adapter = context_adapter

    def original_command(self):
        """ Return source command

                :return: WCommandProto
                """
        return self._WCommandContext__command

    def adapter(self):
        """ Return command adapter

                :return: WCommandAdapter
                """
        return self._WCommandContext__adapter

    @verify_type('paranoid', command_tokens=str, command_context=(WContextProto, None))
    def match(self, *command_tokens, command_context=None, **command_env):
        """ Match command

                :param command_tokens: command tokens to check
                :param command_context: command context
                :param command_env: command environment
                :return: bool
                """
        if self.adapter().match(command_context, **command_env) is False:
            return False
        command_tokens = self.adapter().adapt(command_context=command_context, *command_tokens, **command_env)
        return self.original_command().match(command_context=command_context, *command_tokens, **command_env)

    @verify_type('paranoid', command_tokens=str, command_context=(WContextProto, None))
    def exec(self, *command_tokens, command_context=None, **command_env):
        """ Execute command

                :param command_tokens: command tokens to execute
                :param command_context: command context
                :param command_env: command environment
                :return: WCommandResultProto
                """
        if self.adapter().match(command_context, **command_env) is False:
            cmd = WCommandProto.join_tokens(*command_tokens)
            spec = self.adapter().specification()
            if spec is not None:
                spec = [x.context_name() for x in spec]
                spec.reverse()
                spec = ','.join(spec)
            raise RuntimeError('Command mismatch: %s (context: %s)' % (cmd, spec))
        command_tokens = self.adapter().adapt(command_context=command_context, *command_tokens, **command_env)
        return self.original_command().exec(command_context=command_context, *command_tokens, **command_env)
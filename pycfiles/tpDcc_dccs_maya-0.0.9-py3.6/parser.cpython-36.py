# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/parser.py
# Compiled at: 2020-05-02 23:38:23
# Size of source mod 2**32: 9756 bytes
"""
Module that contains Maya File Parser classes
"""
import json

class MayaParserBase(object):
    __doc__ = '\n    Base class to defines Maya files parser\n    '

    def on_requires_maya(self, version):
        """

        :param version:
        :return:
        """
        pass

    def on_requires_plugin(self, plugin, version):
        """

        :param plugin:
        :param version:
        :return:
        """
        pass

    def on_file_info(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        pass

    def on_current_unit(self, angle, linear, time):
        """

        :param angle:
        :param linear:
        :param time:
        :return:
        """
        pass

    def on_file_reference(self, path):
        """

        :param path:
        :return:
        """
        pass

    def on_create_node(self, nodetype, name, parent):
        """

        :param nodetype:
        :param name:
        :param parent:
        :return:
        """
        pass

    def on_select(self, name):
        """

        :param name:
        :return:
        """
        pass

    def on_add_attr(self, node, name):
        """

        :param node:
        :param name:
        :return:
        """
        pass

    def on_set_attr(self, name, value, attr_type):
        """

        :param name:
        :param value:
        :param attr_type:
        :return:
        """
        pass

    def on_set_attr_flags(self, plug, keyable=None, channel_box=None, lock=None):
        """

        :param plug:
        :param keyable:
        :param channel_box:
        :param lock:
        :return:
        """
        pass

    def on_connect_attr(self, src_plug, dst_plug):
        """

        :param src_plug:
        :param dst_plug:
        :return:
        """
        pass


class MayaAsciiError(ValueError):
    __doc__ = '\n    Custom value error used by Maya parsers\n    '


class MayaAsciiParserBase(MayaParserBase):
    __doc__ = '\n    Base class for Maya ASCII files parser\n    '

    def __init__(self):
        self._MayaAsciiParserBase__command_handlers = {'requires':self._exec_requires, 
         'fileInfo':self._exec_file_info, 
         'file':self._exec_file, 
         'createNode':self._exec_create_node, 
         'setAttr':self._exec_set_attr}

    def on_comment(self, value):
        """

        :param value:
        :return:
        """
        pass

    def register_handler(self, command, handler):
        """

        :param command:
        :param handler:
        :return:
        """
        self._MayaAsciiParserBase__command_handlers[command] = handler

    def exec_command(self, command, args):
        """

        :param command:
        :param args:
        :return:
        """
        handler = self._MayaAsciiParserBase__command_handlers.get(command, None)
        if handler is not None:
            handler(args)

    def has_command(self, command):
        """

        :param command:
        :return:
        """
        return command in self._MayaAsciiParserBase__command_handlers

    def _exec_requires(self, args):
        """

        :param args:
        :return:
        """
        if args[0] == 'maya':
            self.on_requires_maya(args[1])
        else:
            self.on_requires_plugin(args[0], args[1])

    def _exec_file_info(self, args):
        """

        :param args:
        :return:
        """
        self.on_file_info(args[0], args[1])

    def _exec_file(self, args):
        """

        :param args:
        :return:
        """
        reference = False
        reference_depth_info = None
        namespace = None
        defer_reference = False
        reference_node = None
        argptr = 0
        while argptr < len(args):
            arg = args[argptr]
            if arg in ('-r', '--reference'):
                reference = True
                argptr += 1
            elif arg in ('-rdi', '--referenceDepthInfo'):
                reference_depth_info = int(args[(argptr + 1)])
                argptr += 2
            elif arg in ('-ns', '--namespace'):
                namespace = args[(argptr + 1)]
                argptr += 2
            elif arg in ('-dr', '--deferReference'):
                defer_reference = bool(int(args[(argptr + 1)]))
                argptr += 2
            elif arg in ('-rfn', '--referenceNode'):
                reference_node = args[(argptr + 1)]
                argptr += 2
            else:
                if arg in ('-op', ):
                    argptr += 2
                else:
                    if arg in ('-typ', '--type'):
                        argptr += 2
                    else:
                        break

        if argptr < len(args):
            path = args[argptr]
            self.on_file_reference(path)

    def _exec_create_node(self, args):
        nodetype = args[0]
        name = None
        parent = None
        argptr = 1
        while argptr < len(args):
            arg = args[argptr]
            if arg in ('-n', '--name'):
                name = args[(argptr + 1)]
                argptr += 2
            else:
                if arg in ('-p', '--parent'):
                    parent = args[(argptr + 1)]
                    argptr += 2
                else:
                    if arg in ('-s', '--shared'):
                        argptr += 1
                    else:
                        raise MayaAsciiError('Unexpected argument: %s' % arg)

        self.on_create_node(nodetype, name, parent)

    def _exec_set_attr(self, args):
        name = args.pop(0)[1:]
        attr_type = None
        value = None
        argptr = 1
        while argptr < len(args):
            arg = args[argptr]
            if arg in ('-type', '--type'):
                attr_type = args[(argptr + 1)]
                value = args[argptr + 2:]
                argptr += 2
            else:
                argptr += 1

        if not value:
            value = args[(-1)]
        if not attr_type:
            types = {str: 'string', 
             float: 'double', 
             int: 'integer'}
            try:
                attr_type = types[type(json.loads(value))]
            except KeyError:
                attr_type = 'string'
            except ValueError:
                attr_type = types.get(type(value), 'string')

        self.on_set_attr(name, value, attr_type)


class MayaAsciiParser(MayaAsciiParserBase):
    __doc__ = '\n    Class to parse Maya ASCII files\n    '

    def __init__(self, stream):
        super(MayaAsciiParser, self).__init__()
        self._MayaAsciiParser__stream = stream

    def parse(self):
        """

        :return:
        """
        while self._MayaAsciiParser__parse_next_command():
            pass

    def __parse_next_command(self):
        """

        :return:
        """
        lines = []
        line = self._MayaAsciiParser__stream.readline()
        while True:
            if not line:
                break
            else:
                if line.startswith('//'):
                    self.on_comment(line[2:].strip())
                else:
                    line = line.rstrip('\r\n')
            if line:
                if line.endswith(';'):
                    lines.append(line[:-1])
                    break
            if line:
                lines.append(line)
            line = self._MayaAsciiParser__stream.readline()

        if lines:
            self._MayaAsciiParser__parse_command_lines(lines)
            return True
        else:
            return False

    def __parse_command_lines(self, lines):
        command, _, lines[0] = lines[0].partition(' ')
        command = command.lstrip()
        if self.has_command(command):
            args = []
            for line in lines:
                while True:
                    line = line.strip()
                    if not line:
                        break
                    if line[0] in '\'"':
                        string_delim = line[0]
                        escaped = False
                        string_end = len(line)
                        for i in range(1, len(line)):
                            if not escaped and line[i] == string_delim:
                                string_end = i
                                break
                            elif not escaped and line[i] == '\\':
                                escaped = True
                            else:
                                escaped = False

                        arg, line = line[1:string_end], line[string_end + 1:]
                    else:
                        arg, _, line = line.partition(' ')
                    args.append(arg)

            self.exec_command(command, args)
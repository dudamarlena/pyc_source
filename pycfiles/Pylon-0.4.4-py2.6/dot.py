# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pylon\io\dot.py
# Compiled at: 2010-12-26 13:36:33
""" Defines a class for writing case data in Graphviz DOT language.
"""
import logging, subprocess, StringIO
from pylon.io.common import _CaseWriter
logger = logging.getLogger(__name__)
BUS_ATTR = {'color': 'blue'}
BRANCH_ATTR = {'color': 'green'}
GENERATOR_ATTR = {}

class DotWriter(_CaseWriter):
    """ Write case data to file in Graphviz DOT language.
    """

    def __init__(self, case, bus_attr=None, branch_attr=None, gen_attr=None):
        """ Initialises a new DOTWriter instance.
        """
        super(DotWriter, self).__init__(case)
        self.bus_attr = BUS_ATTR if bus_attr is None else bus_attr
        self.branch_attr = BRANCH_ATTR if branch_attr is None else branch_attr
        self.gen_attr = GENERATOR_ATTR if gen_attr is None else gen_attr
        return

    def write(self, file_or_filename, prog=None, format='xdot'):
        """ Writes the case data in Graphviz DOT language.

        The format 'raw' is used to dump the Dot representation of the Case
        object, without further processing. The output can be processed by any
        of graphviz tools, defined in 'prog'.
        """
        if prog is None:
            file = super(DotWriter, self).write(file_or_filename)
        else:
            buf = StringIO.StringIO()
            super(DotWriter, self).write(buf)
            buf.seek(0)
            data = self.create(buf.getvalue(), prog, format)
            if isinstance(file_or_filename, basestring):
                file = None
                try:
                    try:
                        file = open(file_or_filename, 'wb')
                    except:
                        logger.error('Error opening %s.' % file_or_filename)

                finally:
                    if file is not None:
                        file.write(data)
                        file.close()

            else:
                file = file_or_filename
                file.write(data)
        return file

    def _write_data(self, file):
        super(DotWriter, self)._write_data(file)
        file.write('}\n')

    def write_case_data(self, file):
        """ Writes the case data to file
        """
        file.write('digraph %s {\n' % self.case.name)

    def write_bus_data(self, file, padding='    '):
        """ Writes bus data to file.
        """
        for bus in self.case.buses:
            attrs = [ '%s="%s"' % (k, v) for (k, v) in self.bus_attr.iteritems() ]
            attr_str = (', ').join(attrs)
            file.write('%s%s [%s];\n' % (padding, bus.name, attr_str))

    def write_branch_data(self, file, padding='    '):
        """ Writes branch data in Graphviz DOT language.
        """
        attrs = [ '%s="%s"' % (k, v) for (k, v) in self.branch_attr.iteritems() ]
        attr_str = (', ').join(attrs)
        for br in self.case.branches:
            file.write('%s%s -> %s [%s];\n' % (
             padding, br.from_bus.name, br.to_bus.name, attr_str))

    def write_generator_data(self, file, padding='    '):
        """ Write generator data in Graphviz DOT language.
        """
        attrs = [ '%s="%s"' % (k, v) for (k, v) in self.gen_attr.iteritems() ]
        attr_str = (', ').join(attrs)
        edge_attrs = [ '%s="%s"' % (k, v) for (k, v) in {}.iteritems() ]
        edge_attr_str = (', ').join(edge_attrs)
        for g in self.case.generators:
            file.write('%s%s [%s];\n' % (padding, g.name, attr_str))
            file.write('%s%s -> %s [%s];\n' % (
             padding, g.name, g.bus.name, edge_attr_str))

    def create(self, dotdata, prog='dot', format='xdot'):
        """ Creates and returns a representation of the graph using the
        Graphviz layout program given by 'prog', according to the given format.

        Writes the graph to a temporary dot file and processes it with the
        program given by 'prog' (which defaults to 'dot'), reading the output
        and returning it as a string if the operation is successful. On failure
        None is returned.

        Based on PyDot by Ero Carrera.
        """
        import os, tempfile
        from dot2tex.dotparsing import find_graphviz
        progs = find_graphviz()
        if progs is None:
            logger.warning('GraphViz executables not found.')
            return
        else:
            if not progs.has_key(prog):
                logger.warning('Invalid program [%s]. Available programs are: %s' % (
                 prog, progs.keys()))
                return
            (tmp_fd, tmp_name) = tempfile.mkstemp()
            os.close(tmp_fd)
            dot_fd = file(tmp_name, 'w+b')
            dot_fd.write(dotdata)
            dot_fd.close()
            tmp_dir = os.path.dirname(tmp_name)
            p = subprocess.Popen((progs[prog], '-T' + format, tmp_name), cwd=tmp_dir, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            stderr = p.stderr
            stdout = p.stdout
            stdout_output = list()
            while True:
                data = stdout.read()
                if not data:
                    break
                stdout_output.append(data)

            stdout.close()
            if stdout_output:
                stdout_output = ('').join(stdout_output)
            if not stderr.closed:
                stderr_output = list()
                while True:
                    data = stderr.read()
                    if not data:
                        break
                    stderr_output.append(data)

                stderr.close()
                if stderr_output:
                    stderr_output = ('').join(stderr_output)
            status = p.wait()
            if status != 0:
                logger.error('Program [%s] terminated with status: %d. stderr follows: %s' % (
                 prog, status, stderr_output))
            elif stderr_output:
                logger.error('%s', stderr_output)
            os.unlink(tmp_name)
            return stdout_output
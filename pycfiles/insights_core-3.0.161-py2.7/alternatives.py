# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/alternatives.py
# Compiled at: 2019-05-16 13:41:33
"""
Alternatives - command ``/usr/bin/alternatives`` output
=======================================================
"""
from insights import parser, CommandParser
from insights.core import ParseException
from insights.specs import Specs

class AlternativesOutput(CommandParser):
    r"""
    Read the output of ``/usr/sbin/alternatives --display *program*`` and
    convert into information about the given program's alternatives.

    Typical input is::

        java - status is auto.
         link currently points to /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.111-1.b15.el7_2.x86_64/jre/bin/java
        /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.111-2.6.7.2.el7_2.x86_64/jre/bin/java - priority 1700111
        /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.111-1.b15.el7_2.x86_64/jre/bin/java - priority 1800111
        /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java - priority 16091
         slave ControlPanel: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel
         slave keytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/keytool
         slave policytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/policytool
         slave rmid: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmid
        Current `best' version is /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java.

    Lines are interpreted this way:

    * Program lines are of the form '*name* - status is *status*', and start
      the information for a program.  Lines before this are ignored.
    * The current link to this program is found on lines starting with 'link
      currently points to'.
    * Lines starting with '/' and with ' - priority ' in them record an
      alternative path and its priority.
    * Lines starting with 'slave *program*: *path*' are recorded against the
      alternative path.
    * Lines starting with 'Current \`best' version is' indicate the default
      choice of an 'auto' status alternative.

    The output of ``alternatives --display *program*`` can only ever list one
    program, so as long as one 'status is' line is found (as described above),
    the content of the object displays that program.

    Attributes:
        program (str): The name of the program found in the 'status is' line.
            This attribute is set to ``None`` if a status line is not found.
        status (str): The status of the program, or ``None`` if not found.
        link (str): The link to this program, or ``None`` if the 'link
            currently points to`` line is not found.
        best (str): The 'best choice' path that ``alternatives`` would use, or
            ``None`` if the 'best choice' line is not found.
        paths (dict): The alternative paths for this program.  Each path is a
            dictionary containing the following keys:

              * ``path``: the actual path of this alternative for the program
              * ``priority``: the priority, as an integer (e.g. 1700111)
              * ``slave``: a dictionary of programs dependent on this alternative -
                the key is the program name (e.g. 'ControlPanel') and the value is
                the path to that program for this alternative path.

    Examples:
        >>> java = AlternativesOutput(context_wrap(JAVA_ALTERNATIVES))
        >>> java.program
        'java'
        >>> java.link
        '/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.111-1.b15.el7_2.x86_64/jre/bin/java'
        >>> len(java.paths)
        3
        >>> java.paths[0]['path']
        '/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.111-2.6.7.2.el7_2.x86_64/jre/bin/java'
        >>> java.paths[0]['priority']
        1700111
        >>> java.paths[2]['slave']['ControlPanel']
        '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel'
"""

    def parse_content(self, content):
        """
        Parse the output of the ``alternatives`` command.
        """
        self.program = None
        self.status = None
        self.link = None
        self.best = None
        self.paths = []
        current_path = None
        for line in content:
            words = line.split(None)
            if ' - status is' in line:
                if self.program:
                    raise ParseException(('Program line for {newprog} found in output for {oldprog}').format(newprog=words[0], oldprog=self.program))
                self.program = words[0]
                self.status = words[4][:-1]
                self.alternatives = []
                current_path = {}
            elif not self.program:
                continue
            elif line.startswith(' link currently points to ') and len(words) == 5:
                self.link = words[4]
            elif ' - priority ' in line and len(words) == 4 and words[3].isdigit():
                self.paths.append({'path': words[0], 
                   'priority': int(words[3]), 
                   'slave': {}})
                current_path = self.paths[(-1)]
            elif line.startswith(' slave ') and len(words) == 3 and current_path:
                current_path['slave'][words[1][:-1]] = words[2]
            elif line.startswith("Current `best' version is ") and len(words) == 5:
                self.best = words[4][:-1]

        return


@parser(Specs.display_java)
class JavaAlternatives(AlternativesOutput):
    """
    Class to read the ``/usr/sbin/alternatives --display java`` output.

    Uses the ``AlternativesOutput`` base class to get information about the
    alternatives for ``java`` available and which one is currently in use.

    Examples:
        >>> java = shared[JavaAlternatives]
        >>> java.program
        'java'
        >>> java.link
        '/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.111-1.b15.el7_2.x86_64/jre/bin/java'
        >>> len(java.paths)
        3
        >>> java.paths[0]['path']
        '/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.111-2.6.7.2.el7_2.x86_64/jre/bin/java'
        >>> java.paths[0]['priority']
        1700111
        >>> java.paths[2]['slave']['ControlPanel']
        '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel'
    """
    pass
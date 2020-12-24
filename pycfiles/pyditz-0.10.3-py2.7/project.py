# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/command/project.py
# Compiled at: 2016-03-07 14:40:46
"""
Project commands.
"""

class CmdProject(object):

    def do_add_component(self, arg):
        """add-component [name] -- Add a component"""
        name = self.getarg(arg, 1) or self.getline('Name: ', allowempty=False)
        self.db.add_component(name)
        self.write('Added component', name)

    def do_add_release(self, arg):
        """add-release [name] -- Add a release"""
        name = self.getarg(arg, 1) or self.getline('Name: ', allowempty=False)
        self.write('Adding release', name)
        comment = self.getcomment()
        self.db.add_release(name, comment=comment)
        self.write('Added release', name)

    def do_release(self, arg):
        """release <unreleased_release> -- Release a release"""
        name = self.getrelease(arg, 1)
        comment = self.getcomment()
        self.db.release_release(name, comment)
        self.write('Released', name)

    def do_export(self, arg):
        """export <format> [path] -- Export issue database"""
        fmt = self.getarg(arg, 1)
        if not fmt:
            self.error('no export format specified')
        path = self.getarg(arg, 2) or fmt
        self.db.export(fmt, path)
        self.write("Exported issues to '%s'" % path)

    def help_export(self):
        from ditz.exporter import get_exporters
        self.write(self.do_export.__doc__)
        self.write()
        self.write('available formats:')
        for name, desc in get_exporters():
            self.write('    %s -- %s' % (name, desc))

    def do_archive(self, arg):
        """archive <release> [dir] -- Archive a release"""
        name = self.getrelease(arg, 1)
        path = self.getarg(arg, 2) or 'ditz-archive-%s' % name
        self.db.archive_release(name, path)
        self.write('Archived to', path)

    def do_validate(self, arg):
        """validate -- Fix or report problems with issue database"""
        changes = self.db.validate()
        if changes:
            for idx, msglist in sorted(changes.items()):
                for msg in msglist:
                    self.write('issue %s: %s' % (idx, msg))

        else:
            self.write('No problems found')
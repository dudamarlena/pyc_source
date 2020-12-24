# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cc/buildout_reports/xxx.py
# Compiled at: 2007-08-22 14:18:31
"""Generate a XXX/TODO report.
"""
import cc.buildout_reports, os, stat, logging, subprocess, zc.buildout

class XxxReport:
    """Generate an HTML XXX/TODO comment report for the project.  Supports
    the following configuration parameters:

    * pattern: the pattern to scan for; if not specified, defaults to
        (XXX|TODO)
        
    * report_file: the file to save the report to; if not specified, defaults
        to XXXreport.html, stored in the buildout directory.  If specified
        as a relative path, it is interpreted as relative to the buildout
        directory.
        
    """
    __module__ = __name__

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        if 'pattern' not in options:
            options['pattern'] = '?(XXX|TODO)'
            logging.getLogger(name).info('No comment pattern for XXX report specified; using %s', options['pattern'])
        if 'report_file' not in options:
            options['report_file'] = os.path.join(buildout['buildout']['directory'], 'XXXreport.html')
            logging.getLogger(name).info('No output file for XXX report specified; using %s', options['report_file'])
        else:
            options['report_file'] = os.path.abspath(options['report_file'])
        self.script_name = os.path.join(os.path.dirname(cc.buildout_reports.__file__), 'xxx_report.sh')
        if not os.access(self.script_name, os.X_OK):
            os.chmod(self.script_name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def install(self):
        """Generate the XXX report for this project."""
        subprocess.call([self.script_name, self.buildout['buildout']['directory'], self.options['report_file'], self.options['pattern']])
        return [
         self.options['report_file']]

    update = install
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/sk/recipe/jython/impl.py
# Compiled at: 2010-02-20 21:11:04
"""Jython installer recipe for Buildout: implementation."""
import logging, os, os.path, zc.buildout, subprocess
from zc.buildout.download import Download
_defaultURL = 'http://sourceforge.net/projects/jython/files/jython/jython_installer-2.5.1.jar'
_defaultMD5 = '2ee978eff4306b23753b3fe9d7af5b37'

class Recipe(object):
    """This is a Buildout recipe that automates the installation of Jython."""
    __module__ = __name__

    def __init__(self, buildout, name, options):
        """Initialize the recipe."""
        self.buildout, self.name, self.options = buildout, name, options
        if 'md5sum' in options and 'url' not in options:
            raise zc.buildout.UserError('You must specify the "url" to a Jython installer when specifying the "md5sum" of it.')
        if 'md5sum' not in options and 'url' in options:
            defaultMD5 = ''
        else:
            defaultMD5 = _defaultMD5
        options['location'] = os.path.join(buildout['buildout']['parts-directory'], name)
        options['executable'] = os.path.join(options['location'], 'bin', 'jython')
        options['url'] = options.get('url', _defaultURL).strip()
        options['md5sum'] = options.get('md5sum', defaultMD5).strip()
        options['java'] = options.get('java', 'java').strip()
        options['jre'] = options.get('jre', '').strip()
        self.parts = []
        for i in options.get('include-parts', '').splitlines():
            if i.strip():
                self.parts.append(i)

    def install(self):
        """Install Jython."""
        logger = logging.getLogger(self.name)
        downloader = Download(self.buildout['buildout'], namespace='sk.recipe.jython', logger=logger)
        url, md5sum = self.options['url'], self.options['md5sum']
        if len(md5sum) == 0:
            md5sum = None
        (installerPath, isInstallerTemporary) = downloader(url, md5sum)
        java, jre, destination = self.options['java'], self.options['jre'], self.options['location']
        if not os.path.isdir(destination):
            os.makedirs(destination)
        args = [
         java, '-jar', installerPath, '--silent', '--directory', destination]
        if jre:
            args.extend(['--jre', jre])
        if len(self.parts) > 0:
            args.append('--include')
            args.extend(self.parts)
        rc = subprocess.call(args)
        if rc != 0:
            raise SystemError('Jython installer return nonzero (%d) status; invoked with %r' % (rc, args))
        return destination

    def update(self):
        """Update Jython. No update facility is provided, though."""
        pass
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/metadirectives.py
# Compiled at: 2010-11-18 05:52:41
from zope.interface.interface import Interface
import zope.configuration.fields, zope.schema

class ICacheBursterDirective(Interface):
    """
    Examples:
    
    <cacheburster from="(.*).css" 
                 to="\x01.{version}.css"
                 fileset="resources/css/*.css"
                 />
                 
    For:     
      file path:     resources/css/defaultstyles.css
      resource name: styles.css
      
    You get:         styles.884863d2.css
    ---------------------------------------------------------------------------
          
    <cacheburster from="(.*)-module.js" 
                 to="\x01-module.js?{version}"
                 manager="md5" 
                 />
                 
    For:     
      file path:     any
      resource name: admin-module.js
      
    You get:         admin-module.js?202cb962ac59075b964b07152d234b70
    ---------------------------------------------------------------------------

    <cachebuster from="any_script.pack" 
                 to="any_script.{version}" 
                 manager="versionfile"
                 />
                 
    For:     
      file path:     any
      resource name: any_script.pack
      
    You get:         any_script.1
    """
    from_ = zope.schema.TextLine(title='The original URL pattern which need to be replace', description='Field contain regular expression pattern.', required=True)
    to = zope.schema.TextLine(title='The replacement URL pattern which the `in` needs to be converted to', description='Field contain regular expression pattern.         Cache Buster picks up version value and populates the replacement         variable {version}.', required=True)
    manager = zope.schema.TextLine(title='Version manager', description='A name of which is supposed to store the version         (or revision or build number) for the project or set resources.         The cache buster simply picks up this value and populates the replacement         variable {version}.                 You can select one of set methods: md5, crc32, versionfile or custom.         In developer mode the hash is recomputed each time the         resource is asked for its URL, while in production mode the hash is         computed only once, so remember to restart the server after changing         resource files (otherwise browsers will still see the old URL unchanged and         use their outdated cached versions of the files)', required=True, default='crc32')
    fileset = zope.configuration.fields.Tokens(title='Path expressions', description='Search pattern for file or group of files to which you         want to apply the cache busting rules to.         The glob module used for fetch file list according to the rules used by         the Unix shell. No tilde expansion is done, but *, ?, and character         ranges expressed with [] will be correctly matched.', required=False, value_type=zope.configuration.fields.Path(), unique=True)
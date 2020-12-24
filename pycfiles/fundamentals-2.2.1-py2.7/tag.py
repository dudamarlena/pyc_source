# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/files/tag.py
# Compiled at: 2020-04-17 06:44:40
"""
*Add tags and ratings to your macOS files and folders*

:Author:
    David Young
"""
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime, date, time
import codecs

def tag(log, filepath, tags=False, rating=False, wherefrom=False):
    """Add tags and ratings to your macOS files and folders

    **Key Arguments**

    - ``log`` -- logger
    - ``filepath`` -- the path to the file needing tagged
    - ``tags`` -- comma or space-separated string, or list of tags. Use `False` to leave file tags as they are. Use "" or [] to remove tags. Default *False*.
    - ``rating`` -- a rating to add to the file. Use 0 to remove rating or `False` to leave file rating as it is. Default *False*.
    - ``wherefrom`` -- add a URL to indicate where the file come from. Use `False` to leave file location as it is. Use "" to remove location. Default *False*.
    

    **Return**

    - None
    

    **Usage**

    To add any combination of tags, rating and a source URL to a file on macOS, use the following:

    ```python
    from fundamentals.files.tag import tag
    tag(
        log=log,
        filepath="/path/to/my.file",
        tags="test,tags, fundamentals",
        rating=3,
        wherefrom="http://www.thespacedoctor.co.uk"
    )
    ```
    
    """
    log.debug('starting the ``tag`` function')
    if isinstance(tags, list):
        tags = (' ').join(tags)
    if tags and len(tags):
        tags = tags.replace(',', ' ')
        tags = '<string>' + tags.replace('  ', ' ').replace('  ', ' ').replace(' ', '</string><string>') + '</string>'
    if tags != False:
        now = datetime.now()
        now = now.strftime('%Y%m%dt%H%M%S%f')
        tagPlist = '/tmp/fund-%(now)s-tags.plist' % locals()
        try:
            writeFile = codecs.open(tagPlist, encoding='utf-8', mode='w')
        except IOError as e:
            message = 'could not open the file %s' % (tagPlist,)
            raise IOError(message)

        writeFile.write('\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<array>\n%(tags)s \n</array>\n</plist>' % locals())
        writeFile.close()
        cmd = 'plutil -convert binary1 %(tagPlist)s' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output: %(stdout)s' % locals())
        log.debug('output: %(stderr)s' % locals())
        cmd = 'xattr -wx "com.apple.metadata:_kMDItemUserTags" "`xxd -ps %(tagPlist)s`" "%(filepath)s"' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output: %(stdout)s' % locals())
        log.debug('output: %(stderr)s' % locals())
        os.remove(tagPlist)
    if rating != False:
        ratingsContainer = os.path.dirname(__file__) + '/resources/ratings/'
        ratingPlist = '%(ratingsContainer)s%(rating)s.plist' % locals()
        cmd = 'xattr -wx "com.apple.metadata:kMDItemStarRating" "`xxd -ps %(ratingPlist)s`" "%(filepath)s"' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output: %(stdout)s' % locals())
        log.debug('output: %(stderr)s' % locals())
        cmd = 'xattr -wx "org.openmetainfo:kMDItemStarRating" "`xxd -ps %(ratingPlist)s`" "%(filepath)s"' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output: %(stdout)s' % locals())
        log.debug('output: %(stderr)s' % locals())
    if wherefrom != False:
        if len(wherefrom):
            wherefrom = '<string>%(wherefrom)s</string>' % locals()
        now = datetime.now()
        now = now.strftime('%Y%m%dt%H%M%S%f')
        urlPlist = '/tmp/fund-%(now)s-url.plist' % locals()
        try:
            writeFile = codecs.open(urlPlist, encoding='utf-8', mode='w')
        except IOError as e:
            message = 'could not open the file %s' % (urlPlist,)
            raise IOError(message)

        writeFile.write('\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n%(wherefrom)s\n</plist>' % locals())
        writeFile.close()
        cmd = 'xattr -wx "com.apple.metadata:kMDItemURL" "`xxd -ps %(urlPlist)s`" "%(filepath)s"' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output URL: %(stdout)s' % locals())
        log.debug('output URL: %(stderr)s' % locals())
        now = datetime.now()
        now = now.strftime('%Y%m%dt%H%M%S%f')
        urlPlist = '/tmp/fund-%(now)s-url.plist' % locals()
        try:
            writeFile = codecs.open(urlPlist, encoding='utf-8', mode='w')
        except IOError as e:
            message = 'could not open the file %s' % (urlPlist,)
            raise IOError(message)

        writeFile.write('\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<array>\n%(wherefrom)s\n</array>\n</plist>' % locals())
        writeFile.close()
        cmd = 'xattr -wx "com.apple.metadata:kMDItemWhereFroms" "`xxd -ps %(urlPlist)s`" "%(filepath)s"' % locals()
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        log.debug('output URL: %(stdout)s' % locals())
        log.debug('output URL: %(stderr)s' % locals())
    log.debug('completed the ``tag`` function')
    return
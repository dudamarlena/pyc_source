# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/single_page.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 1308 bytes


class SinglePage(object):

    def __init__(self, page_object, request=None):
        self.request = request

    def on_create(self):
        pass

    @property
    def html_content(self):
        """The html content of the page. This formats the page
        using the CreoleFormatter"""
        logger.debug('html_content entered')
        try:
            content_obj = self.page_object.content.all()[0]
        except IndexError as e:
            try:
                if settings.DEBUG:
                    msg = 'We did not find a content_obj so returning a fake content since DEBUG is swithed on.'
                    logger.debug(msg)
                    return CreoleFormatter().html(fake_content=True)
                return 'Error: There is no content for this page.'
            finally:
                e = None
                del e

        _html_content = CreoleFormatter((content_obj.content), view=self).html()
        logger.debug('Call to YACMSObject.html_content returns: \n {}'.format(_html_content))
        return _html_content
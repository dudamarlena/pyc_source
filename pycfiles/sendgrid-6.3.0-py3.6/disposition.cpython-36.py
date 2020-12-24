# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/disposition.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 3123 bytes


class Disposition(object):
    __doc__ = 'The content-disposition of the Attachment specifying how you would like\n    the attachment to be displayed.'

    def __init__(self, disposition=None):
        """Create a Disposition object

        :param disposition: The content-disposition of the attachment,
                            specifying display style.
                            Specifies how you would like the attachment to be
                            displayed.
                            - "inline" results in the attached file being
                              displayed automatically within the message.
                            - "attachment" results in the attached file
                              requiring some action to display (e.g. opening
                              or downloading the file).
                            If unspecified, "attachment" is used. Must be one
                            of the two choices.
        :type disposition: string, optional
        """
        self._disposition = None
        if disposition is not None:
            self.disposition = disposition

    @property
    def disposition(self):
        """The content-disposition of the attachment, specifying display style.
           Specifies how you would like the attachment to be displayed.
           - "inline" results in the attached file being displayed
             automatically within the message.
           - "attachment" results in the attached file requiring some action to
             display (e.g. opening or downloading the file).
           If unspecified, "attachment" is used. Must be one of the two
           choices.

        :rtype: string
        """
        return self._disposition

    @disposition.setter
    def disposition(self, value):
        """The content-disposition of the attachment, specifying display style.
           Specifies how you would like the attachment to be displayed.
           - "inline" results in the attached file being displayed
             automatically within the message.
           - "attachment" results in the attached file requiring some action to
             display (e.g. opening or downloading the file).
           If unspecified, "attachment" is used. Must be one of the two
           choices.

        :param value: The content-disposition of the attachment, specifying
                      display style.
           Specifies how you would like the attachment to be displayed.
           - "inline" results in the attached file being displayed
             automatically within the message.
           - "attachment" results in the attached file requiring some action to
             display (e.g. opening or downloading the file).
           If unspecified, "attachment" is used. Must be one of the two
           choices.
        :type value: string
        """
        self._disposition = value

    def get(self):
        """
        Get a JSON-ready representation of this Disposition.

        :returns: This Disposition, ready for use in a request body.
        :rtype: string
        """
        return self.disposition
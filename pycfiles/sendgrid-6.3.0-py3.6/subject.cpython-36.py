# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/subject.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1806 bytes


class Subject(object):
    __doc__ = 'A subject for an email message.'

    def __init__(self, subject, p=None):
        """Create a Subjuct.

        :param subject: The subject for an email
        :type subject: string
        :param name: p is the Personalization object or Personalization object
                     index
        :type name: Personalization, integer, optional
        """
        self._subject = None
        self._personalization = None
        self.subject = subject
        if p is not None:
            self.personalization = p

    @property
    def subject(self):
        """The subject of an email.

        :rtype: string
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """The subject of an email.

        :param value: The subject of an email.
        :type value: string
        """
        self._subject = value

    @property
    def personalization(self):
        """The Personalization object or Personalization object index

        :rtype: Personalization, integer
        """
        return self._personalization

    @personalization.setter
    def personalization(self, value):
        """The Personalization object or Personalization object index

        :param value: The Personalization object or Personalization object
                      index
        :type value: Personalization, integer
        """
        self._personalization = value

    def __str__(self):
        """Get a JSON representation of this Mail request.

        :rtype: string
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this Subject.

        :returns: This Subject, ready for use in a request body.
        :rtype: string
        """
        return self.subject
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/send_at.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 2440 bytes


class SendAt(object):
    __doc__ = "A unix timestamp allowing you to specify when you want your\n    email to be delivered. This may be overridden by the\n    personalizations[x].send_at parameter. You can't schedule more\n    than 72 hours in advance. If you have the flexibility, it's\n    better to schedule mail for off-peak times. Most emails are\n    scheduled and sent at the top of the hour or half hour.\n    Scheduling email to avoid those times (for example, scheduling\n    at 10:53) can result in lower deferral rates because it won't\n    be going through our servers at the same times as everyone else's\n    mail."

    def __init__(self, send_at=None, p=None):
        """Create a unix timestamp specifying when your email should
        be delivered.

        :param send_at: Unix timestamp
        :type send_at: integer
        :param name: p is the Personalization object or Personalization object
                     index
        :type name: Personalization, integer, optional
        """
        self._send_at = None
        self._personalization = None
        if send_at is not None:
            self.send_at = send_at
        if p is not None:
            self.personalization = p

    @property
    def send_at(self):
        """A unix timestamp.

        :rtype: integer
        """
        return self._send_at

    @send_at.setter
    def send_at(self, value):
        """A unix timestamp.

        :param value: A unix timestamp.
        :type value: integer
        """
        self._send_at = value

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
        """Get a JSON representation of this object.

        :rtype: integer
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this SendAt object.

        :returns: The unix timestamp, ready for use in a request body.
        :rtype: integer
        """
        return self.send_at
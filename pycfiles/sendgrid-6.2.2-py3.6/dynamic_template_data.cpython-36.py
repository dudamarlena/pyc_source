# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/dynamic_template_data.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 2330 bytes


class DynamicTemplateData(object):
    __doc__ = 'To send a dynamic template, specify the template ID with the\n       template_id parameter.\n    '

    def __init__(self, dynamic_template_data=None, p=0):
        """Data for a transactional template.
        Should be JSON-serializeable structure.

        :param dynamic_template_data: Data for a transactional template.
        :type dynamic_template_data: A JSON-serializeable structure
        :param name: p is the Personalization object or Personalization object
                     index
        :type name:  Personalization, integer, optional
        """
        self._dynamic_template_data = None
        self._personalization = None
        if dynamic_template_data is not None:
            self.dynamic_template_data = dynamic_template_data
        if p is not None:
            self.personalization = p

    @property
    def dynamic_template_data(self):
        """Data for a transactional template.

        :rtype: A JSON-serializeable structure
        """
        return self._dynamic_template_data

    @dynamic_template_data.setter
    def dynamic_template_data(self, value):
        """Data for a transactional template.

        :param value: Data for a transactional template.
        :type value: A JSON-serializeable structure
        """
        self._dynamic_template_data = value

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

        :rtype: A JSON-serializeable structure
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this DynamicTemplateData object.

        :returns: Data for a transactional template.
        :rtype: A JSON-serializeable structure.
        """
        return self.dynamic_template_data
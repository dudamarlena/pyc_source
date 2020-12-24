# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/fields.py
# Compiled at: 2018-09-05 07:41:13
# Size of source mod 2**32: 1923 bytes
from io import BytesIO
import atoma, atoma.opml
from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.utils.translation import gettext_lazy as _

class OPMLField(FileField):
    default_error_messages = {'invalid_opml':_('Upload a valid OPML file. The file you uploaded was either not an OPML or a corrupted one.'), 
     'no_opml_feeds':_('Uploaded OPML file does not contain any feed URL.'), 
     'too_many_opml_feeds':_('Uploaded OPML file contains too many feed URLs.')}

    def to_python(self, data):
        f = super().to_python(data)
        if f is None:
            return
        else:
            if hasattr(data, 'temporary_file_path'):
                file = data.temporary_file_path()
            else:
                if hasattr(data, 'read'):
                    file = BytesIO(data.read())
                else:
                    file = BytesIO(data['content'])
                try:
                    opml = atoma.opml.parse_opml_file(file)
                except atoma.FeedXMLError as e:
                    raise ValidationError((self.error_messages['invalid_opml']),
                      code='invalid_opml') from e

                feed_uris = set(atoma.opml.get_feed_list(opml))
                if len(feed_uris) == 0:
                    raise ValidationError((self.error_messages['no_opml_feeds']),
                      code='no_opml_feeds')
                if len(feed_uris) > 1000:
                    raise ValidationError((self.error_messages['too_many_opml_feeds']),
                      code='too_many_opml_feeds')
                if hasattr(f, 'seek') and callable(f.seek):
                    f.seek(0)
            return feed_uris
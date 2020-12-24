# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/forms.py
# Compiled at: 2011-02-18 19:15:08
import formencode
from pylons import tmpl_context as c, request

class CommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    body = formencode.validators.String(not_empty=True, max=4000)
    author = formencode.validators.String(not_empty=False, max=50)
    author_website = formencode.validators.URL(not_empty=False, add_http=True)
    post_id = formencode.validators.Number()
    antiSpam = formencode.validators.Number(not_empty=True, min=3, max=4)


class FilterForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    filter = formencode.validators.String(not_empty=True, max=50)


class PostForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    body = formencode.validators.String(not_empty=True)
    subject = formencode.validators.String(not_empty=True, max=300)


def validate(schema):
    try:
        c.form_result = schema.to_python(dict(request.params))
        c.form_errors = {}
    except formencode.Invalid, error:
        c.form_result = error.value
        c.form_errors = error.error_dict or {}
        return False

    return True
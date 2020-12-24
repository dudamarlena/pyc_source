# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/models/user.py
# Compiled at: 2020-04-10 11:06:25
# Size of source mod 2**32: 861 bytes
from typing import Optional
import attr
from marshmallow_annotations.ext.attrs import AttrsSchema

@attr.s(auto_attribs=True, kw_only=True)
class User:
    id = None
    id: Optional[str]
    email = None
    email: Optional[str]
    first_name = None
    first_name: Optional[str]
    last_name = None
    last_name: Optional[str]
    full_name = None
    full_name: Optional[str]
    is_active = True
    is_active: bool
    github_username = None
    github_username: Optional[str]
    team_name = None
    team_name: Optional[str]
    slack_id = None
    slack_id: Optional[str]
    employee_type = None
    employee_type: Optional[str]
    manager_fullname = None
    manager_fullname: Optional[str]
    role_name = None
    role_name: Optional[str]


class UserSchema(AttrsSchema):

    class Meta:
        target = User
        register_as_scheme = True
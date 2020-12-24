# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/client/users.py
# Compiled at: 2017-09-19 13:56:43
# Size of source mod 2**32: 6381 bytes
from chisubmit.client.types import ChisubmitAPIObject, Attribute, APIStringType, APIObjectType, APIIntegerType, APIBooleanType, APIListType

class User(ChisubmitAPIObject):
    _api_attributes = {'username': Attribute(name='username', attrtype=APIStringType, editable=False), 
     
     'first_name': Attribute(name='first_name', attrtype=APIStringType, editable=False), 
     
     'last_name': Attribute(name='name', attrtype=APIStringType, editable=False), 
     
     'email': Attribute(name='email', attrtype=APIStringType, editable=False)}
    _api_relationships = {}


class Instructor(ChisubmitAPIObject):
    _api_attributes = {'username': Attribute(name='username', attrtype=APIStringType, editable=False), 
     
     'user': Attribute(name='user', attrtype=APIObjectType(User), editable=False), 
     
     'git_username': Attribute(name='git_username', attrtype=APIStringType, editable=True), 
     
     'git_staging_username': Attribute(name='git_staging_username', attrtype=APIStringType, editable=True)}
    _api_relationships = {}


class Student(ChisubmitAPIObject):
    _api_attributes = {'username': Attribute(name='username', attrtype=APIStringType, editable=False), 
     
     'user': Attribute(name='user', attrtype=APIObjectType(User), editable=False), 
     
     'git_username': Attribute(name='git_username', attrtype=APIStringType, editable=True), 
     
     'extensions': Attribute(name='extensions', attrtype=APIIntegerType, editable=True), 
     
     'dropped': Attribute(name='dropped', attrtype=APIBooleanType, editable=True)}
    _api_relationships = {}


class Grader(ChisubmitAPIObject):
    _api_attributes = {'url': Attribute(name='url', attrtype=APIStringType, editable=False), 
     
     'username': Attribute(name='username', attrtype=APIStringType, editable=False), 
     
     'user': Attribute(name='user', attrtype=APIObjectType(User), editable=False), 
     
     'conflicts_usernames': Attribute(name='conflicts_usernames', attrtype=APIListType(APIStringType), editable=True), 
     
     'conflicts': Attribute(name='conflicts', attrtype=APIListType(APIObjectType(Student)), editable=False), 
     
     'git_username': Attribute(name='git_username', attrtype=APIStringType, editable=True), 
     
     'git_staging_username': Attribute(name='git_staging_username', attrtype=APIStringType, editable=True)}
    _api_relationships = {}
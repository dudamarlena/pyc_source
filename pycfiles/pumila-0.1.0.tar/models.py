# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pumblr/models.py
# Compiled at: 2010-09-12 02:27:20
from utils import make_variable_name

class Model(object):

    def __init__(self):
        pass

    @classmethod
    def parse(kls, json):
        """Parse a JSON object into a model instance"""
        raise NotImplementedError


class ApiRead(Model):

    @classmethod
    def parse(kls, json):
        apiread = kls()
        for (key, value) in json.iteritems():
            if key == 'tumblelog':
                setattr(apiread, make_variable_name(key), TumbleLog.parse(value))
            elif key == 'posts':
                setattr(apiread, make_variable_name(key), [ Post.parse(p) for p in value ])
            else:
                setattr(apiread, make_variable_name(key), value)

        return apiread


class TumbleLog(Model):

    @classmethod
    def parse(kls, json):
        tumblelog = kls()
        for (key, value) in json.iteritems():
            setattr(tumblelog, make_variable_name(key), value)

        return tumblelog


class Post(Model):

    @classmethod
    def parse(kls, json):
        post = kls()
        for (key, value) in json.iteritems():
            if key == 'tumblelog':
                setattr(post, make_variable_name(key), TumbleLog.parse(value))
            else:
                setattr(post, make_variable_name(key), value)

        return post
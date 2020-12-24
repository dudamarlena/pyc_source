# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/core/inject.py
# Compiled at: 2015-12-21 17:12:58
config = None

class Inject(object):

    def __init__(self, *args):
        self.args = args

    @staticmethod
    def read_config(config):
        exec 'import ' + config + ' as conf'
        return conf

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            conf = self.read_config(config)
            for arg in self.args:
                conf_arg_name = arg.split(':')[0]
                property_name = arg.split(':')[(-1)]
                setattr(args[0], property_name, resolve_attr(conf, conf_arg_name, args))

            return f(*args, **kwargs)

        return wrapped_f


class InjectOptional(Inject):

    def __init__(self, *args):
        super(InjectOptional, self).__init__(*args)

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            try:
                conf = self.read_config(config)
                for arg in self.args:
                    conf_arg_name = arg.split(':')[0]
                    property_name = arg.split(':')[(-1)]
                    setattr(args[0], property_name, resolve_attr(conf, conf_arg_name, args))

            except:
                pass

            return f(*args, **kwargs)

        return wrapped_f


class InjectWithDefault(Inject):

    def __init__(self, *args):
        super(InjectWithDefault, self).__init__(*args)

    def __call__(self, f):

        def wrapped_f(*args, **kwargs):
            conf = self.read_config(config)
            for arg, default_value in self.args:
                conf_arg_name = arg.split(':')[0]
                property_name = arg.split(':')[(-1)]
                try:
                    attr = resolve_attr(conf, conf_arg_name, args)
                except:
                    attr = default_value

                setattr(args[0], property_name, attr)

            return f(*args, **kwargs)

        return wrapped_f


def resolve_attr(conf, conf_arg_name, args):
    try:
        return getattr(conf, args[0].address.split('.')[0] + '__' + conf_arg_name)()
    except:
        return getattr(conf, conf_arg_name)()
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/rstobj-project/rstobj/base.py
# Compiled at: 2018-12-02 17:44:02
# Size of source mod 2**32: 1616 bytes
import six, attr
from attrs_mate import AttrsClass
from .templates import env
from .option import Options

@attr.s
class RstObj(AttrsClass):
    meta_not_none_fields = tuple()

    def validate_not_none_fields(self):
        for field in self.meta_not_none_fields:
            if getattr(self, field) is None:
                msg = "`{}.{}` can't be None!".format(self.__class__.__name__, field)
                raise ValueError(msg)

    def __attrs_post_init__(self):
        self.validate_not_none_fields()

    @property
    def template_name(self):
        return '{}.{}.rst'.format(self.__module__, self.__class__.__name__)

    @property
    def template(self):
        return env.get_template(self.template_name)

    def render(self, indent=None, first_line_indent=None, **kwargs):
        out = self.template.render(obj=self)
        if indent:
            origin_lines = out.split('\n')
            target_lines = [Options.tab * indent + line.rstrip() for line in origin_lines]
            if first_line_indent is not None:
                if first_line_indent >= 0:
                    target_lines[0] = Options.tab * first_line_indent + origin_lines[0].rstrip()
                else:
                    raise TypeError
            out = '\n'.join(target_lines)
        return out

    @staticmethod
    def str_or_render(value, **kwargs):
        if isinstance(value, RstObj):
            return (value.render)(**kwargs)
        else:
            return six.text_type(value)
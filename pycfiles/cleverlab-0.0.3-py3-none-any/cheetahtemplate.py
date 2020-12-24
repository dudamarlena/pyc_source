# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/publishers/cheetahtemplate.py
# Compiled at: 2006-08-02 05:57:50
from Cheetah.Template import Template as CT
from harold.publishers.common import TemplateMixin, request_args

class CheetahTemplate(TemplateMixin):
    """ Instances read Cheetah templates and render them.

    """
    __module__ = __name__
    ext = '.tmpl'
    index = 'index.tmpl'

    class ref:
        __module__ = __name__
        src = 'non-empty string to supress warnings'
        module = CT(src)
        disallow = set(dir(module))

    def render(self, filename, args):
        """ After a template is located, the mixin calls this method
        to complete the rendering process.

        @param filename name of template module to import
        @param args sequence of additional items from the request
        @return rendered template
        """
        try:
            method_name = args.pop(0)
        except (IndexError,):
            method_name = ''

        def simple():
            context = self.context()()
            search = [dict(args=args, form=self.form(), context=context), context]
            template = CT(file=filename, searchList=search)
            return str(template)

        if not method_name:
            return simple()
        context = self.context()
        search = [dict(args=args, form=self.form(), context=context()), context()]
        template = CT(file=filename, searchList=search)
        view_names = set(dir(template)) - self.ref.disallow
        if method_name not in view_names:
            args.insert(0, method_name)
            return simple()
        call = getattr(template, method_name)
        (cargs, ckwds) = request_args(call, args, self.form(), context)
        return call(*cargs, **ckwds)
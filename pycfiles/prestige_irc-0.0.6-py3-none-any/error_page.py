# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/flask-pilot/pylot/component/views/error_page.py
# Compiled at: 2015-05-21 02:46:55
__doc__ = '\nError Page\n'
from pylot import Pylot

def error_page(template_dir=None):
    """
    Create the Error view
    Must be instantiated

    import error_view
    ErrorView = error_view()

    :param template_dir: The directory containing the view pages
    :return:
    """
    if not template_dir:
        template_dir = 'Pylot/Error'
    template_page = '%s/index.html' % template_dir

    class Error(Pylot):
        """
        Error Views
        """

        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            @app.errorhandler(400)
            def error_400(error):
                return cls.index(error, 400)

            @app.errorhandler(401)
            def error_401(error):
                return cls.index(error, 401)

            @app.errorhandler(403)
            def error_403(error):
                return cls.index(error, 403)

            @app.errorhandler(404)
            def error_404(error):
                return cls.index(error, 404)

            @app.errorhandler(500)
            def error_500(error):
                return cls.index(error, 500)

            @app.errorhandler(503)
            def error_503(error):
                return cls.index(error, 503)

        @classmethod
        def index(cls, error, code):
            cls.set_meta__(title='Error %s' % code)
            return (
             cls.render(error=error, view_template=template_page), code)

    return Error


ErrorV = error_page()
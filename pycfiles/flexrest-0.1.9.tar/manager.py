# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ali/work/my_projects/flexrest/flexrest/manager.py
# Compiled at: 2016-01-07 12:20:46


class FlexRestManager(object):
    common_decorators = {}

    def __init__(self, db_base, db_session_callback, strict_slash=False, app=None, common_decorators=None):
        self.db_session_callback = db_session_callback
        self.db_base = db_base
        self.strict_slash = strict_slash
        FlexRestManager.common_decorators = common_decorators or []
        if app is not None:
            self.init_app(app)
        return

    def init_app(self, app):
        """
        Configures an application. This registers an `after_request` call, and
        attaches this `LoginManager` to it as `app.login_manager`.

        :param app: The :class:`flask.Flask` object to configure.
        :type app: :class:`flask.Flask`
        :param add_context_processor: Whether to add a context processor to
            the app that adds a `current_user` variable to the template.
            Defaults to ``True``.
        :type add_context_processor: bool
        """
        app.flexrest_manager = self
        app.url_map.strict_slashes = self.strict_slash
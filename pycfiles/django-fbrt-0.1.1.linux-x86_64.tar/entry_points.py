# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/fbrt/entry_points.py
# Compiled at: 2014-09-07 19:09:34
from django.conf.urls import url
from django.core.exceptions import ImproperlyConfigured
from fandjango.decorators import facebook_authorization_required as fb_auth
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.http import urlencode
from functools import wraps
from response import *
from messaging import *
from django_websocket.decorators import websocket

def fb_auth_ajax(view, permissions):

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        response = JSONResponse({'errors': 'Must fully authorize the application'}, status=403)
        if request.facebook and request.facebook.user and permissions and [ p for p in permissions if p not in request.facebook.user.permissions ]:
            return response
        if not request.facebook or not request.facebook.user:
            return response
        return view(request, *args, **kwargs)

    return wrapper


class CookieSafeFBEntryPointError(Exception):
    pass


class CookieSafeFBEntryPoint(object):

    def __init__(self, base_path, page='', permissions=[]):
        """
        Crea un punto de entrada para una aplicacion de
        Facebook. Por ahora bancamos puntos de entrada de
        aplicacion o de tab. despues vemos de bancar mas.
 
        :param page:
        :param permissions:
        :param base_path: path base (en django) que sirve todo
            este entry point
        :return:
        """
        if not page:
            self.istab = False
            self.baseurl = 'http://apps.facebook.com/%s/' % settings.FACEBOOK_APPLICATION_NAMESPACE
        else:
            self.istab = True
            self.baseurl = 'https://www.facebook.com/%s/app_%s' % (page, settings.FACEBOOK_APPLICATION_ID)
        self.permissions = permissions
        self.base_path = base_path

    def _make_facebook_url(self, request):
        """
        Devuelve una url transformada a la
        correspondiente url de facebook.
        """
        path = request.path
        base_path = self.base_path.rstrip('/')
        if not path.startswith(base_path):
            raise CookieSafeFBEntryPointError('URL %s is not child of %s' % (path, self.base_path))
        if not self.istab:
            return self.baseurl.rstrip('/') + path[len(base_path):]
        return self.baseurl

    @staticmethod
    def firsthand_cookie_view(request):
        """
        Crea la cookie de primera mano para
        que luego pueda ser editada.
        """
        response = HttpResponse(content='\n<html>\n    <body>\n        <script type="text/javascript">\n            window.top.location.href = %s;\n        </script>\n    </body>\n</html>\n' % json.dumps(request.GET.get('back', 'http://www.facebook.com')))
        response.set_cookie(getattr(settings, 'FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_NAME', 'safari_sucks'), True)
        return response

    @staticmethod
    def firsthand_cookie_url(pattern):
        """
        Crea la entrada de URL para la url de la vista que pone la cookie inicial.
        """
        return url(pattern, CookieSafeFBEntryPoint.firsthand_cookie_view, name=settings.FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_URL)

    def fb_entry_point(self):
        """
        Genera dinamicamente un decorador que, tomando la vista, arma
        una vista decorada por el facebook_authorization_required con
        los parametros seleccionados desde los atributos de esta clase.
        :param args:
        :param kwargs:
        :return:
        """

        def _is_firsthand_cookie(view):

            def wrapped(request, *args, **kwargs):
                if not request.COOKIES.get(getattr(settings, 'FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_NAME', 'safari_sucks'), False):
                    target = settings.FANDJANGO_SITE_URL.rstrip('/') + resolve_url(settings.FACEBOOK_ENTRYPOINT_PUT_1ST_COOKIE_URL)
                    current = self._make_facebook_url(request)
                    template = '\n<html>\n    <body>\n        <script type="text/javascript">\n            window.top.location.href = %s;\n        </script>\n    </body>\n</html>\n' % json.dumps(target + '?' + urlencode({'back': current}))
                    return HttpResponse(content=template)
                else:
                    return view(request, *args, **kwargs)

            return wrapped

        def decorator(view):
            return wraps(view)(fb_auth(redirect_uri=self.baseurl, permissions=self.permissions)(_is_firsthand_cookie(view)))

        return decorator

    def fb_ajax_entry_point(self):
        """
        Es igual a fb_entry_point PERO con json/ajax. La otra diferencia es que
        esta no puede llenar cookies, ya que es solamente json.
        :param args:
        :param kwargs:
        :return:
        """
        return lambda view: fb_auth_ajax(view, self.permissions)

    def fb_websocket_entry_point(self):
        """
        Es igual a fb_entry_point PERO con websockets. La otra diferencia es que
        esta no puede llenar cookies, ya que es una peticion websockets.
        """
        permissions = self.permissions

        def decorator(view):

            @websocket
            def wrapped(request, ws, *args, **kwargs):
                if request.facebook and request.facebook.user and permissions and [ p for p in permissions if p not in request.facebook.user.permissions ]:
                    ws.close(4003, 'You must fully authorize the application')
                if not request.facebook or not request.facebook.user:
                    ws.close(4003, 'You must fully authorize the application')
                view(request, ws, *args, **kwargs)

            return wrapped

        return decorator

    def authorized_url(self, pattern, view, name=None, kwargs={}, urltype='normal'):
        """
        Crea la entrada de URL para esta vista en particular.
        """
        trimmed_bp = self.base_path.strip('/')
        trimmed_pt = pattern.lstrip('^/')
        if urltype == 'ajax':
            decorator = self.fb_ajax_entry_point()
        elif urltype == 'websocket':
            decorator = self.fb_websocket_entry_point()
        elif urltype == 'normal':
            decorator = self.fb_entry_point()
        else:
            raise ImproperlyConfigured('Entry points can either be normal, ajax, or websocket points')
        return url('^%s/%s' % (trimmed_bp, trimmed_pt), decorator(view), kwargs, name)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/jwql_proj/urls.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 1906 bytes
"""Maps URL paths to views in the ``jwql`` project.

This module connects requested URL paths to the corresponding view in
``views.py`` for each webpage in the JWQL application. When Django is
provided a path, it searches through the urlpatterns list provided
here until it finds one that matches. It then calls the assigned view
to load the appropriate webpage, passing an HttpRequest object.

Authors
-------

    - Lauren Chambers

Use
---

    Function views
        1. Add an import:
            from my_app import views
        2. Add a URL to urlpatterns:
            path('', views.home, name='home')
    Class-based views
        1. Add an import:
            from other_app.views import Home
        2. Add a URL to urlpatterns:
            path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function:
            from django.urls import include, path
        2. Add a URL to urlpatterns:
            path('blog/', include('blog.urls'))

References
----------

    For more information please see:
        ``https://docs.djangoproject.com/en/2.0/topics/http/urls/``

Notes
-----

    Be aware that when a url is requested, it will be directed to the
    first matching path in the ``urlpatterns`` list that it finds. The
    ``<str:var>`` tag is just a placeholder. To avoid complications,
    users should order their paths in order from shortest to longest,
    and after that from most to least specific.
"""
from django.contrib import admin
from django.urls import include, path
from ..apps.jwql import views
handler404 = views.not_found
handler500 = views.not_found
handler403 = views.not_found
handler400 = views.not_found
urlpatterns = [
 path('', include('jwql.website.apps.jwql.urls')),
 path('admin/', admin.site.urls)]
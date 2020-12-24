# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/tests/urls.py
from rest_framework import routers
from .views import WeatherStationViewSet
from .views import TemperatureRecordViewSet

class ClimateAPI(routers.APIRootView):
    __doc__ = '\n    Example API KNMI climate data.\n\n    Note: this is used for testing drf_amsterdam project.\n    '

    def get_api_root_view(self, **kwargs):
        view = (super().get_api_root_view)(**kwargs)
        cls = view.cls

        class Climate(cls):

            def get_view_name(self):
                return 'Example API KNMI climate data'

        Climate.__doc__ = self.__doc__
        return Climate.as_view()


class ApiRouter(routers.DefaultRouter):
    __doc__ = 'The main router'
    APIRootView = ClimateAPI


router = ApiRouter()
router.register('weatherstation', WeatherStationViewSet)
router.register('temperature_record', TemperatureRecordViewSet)
urlpatterns = router.urls
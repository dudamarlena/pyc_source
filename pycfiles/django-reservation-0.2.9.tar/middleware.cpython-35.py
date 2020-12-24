# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/middleware.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 846 bytes
"""
Free as freedom will be 2/9/2016

@author: luisza
"""
from __future__ import unicode_literals
from djreservation.models import Reservation

class ReservationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.COOKIES.get('reservation'):
            try:
                reservation = Reservation.objects.get(pk=request.COOKIES.get('reservation'))
                setattr(request, 'reservation', reservation)
            except:
                pass

            response = self.get_response(request)
            return response
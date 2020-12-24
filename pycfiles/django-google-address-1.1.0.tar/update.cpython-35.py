# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/update.py
# Compiled at: 2017-05-03 17:07:44
# Size of source mod 2**32: 1138 bytes
import threading
from google_address.api import GoogleAddressApi
from google_address.models import Address, AddressComponent

def update_address(instance):
    response = GoogleAddressApi().query(instance.raw)
    if len(response['results']) > 0:
        result = response['results'][0]
    else:
        return False
    instance.address_components.clear()
    for api_component in result['address_components']:
        component = AddressComponent.get_or_create_component(api_component)
        instance.address_components.add(component)

    try:
        if result['geometry']:
            Address.objects.filter(pk=instance.pk).update(lat=result['geometry']['location']['lat'], lng=result['geometry']['location']['lng'])
    except:
        pass

    instance.address_line = instance.get_address()
    Address.objects.filter(pk=instance.pk).update(address_line=instance.address_line, city_state=instance.get_city_state())


class UpdateThread(threading.Thread):

    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run(self):
        return update_address(self.instance)
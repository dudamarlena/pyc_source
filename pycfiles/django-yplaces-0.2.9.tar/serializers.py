# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andretavares/Dev/AptanaStudio3Workspace/restauranteur/yplaces/api/serializers.py
# Compiled at: 2014-03-07 13:30:59
import logging
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from yapi.serializers import BaseSerializer
logger = logging.getLogger(__name__)

class PlaceSerializer(BaseSerializer):
    """
    Adds methods required for instance serialization.
    """

    def to_simple(self, obj, user=None):
        """
        Please refer to the interface documentation.
        """
        simple = {'id': obj.pk, 
           'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:id', args=[obj.pk]), 
           'name': obj.name, 
           'slug': slugify(obj.name), 
           'address': obj.address, 
           'postal_code': obj.postal_code, 
           'city': obj.city, 
           'state': obj.state, 
           'country': obj.country, 
           'latitude': obj.latitude, 
           'longitude': obj.longitude, 
           'email': obj.email, 
           'phone_number': obj.phone_number, 
           'website': obj.website, 
           'description': obj.description, 
           'photos': {'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:photos', args=[obj.pk])}, 
           'reviews': {'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:reviews', args=[obj.pk])}, 
           'rating': obj.get_rating_value(), 
           'profile_image_url': settings.HOST_URL + settings.STATIC_URL + 'yplaces/images/default_place_picture.png', 
           'marker_image_url': obj.get_marker_image_url()}
        if user and user.is_staff:
            simple.update({'created_at': obj.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
               'created_by': {'email': obj.created_by.email}, 
               'active': obj.active})
        return simple


class PhotoSerializer(BaseSerializer):
    """
    Adds methods required for instance serialization.
    """

    def to_simple(self, obj, user=None):
        """
        Please refer to the interface documentation.
        """
        simple = {'id': obj.pk, 
           'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:photo_id', args=[obj.place.pk, obj.pk]), 
           'image_url': obj.file.url, 
           'added_by': {'name': obj.added_by.name, 
                        'photo_url': obj.added_by.get_photo_url()}, 
           'added_at': obj.added_at.strftime('%Y-%m-%d %H:%M:%S')}
        return simple


class ReviewSerializer(BaseSerializer):
    """
    Adds methods required for instance serialization.
    """

    def to_simple(self, obj, user=None):
        """
        Please refer to the interface documentation.
        """
        simple = {'id': obj.pk, 
           'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:review_id', args=[obj.place.pk, obj.pk]), 
           'user': {'name': obj.user.name, 
                    'photo_url': obj.user.get_photo_url()}, 
           'date': obj.date.strftime('%Y-%m-%d %H:%M:%S'), 
           'rating': obj.rating, 
           'comment': obj.comment, 
           'photo': None, 
           'place': {'name': obj.place.name, 
                     'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:id', args=[obj.place.pk]), 
                     'rating': {'average': 0, 'reviews': 0}}}
        if obj.photo:
            simple['photo'] = {'id': obj.photo.pk, 'url': settings.HOST_URL + reverse(settings.YPLACES['api_url_namespace'] + ':yplaces:photo_id', args=[obj.place.pk, obj.photo.pk]), 
               'image_url': obj.photo.file.url}
        rating = obj.place.get_rating()
        if rating:
            simple['place']['rating'] = {'average': rating.average, 'reviews': rating.reviews}
        return simple
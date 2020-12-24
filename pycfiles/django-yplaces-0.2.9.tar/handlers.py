# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andretavares/Dev/AptanaStudio3Workspace/francesinhas3/yplaces/api/handlers.py
# Compiled at: 2014-05-19 18:57:48
import logging
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseForbidden
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from yapi.authentication import ApiKeyAuthentication, SessionAuthentication
from yapi.decorators import authentication_classes, permission_classes
from yapi.permissions import IsStaff
from yapi.resource import Resource
from yapi.response import HTTPStatus, Response
from yutils.email import EmailMessage
from serializers import PlaceSerializer, PhotoSerializer, ReviewSerializer
from yplaces.forms import PlaceForm, PhotoForm, ReviewForm
from yplaces.models import Place, Photo, Review
logger = logging.getLogger(__name__)

class PlacesHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'POST', 'GET']

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    def post(self, request):
        """
        Process POST request.
        """
        request.data['created_by'] = request.auth['user'].pk
        form = PlaceForm(request.data)
        try:
            new_instance = form.save()
            if not request.auth['user'].is_staff:
                try:
                    d = Context({'place': new_instance, 'host_url': settings.HOST_URL})
                    plaintext = get_template('yplaces/email/place_added.txt')
                    text_content = plaintext.render(d)
                    html = get_template('yplaces/email/place_added.html')
                    html_content = html.render(d)
                    subject = _('Place Added')
                    from_email = settings.YPLACES['email_from']
                    to = settings.YPLACES['admin_emails']
                    email = EmailMessage(sender=from_email, recipients=to, subject=subject, text_content=text_content, html_content=html_content, tags=[
                     'Place Added'])
                    result = email.send()
                    if not result['sent']:
                        logger.warning('Email Not Sent! Result: ' + str(result['result']))
                        raise
                except:
                    logger.warning('Unable to send email', exc_info=1)

            return Response(request=request, data=new_instance, serializer=PlaceSerializer, status=HTTPStatus.SUCCESS_201_CREATED)
        except ValueError:
            return Response(request=request, data={'message': 'Invalid parameters', 'parameters': form.errors}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

        return

    def get(self, request):
        """
        Process GET request.
        """
        results = Place.objects.all()
        filters = {}
        if not request.user or not request.user.is_staff:
            results = results.filter(active=True)
        else:
            if request.user and request.user.is_staff:
                try:
                    active = request.GET['active']
                    if active != '':
                        [
                         'true', 'false'].index(active)
                        active = active.lower() == 'true'
                        results = results.filter(active=active)
                        filters['active'] = active
                except KeyError:
                    pass
                except ValueError:
                    return Response(request=request, data={'message': 'Invalid parameters', 'parameters': {'active': ['Invalid value']}}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

            try:
                pagination = request.GET['pagination']
                ['true', 'false'].index(pagination)
                pagination = pagination.lower() == 'true'
            except KeyError:
                pagination = True
            except ValueError:
                return Response(request=request, data={'message': 'Invalid parameters', 'parameters': {'pagination': ['Invalid value']}}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

            latLng = request.GET.get('latLng', None)
            if latLng:
                try:
                    latLng = [ float(i) for i in latLng.split(',') ]
                    if len(latLng) != 2:
                        raise ValueError
                    latLng = (
                     latLng[0], latLng[1])
                except ValueError:
                    return Response(request=request, data={'message': 'Invalid parameters', 'parameters': {'latLng': ['Invalid value']}}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

                radius = request.GET.get('radius', 0.5)
                try:
                    radius = float(radius)
                except ValueError:
                    return Response(request=request, data={'message': 'Invalid parameters', 'parameters': {'radius': ['Invalid value']}}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

                filters['latLng'] = request.GET.get('latLng', None)
                filters['radius'] = radius
                results = Place.search_radius(latLng=latLng, radius=radius, querySet=results)
            try:
                name = request.GET['name']
                if name != '':
                    results = results.filter(Q(name__icontains=name))
                    filters['name'] = name
            except KeyError:
                pass

            try:
                location = request.GET['location']
                results = results.filter(Q(address__icontains=location) | Q(city__icontains=location) | Q(state__icontains=location) | Q(country__icontains=location))
            except KeyError:
                location = ''

        return Response(request=request, data=results, filters=filters, serializer=PlaceSerializer, pagination=pagination, status=HTTPStatus.SUCCESS_200_OK)


class PlaceIdHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'GET', 'PUT']

    def get(self, request, pk):
        """
        Process GET request.
        """
        try:
            instance = Place.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not instance.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        return Response(request=request, data=instance, serializer=PlaceSerializer, status=HTTPStatus.SUCCESS_200_OK)

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    @permission_classes([IsStaff])
    def put(self, request, pk):
        """
        Process PUT request.
        """
        try:
            instance = Place.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        request.data['created_by'] = instance.created_by.pk
        form = PlaceForm(request.data, instance=instance)
        try:
            form.save()
            return Response(request=request, data=instance, serializer=PlaceSerializer, status=HTTPStatus.SUCCESS_200_OK)
        except ValueError:
            return Response(request=request, data={'message': 'Invalid parameters', 'parameters': form.errors}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

        return


class PhotosHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'POST', 'GET']

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    def post(self, request, pk):
        """
        Process POST request.
        """
        try:
            place = Place.objects.get(pk=pk, active=True)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        request.data['added_by'] = request.auth['user'].pk
        request.data['place'] = place.pk
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                photo = Photo.new(place=place, photo_file=form.cleaned_data['file'], user=request.auth['user'])
            except IOError:
                return Response(request=request, data={'message': 'Error uploading place photo #1'}, serializer=None, status=HTTPStatus.SERVER_ERROR_500_INTERNAL_SERVER_ERROR)

            return Response(request=request, data=photo, serializer=PhotoSerializer, status=HTTPStatus.SUCCESS_201_CREATED)
        else:
            return Response(request=request, data={'message': 'Invalid parameters', 'parameters': form.errors}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)
            return

    def get(self, request, pk):
        """
        Process GET request.
        """
        try:
            place = Place.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not place.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        results = place.photo_set.all()
        return Response(request=request, data=results, serializer=PhotoSerializer, status=HTTPStatus.SUCCESS_200_OK)


class PhotoIdHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'GET', 'DELETE']

    def get(self, request, pk, photo_pk):
        """
        Process GET request.
        """
        try:
            place = Place.objects.get(pk=pk)
            instance = Photo.objects.get(pk=photo_pk, place=place)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not place.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        return Response(request=request, data=instance, serializer=PhotoSerializer, status=HTTPStatus.SUCCESS_200_OK)

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    @permission_classes([IsStaff])
    def delete(self, request, pk, photo_pk):
        """
        Process DELETE request.
        """
        try:
            place = Place.objects.get(pk=pk)
            instance = Photo.objects.get(pk=photo_pk, place=place)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        instance.destroy()
        return HttpResponse(status=HTTPStatus.SUCCESS_204_NO_CONTENT)


class ReviewsHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'POST', 'GET']

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    def post(self, request, pk):
        """
        Process POST request.
        """
        try:
            place = Place.objects.get(pk=pk, active=True)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if len(request.FILES) == 0:
            request.data['user'] = request.auth['user'].pk
            request.data['place'] = place.pk
            form = ReviewForm(request.data)
            try:
                new_instance = form.save()
                return Response(request=request, data=new_instance, serializer=ReviewSerializer, status=HTTPStatus.SUCCESS_201_CREATED)
            except ValueError:
                return Response(request=request, data={'message': 'Invalid parameters', 'parameters': form.errors}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)

        else:
            request.POST['user'] = request.auth['user'].pk
            request.POST['place'] = place.pk
            review_form = ReviewForm(request.POST)
            photo_form = PhotoForm(request.POST, request.FILES)
            if review_form.is_valid() and photo_form.is_valid():
                try:
                    photo = Photo.new(place=place, photo_file=photo_form.cleaned_data['file'], user=request.auth['user'])
                    review = review_form.save()
                    review.photo = photo
                    review.save()
                    return Response(request=request, data=review, serializer=ReviewSerializer, status=HTTPStatus.SUCCESS_201_CREATED)
                except IOError:
                    return Response(request=request, data={'message': 'Error creating review #1'}, serializer=None, status=HTTPStatus.SERVER_ERROR_500_INTERNAL_SERVER_ERROR)

            else:
                return Response(request=request, data={'message': 'Invalid parameters', 'parameters': review_form.errors}, serializer=None, status=HTTPStatus.CLIENT_ERROR_400_BAD_REQUEST)
        return

    def get(self, request, pk):
        """
        Process GET request.
        """
        try:
            place = Place.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not place.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        results = place.review_set.all()
        return Response(request=request, data=results, serializer=ReviewSerializer, status=HTTPStatus.SUCCESS_200_OK)


class ReviewIdHandler(Resource):
    """
    API endpoint handler.
    """
    allowed_methods = [
     'GET', 'DELETE']

    def get(self, request, pk, review_pk):
        """
        Process GET request.
        """
        try:
            place = Place.objects.get(pk=pk)
            instance = Review.objects.get(pk=review_pk, place=place)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not place.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        return Response(request=request, data=instance, serializer=ReviewSerializer, status=HTTPStatus.SUCCESS_200_OK)

    @authentication_classes([SessionAuthentication, ApiKeyAuthentication])
    def delete(self, request, pk, review_pk):
        """
        Process DELETE request.
        """
        try:
            place = Place.objects.get(pk=pk)
            instance = Review.objects.get(pk=review_pk, place=place)
        except ObjectDoesNotExist:
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)

        if not place.active and (not request.user or not request.user.is_staff):
            return HttpResponse(status=HTTPStatus.CLIENT_ERROR_404_NOT_FOUND)
        else:
            if instance.user != request.auth['user']:
                return HttpResponseForbidden()
            instance.destroy()
            return HttpResponse(status=HTTPStatus.SUCCESS_204_NO_CONTENT)
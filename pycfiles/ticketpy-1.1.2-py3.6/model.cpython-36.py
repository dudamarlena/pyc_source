# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ticketpy\model.py
# Compiled at: 2017-10-21 19:19:19
# Size of source mod 2**32: 17452 bytes
"""Models for API objects"""
from datetime import datetime
import re, ticketpy

def _assign_links(obj, json_obj, base_url=None):
    """Assigns ``links`` attribute to an object from JSON"""
    json_links = json_obj.get('_links')
    if not json_links:
        obj.links = {}
    else:
        obj_links = {}
        for k, v in json_links.items():
            if 'href' in v:
                href = re.sub('({.+})', '', v['href'])
                if base_url:
                    href = '{}{}'.format(base_url, href)
                obj_links[k] = href
            else:
                obj_links[k] = v

        obj.links = obj_links


class Page(list):
    __doc__ = 'API response page'

    def __init__(self, number=None, size=None, total_elements=None, total_pages=None):
        super().__init__([])
        self.number = number
        self.size = size
        self.total_elements = total_elements
        self.total_pages = total_pages

    @staticmethod
    def from_json(json_obj):
        """Instantiate and return a Page(list)"""
        pg = Page()
        pg.json = json_obj
        _assign_links(pg, json_obj, ticketpy.ApiClient.root_url)
        pg.number = json_obj['page']['number']
        pg.size = json_obj['page']['size']
        pg.total_pages = json_obj['page']['totalPages']
        pg.total_elements = json_obj['page']['totalElements']
        embedded = json_obj.get('_embedded')
        if not embedded:
            return pg
        else:
            object_models = {'events':Event, 
             'venues':Venue, 
             'attractions':Attraction, 
             'classifications':Classification}
            for k, v in embedded.items():
                if k in object_models:
                    obj_type = object_models[k]
                    pg += [obj_type.from_json(obj) for obj in v]

            return pg

    def __str__(self):
        return ('Page {number}/{total_pages}, Size: {size}, Total elements: {total_elements}'.format)(**self.__dict__)


class Event:
    __doc__ = 'Ticketmaster event\n\n    The JSON returned from the Discovery API (at least, as far as \n    what\'s being used here) looks like:\n\n    .. code-block:: json\n\n        {\n            "name": "Event name",\n            "dates": {\n                "start": {\n                    "localDate": "2019-04-01",\n                    "localTime": "2019-04-01T23:00:00Z"\n                },\n                "status": {\n                    "code": "onsale"\n                }\n            },\n            "classifications": [\n                {\n                    "genre": {\n                        "name": "Rock"\n                    }\n                },\n                {\n                    "genre": {\n                        "name": "Funk"\n                    }\n                }\n            ],\n            "priceRanges": [\n                {\n                    "min": 10,\n                    "max": 25\n                }\n            ],\n            "_embedded": {\n                "venues": [\n                    {\n                        "name": "The Tabernacle"\n                    }\n                ]\n            }\n        }\n    '

    def __init__(self, event_id=None, name=None, start_date=None, start_time=None, status=None, price_ranges=None, venues=None, utc_datetime=None, classifications=None, links=None):
        self.id = event_id
        self.name = name
        self.local_start_date = start_date
        self.local_start_time = start_time
        self.status = status
        self.classifications = classifications
        self.price_ranges = price_ranges
        self.venues = venues
        self.links = links
        self._Event__utc_datetime = None
        if utc_datetime is not None:
            self.utc_datetime = utc_datetime

    @property
    def utc_datetime(self):
        """Start date/time in UTC (*YYYY-MM-DDTHH:MM:SSZ*)"""
        return self._Event__utc_datetime

    @utc_datetime.setter
    def utc_datetime(self, utc_datetime):
        if not utc_datetime:
            self._Event__utc_datetime = None
        else:
            ts_format = '%Y-%m-%dT%H:%M:%SZ'
            self._Event__utc_datetime = datetime.strptime(utc_datetime, ts_format)

    @staticmethod
    def from_json(json_event):
        """Creates an ``Event`` from API's JSON response"""
        e = Event()
        e.json = json_event
        e.id = json_event.get('id')
        e.name = json_event.get('name')
        dates = json_event.get('dates', {})
        start_dates = dates.get('start', {})
        e.local_start_date = start_dates.get('localDate')
        e.local_start_time = start_dates.get('localTime')
        e.utc_datetime = start_dates.get('dateTime')
        status = dates.get('status', {})
        e.status = status.get('code')
        if 'classifications' in json_event:
            e.classifications = [EventClassification.from_json(cl) for cl in json_event['classifications']]
        price_ranges = []
        if 'priceRanges' in json_event:
            for pr in json_event['priceRanges']:
                price_ranges.append({'min':pr['min'],  'max':pr['max']})

        e.price_ranges = price_ranges
        venues = []
        if 'venues' in json_event.get('_embedded', {}):
            for v in json_event['_embedded']['venues']:
                venues.append(Venue.from_json(v))

        e.venues = venues
        _assign_links(e, json_event)
        return e

    def __str__(self):
        tmpl = 'Event:            {name}\nVenues:           {venues}\nStart date:       {local_start_date}\nStart time:       {local_start_time}\nPrice ranges:     {price_ranges}\nStatus:           {status}\nClassifications:  {classifications!s}\n'
        return (tmpl.format)(**self.__dict__)


class Venue:
    __doc__ = 'A Ticketmaster venue\n    \n    The JSON returned from the Discovery API looks something like this \n    (*edited for brevity*):\n    \n    .. code-block:: json\n    \n        {\n            "id": "KovZpaFEZe",\n            "name": "The Tabernacle",\n            "url": "http://www.ticketmaster.com/venue/115031",\n            "timezone": "America/New_York",\n            "address": {\n                "line1": "152 Luckie Street"\n            },\n            "city": {\n                "name": "Atlanta"\n            },\n            "postalCode": "30303",\n            "state": {\n                "stateCode": "GA",\n                "name": "Georgia"\n            },\n            "country": {\n                "name": "United States Of America",\n                "countryCode": "US"\n            },\n            "location": {\n                "latitude": "33.758688",\n                "longitude": "-84.391449"\n            },\n            "social": {\n                "twitter": {\n                    "handle": "@TabernacleATL"\n                }\n            },\n            "markets": [\n                {\n                    "id": "10"\n                }\n            ]\n        }\n\n    \n    '

    def __init__(self, name=None, address=None, city=None, state_code=None, postal_code=None, latitude=None, longitude=None, markets=None, url=None, box_office_info=None, dmas=None, general_info=None, venue_id=None, social=None, timezone=None, images=None, parking_detail=None, accessible_seating_detail=None, links=None):
        self.name = name
        self.id = venue_id
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.state_code = state_code
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.url = url
        self.box_office_info = box_office_info
        self.dmas = dmas
        self.markets = markets
        self.general_info = general_info
        self.social = social
        self.images = images
        self.parking_detail = parking_detail
        self.accessible_seating_detail = accessible_seating_detail
        self.links = links

    @property
    def location(self):
        """Location-based data (full address, lat/lon, timezone"""
        return {'address':self.address, 
         'postal_code':self.postal_code, 
         'city':self.city, 
         'state_code':self.state_code, 
         'timezone':self.timezone, 
         'latitude':self.latitude, 
         'longitude':self.longitude}

    @staticmethod
    def from_json(json_venue):
        """Returns a ``Venue`` object from JSON"""
        v = Venue()
        v.json = json_venue
        v.id = json_venue.get('id')
        v.name = json_venue.get('name')
        v.url = json_venue.get('url')
        v.postal_code = json_venue.get('postalCode')
        v.general_info = json_venue.get('generalInfo')
        v.box_office_info = json_venue.get('boxOfficeInfo')
        v.dmas = json_venue.get('dmas')
        v.social = json_venue.get('social')
        v.timezone = json_venue.get('timezone')
        v.images = json_venue.get('images')
        v.parking_detail = json_venue.get('parkingDetail')
        v.accessible_seating_detail = json_venue.get('accessibleSeatingDetail')
        if 'markets' in json_venue:
            v.markets = [m.get('id') for m in json_venue.get('markets')]
        if 'city' in json_venue:
            v.city = json_venue['city'].get('name')
        if 'address' in json_venue:
            v.address = json_venue['address'].get('line1')
        if 'location' in json_venue:
            v.latitude = json_venue['location'].get('latitude')
            v.longitude = json_venue['location'].get('longitude')
        if 'state' in json_venue:
            v.state_code = json_venue['state'].get('stateCode')
        _assign_links(v, json_venue)
        return v

    def __str__(self):
        return ('{name} at {address} in {city} {state_code}'.format)(**self.__dict__)


class Attraction:
    """Attraction"""

    def __init__(self, attraction_id=None, attraction_name=None, url=None, classifications=None, images=None, test=None, links=None):
        self.id = attraction_id
        self.name = attraction_name
        self.url = url
        self.classifications = classifications
        self.images = images
        self.test = test
        self.links = links

    @staticmethod
    def from_json(json_obj):
        """Convert JSON object to ``Attraction`` object"""
        att = Attraction()
        att.json = json_obj
        att.id = json_obj.get('id')
        att.name = json_obj.get('name')
        att.url = json_obj.get('url')
        att.test = json_obj.get('test')
        att.images = json_obj.get('images')
        classifications = json_obj.get('classifications')
        att.classifications = [Classification.from_json(cl) for cl in classifications]
        _assign_links(att, json_obj)
        return att

    def __str__(self):
        if self.name is not None:
            return str(self.name)
        else:
            return 'Unknown'


class Classification:
    __doc__ = 'Classification object (segment/genre/sub-genre)\n    \n    For the structure returned by ``EventSearch``, see ``EventClassification``\n    '

    def __init__(self, segment=None, classification_type=None, subtype=None, primary=None, links=None):
        self.segment = segment
        self.type = classification_type
        self.subtype = subtype
        self.primary = primary
        self.links = links

    @staticmethod
    def from_json(json_obj):
        """Create/return ``Classification`` object from JSON"""
        cl = Classification()
        cl.json = json_obj
        cl.primary = json_obj.get('primary')
        if 'segment' in json_obj:
            cl.segment = Segment.from_json(json_obj['segment'])
        if 'type' in json_obj:
            cl_t = json_obj['type']
            cl.type = ClassificationType(cl_t['id'], cl_t['name'])
        if 'subType' in json_obj:
            cl_st = json_obj['subType']
            cl.subtype = ClassificationSubType(cl_st['id'], cl_st['name'])
        _assign_links(cl, json_obj)
        return cl

    def __str__(self):
        return str(self.type)


class EventClassification:
    __doc__ = "Classification as it's represented in event search results\n\n    See ``Classification()`` for results from classification searches\n    "

    def __init__(self, genre=None, subgenre=None, segment=None, classification_type=None, classification_subtype=None, primary=None, links=None):
        self.genre = genre
        self.subgenre = subgenre
        self.segment = segment
        self.type = classification_type
        self.subtype = classification_subtype
        self.primary = primary
        self.links = links

    @staticmethod
    def from_json(json_obj):
        """Create/return ``EventClassification`` object from JSON"""
        ec = EventClassification()
        ec.json = json_obj
        ec.primary = json_obj.get('primary')
        segment = json_obj.get('segment')
        if segment:
            ec.segment = Segment.from_json(segment)
        genre = json_obj.get('genre')
        if genre:
            ec.genre = Genre.from_json(genre)
        subgenre = json_obj.get('subGenre')
        if subgenre:
            ec.subgenre = SubGenre.from_json(subgenre)
        cl_t = json_obj.get('type')
        if cl_t:
            ec.type = ClassificationType(cl_t['id'], cl_t['name'])
        cl_st = json_obj.get('subType')
        if cl_st:
            ec.subtype = ClassificationSubType(cl_st['id'], cl_st['name'])
        _assign_links(ec, json_obj)
        return ec

    def __str__(self):
        return ('Segment: {segment} / Genre: {genre} / Subgenre: {subgenre} / Type: {type} / Subtype: {subtype}'.format)(**self.__dict__)


class ClassificationType:

    def __init__(self, type_id=None, type_name=None, subtypes=None):
        self.id = type_id
        self.name = type_name
        self.subtypes = subtypes

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'Unknown'


class ClassificationSubType:

    def __init__(self, type_id=None, type_name=None):
        self.id = type_id
        self.name = type_name

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'Unknown'


class Segment:

    def __init__(self, segment_id=None, segment_name=None, genres=None, links=None):
        self.id = segment_id
        self.name = segment_name
        self.genres = genres
        self.links = links

    @staticmethod
    def from_json(json_obj):
        """Create and return a ``Segment`` from JSON"""
        seg = Segment()
        seg.json = json_obj
        seg.id = json_obj['id']
        seg.name = json_obj.get('name')
        if '_embedded' in json_obj:
            genres = json_obj['_embedded']['genres']
            seg.genres = [Genre.from_json(g) for g in genres]
        _assign_links(seg, json_obj)
        return seg

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'Unknown'


class Genre:

    def __init__(self, genre_id=None, genre_name=None, subgenres=None, links=None):
        self.id = genre_id
        self.name = genre_name
        self.subgenres = subgenres
        self.links = links

    @staticmethod
    def from_json(json_obj):
        g = Genre()
        g.json = json_obj
        g.id = json_obj.get('id')
        g.name = json_obj.get('name')
        if '_embedded' in json_obj:
            embedded = json_obj['_embedded']
            subgenres = embedded['subgenres']
            g.subgenres = [SubGenre.from_json(sg) for sg in subgenres]
        _assign_links(g, json_obj)
        return g

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'Unknown'


class SubGenre:

    def __init__(self, subgenre_id=None, subgenre_name=None, links=None):
        self.id = subgenre_id
        self.name = subgenre_name
        self.links = links

    @staticmethod
    def from_json(json_obj):
        sg = SubGenre()
        sg.json = json_obj
        sg.id = json_obj['id']
        sg.name = json_obj['name']
        _assign_links(sg, json_obj)
        return sg

    def __str__(self):
        if self.name is not None:
            return self.name
        else:
            return 'Unknown'
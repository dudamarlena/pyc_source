# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/facilities.py
# Compiled at: 2020-04-30 08:35:11
# Size of source mod 2**32: 9882 bytes
import json, operator, sys, logging, requests
from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from dateutil.parser import parse
from tom_observations.facility import get_service_class
from tom_observations.facilities.lco import LCOFacility, LCOImagingObservationForm, make_request, PORTAL_URL
try:
    AUTO_THUMBNAILS = settings.AUTO_THUMBNAILS
except AttributeError:
    AUTO_THUMBNAILS = False

logger = logging.getLogger(__name__)

class EducationLCOForm(LCOImagingObservationForm):
    EXPOSURE_FIELDS = {'exposure_count':(
      forms.IntegerField, {'min_value': 1}), 
     'exposure_time':(
      forms.FloatField, {'min_value': 0.1})}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        del self.fields['filter']
        del self.fields['exposure_count']
        del self.fields['exposure_time']
        self.filter_fields = []
        for filter_code, filter_name in sorted((self.filter_choices()), key=(operator.itemgetter(1))):
            keys = []
            for exp_field_name, (exp_field_class, kwargs) in self.EXPOSURE_FIELDS.items():
                key = f"{filter_code}_{exp_field_name}"
                self.fields[key] = exp_field_class(required=False, **kwargs)
                keys.append(key)

            self.filter_fields.append((filter_code, filter_name, keys))

    def is_valid(self):
        if not self.is_bound or self.errors:
            return False
        obs_module = get_service_class(self.cleaned_data['facility'])
        errors = obs_module().validate_observation(self.observation_payload())
        if errors:
            self.add_error(None, self._flatten_error_dict(errors))
        return not errors

    def clean(self):
        num_filters = 0
        error_messages = []
        for code, name, _ in self.filter_fields:
            time_key = f"{code}_exposure_time"
            count_key = f"{code}_exposure_count"
            time = self.cleaned_data.get(time_key)
            count = self.cleaned_data.get(count_key)
            if not time:
                if not count:
                    del self.cleaned_data[time_key]
                    del self.cleaned_data[count_key]
                    continue
                else:
                    if not count:
                        error_messages.append(f"Exposure count missing for filter '{name}'")
                        continue
                if not time:
                    error_messages.append(f"Exposure time missing for filter '{name}'")
                    continue
                else:
                    num_filters += 1

        if error_messages:
            raise forms.ValidationError(error_messages)
        if num_filters == 0:
            raise forms.ValidationError('No filters selected')
        return super().clean()

    @staticmethod
    def get_schedulable_codes(api_response):
        """
        For a JSON response from the instruments API, return a dictionary
        mapping instrument names to lists of filter/slit codes which are
        schedulable
        """
        info = {}
        for name, val in api_response.items():
            keys = ('filters', 'slits')
            for key in keys:
                objs = val['optical_elements'].get(key, [])
                allowed = [obj['code'] for obj in objs if obj['schedulable']]
                if name not in info:
                    info[name] = []
                info[name] += allowed

        return info

    def get_extra_context(self):
        """
        Provide extra context to the view using this form.
        """
        json_response = make_request('GET', PORTAL_URL + '/api/instruments/').json()
        info = EducationLCOForm.get_schedulable_codes(json_response)
        return {'instrument_filters':json.dumps(info), 
         'filter_fields':self.filter_fields}

    def observation_payload(self):
        payload = super().observation_payload()
        payload['requests'][0]['configurations'] = list(self._build_configurations())
        return payload

    def _build_configuration(self):
        pass

    def _build_configurations(self):
        """
        Generator which yields dicts for the 'configurations' key of the
        'request' object in the observation payload
        """
        for filter_code, _, _ in self.filter_fields:
            try:
                instrument_config = {'exposure_count':self.cleaned_data[f"{filter_code}_exposure_count"], 
                 'exposure_time':self.cleaned_data[f"{filter_code}_exposure_time"], 
                 'optical_elements':{'filter': filter_code}}
            except KeyError:
                continue

            yield {'type':self.instrument_to_type(self.cleaned_data['instrument_type']),  'instrument_type':self.cleaned_data['instrument_type'], 
             'target':self._build_target_fields(), 
             'instrument_configs':[
              instrument_config], 
             'acquisition_config':{},  'guiding_config':{},  'constraints':{'max_airmass': self.cleaned_data['max_airmass']}}


class EducationLCOFacility(LCOFacility):

    def get_form(self, *args):
        return EducationLCOForm

    def data_products(self, observation_id, product_id=None):
        """
        Override this method to include reduction level in the dict for each
        data product
        """
        products = []
        for frame in self._archive_frames(observation_id, product_id):
            extra = {'date_obs':frame['DATE_OBS'], 
             'instrument':frame['INSTRUME'], 
             'siteid':frame['SITEID'], 
             'telid':frame['TELID'], 
             'exp_time':frame['EXPTIME'], 
             'filter':frame['FILTER']}
            products.append({'id':frame['id'], 
             'filename':frame['filename'], 
             'created':parse(frame['DATE_OBS']), 
             'url':frame['url'], 
             'reduced':frame['RLEVEL'] == 91, 
             'extra':extra})

        return products

    def save_data_products(self, observation_record, product_id=None, reduced=True):
        from tom_dataproducts.models import DataProduct
        from tom_dataproducts.utils import create_image_dataproduct
        final_products = []
        products = self.data_products(observation_record.observation_id, product_id)
        logger.debug(f"Saving {len(products)} files")
        for product in products:
            if reduced:
                if 'e91' not in product['filename']:
                    continue
            dp, created = DataProduct.objects.get_or_create(product_id=(product['id']),
              target=(observation_record.target),
              observation_record=observation_record,
              extra_data=(json.dumps(product['extra'])))
            if created:
                product_data = requests.get(product['url']).content
                dfile = ContentFile(product_data)
                dp.data.save(product['filename'], dfile)
                dp.data_product_type = self.find_data_product_type(dp.data.name)
                dp.save()
                logger.debug(f"Saved {product['filename']}")
            if AUTO_THUMBNAILS:
                create_image_dataproduct(dp)
            final_products.append(dp)

        return final_products
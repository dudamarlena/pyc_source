# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_vision_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 51262 bytes
from copy import deepcopy
from google.api_core.exceptions import AlreadyExists
from airflow.contrib.hooks.gcp_vision_hook import CloudVisionHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudVisionProductSetCreateOperator(BaseOperator):
    """CloudVisionProductSetCreateOperator"""
    template_fields = ('location', 'project_id', 'product_set_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, product_set, location, project_id=None, product_set_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductSetCreateOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.project_id = project_id
        self.product_set = product_set
        self.product_set_id = product_set_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        try:
            return self._hook.create_product_set(location=(self.location),
              project_id=(self.project_id),
              product_set=(self.product_set),
              product_set_id=(self.product_set_id),
              retry=(self.retry),
              timeout=(self.timeout),
              metadata=(self.metadata))
        except AlreadyExists:
            self.log.info('Product set with id %s already exists. Exiting from the create operation.', self.product_set_id)
            return self.product_set_id


class CloudVisionProductSetGetOperator(BaseOperator):
    """CloudVisionProductSetGetOperator"""
    template_fields = ('location', 'project_id', 'product_set_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, product_set_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductSetGetOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.project_id = project_id
        self.product_set_id = product_set_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        return self._hook.get_product_set(location=(self.location),
          product_set_id=(self.product_set_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionProductSetUpdateOperator(BaseOperator):
    """CloudVisionProductSetUpdateOperator"""
    template_fields = ('location', 'project_id', 'product_set_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, product_set, location=None, product_set_id=None, project_id=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductSetUpdateOperator, self).__init__)(*args, **kwargs)
        self.product_set = product_set
        self.update_mask = update_mask
        self.location = location
        self.project_id = project_id
        self.product_set_id = product_set_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        return self._hook.update_product_set(location=(self.location),
          product_set_id=(self.product_set_id),
          project_id=(self.project_id),
          product_set=(self.product_set),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionProductSetDeleteOperator(BaseOperator):
    """CloudVisionProductSetDeleteOperator"""
    template_fields = ('location', 'project_id', 'product_set_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, product_set_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductSetDeleteOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.project_id = project_id
        self.product_set_id = product_set_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        self._hook.delete_product_set(location=(self.location),
          product_set_id=(self.product_set_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionProductCreateOperator(BaseOperator):
    """CloudVisionProductCreateOperator"""
    template_fields = ('location', 'project_id', 'product_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, product, project_id=None, product_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductCreateOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.product = product
        self.project_id = project_id
        self.product_id = product_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        try:
            return self._hook.create_product(location=(self.location),
              product=(self.product),
              project_id=(self.project_id),
              product_id=(self.product_id),
              retry=(self.retry),
              timeout=(self.timeout),
              metadata=(self.metadata))
        except AlreadyExists:
            self.log.info('Product with id %s already exists. Exiting from the create operation.', self.product_id)
            return self.product_id


class CloudVisionProductGetOperator(BaseOperator):
    """CloudVisionProductGetOperator"""
    template_fields = ('location', 'project_id', 'product_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, product_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductGetOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.product_id = product_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        return self._hook.get_product(location=(self.location),
          product_id=(self.product_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionProductUpdateOperator(BaseOperator):
    """CloudVisionProductUpdateOperator"""
    template_fields = ('location', 'project_id', 'product_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, product, location=None, product_id=None, project_id=None, update_mask=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductUpdateOperator, self).__init__)(*args, **kwargs)
        self.product = product
        self.location = location
        self.product_id = product_id
        self.project_id = project_id
        self.update_mask = update_mask
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        return self._hook.update_product(product=(self.product),
          location=(self.location),
          product_id=(self.product_id),
          project_id=(self.project_id),
          update_mask=(self.update_mask),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionProductDeleteOperator(BaseOperator):
    """CloudVisionProductDeleteOperator"""
    template_fields = ('location', 'project_id', 'product_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, product_id, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionProductDeleteOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.product_id = product_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id
        self._hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))

    def execute(self, context):
        self._hook.delete_product(location=(self.location),
          product_id=(self.product_id),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionAnnotateImageOperator(BaseOperator):
    """CloudVisionAnnotateImageOperator"""
    template_fields = ('request', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, request, retry=None, timeout=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionAnnotateImageOperator, self).__init__)(*args, **kwargs)
        self.request = request
        self.retry = retry
        self.timeout = timeout
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        if not isinstance(self.request, list):
            response = hook.annotate_image(request=(self.request), retry=(self.retry), timeout=(self.timeout))
        else:
            response = hook.batch_annotate_images(requests=(self.request),
              retry=(self.retry),
              timeout=(self.timeout))
        return response


class CloudVisionReferenceImageCreateOperator(BaseOperator):
    """CloudVisionReferenceImageCreateOperator"""
    template_fields = ('location', 'reference_image', 'product_id', 'reference_image_id',
                       'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, location, reference_image, product_id, reference_image_id=None, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionReferenceImageCreateOperator, self).__init__)(*args, **kwargs)
        self.location = location
        self.product_id = product_id
        self.reference_image = reference_image
        self.reference_image_id = reference_image_id
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        try:
            hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
            return hook.create_reference_image(location=(self.location),
              product_id=(self.product_id),
              reference_image=(self.reference_image),
              reference_image_id=(self.reference_image_id),
              project_id=(self.project_id),
              retry=(self.retry),
              timeout=(self.timeout),
              metadata=(self.metadata))
        except AlreadyExists:
            self.log.info('ReferenceImage with id %s already exists. Exiting from the create operation.', self.product_id)
            return self.reference_image_id


class CloudVisionAddProductToProductSetOperator(BaseOperator):
    """CloudVisionAddProductToProductSetOperator"""
    template_fields = ('location', 'product_set_id', 'product_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, product_set_id, product_id, location, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionAddProductToProductSetOperator, self).__init__)(*args, **kwargs)
        self.product_set_id = product_set_id
        self.product_id = product_id
        self.location = location
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.add_product_to_product_set(product_set_id=(self.product_set_id),
          product_id=(self.product_id),
          location=(self.location),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionRemoveProductFromProductSetOperator(BaseOperator):
    """CloudVisionRemoveProductFromProductSetOperator"""
    template_fields = ('location', 'product_set_id', 'product_id', 'project_id', 'gcp_conn_id')

    @apply_defaults
    def __init__(self, product_set_id, product_id, location, project_id=None, retry=None, timeout=None, metadata=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionRemoveProductFromProductSetOperator, self).__init__)(*args, **kwargs)
        self.product_set_id = product_set_id
        self.product_id = product_id
        self.location = location
        self.project_id = project_id
        self.retry = retry
        self.timeout = timeout
        self.metadata = metadata
        self.gcp_conn_id = gcp_conn_id

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.remove_product_from_product_set(product_set_id=(self.product_set_id),
          product_id=(self.product_id),
          location=(self.location),
          project_id=(self.project_id),
          retry=(self.retry),
          timeout=(self.timeout),
          metadata=(self.metadata))


class CloudVisionDetectTextOperator(BaseOperator):
    """CloudVisionDetectTextOperator"""
    template_fields = ('image', 'max_results', 'timeout', 'gcp_conn_id')

    def __init__(self, image, max_results=None, retry=None, timeout=None, language_hints=None, web_detection_params=None, additional_properties=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionDetectTextOperator, self).__init__)(*args, **kwargs)
        self.image = image
        self.max_results = max_results
        self.retry = retry
        self.timeout = timeout
        self.gcp_conn_id = gcp_conn_id
        self.kwargs = kwargs
        self.additional_properties = prepare_additional_parameters(additional_properties=additional_properties,
          language_hints=language_hints,
          web_detection_params=web_detection_params)

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.text_detection(image=(self.image),
          max_results=(self.max_results),
          retry=(self.retry),
          timeout=(self.timeout),
          additional_properties=(self.additional_properties))


class CloudVisionDetectDocumentTextOperator(BaseOperator):
    """CloudVisionDetectDocumentTextOperator"""
    template_fields = ('image', 'max_results', 'timeout', 'gcp_conn_id')

    def __init__(self, image, max_results=None, retry=None, timeout=None, language_hints=None, web_detection_params=None, additional_properties=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionDetectDocumentTextOperator, self).__init__)(*args, **kwargs)
        self.image = image
        self.max_results = max_results
        self.retry = retry
        self.timeout = timeout
        self.gcp_conn_id = gcp_conn_id
        self.additional_properties = prepare_additional_parameters(additional_properties=additional_properties,
          language_hints=language_hints,
          web_detection_params=web_detection_params)

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.document_text_detection(image=(self.image),
          max_results=(self.max_results),
          retry=(self.retry),
          timeout=(self.timeout),
          additional_properties=(self.additional_properties))


class CloudVisionDetectImageLabelsOperator(BaseOperator):
    """CloudVisionDetectImageLabelsOperator"""
    template_fields = ('image', 'max_results', 'timeout', 'gcp_conn_id')

    def __init__(self, image, max_results=None, retry=None, timeout=None, additional_properties=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionDetectImageLabelsOperator, self).__init__)(*args, **kwargs)
        self.image = image
        self.max_results = max_results
        self.retry = retry
        self.timeout = timeout
        self.gcp_conn_id = gcp_conn_id
        self.additional_properties = additional_properties

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.label_detection(image=(self.image),
          max_results=(self.max_results),
          retry=(self.retry),
          timeout=(self.timeout),
          additional_properties=(self.additional_properties))


class CloudVisionDetectImageSafeSearchOperator(BaseOperator):
    """CloudVisionDetectImageSafeSearchOperator"""
    template_fields = ('image', 'max_results', 'timeout', 'gcp_conn_id')

    def __init__(self, image, max_results=None, retry=None, timeout=None, additional_properties=None, gcp_conn_id='google_cloud_default', *args, **kwargs):
        (super(CloudVisionDetectImageSafeSearchOperator, self).__init__)(*args, **kwargs)
        self.image = image
        self.max_results = max_results
        self.retry = retry
        self.timeout = timeout
        self.gcp_conn_id = gcp_conn_id
        self.additional_properties = additional_properties

    def execute(self, context):
        hook = CloudVisionHook(gcp_conn_id=(self.gcp_conn_id))
        return hook.safe_search_detection(image=(self.image),
          max_results=(self.max_results),
          retry=(self.retry),
          timeout=(self.timeout),
          additional_properties=(self.additional_properties))


def prepare_additional_parameters(additional_properties, language_hints, web_detection_params):
    """
    Creates additional_properties parameter based on language_hints, web_detection_params and
    additional_properties parameters specified by the user
    """
    if language_hints is None:
        if web_detection_params is None:
            return additional_properties
    if additional_properties is None:
        return {}
    else:
        merged_additional_parameters = deepcopy(additional_properties)
        if 'image_context' not in merged_additional_parameters:
            merged_additional_parameters['image_context'] = {}
        merged_additional_parameters['image_context']['language_hints'] = merged_additional_parameters['image_context'].get('language_hints', language_hints)
        merged_additional_parameters['image_context']['web_detection_params'] = merged_additional_parameters['image_context'].get('web_detection_params', web_detection_params)
        return merged_additional_parameters
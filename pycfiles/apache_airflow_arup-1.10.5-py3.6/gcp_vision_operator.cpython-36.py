# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_vision_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 51262 bytes
from copy import deepcopy
from google.api_core.exceptions import AlreadyExists
from airflow.contrib.hooks.gcp_vision_hook import CloudVisionHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CloudVisionProductSetCreateOperator(BaseOperator):
    __doc__ = '\n    Creates a new ProductSet resource.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductSetCreateOperator`\n\n    :param product_set: (Required) The ProductSet to create. If a dict is provided, it must be of the same\n        form as the protobuf message `ProductSet`.\n    :type product_set: dict or google.cloud.vision_v1.types.ProductSet\n    :param location: (Required) The region where the ProductSet should be created. Valid regions\n        (as of 2019-02-05) are: us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param project_id: (Optional) The project in which the ProductSet should be created. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param product_set_id: (Optional) A user-supplied resource id for this ProductSet.\n        If set, the server will attempt to use this value as the resource id. If it is\n        already in use, an error is returned with code ALREADY_EXISTS. Must be at most\n        128 characters long. It cannot contain the character /.\n    :type product_set_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Gets information associated with a ProductSet.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductSetGetOperator`\n\n    :param location: (Required) The region where the ProductSet is located. Valid regions (as of 2019-02-05)\n        are: us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_set_id: (Required) The resource id of this ProductSet.\n    :type product_set_id: str\n    :param project_id: (Optional) The project in which the ProductSet is located. If set\n        to None or missing, the default `project_id` from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Makes changes to a `ProductSet` resource. Only display_name can be updated currently.\n\n    .. note:: To locate the `ProductSet` resource, its `name` in the form\n        `projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID` is necessary.\n\n    You can provide the `name` directly as an attribute of the `product_set` object.\n    However, you can leave it blank and provide `location` and `product_set_id` instead\n    (and optionally `project_id` - if not present, the connection default will be used)\n    and the `name` will be created by the operator itself.\n\n    This mechanism exists for your convenience, to allow leaving the `project_id` empty\n    and having Airflow use the connection default `project_id`.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductSetUpdateOperator`\n\n    :param product_set: (Required) The ProductSet resource which replaces the one on the\n        server. If a dict is provided, it must be of the same form as the protobuf\n        message `ProductSet`.\n    :type product_set: dict or google.cloud.vision_v1.types.ProductSet\n    :param location: (Optional) The region where the ProductSet is located. Valid regions (as of 2019-02-05)\n        are: us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_set_id: (Optional) The resource id of this ProductSet.\n    :type product_set_id: str\n    :param project_id: (Optional) The project in which the ProductSet should be created. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param update_mask: (Optional) The `FieldMask` that specifies which fields to update. If update_mask\n        isn’t specified, all mutable fields are to be updated. Valid mask path is display_name. If a dict is\n        provided, it must be of the same form as the protobuf message `FieldMask`.\n    :type update_mask: dict or google.cloud.vision_v1.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n\n    '
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
    __doc__ = '\n    Permanently deletes a `ProductSet`. `Products` and `ReferenceImages` in the\n    `ProductSet` are not deleted. The actual image files are not deleted from Google\n    Cloud Storage.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductSetDeleteOperator`\n\n    :param location: (Required) The region where the ProductSet is located. Valid regions (as of 2019-02-05)\n        are: us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_set_id: (Required) The resource id of this ProductSet.\n    :type product_set_id: str\n    :param project_id: (Optional) The project in which the ProductSet should be created.\n        If set to None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n\n    '
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
    __doc__ = '\n    Creates and returns a new product resource.\n\n    Possible errors regarding the `Product` object provided:\n\n    - Returns `INVALID_ARGUMENT` if `display_name` is missing or longer than 4096 characters.\n    - Returns `INVALID_ARGUMENT` if `description` is longer than 4096 characters.\n    - Returns `INVALID_ARGUMENT` if `product_category` is missing or invalid.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductCreateOperator`\n\n    :param location: (Required) The region where the Product should be created. Valid regions\n        (as of 2019-02-05) are: us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product: (Required) The product to create. If a dict is provided, it must be of the same form as\n        the protobuf message `Product`.\n    :type product: dict or google.cloud.vision_v1.types.Product\n    :param project_id: (Optional) The project in which the Product should be created. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param product_id: (Optional) A user-supplied resource id for this Product.\n        If set, the server will attempt to use this value as the resource id. If it is\n        already in use, an error is returned with code ALREADY_EXISTS. Must be at most\n        128 characters long. It cannot contain the character /.\n    :type product_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n\n    '
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
    __doc__ = '\n    Gets information associated with a `Product`.\n\n    Possible errors:\n\n    - Returns `NOT_FOUND` if the `Product` does not exist.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductGetOperator`\n\n    :param location: (Required) The region where the Product is located. Valid regions (as of 2019-02-05) are:\n        us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_id: (Required) The resource id of this Product.\n    :type product_id: str\n    :param project_id: (Optional) The project in which the Product is located. If set to\n        None or missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n\n    '
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
    __doc__ = '\n    Makes changes to a Product resource. Only the display_name, description, and labels fields can be\n    updated right now.\n\n    If labels are updated, the change will not be reflected in queries until the next index time.\n\n    .. note:: To locate the `Product` resource, its `name` in the form\n        `projects/PROJECT_ID/locations/LOC_ID/products/PRODUCT_ID` is necessary.\n\n    You can provide the `name` directly as an attribute of the `product` object. However, you can leave it\n    blank and provide `location` and `product_id` instead (and optionally `project_id` - if not present,\n    the connection default will be used) and the `name` will be created by the operator itself.\n\n    This mechanism exists for your convenience, to allow leaving the `project_id` empty and having Airflow\n    use the connection default `project_id`.\n\n    Possible errors related to the provided `Product`:\n\n    - Returns `NOT_FOUND` if the Product does not exist.\n    - Returns `INVALID_ARGUMENT` if `display_name` is present in update_mask but is missing from the request\n        or longer than 4096 characters.\n    - Returns `INVALID_ARGUMENT` if `description` is present in update_mask but is longer than 4096\n        characters.\n    - Returns `INVALID_ARGUMENT` if `product_category` is present in update_mask.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductUpdateOperator`\n\n    :param product: (Required) The Product resource which replaces the one on the server. product.name is\n        immutable. If a dict is provided, it must be of the same form as the protobuf message `Product`.\n    :type product: dict or google.cloud.vision_v1.types.ProductSet\n    :param location: (Optional) The region where the Product is located. Valid regions (as of 2019-02-05) are:\n        us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_id: (Optional) The resource id of this Product.\n    :type product_id: str\n    :param project_id: (Optional) The project in which the Product is located. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param update_mask: (Optional) The `FieldMask` that specifies which fields to update. If update_mask\n        isn’t specified, all mutable fields are to be updated. Valid mask paths include product_labels,\n        display_name, and description. If a dict is provided, it must be of the same form as the protobuf\n        message `FieldMask`.\n    :type update_mask: dict or google.cloud.vision_v1.types.FieldMask\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Permanently deletes a product and its reference images.\n\n    Metadata of the product and all its images will be deleted right away, but search queries against\n    ProductSets containing the product may still work until all related caches are refreshed.\n\n    Possible errors:\n\n    - Returns `NOT_FOUND` if the product does not exist.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionProductDeleteOperator`\n\n    :param location: (Required) The region where the Product is located. Valid regions (as of 2019-02-05) are:\n        us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param product_id: (Required) The resource id of this Product.\n    :type product_id: str\n    :param project_id: (Optional) The project in which the Product is located. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Run image detection and annotation for an image or a batch of images.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionAnnotateImageOperator`\n\n    :param request: (Required) Annotation request for image or a batch.\n        If a dict is provided, it must be of the same form as the protobuf\n        message class:`google.cloud.vision_v1.types.AnnotateImageRequest`\n    :type request: list[dict or google.cloud.vision_v1.types.AnnotateImageRequest] for batch or\n        dict or google.cloud.vision_v1.types.AnnotateImageRequest for single image.\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Creates and returns a new ReferenceImage ID resource.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionReferenceImageCreateOperator`\n\n    :param location: (Required) The region where the Product is located. Valid regions (as of 2019-02-05) are:\n        us-east1, us-west1, europe-west1, asia-east1\n    :type location: str\n    :param reference_image: (Required) The reference image to create. If an image ID is specified, it is\n        ignored.\n        If a dict is provided, it must be of the same form as the protobuf message\n        :class:`google.cloud.vision_v1.types.ReferenceImage`\n    :type reference_image: dict or google.cloud.vision_v1.types.ReferenceImage\n    :param reference_image_id: (Optional) A user-supplied resource id for the ReferenceImage to be added.\n        If set, the server will attempt to use this value as the resource id. If it is already in use, an\n        error is returned with code ALREADY_EXISTS. Must be at most 128 characters long. It cannot contain\n        the character `/`.\n    :type reference_image_id: str\n    :param product_id: (Optional) The resource id of this Product.\n    :type product_id: str\n    :param project_id: (Optional) The project in which the Product is located. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Adds a Product to the specified ProductSet. If the Product is already present, no change is made.\n\n    One Product can be added to at most 100 ProductSets.\n\n    Possible errors:\n\n    - Returns `NOT_FOUND` if the Product or the ProductSet doesn’t exist.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionAddProductToProductSetOperator`\n\n    :param product_set_id: (Required) The resource id for the ProductSet to modify.\n    :type product_set_id: str\n    :param product_id: (Required) The resource id of this Product.\n    :type product_id: str\n    :param location: (Required) The region where the ProductSet is located. Valid regions (as of 2019-02-05)\n        are: us-east1, us-west1, europe-west1, asia-east1\n    :type: str\n    :param project_id: (Optional) The project in which the Product is located. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Removes a Product from the specified ProductSet.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionRemoveProductFromProductSetOperator`\n\n    :param product_set_id: (Required) The resource id for the ProductSet to modify.\n    :type product_set_id: str\n    :param product_id: (Required) The resource id of this Product.\n    :type product_id: str\n    :param location: (Required) The region where the ProductSet is located. Valid regions (as of 2019-02-05)\n        are: us-east1, us-west1, europe-west1, asia-east1\n    :type: str\n    :param project_id: (Optional) The project in which the Product is located. If set to None or\n        missing, the default project_id from the GCP connection is used.\n    :type project_id: str\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to\n        complete. Note that if retry is specified, the timeout applies to each individual\n        attempt.\n    :type timeout: float\n    :param metadata: (Optional) Additional metadata that is provided to the method.\n    :type metadata: sequence[tuple[str, str]]\n    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud Platform.\n    :type gcp_conn_id: str\n    '
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
    __doc__ = '\n    Detects Text in the image\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionDetectTextOperator`\n\n    :param image: (Required) The image to analyze. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.Image\n    :type image: dict or google.cloud.vision_v1.types.Image\n    :param max_results: (Optional) Number of results to return.\n    :type max_results: int\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Number of seconds before timing out.\n    :type timeout: float\n    :param language_hints: List of languages to use for TEXT_DETECTION.\n        In most cases, an empty value yields the best results since it enables automatic language detection.\n        For languages based on the Latin alphabet, setting language_hints is not needed.\n    :type language_hints: str, list or google.cloud.vision.v1.ImageContext.language_hints:\n    :param web_detection_params: Parameters for web detection.\n    :type web_detection_params: dict or google.cloud.vision.v1.ImageContext.web_detection_params\n    :param additional_properties: Additional properties to be set on the AnnotateImageRequest. See more:\n        :class:`google.cloud.vision_v1.types.AnnotateImageRequest`\n    :type additional_properties: dict\n    '
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
    __doc__ = '\n    Detects Document Text in the image\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionDetectDocumentTextOperator`\n\n    :param image: (Required) The image to analyze. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.Image\n    :type image: dict or google.cloud.vision_v1.types.Image\n    :param max_results: Number of results to return.\n    :type max_results: int\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Number of seconds before timing out.\n    :type timeout: float\n    :param language_hints: List of languages to use for TEXT_DETECTION.\n        In most cases, an empty value yields the best results since it enables automatic language detection.\n        For languages based on the Latin alphabet, setting language_hints is not needed.\n    :type language_hints: str, list or google.cloud.vision.v1.ImageContext.language_hints:\n    :param web_detection_params: Parameters for web detection.\n    :type web_detection_params: dict or google.cloud.vision.v1.ImageContext.web_detection_params\n    :param additional_properties: Additional properties to be set on the AnnotateImageRequest. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.AnnotateImageRequest\n    :type additional_properties: dict\n    '
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
    __doc__ = '\n    Detects Document Text in the image\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionDetectImageLabelsOperator`\n\n    :param image: (Required) The image to analyze. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.Image\n    :type image: dict or google.cloud.vision_v1.types.Image\n    :param max_results: Number of results to return.\n    :type max_results: int\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Number of seconds before timing out.\n    :type timeout: float\n    :param additional_properties: Additional properties to be set on the AnnotateImageRequest. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.AnnotateImageRequest\n    :type additional_properties: dict\n    '
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
    __doc__ = '\n    Detects Document Text in the image\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:CloudVisionDetectImageSafeSearchOperator`\n\n    :param image: (Required) The image to analyze. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.Image\n    :type image: dict or google.cloud.vision_v1.types.Image\n    :param max_results: Number of results to return.\n    :type max_results: int\n    :param retry: (Optional) A retry object used to retry requests. If `None` is\n        specified, requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: Number of seconds before timing out.\n    :type timeout: float\n    :param additional_properties: Additional properties to be set on the AnnotateImageRequest. See more:\n        https://googleapis.github.io/google-cloud-python/latest/vision/gapic/v1/types.html#google.cloud.vision_v1.types.AnnotateImageRequest\n    :type additional_properties: dict\n    '
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
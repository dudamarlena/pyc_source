# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_acl_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5893 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageBucketCreateAclEntryOperator(BaseOperator):
    __doc__ = '\n    Creates a new ACL entry on the specified bucket.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GoogleCloudStorageBucketCreateAclEntryOperator`\n\n    :param bucket: Name of a bucket.\n    :type bucket: str\n    :param entity: The entity holding the permission, in one of the following forms:\n        user-userId, user-email, group-groupId, group-email, domain-domain,\n        project-team-projectId, allUsers, allAuthenticatedUsers\n    :type entity: str\n    :param role: The access permission for the entity.\n        Acceptable values are: "OWNER", "READER", "WRITER".\n    :type role: str\n    :param user_project: (Optional) The project to be billed for this request.\n        Required for Requester Pays buckets.\n    :type user_project: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google Cloud Storage.\n    :type google_cloud_storage_conn_id: str\n    '
    template_fields = ('bucket', 'entity', 'role', 'user_project')

    @apply_defaults
    def __init__(self, bucket, entity, role, user_project=None, google_cloud_storage_conn_id='google_cloud_default', *args, **kwargs):
        (super(GoogleCloudStorageBucketCreateAclEntryOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.entity = entity
        self.role = role
        self.user_project = user_project
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id))
        hook.insert_bucket_acl(bucket=(self.bucket), entity=(self.entity), role=(self.role), user_project=(self.user_project))


class GoogleCloudStorageObjectCreateAclEntryOperator(BaseOperator):
    __doc__ = '\n    Creates a new ACL entry on the specified object.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GoogleCloudStorageObjectCreateAclEntryOperator`\n\n    :param bucket: Name of a bucket.\n    :type bucket: str\n    :param object_name: Name of the object. For information about how to URL encode object\n        names to be path safe, see:\n        https://cloud.google.com/storage/docs/json_api/#encoding\n    :type object_name: str\n    :param entity: The entity holding the permission, in one of the following forms:\n        user-userId, user-email, group-groupId, group-email, domain-domain,\n        project-team-projectId, allUsers, allAuthenticatedUsers\n    :type entity: str\n    :param role: The access permission for the entity.\n        Acceptable values are: "OWNER", "READER".\n    :type role: str\n    :param generation: (Optional) If present, selects a specific revision of this object\n        (as opposed to the latest version, the default).\n    :type generation: str\n    :param user_project: (Optional) The project to be billed for this request.\n        Required for Requester Pays buckets.\n    :type user_project: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google Cloud Storage.\n    :type google_cloud_storage_conn_id: str\n    '
    template_fields = ('bucket', 'object_name', 'entity', 'role', 'generation', 'user_project')

    @apply_defaults
    def __init__(self, bucket, object_name, entity, role, generation=None, user_project=None, google_cloud_storage_conn_id='google_cloud_default', *args, **kwargs):
        (super(GoogleCloudStorageObjectCreateAclEntryOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.object_name = object_name
        self.entity = entity
        self.role = role
        self.generation = generation
        self.user_project = user_project
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id))
        hook.insert_object_acl(bucket=(self.bucket), object_name=(self.object_name), entity=(self.entity),
          role=(self.role),
          generation=(self.generation),
          user_project=(self.user_project))
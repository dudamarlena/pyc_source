# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ooyala/constants.py
# Compiled at: 2011-08-18 05:15:41


class OoyalaAPI(object):
    BASE_URL = 'http://api.ooyala.com/'

    class BACKLOT(object):
        QUERY = 'query'
        THUMB = 'thumbnails'
        ATTR = 'edit'
        LABEL = 'labels'
        CHANNEL = 'channels'
        URL = 'partner/'

    class INGESTION(object):
        URL = 'partner/ingestion/'
        INGESTION = 'ingestion'

    class ANALYTICS(object):
        URL = ''
        ANALYTICS = 'analytics'


class OoyalaConstants(object):
    OOYALA_ATTR_STATUS_PAUSED = 'paused'
    OOYALA_ATTR_STATUS_LIVE = 'live'
    OOYALA_ATTR_STATUS_DELETED = 'deleted'
    OOYALA_ATTR_STATS_LIFETIME = 'lifetime'
    OOYALA_QUERY_STATUS_DELETED = 'deleted'
    OOYALA_QUERY_STATUS_LIVE = 'live'
    OOYALA_QUERY_STATUS_ERROR = 'error'
    OOYALA_QUERY_STATUS_FILEMISSING = 'filemissing'
    OOYALA_QUERY_STATUS_UPLOADING = 'uploading'
    OOYALA_QUERY_STATUS_PAUSED = 'paused'
    OOYALA_QUERY_STATUS_UPLOADED = 'uploaded'
    OOYALA_QUERY_STATUS_NA = ('na', )
    OOYALA_QUERY_STATUS_CREMOVED = 'cremoved'
    OOYALA_QUERY_STATUS_API_UPLOADING = 'auploading'
    OOYALA_QUERY_STATUS_API_UPLOADED = 'auploaded'
    OOYALA_QUERY_STATUS_DUPLICATE = 'duplicate'
    OOYALA_QUERY_STATUS_PENDING = 'pending'
    OOYALA_QUERY_STATUS_PROCESSING = 'processing'
    OOYALA_FIELDS_LABELS = 'labels'
    OOYALA_FIELDS_METADATA = 'metadata'
    OOYALA_FIELDS_RATINGS = 'ratings'
    OOYALA_QUERY_LIMIT = 1000

    class LABEL_MODE(object):
        LIST = 'listLabels'
        CREATE = 'createLabels'
        DELETE = 'deleteLabels'
        ASSIGN = 'assignLabels'
        UNASSIGN = 'unassignLabels'
        RENAME = 'renameLabels'
        CLEAR = 'clearLabels'

    class CHANNEL_MODE(object):
        LIST = 'list'
        ASSIGN = 'assign'
        CREATE = 'create'

    class STATS(object):
        DAY = '1d'
        TWO_DAYS = '2d'
        THREE_DAYS = '3d'
        FOUR_DAYS = '4d'
        WORKWEEK = '5d'
        WEEK = '7d'
        FORTNIGHT = '14d'
        FOUR_WEEKS = '28d'
        TWENTYNINE_DAYS = '29d'
        THIRTY_DAYS = '30d'
        THIRTYONE_DAYS = '31d'

    class GRANULATIRY(object):
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'
        TOTAL = 'total'

    class ANALYTIC_METHODS(object):
        TOTALS = 'account.totals'
        GEO_TOTALS = 'account.geoTotals'
        ACCOUNT_VIDEOS = 'account.videoTotals'
        ACCOUNT_DOMAIN = 'account.domainTotals'
        VIDEO = 'video.totals'
        VIDEO_DOMAIN = 'video.domainTotals'
        VIDEO_BEHAVIORAL = 'video.behavioral'

    OOYALA_ORDER_ASC = 'asc'
    OOYALA_ORDER_DESC = 'desc'
    OOYALA_QUERY_MODE_OR = 'or'
    OOYALA_QUERY_MODE_AND = 'and'
    DEFAULT_EXPIRE_TIME = 3000
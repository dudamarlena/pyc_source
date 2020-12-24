# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/controllers/fileupload_controller.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 4521 bytes
import boto3, logging
from lantern_flask import settings
from lantern_flask.utils.request import http_response, http_error
s3 = boto3.resource('s3')
log = logging.getLogger(__name__)

class FileUploadController(object):
    __doc__ = ' Handles all operations related to Upload files to S3\n    '

    def __init__(self, bucket_name, static_url=None, debug=False):
        """ Constructor

        Arguments:
            bucket_name {str} -- Destination Bucket Name

        Keyword Arguments:
            static_url {str} -- Custom Static Url, It can be a dns used for the bucket (default: {None})
                If static_url==None a default static_url will be initialized for us-wes-2
            debug {bool} -- if set to True will raise any exception without handling it (default: {False})
        """
        self.debug = debug if debug else settings.get('LOCAL_USER', False)
        self.bucket_name = bucket_name
        self.static_url = static_url if static_url else 'https://s3-us-west-2.amazonaws.com/%s/' % bucket_name

    def upload_stream(self, stream, filename, mimetype, return_raw=False):
        """ Return a file stream, this is a manual operation use upload_file and upload_image instead

        Arguments:
            stream {FileStorage or any other file opened} -- File Stream to be uploaded to s3
            filename {str} -- Destination filename
            mimetype {str} -- mimetype without charset

        Keyword Arguments:
            return_raw {bool} -- If set to True it will retunr just the url not the response (default: {False})

        Returns:
            [HttpReseponse, status or url] -- return url or httpresponse,status depending on return_raw
        """
        try:
            s3.Bucket('iotsigfox-lantern-client-staticfiles').put_object(Key=filename,
              Body=stream,
              ContentType=mimetype)
            final_url = '{}{}'.format(self.static_url, filename)
            if return_raw:
                return final_url
            return http_response(code=code, message='Uploaded', data=final_url)
        except Exception as e:
            log.error(str(e))
            if self.debug:
                raise e
            else:
                if return_raw:
                    return
                http_error(code=500, message='Error trying to upload the file', detail=(str(e)))

    def upload_file(self, stream, filename, mimetype=None, return_raw=False):
        """ Upload files without checking extention

        Arguments:
            stream {FileStorage or any other file opened} -- File Stream to be uploaded to s3
            filename {str} -- Destination filename
            mimetype {str} -- mimetype without charset

        Keyword Arguments:
            return_raw {bool} -- If set to True it will retunr just the url not the response (default: {False})

        Returns:
            [HttpReseponse, status or url] -- return url or httpresponse,status depending on return_raw
        """
        mimetype = mimetype if mimetype else stream.mimetype
        return self.upload_stream(stream=stream, filename=filename, mimetype=mimetype, return_raw=return_raw)

    def upload_image(self, stream, filename, mimetype=None, return_raw=False):
        """ Upload Images to S3
            We are validating image is present in the mimetype to make sure a supported image is being uploaded.
            
            Arguments:
                    stream {FileStorage or any other file opened} -- File Stream to be uploaded to s3
                    filename {str} -- Destination filename
                    mimetype {str} -- mimetype without charset
                
                Keyword Arguments:
                    return_raw {bool} -- If set to True it will retunr just the url not the response (default: {False})
                
                Returns:
                    [HttpReseponse, status or url] -- return url or httpresponse,status depending on return_raw
        """
        mimetype = mimetype if mimetype else stream.mimetype
        if 'image' not in mimetype:
            message = '{} not supported for image upload'.format(mimetype)
            detail = 'A image extention is required'
            if self.debug:
                raise Exception(message)
            else:
                if return_raw:
                    return
                else:
                    return http_error(code=415, message=message, detail=detail)
        return self.upload_stream(stream=stream, filename=filename, mimetype=mimetype, return_raw=return_raw)
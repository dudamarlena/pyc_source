# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/aws/rekognition.py
# Compiled at: 2017-11-06 21:55:23
# Size of source mod 2**32: 2018 bytes
import time
from io import BytesIO
import aiohttp, boto3, aiohttp_jinja2
from ramjet.engines import ioloop, thread_executor
from ramjet.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, logger
logger = logger.getChild('tasks.aws.rekognition')

def bind_handle(add_route):
    logger.info('bind_handle aws.rekognition')
    add_route('/detect/', DemoHandle)


async def download_img--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'download image {}'
                6  LOAD_ATTR                format
                8  LOAD_FAST                'url'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  POP_TOP          

 L.  21        16  LOAD_GLOBAL              aiohttp
               18  LOAD_ATTR                ClientSession
               20  CALL_FUNCTION_0       0  '0 positional arguments'
               22  SETUP_WITH           80  'to 80'
               24  STORE_FAST               'session'

 L.  22        26  LOAD_FAST                'session'
               28  LOAD_ATTR                get
               30  LOAD_FAST                'url'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  BEFORE_ASYNC_WITH
               36  GET_AWAITABLE    
               38  LOAD_CONST               None
               40  YIELD_FROM       
               42  SETUP_ASYNC_WITH     64  'to 64'
               44  STORE_FAST               'resp'

 L.  23        46  LOAD_GLOBAL              BytesIO
               48  LOAD_FAST                'resp'
               50  LOAD_ATTR                read
               52  CALL_FUNCTION_0       0  '0 positional arguments'
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RETURN_VALUE     
             64_0  COME_FROM_ASYNC_WITH    42  '42'
               64  WITH_CLEANUP_START
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      
               76  POP_BLOCK        
               78  LOAD_CONST               None
             80_0  COME_FROM_WITH       22  '22'
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 64_0


def _load_img_labels(aws_conn, im):
    logger.info('request to deteck image...')
    return aws_conn.detect_labels(Image={'Bytes': im.read}, MaxLabels=10)


async def load_img_labels(aws_conn, im):
    logger.info('detect image...')
    return await ioloop.run_in_executor(thread_executor, _load_img_labels, aws_conn, im)


class DemoHandle(aiohttp.web.View):

    def connect2aws(self):
        return boto3.client('rekognition',
          aws_access_key_id=AWS_ACCESS_KEY,
          aws_secret_access_key=AWS_SECRET_KEY,
          region_name='us-west-2')

    @aiohttp_jinja2.template('aws/index.tpl')
    async def get(self):
        pass

    async def post(self):
        try:
            data = await self.request.json
            urls = data['urls']
            assert len(urls) < 5
        except Exception:
            return aiohttp.web.HTTPBadRequest
        else:
            aws_conn = self.connect2aws
            results = {'cost':None, 
             'results':{}}
            start = time.time
            for url in urls:
                im = await download_img(url)
                results['results'].update({url: (await load_img_labels(aws_conn, im))['Labels']})

            results['cost'] = '{:.2f}s'.format(time.time - start)
            return aiohttp.web.json_response(results)
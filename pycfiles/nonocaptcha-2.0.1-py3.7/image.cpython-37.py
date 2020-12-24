# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/nonocaptcha/image.py
# Compiled at: 2018-11-16 07:03:33
# Size of source mod 2**32: 4637 bytes
""" ***IN TESTING*** """
import os, asyncio, threading
from PIL import Image
from http.server import HTTPServer, BaseHTTPRequestHandler
from nonocaptcha import util
from nonocaptcha.base import Base, settings
from nonocaptcha import package_dir
PICTURES = os.path.join(package_dir, settings['data']['pictures'])

class Handler(BaseHTTPRequestHandler):
    base_path = None

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        image_file = os.path.join(self.base_path, self.path.lstrip('/'))
        self.wfile.write(open(image_file, 'rb').read())


class SolveImage(Base):
    url = 'https://www.google.com/searchbyimage?site=search&sa=X&image_url='
    ip_address = 'http://91.121.226.109'

    def __init__(self, browser, image_frame, proxy, proxy_auth, proc_id):
        self.browser = browser
        self.image_frame = image_frame
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.proc_id = proc_id
        self.cur_image_path = None
        self.title = None
        self.pieces = None

    async def get_images(self):
        table = await self.image_frame.querySelector('table')
        rows = await table.querySelectorAll('tr')
        for row in rows:
            cells = await row.querySelectorAll('td')
            for cell in cells:
                yield cell

    async def is_solvable(self):
        el = await self.get_description_element()
        desc = await self.image_frame.evaluate('el => el.innerText', el)
        return 'images' in desc

    async def pictures_of(self):
        el = await self.get_description_element()
        of = await self.image_frame.evaluate('el => el.firstElementChild.innerText', el)
        return of.lstrip('a ')

    async def get_description_element(self):
        name1 = await self.image_frame.querySelector('.rc-imageselect-desc')
        name2 = await self.image_frame.querySelector('.rc-imageselect-desc-no-canonical')
        if name1:
            return name1
        return name2

    async def cycle_to_solvable(self):
        while not await self.is_solvable() or await self.image_no() != 9:
            await self.click_reload_button()

    async def solve_by_image--- This code section failed: ---

 L.  75         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              cycle_to_solvable
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  POP_TOP          

 L.  76        14  LOAD_DEREF               'self'
               16  LOAD_METHOD              pictures_of
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  STORE_FAST               'title'

 L.  77        28  LOAD_CONST               9
               30  STORE_FAST               'pieces'

 L.  78        32  LOAD_DEREF               'self'
               34  LOAD_METHOD              download_image
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  STORE_FAST               'image'

 L.  79        46  LOAD_FAST                'title'
               48  LOAD_DEREF               'self'
               50  STORE_ATTR               title

 L.  80        52  LOAD_GLOBAL              print
               54  LOAD_STR                 'Image of '
               56  LOAD_FAST                'title'
               58  FORMAT_VALUE          0  ''
               60  BUILD_STRING_2        2 
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  POP_TOP          

 L.  81        66  LOAD_FAST                'pieces'
               68  LOAD_DEREF               'self'
               70  STORE_ATTR               pieces

 L.  82        72  LOAD_GLOBAL              os
               74  LOAD_METHOD              mkdir
               76  LOAD_GLOBAL              PICTURES
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_TOP          

 L.  83        82  LOAD_GLOBAL              os
               84  LOAD_ATTR                path
               86  LOAD_METHOD              join
               88  LOAD_GLOBAL              PICTURES
               90  LOAD_GLOBAL              hash
               92  LOAD_FAST                'image'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  FORMAT_VALUE          0  ''
               98  CALL_METHOD_2         2  '2 positional arguments'
              100  LOAD_DEREF               'self'
              102  STORE_ATTR               cur_image_path

 L.  84       104  LOAD_GLOBAL              os
              106  LOAD_METHOD              mkdir
              108  LOAD_DEREF               'self'
              110  LOAD_ATTR                cur_image_path
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          

 L.  85       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              join
              122  LOAD_DEREF               'self'
              124  LOAD_ATTR                cur_image_path
              126  LOAD_FAST                'title'
              128  FORMAT_VALUE          0  ''
              130  LOAD_STR                 '.jpg'
              132  BUILD_STRING_2        2 
              134  CALL_METHOD_2         2  '2 positional arguments'
              136  STORE_FAST               'file_path'

 L.  86       138  LOAD_GLOBAL              util
              140  LOAD_ATTR                save_file
              142  LOAD_FAST                'file_path'
              144  LOAD_FAST                'image'
              146  LOAD_CONST               True
              148  LOAD_CONST               ('binary',)
              150  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              152  GET_AWAITABLE    
              154  LOAD_CONST               None
              156  YIELD_FROM       
              158  POP_TOP          

 L.  87       160  LOAD_GLOBAL              Image
              162  LOAD_METHOD              open
              164  LOAD_FAST                'file_path'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  STORE_FAST               'image_obj'

 L.  88       170  LOAD_GLOBAL              util
              172  LOAD_METHOD              split_image
              174  LOAD_FAST                'image_obj'
              176  LOAD_FAST                'pieces'
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                cur_image_path
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L.  89       186  LOAD_DEREF               'self'
              188  LOAD_METHOD              start_app
              190  CALL_METHOD_0         0  '0 positional arguments'
              192  POP_TOP          

 L.  90       194  LOAD_CLOSURE             'self'
              196  BUILD_TUPLE_1         1 
              198  LOAD_LISTCOMP            '<code_object <listcomp>>'
              200  LOAD_STR                 'SolveImage.solve_by_image.<locals>.<listcomp>'
              202  MAKE_FUNCTION_8          'closure'
              204  LOAD_GLOBAL              range
              206  LOAD_FAST                'pieces'
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  GET_ITER         
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  STORE_FAST               'queries'

 L.  91       216  LOAD_GLOBAL              asyncio
              218  LOAD_ATTR                gather
              220  LOAD_FAST                'queries'
              222  LOAD_STR                 'return_exceptions'
              224  LOAD_CONST               True
              226  BUILD_MAP_1           1 
              228  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              230  GET_AWAITABLE    
              232  LOAD_CONST               None
              234  YIELD_FROM       
              236  STORE_FAST               'results'

 L.  92       238  SETUP_LOOP          274  'to 274'
              240  LOAD_FAST                'results'
              242  GET_ITER         
            244_0  COME_FROM           268  '268'
            244_1  COME_FROM           256  '256'
              244  FOR_ITER            272  'to 272'
              246  STORE_FAST               'r'

 L.  93       248  LOAD_GLOBAL              isinstance
              250  LOAD_FAST                'r'
              252  LOAD_GLOBAL              tuple
              254  CALL_FUNCTION_2       2  '2 positional arguments'
              256  POP_JUMP_IF_FALSE   244  'to 244'
              258  LOAD_FAST                'r'
              260  LOAD_CONST               1
              262  BINARY_SUBSCR    
              264  LOAD_CONST               True
              266  COMPARE_OP               is
              268  POP_JUMP_IF_FALSE   244  'to 244'

 L.  94       270  JUMP_BACK           244  'to 244'
              272  POP_BLOCK        
            274_0  COME_FROM_LOOP      238  '238'

 L.  97       274  LOAD_STR                 'status'
              276  LOAD_STR                 '?'
              278  BUILD_MAP_1           1 
              280  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 272

    async def get_image_url(self):
        image_url = 'document.getElementsByClassName("rc-image-tile-wrapper")[0].getElementsByTagName("img")[0].src'
        return await self.image_frame.evaluate(image_url)

    async def image_no(self):
        return len([i async for i in self.get_images()])

    async def download_image(self):
        image_url = await self.get_image_url()
        return await util.get_page(image_url,
          (self.proxy), (self.proxy_auth), binary=True)

    async def reverse_image_search(self, image_no):
        image_path = f"{self.ip_address}:8080/{image_no}.jpg"
        url = self.url + image_path
        page = await self.browser.newPage()
        await page.goto(url)
        card = await page.querySelector('div.card-section')
        if card:
            best_guess = await page.evaluate('el => el.children[1].innerText', card)
            print(image_no, best_guess)
        else:
            best_guess = ''
        await asyncio.sleep(100)
        await page.close()
        return self.title in best_guess

    def start_app(self):
        Handler.base_path = self.cur_image_path
        httpd = HTTPServer(('0.0.0.0', 8080), Handler)
        threading.Thread(target=(httpd.serve_forever)).start()
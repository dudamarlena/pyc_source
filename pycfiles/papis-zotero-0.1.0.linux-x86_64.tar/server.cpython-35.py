# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/papis_zotero/server.py
# Compiled at: 2019-04-04 21:02:46
# Size of source mod 2**32: 8325 bytes
"""Start a web server listening on port 23119. This server is
compatible with the `zotero connector`. This means that if zotero is
*not* running, you can have items from your web browser added directly
into papis.

"""
import papis_zotero.utils, papis.api, papis.config, papis.document, papis.commands.add, papis.crossref, urllib.request, urllib.error, re, json, logging, tempfile, http.server
logger = logging.getLogger('papis:zotero:server')
logging.basicConfig(filename='', level=logging.INFO)
connector_api_version = 2
zotero_version = '5.0.25'
zotero_port = 23119
papis_translation = {'abstractNote': 'abstract', 
 'publicationTitle': 'journal', 
 'DOI': 'doi', 
 'itemType': 'type', 
 'ISBN': 'isbn'}

def zotero_data_to_papis_data(item):
    """
    {
        'itemType': 'book',
        'language': 'en',
        'shortTitle': 'Nuclear Collective Motion',
        'DOI': '10.1142/6721',
        'accessDate': '2018-07-09T22:57:55Z',
        'extra': 'DOI: 10.1142/6721',
        'creators': [
            {
                'creatorType': 'author',
                'firstName': 'David J',
                'lastName': 'Rowe'
            }
        ],
        'publisher': 'WORLD SCIENTIFIC',
        'ISBN': '9789812790644 9789812790668',
        'url': 'http://www.worldscientific.com/worldscibooks/10.1142/6721',
        'notes': [],
        'seeAlso': [],
        'attachments': [
            {
                'url': 'https://...pdf/10.1103/physrevlett.121.090503',
                'title': 'full text pdf',
                'mimetype': 'application/pdf'
            },
            {
                'url': 'https://...pdf/10.1103/physrevlett.121.090503',
                'title': 'aps snapshot',
                'mimetype': 'text/html'
            }
        ],
        'tags': [],
        'date': '05/2010',
        'libraryCatalog': 'Crossref',
        'title': 'Nuclear Collective Motion: Models and Theory',
        'id': 'SL2sa7hx'
    }
    """
    global logger
    data = {}
    for key in papis_translation.keys():
        if item.get(key):
            data[papis_translation[key]] = item.get(key)
            del item[key]

    if isinstance(item.get('tags'), list):
        try:
            data['tags'] = ' '.join(item['tags'])
        except:
            pass

        del item['tags']
    if item.get('id'):
        del item['id']
    if item.get('attachments'):
        del item['attachments']
    data.update(item)
    if data.get('doi'):
        crossref_data = papis.crossref.doi_to_data(data['doi'])
        if crossref_data.get('title'):
            del crossref_data['title']
        logger.info('Updating also from crossref')
        data.update(crossref_data)
    return data


class PapisRequestHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        logger.info(fmt % args)

    def set_zotero_headers(self):
        self.send_header('X-Zotero-Version', zotero_version)
        self.send_header('X-Zotero-Connector-API-Version', connector_api_version)
        self.end_headers()

    def read_input(self):
        length = int(self.headers['content-length'])
        return self.rfile.read(length)

    def pong(self, POST=True):
        logger.info('pong!')
        if not POST:
            logger.debug('GET request')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.set_zotero_headers()
            response = '            <!DOCTYPE html>\n            <html>\n                <head>\n                    <title>Zotero Connector Server is Available</title>\n                </head>\n                <body>\n                    Zotero Connector Server is Available\n                </body>\n            </html>\n            '
        else:
            logger.debug('POST request')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.set_zotero_headers()
            response = json.dumps({'prefs': {'automaticSnapshots': True}})
        self.wfile.write(bytes(response, 'utf8'))

    def papis_collection(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.set_zotero_headers()
        papis_library = papis.api.get_lib_name()
        response = json.dumps({'libraryID': 1, 
         'libraryName': papis_library, 
         'libraryEditable': True, 
         'editable': True, 
         'id': None, 
         'name': papis_library})
        self.wfile.write(bytes(response, 'utf8'))

    def add(self):
        logger.info('Adding paper from zotero connector')
        rawinput = self.read_input()
        data = json.loads(rawinput.decode('utf8'))
        for item in data['items']:
            files = []
            if item.get('attachments') and len(item.get('attachments')) > 0:
                for attachment in item.get('attachments'):
                    mime = str(attachment.get('mimeType'))
                    logger.info('Checking attachment (mime {0})'.format(mime))
                    if re.match('.*pdf.*', mime):
                        url = attachment.get('url')
                        logger.info("Downloading pdf '{0}'".format(url))
                        try:
                            pdfbuffer = urllib.request.urlopen(url).read()
                        except urllib.error.HTTPError:
                            logger.error('Error downloading pdf, probably you do nothave the rights for the journal.')
                            continue

                        pdfpath = tempfile.mktemp(suffix='.pdf')
                        logger.info("Saving pdf in '{0}'".format(pdfpath))
                        with open(pdfpath, 'wb+') as (fd):
                            fd.write(pdfbuffer)
                        if papis_zotero.utils.is_pdf(pdfpath):
                            files.append(pdfpath)
                        else:
                            logger.error('File retrieved does not appear to be a pdfSo no file will be saved...')

            else:
                logger.warning('Document has no attachments')
            papis_item = zotero_data_to_papis_data(item)
            if len(files) == 0:
                logger.warning('Not adding any attachments...')
            logger.info('Adding paper')
            papis.commands.add.run(files, data=papis_item)

        self.send_response(201)
        self.set_zotero_headers()
        self.wfile.write(rawinput)

    def snapshot(self):
        logger.warning('Snapshot not implemented')
        self.send_response(201)
        self.set_zotero_headers()

    def do_POST(self):
        if self.path == '/connector/ping':
            self.pong()
        else:
            if self.path == '/connector/getSelectedCollection':
                self.papis_collection()
            else:
                if self.path == '/connector/saveSnapshot':
                    self.snapshot()
                elif self.path == '/connector/saveItems':
                    self.add()

    def do_GET(self):
        if self.path == '/connector/ping':
            self.pong(POST=False)
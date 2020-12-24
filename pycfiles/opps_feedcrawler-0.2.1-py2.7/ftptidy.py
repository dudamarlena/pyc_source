# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/opps/feedcrawler/processors/ftptidy.py
# Compiled at: 2014-09-18 10:42:52
import urllib, xml.etree.ElementTree as ET
from ftplib import FTP
from tempfile import NamedTemporaryFile
from django.utils.text import slugify
from base import BaseProcessor
from efe import iptc

class EFEXMLProcessor(BaseProcessor):

    def connect(self):
        self.ftp = FTP(self.feed.source_url)
        self.ftp.login(self.feed.source_username, self.feed.source_password)
        self.verbose_print(self.ftp.getwelcome())
        return self.ftp

    def get_temp_file(self):
        f = NamedTemporaryFile(delete=True)
        self.verbose_print('%s tempfile created' % f.name)
        return f

    def process_file(self, s):
        self.verbose_print('-' * 78)
        if self.log_model.objects.filter(type='created', text=s, feed=self.feed).exists():
            self.verbose_print('%s already exists, skipping.' % s)
            return
        s = s.strip()
        s = s.replace('\n', '')
        ext = s.split('.')[(-1)]
        if ext not in ('XML', 'xml'):
            self.verbose_print('Skipping non xml %s' % s)
            return
        self.verbose_print('Retrieving file %s' % s)
        source_root_folder = self.feed.source_root_folder
        if not source_root_folder.endswith('/'):
            source_root_folder += '/'
        url = ('ftp://{0}:{1}@{2}{3}{4}').format(self.feed.source_username, self.feed.source_password, self.feed.source_url, source_root_folder, s)
        self.verbose_print(url)
        f = self.get_temp_file()
        try:
            urllib.urlretrieve(url, filename=f.name)
            self.verbose_print('File retrieved successfully')
        except Exception as e:
            self.verbose_print('error urlretrieve')
            self.verbose_print(str(e))
            return

        try:
            xml_string = f.read()
            self.verbose_print('xml_string read!')
        except Exception as e:
            self.verbose_print('error f.read')
            self.verbose_print(str(e))
            return

        if not xml_string:
            self.verbose_print('XML Empty')
            f.close()
            return
        data = self.parse_xml(f.name)
        data = self.categorize(data)
        self.verbose_print(str(data))
        f.close()
        created = self.create_entry(data)
        if created:
            self.record_log(s)

    def parse_xml(self, filename):
        data = {}
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
        except:
            return

        try:
            data['headline'] = root.find('./NewsItem/NewsComponent/NewsLines/HeadLine').text
            data['subheadline'] = root.find('./NewsItem/NewsComponent/NewsLines/SubHeadLine').text
        except:
            pass

        try:
            tobject_attrib = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/head/tobject/tobject.subject')
            data['iptc_code'] = tobject_attrib.get('tobject.subject.refnum')
            data['iptc_matter'] = tobject_attrib.get('tobject.subject.matter')
            data['iptc_type'] = tobject_attrib.get('tobject.subject.type')
        except:
            pass

        try:
            pub_data_attrib = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/head/pubdata')
            data['pub_date'] = pub_data_attrib.get('date.publication')
            data['item_len'] = pub_data_attrib.get('item-length')
        except:
            pass

        try:
            data['abstract'] = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.head/abstract/').text
        except:
            pass

        try:
            data['owner'] = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.head/rights/').text
        except:
            pass

        try:
            data['story_data'] = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.head/dateline/story.date').get('norm')
        except:
            pass

        try:
            body = root.find('./NewsItem/NewsComponent/ContentItem/DataContent/nitf/body/body.content')
            data['body'] = ('\n').join(('<p>{0}</p>').format(p.text) for p in body.getchildren())
        except:
            pass

        if not all([data.get('body'), data.get('headline')]):
            self.verbose_print('Data does not have body and headline %s' % str(data))
            return
        return data

    def create_entry(self, data):
        if not data:
            self.verbose_print('data is null')
            return
        try:
            db_entry, created = self.entry_model.objects.get_or_create(entry_feed=self.feed, channel=self.feed.channel, title=entry_title[:140], slug=slugify(entry_title[:150]), entry_title=entry_title, site=self.feed.site, user=self.feed.user, published=True, show_on_root_channel=True)
        except Exception as e:
            self.verbose_print(str(data))
            self.verbose_print(str(e))

    def categorize(self, data):
        if not data.get('iptc_code'):
            self.verbose_print('No iptc code to categorize')
            return data
        else:
            iptc_info = iptc.get(data['iptc_code'])
            if iptc_info:
                data.update(iptc_info)
            else:
                data['parent_desc'] = data.get('iptc_type')
                data['desc'] = data.get('iptc_matter')
                data['cod'] = data['iptc_code']
                data['parent'] = None
                data['cat'] = None
            return data

    def record_log(self, s):
        self.log_model.objects.create(feed=self.feed, type='created', text=s)

    def process(self):
        self.connect()
        self.ftp.cwd(self.feed.source_root_folder)
        self.verbose_print('Root folder changed to: %s' % self.feed.source_root_folder)
        self.count = 0
        self.ftp.retrlines('NLST', self.process_file)


{'story_data': '20130712T192900+0000', 
   'body': '<p>Montevidéu, 12 jul (EFE).- Os países do Mercosul decidiram nesta sexta-feira em sua cúpula semestral no Uruguai revogar a partir do dia 15 de agosto a suspensão do Paraguai, uma vez que Horacio Cartes assuma a presidência do país.</p>\n<p>Após "avaliar positivamente" a realização das eleições gerais no Paraguai no último dia 21 de abril, os presidentes de Brasil, Dilma Rousseff; Argentina, Cristina Kirchner; Uruguai, José Mujica; e Venezuela, Nicolás Maduro, decidiram "cessar" a suspensão imposta no dia 29 de junho de 2012 devido à cassação por parte do Parlamento paraguaio do então presidente Fernando Lugo.</p>\n<p>A partir da posse do novo governo paraguaio "serão considerados cumpridos" os requisitos estabelecidos no artigo 7 do Protocolo de Ushuaia sobre o compromisso democrático.</p>\n<p>A partir do próximo mês, o Paraguai "reassumirá plenamente seu direito de participar dos órgãos do Mercosul e das deliberações", informa a declaração dos líderes.</p>\n<p>As autoridades do Paraguai, o quinto integrante do Mercado Comum do Sul, não participam da reunião. EFE</p>\n<p>jf/rsd</p>', 
   'item_len': '00166', 
   'iptc_matter': 'Organismos internacionais', 
   'headline': 'Mercosul revogará suspensão do Paraguai a partir de 15 de agosto', 
   'iptc_code': '11014000', 
   'iptc_type': 'Política', 
   'subheadline': 'MERCOSUL CÚPULA', 
   'owner': 'Agencia EFE', 
   'pub_date': '20130712T192900+0000', 
   'abstract': 'Os países do Mercosul decidiram nesta sexta-feira em sua cúpula semestral no Uruguai revogar a partir do dia 15 de agosto a suspensão do Paraguai, uma vez que Horacio Cartes assuma a presidência do país.'}
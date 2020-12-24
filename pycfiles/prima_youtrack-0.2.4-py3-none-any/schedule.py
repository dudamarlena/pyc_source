# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/scraper/primaverasound/schedule.py
# Compiled at: 2013-03-15 15:17:05
__doc__ = 'Copyright [2012] [Ricardo García Fernández] [ricarodgarfe@gmail.com]\n\n   Licensed under the Apache License, Version 2.0 (the "License");\n   you may not use this file except in compliance with the License.\n   You may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\n   Unless required by applicable law or agreed to in writing, software\n   distributed under the License is distributed on an "AS IS" BASIS,\n   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n   See the License for the specific language governing permissions and\n   limitations under the License.\n\n'
import requests, lxml.html

class Schedule(object):

    def __init__(self):
        self.conciertos = {}
        api_url = 'http://www.primaverasound.es/programacion'
        config_req = requests.get(api_url)
        config_tree = lxml.html.fromstring(config_req.content)
        dls = config_tree.xpath('//*[@id="page-wrap"]/div[4]/div[2]/dl/dt')
        dds = config_tree.xpath('//*[@id="page-wrap"]/div[4]/div[2]/dl/dd')
        self.dia = 20
        self.anyo = 2013
        self.mes = 5
        self.horarios = []
        self.parse_horarios(dls, dds)

    def parse_horarios(self, dls, dds):
        map(self.parse_horario_dia, dls, dds)

    def parse_horario_dia(self, dl, dd):
        """ dl child
        <a href="#">Lunes 20 de mayo</a>
        """
        dia = dl.find('a')
        dia = clean(text(dia))
        fecha = self.fecha_concierto()
        self.dia += 1
        table_header = dd.find('div/table/thead/tr')
        columns_header = table_header.findall('th')
        conciertos = []
        table_contents = dd.findall('div/table/tbody/tr')
        for artist_data in table_contents:
            concierto = {}
            artist_td_content = artist_data.find('td[1]')
            artist_content = artist_td_content.find('a')
            concierto[columns_header[0].text] = clean(text(artist_content))
            artist_sala = artist_data.find('td[2]')
            concierto[columns_header[1].text] = clean(text(artist_sala))
            artist_hora = artist_data.find('td[3]')
            concierto[columns_header[2].text] = clean(text(artist_hora))
            concierto_id = str(artist_content.attrib['href']).rsplit('=')[1:][0]
            concierto['id'] = concierto_id
            concierto['dia'] = fecha
            conciertos.append(concierto)

        self.horarios.append({'horario': [dia, conciertos]})

    def fecha_concierto(self):
        return str(self.anyo) + '-' + str(self.mes) + '-' + str(self.dia)


def text(element):
    return lxml.html.tostring(element, method='text', encoding=unicode)


def clean(string):
    return string.strip().encode('utf-8')
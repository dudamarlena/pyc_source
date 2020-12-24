# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/DesktopFiles/PROJECTS/DSVISUALIZER/dataspectra/aefiles/scripts/main_page.py
# Compiled at: 2018-02-15 19:15:05
import os, urllib, jinja2, webapp2, base64, load_parameters as LP, query_data as QD, json, load_funcs as LF, upload_datasets as UD, password as PW

class MainPage(webapp2.RequestHandler):

    @PW.basicAuth
    def get(self):
        template_values = LP.siteJsonData
        template_values.update({'siteJsonVal': json.dumps(LP.siteJsonData)})
        defaultSearchTerm = LP.siteJsonData['defaultterm']
        template_values['clickedButtonKey'] = template_values['defaultpanel']
        template_values = fill_in_template_values(template_values, defaultSearchTerm)
        template_values['searchTerm'] = defaultSearchTerm
        template = LP.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Search(webapp2.RequestHandler):

    def post(self):
        template_values = LP.siteJsonData
        template_values.update({'siteJsonVal': json.dumps(LP.siteJsonData)})
        queryIn = self.request.get('searchTerm')
        template_values['clickedButtonKey'] = self.request.get('clickedButton')
        template_values['searchTerm'] = queryIn
        template_values = fill_in_template_values(template_values, queryIn)
        template = LP.JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


def fill_in_template_values(template_values, searchTerm):
    dataJson = QD.extract_data_for_term(searchTerm, LP.datasetModelDict, LP.searchlookupDict)
    data_template_values = {'dataJsonVal': json.dumps(dataJson)}
    template_values.update(data_template_values)
    figureJson = LF.json_load_byteified(open('static/figures.json'))
    figure_template_values = {'figureJsonVal': json.dumps(figureJson)}
    template_values.update(figure_template_values)
    datasetJson = LF.json_load_byteified(open('static/datasets.json'))
    dataset_template_values = {'datasetJsonVal': json.dumps(datasetJson)}
    template_values.update(dataset_template_values)
    sidebarJson = LF.json_load_byteified(open('static/sidebar.json'))
    buttonKeyNames = [ [x[2], x[1]] for x in sidebarJson if x[0] == 'BUTTON' ]
    sidebar_template_values = {'sidebarJsonVal': json.dumps(sidebarJson), 
       'buttonKeyNames': buttonKeyNames}
    template_values.update(sidebar_template_values)
    panelJson = LF.json_load_byteified(open('static/panels.json'))
    panel_template_values = {'panelJsonVal': json.dumps(panelJson)}
    template_values.update(panel_template_values)
    densityDict = dict()
    for i in figureJson:
        if figureJson[i]['figuretype'] == 'density':
            data = LF.read_csv('static/' + figureJson[i]['densityfile'])
            densityDict[i] = dict()
            densityDict[i]['percentile'] = data[0]
            densityDict[i]['density'] = data[1:]

    density_template_values = {'densityDictVal': json.dumps(densityDict)}
    template_values.update(density_template_values)
    searchMetaList = list()
    for i in figureJson:
        for j in figureJson[i]['paramList']:
            if 'meta' in j[3]:
                searchTerm = j[3].split('meta.')[1]
                metakey = figureJson[i]['metakey']
                if (searchTerm, metakey) not in searchMetaList:
                    searchMetaList.append([searchTerm, metakey])

    metaDataDict = dict()
    for i in searchMetaList:
        searchTerm, metakey = i[0], i[1]
        data = QD.extract_data_for_term_and_dataset(searchTerm, LP.datasetModelDict, metakey)
        metaDataDict[metakey + '.' + searchTerm] = data

    meta_data_template_values = {'metaDataDictVal': json.dumps(metaDataDict)}
    template_values.update(meta_data_template_values)
    return template_values


class AuthTest(webapp2.RequestHandler):

    @PW.basicAuth
    def get(self):
        self.response.write('Toodles')


app = webapp2.WSGIApplication([
 (
  '/', MainPage),
 (
  '/search', Search),
 (
  '/loadLocal', UD.LocalUploadDatastore)], debug=True)
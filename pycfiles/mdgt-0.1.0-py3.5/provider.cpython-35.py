# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mdgt\provider.py
# Compiled at: 2016-10-17 15:09:43
# Size of source mod 2**32: 4769 bytes


class Provider:
    __doc__ = 'Providers parse microdata using XPath rules\n\n    The provider class loads a provider file and then uses the rules contained\n    within to retrieve a search query from the internet and then parse the\n    microdata.\n    '

    def __init__(self, name, provider_dir=None):
        """Loads a provider.
        The method will search to providers directory for a file [name].json to
        load.

        Args:
            name (str): The name of the provider to load.
            provider_dir (str): Directory in which to search for providers.
        """
        import json
        self.name = name
        p = self._find_provider(name, provider_dir)
        if not p or not p.exists():
            raise RuntimeError('Provider ' + name + ' does not exist.')
        with p.open() as (f):
            self.modJson = json.loads(f.read())

    def _find_provider(self, name, provider_dir=None):
        """Tries to find a provider file in different locations.

        Args:
            name (str): The name of the provider to search for.

        Returns:
            A Path object if the provider file is found or None otherwise.
        """
        from pathlib import Path
        from pkg_resources import resource_filename
        if provider_dir:
            file_path = Path(provider_dir + '/' + name + '.json')
            if file_path.exists():
                pass
            return file_path
        file_path = Path('./providers/' + name + '.json')
        if file_path.exists():
            return file_path
        package_dir = resource_filename(__name__, 'providers')
        file_path = Path(package_dir + '/' + name + '.json')
        if file_path.exists():
            return file_path

    def scrape(self, query):
        """Uses the loaded provider to scrape and parse microdata.

        Args:
            query (str): The query string the provider will use to search for
            relevant microdata.

        Returns:
            A dict object containing the scraped information.
        """
        from lxml import html
        import requests
        search = self.modJson['search']
        uriSearch = search['uriRoot'] + search['searchPath'].replace('*', query)
        page = requests.get(uriSearch)
        tree = html.fromstring(page.content)
        if 'firstResultXpath' in search:
            resNode = tree.xpath(search['firstResultXpath'])[0]
            resUri = resNode.get('href')
            if resUri[0] == '/':
                resUri = search['uriRoot'] + resUri
            page = requests.get(resUri)
            tree = html.fromstring(page.content)
        data = dict()
        Provider.parse_node(tree, self.modJson['root'], data)
        return data

    def parse_node(parentTree, modNode, dataDict):
        """Recursively parses and lxml node.

        Args:
            parentTree (etree): The lxml etree object to be parsed.
            modNode (dict): The node from the json file containing the current
                node's parsing rules.
            dataDict (dict): The dict containing all parsed information.
        """
        from lxml import html, etree
        dataList = []
        tree = parentTree.xpath(modNode['xpath'])
        if 'repeat' not in modNode or not modNode['repeat']:
            tree = tree[0:1]
        for t in tree:
            if 'value' in modNode:
                val = modNode['value']
                if val['type'] == 'text':
                    dataList.append(t.text.strip())
                else:
                    if val['type'] == 'striptext':
                        ts = etree.tostring(t, method='text').decode('utf-8')
                        dataList.append(ts.strip())
                    elif val['type'] == 'attr':
                        dataList.append(t.get(val['attr']))
                if len(dataList) == 1:
                    dataDict[val['name']] = dataList[0]
                else:
                    if len(dataList) > 1:
                        dataDict[val['name']] = dataList
                    if 'items' in modNode:
                        for i in modNode['items']:
                            Provider.parse_node(t, i, dataDict)
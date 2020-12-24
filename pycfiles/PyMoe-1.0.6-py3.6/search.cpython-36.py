# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Anilist\search.py
# Compiled at: 2018-06-02 11:59:52
# Size of source mod 2**32: 9178 bytes
import json, requests

class ASearch:

    def __init__(self, settings):
        self.settings = settings

    def character(self, term, page=1, perpage=3):
        """
        Search for a character by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.
        
        :param term str: Name to search by
        :param page int: Which page are we requesting? Starts at 1.
        :param perpage int: How many results per page are we requesting?
        :return: Json object with returned results.
        :rtype: Json object with returned results.
        """
        query_string = '            query ($query: String, $page: Int, $perpage: Int) {\n                Page (page: $page, perPage: $perpage) {\n                    pageInfo {\n                        total\n                        currentPage\n                        lastPage\n                        hasNextPage\n                    }\n                    characters (search: $query) {\n                        id\n                        name {\n                            first\n                            last\n                        }\n                        image {\n                            large\n                        }\n                    }\n                }\n            }\n        '
        vars = {'query':term,  'page':page,  'perpage':perpage}
        r = requests.post((self.settings['apiurl']), headers=(self.settings['header']),
          json={'query':query_string, 
         'variables':vars})
        jsd = r.text
        try:
            jsd = json.loads(jsd)
        except ValueError:
            return
        else:
            return jsd

    def anime(self, term, page=1, perpage=3):
        """
        Search for an anime by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.
        
        :param term str: Name to search by
        :param page int: Which page are we requesting? starts at 1.
        :param perpage int: How many results per page? defaults to 3.
        :return: List of dictionaries which are anime objects or None
        :rtype: list of dict or NoneType
        """
        query_string = '            query ($query: String, $page: Int, $perpage: Int) {\n                Page (page: $page, perPage: $perpage) {\n                    pageInfo {\n                        total\n                        currentPage\n                        lastPage\n                        hasNextPage\n                    }\n                    media (search: $query, type: ANIME) {\n                        id\n                        title {\n                            romaji\n                            english\n                        }\n                        coverImage {\n                            large\n                        }\n                        averageScore\n                        popularity\n                        episodes\n                        season\n                        hashtag\n                        isAdult\n                    }\n                }\n            }\n        '
        vars = {'query':term,  'page':page,  'perpage':perpage}
        r = requests.post((self.settings['apiurl']), headers=(self.settings['header']),
          json={'query':query_string, 
         'variables':vars})
        jsd = r.text
        try:
            jsd = json.loads(jsd)
        except ValueError:
            return
        else:
            return jsd

    def manga(self, term, page=1, perpage=3):
        """
        Search for a manga by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.
        
        :param term str: Name to search by
        :param page int: Which page are we requesting? Starts at 1.
        :param perpage int: How many results per page? defaults to 3.
        :return: List of dictionaries which are manga objects or None
        :rtype: list of dict or NoneType
        """
        query_string = '            query ($query: String, $page: Int, $perpage: Int) {\n                Page (page: $page, perPage: $perpage) {\n                    pageInfo {\n                        total\n                        currentPage\n                        lastPage\n                        hasNextPage\n                    }\n                    media (search: $query, type: MANGA) {\n                        id\n                        title {\n                            romaji\n                            english\n                        }\n                        coverImage {\n                            large\n                        }\n                        averageScore\n                        popularity\n                        chapters\n                        volumes\n                        season\n                        hashtag\n                        isAdult\n                    }\n                }\n            }\n        '
        vars = {'query':term,  'page':page,  'perpage':perpage}
        r = requests.post((self.settings['apiurl']), headers=(self.settings['header']),
          json={'query':query_string, 
         'variables':vars})
        jsd = r.text
        try:
            jsd = json.loads(jsd)
        except ValueError:
            return
        else:
            return jsd

    def staff(self, term, page=1, perpage=3):
        """
        Search for staff by term. Staff means actors, directors, etc.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.
        
        :param term str: Name to search by
        :param page int: What page are we requesting? Starts at 1.
        :param perpage int: How many results per page? Defaults to 3.
        :return: List of dictionaries which are staff objects or None
        :rtype: list of dict or NoneType
        """
        query_string = '            query ($query: String, $page: Int, $perpage: Int) {\n                Page (page: $page, perPage: $perpage) {\n                    pageInfo {\n                        total\n                        currentPage\n                        lastPage\n                        hasNextPage\n                    }\n                    staff (search: $query) {\n                        id\n                        name {\n                            first\n                            last\n                        }\n                        image {\n                            large\n                        }\n                    }\n                }\n            }\n        '
        vars = {'query':term,  'page':page,  'perpage':perpage}
        r = requests.post((self.settings['apiurl']), headers=(self.settings['header']),
          json={'query':query_string, 
         'variables':vars})
        jsd = r.text
        try:
            jsd = json.loads(jsd)
        except ValueError:
            return
        else:
            return jsd

    def studio(self, term, page=1, perpage=3):
        """
        Search for a studio by term.
        Results are paginated by default. Page specifies which page we're on.
        Perpage specifies how many per page to request. 3 is just the example from the API docs.
        
        :param term str: Name to search by
        :param page int: What page are we requesting? starts at 1.
        :param perpage int: How many results per page? defaults to 3.
        :return: List of dictionaries which are studio objects or None
        :rtype: list of dict or NoneType
        """
        query_string = '            query ($query: String, $page: Int, $perpage: Int) {\n                Page (page: $page, perPage: $perpage) {\n                    pageInfo {\n                        total\n                        currentPage\n                        lastPage\n                        hasNextPage\n                    }\n                    studios (search: $query) {\n                        id\n                        name\n                    }\n                }\n            }\n        '
        vars = {'query':term,  'page':page,  'perpage':perpage}
        r = requests.post((self.settings['apiurl']), headers=(self.settings['header']),
          json={'query':query_string, 
         'variables':vars})
        jsd = r.text
        try:
            jsd = json.loads(jsd)
        except ValueError:
            return
        else:
            return jsd
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Anilist\get.py
# Compiled at: 2018-03-02 17:53:54
# Size of source mod 2**32: 7516 bytes
import json, requests

class AGet:

    def __init__(self, settings):
        self.settings = settings

    def anime(self, item_id):
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        query_string = '            query ($id: Int) {\n                Media(id: $id, type: ANIME) {\n                    title {\n                        romaji\n                        english\n                    }\n                    startDate {\n                        year\n                        month\n                        day\n                    }\n                    endDate {\n                        year\n                        month\n                        day\n                    }\n                    coverImage {\n                        large\n                    }\n                    bannerImage\n                    format\n                    status\n                    episodes\n                    season\n                    description\n                    averageScore\n                    meanScore\n                    genres\n                    synonyms\n                    nextAiringEpisode {\n                        airingAt\n                        timeUntilAiring\n                        episode\n                    }\n                }\n            }\n        '
        vars = {'id': item_id}
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

    def manga(self, item_id):
        """
        The function to retrieve an anime's details.

        :param int item_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        query_string = '            query ($id: Int) {\n                Media(id: $id, type: MANGA) {\n                    title {\n                        romaji\n                        english\n                    }\n                    startDate {\n                        year\n                        month\n                        day\n                    }\n                    endDate {\n                        year\n                        month\n                        day\n                    }\n                    coverImage {\n                        large\n                    }\n                    bannerImage\n                    format\n                    chapters\n                    volumes\n                    status\n                    description\n                    averageScore\n                    meanScore\n                    genres\n                    synonyms\n                }\n            }\n        '
        vars = {'id': item_id}
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

    def staff(self, item_id):
        """
        The function to retrieve a manga's details.

        :param int item_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        query_string = '            query ($id: Int) {\n                Staff(id: $id) {\n                    name {\n                        first\n                        last\n                        native\n                    }\n                    description\n                    language\n                }\n            }\n        '
        vars = {'id': item_id}
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

    def studio(self, item_id):
        """
        The function to retrieve a studio's details.

        :param int item_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        query_string = '            query ($id: Int) {\n                Studio(id: $id) {\n                    name\n                }\n            }\n        '
        vars = {'id': item_id}
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

    def character(self, item_id):
        """
        The function to retrieve a character's details.

        :param int item_id: the anime's ID
        :return: dict or None
        :rtype: dict or NoneType
        """
        query_string = '            query ($id: Int) {\n                Character (id: $id) {\n                    name {\n                        first\n                        last\n                        native\n                    }\n                    description\n                    image {\n                        large\n                    }\n                }\n            }\n        '
        vars = {'id': item_id}
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

    def review(self, item_id, html=True):
        """
        With the change to v2 of the api, reviews have their own IDs. This accepts the ID of the review.
        You can set html to False if you want the review body returned without html formatting.
        The API Default is true.

        :param item_id: the Id of the review
        :param html: do you want the body returned with html formatting?
        :return: json object
        :rtype: json object containing review information
        """
        query_string = '            query ($id: Int, $html: Boolean) {\n                Review (id: $id) {\n                    summary\n                    body(asHtml: $html)\n                    score\n                    rating\n                    ratingAmount\n                    createdAt\n                    updatedAt\n                    private\n                    media {\n                        id\n                    }\n                    user {\n                        id\n                        name\n                        avatar {\n                            large\n                        }\n                    }\n                }\n            }\n        '
        vars = {'id':item_id,  'html':html}
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
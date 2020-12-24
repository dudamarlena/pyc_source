# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pelock\aztecdecoder.py
# Compiled at: 2016-08-08 18:04:20
# Size of source mod 2**32: 3444 bytes
import struct, io, json, requests

class AZTecDecoder(object):
    API_URL = 'https://www.pelock.com/api/aztec-decoder/v1'
    _api_key = ''

    def __init__(self, api_key):
        """Inicjalizacja klasy AZTecDecoder

        :param api_key: Klucz do uslugi WebApi
        """
        self._api_key = api_key

    def decode_text(self, text):
        """Dekodowanie zaszyfrowanej wartosci tekstowej do
           wyjsciowej tablicy w formacie JSON.

        :param text: Odczytana wartosc z kodem AZTEC2D w formie ASCII
        :return Rozkodowana tablica elementow JSON lub None jesli blad
        :rtype object
        """
        params = {'command': 'decode-text', 'text': text}
        return self.post_request(params)

    def decode_text_from_file(self, text_file_path):
        """Dekodowanie zaszyfrowanej wartosci tekstowej
           ze wskaznego pliku do wyjsciowej tablicy z
           formatu JSON.

        :param text_file_path: Sciezka do pliku z odczytana wartoscia kodu AZTEC2D
        :return Rozkodowana tablica elementow JSON lub None jesli blad
        :rtype object
        """
        with open(text_file_path, 'r') as (f):
            text = f.read()
            if text:
                return self.decode_text(text)

    def decode_image_from_file(self, image_file_path):
        """Dekodowanie zaszyfrowanej wartosci zakodowanej
           w obrazku PNG lub JPG/JPEG do wyjsciowej tablicy
           w formacie JSON.

        :param image_file_path: Sciezka do obrazka z kodem AZTEC2D
        :return Rozkodowana tablica elementow JSON lub None jesli blad
        :rtype object
        """
        params = {'command': 'decode-image', 'image': image_file_path}
        return self.post_request(params)

    def post_request(self, params_array):
        """Wysyla zapytanie POST do serwera WebApi

        :param params_array: Tablica z parametrami dla zapytania POST
        :return: Rozkodowana tablica elementow JSON lub None jesli blad
        :rtype: object
        """
        if not self._api_key:
            return
        else:
            params_array['key'] = self._api_key
            if 'image' in params_array:
                files = {'image': open(params_array['image'], 'rb')}
                params_array.pop('image', None)
                response = requests.post(self.API_URL, files=files, data=params_array)
            else:
                response = requests.post(self.API_URL, data=params_array)
            if response and response.ok:
                return json.loads(response.text)
            return
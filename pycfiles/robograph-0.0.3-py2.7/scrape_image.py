# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/scrape_image.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import graph
from robograph.datamodel.nodes.lib import files, value, http

def scraper_image(img_url, target_path):
    url = value.Value(value=img_url)
    client = http.Get(mime_type='image/png')
    writer = files.BinaryFileWriter(filepath=target_path)
    g = graph.Graph('scrape_image', [url, client, writer])
    g.connect(writer, client, 'data')
    g.connect(client, url, 'url')
    return g
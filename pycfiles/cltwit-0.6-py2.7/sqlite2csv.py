# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/sqlite2csv.py
# Compiled at: 2013-02-01 18:07:17
"""
Exporte le contenu d'une base sqlite en csv (encodage utf-8)

import sqlite3
# Requête des données à exporter
c.execute('select champ1, champ2, champ3 from table')
# On appelle la classe sqlite2csv qui se charge de l'export
export = sqlite2csv(open(FICHIER.csv, "wb"))
# Entête du fichier csv
export.writerow(["Champ1", "Champ2", "Champ3"])
# Lignes du fichier csv
export.writerows(c)
# On ferme la connexion sqlite et le curseur
c.close
conn.close
"""
import csv, codecs, cStringIO

class sqlite2csv:

    def __init__(self, f, dialect=csv.excel, encoding='utf-8', **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([ unicode(s).encode('utf-8') for s in row ])
        data = self.queue.getvalue()
        data = data.decode('utf-8')
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
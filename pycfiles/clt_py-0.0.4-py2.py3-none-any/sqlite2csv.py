# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/sqlite2csv.py
# Compiled at: 2013-02-01 18:07:17
__doc__ = '\nExporte le contenu d\'une base sqlite en csv (encodage utf-8)\n\nimport sqlite3\n# Requête des données à exporter\nc.execute(\'select champ1, champ2, champ3 from table\')\n# On appelle la classe sqlite2csv qui se charge de l\'export\nexport = sqlite2csv(open(FICHIER.csv, "wb"))\n# Entête du fichier csv\nexport.writerow(["Champ1", "Champ2", "Champ3"])\n# Lignes du fichier csv\nexport.writerows(c)\n# On ferme la connexion sqlite et le curseur\nc.close\nconn.close\n'
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
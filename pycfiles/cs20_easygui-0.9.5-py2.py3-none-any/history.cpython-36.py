# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/benjaminrafetto/Code/cs207/cs207-FinalProject/build/lib/kinetics/history.py
# Compiled at: 2017-12-11 01:09:29
# Size of source mod 2**32: 6482 bytes
import time, pymysql

class History:

    def __init__(self, filename, reactions_set, T, X, rr):
        self.filename = filename
        self.reactions = reactions_set.reactions
        self.species = reactions_set.species
        self.T = T
        self.X = X
        self.rr = rr
        self.host = 'cs207reactions.cuj7kddh2nbn.us-east-1.rds.amazonaws.com'
        self.port = 3306
        self.dbname = 'cs207reactions'
        self.user = 'rafettob'
        self.password = 'cs207g72017'
        self.db = pymysql.connect((self.host), user=(self.user), port=(self.port), passwd=(self.password), db=(self.dbname))

    def write(self):
        cursor = self.db.cursor()
        created_at = time.strftime('%Y-%m-%d %H:%M:%S')
        self.reaction_set_id = self.write_reaction_set(cursor, created_at)
        self.process_reactions(cursor, created_at, self.reaction_set_id)

    def process_reactions(self, cursor, timestamp, reaction_set_id):
        for i, (_, reaction) in enumerate(self.reactions.items()):
            reaction_type = reaction['type']
            reversibility = reaction['reversible']
            equation = reaction['equation']
            coeff_params = reaction['coeff_params']
            v1, v2 = str(reaction['v1']), str(reaction['v2'])
            self.write_reaction(cursor, timestamp, reaction_set_id, reaction_type=reaction_type, reversibility=reversibility, equation=equation,
              coeff_params=coeff_params,
              v1=v1,
              v2=v2)

    def write_reaction_set(self, cursor, timestamp):
        cursor.execute('CREATE TABLE IF NOT EXISTS reaction_set (\n\t\t    reaction_set_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,\n\t\t    filename INT NOT NULL,\n\t\t    num_reactions INTEGER NOT NULL,\n\t\t    species TEXT NOT NULL,\n\t\t    concentration TEXT NOT NULL,\n\t\t    T REAL NOT NULL,\n\t\t    reaction_rate TEXT NOT NULL,\n\t\t    createdAt DATETIME NOT NULL)')
        vals_to_insert = (
         self.filename, len(self.reactions), str(self.species),
         str(self.X), self.T, str(self.rr), timestamp)
        cursor.execute('INSERT INTO reaction_set (filename, num_reactions, \n\t\t\t\t\t   species, concentration, T, reaction_rate, createdAt) \n\t\t\t\t\t   VALUES (%s, %s, %s, %s, %s, %s, %s)', vals_to_insert)
        self.db.commit()
        return cursor.lastrowid

    def write_reaction(self, cursor, timestamp, reaction_set_id, **kwargs):
        cursor.execute('CREATE TABLE IF NOT EXISTS reaction (\n\t\t    reaction_id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,\n\t\t    reaction_set_id INTEGER NOT NULL,\n\t\t    type TEXT NOT NULL, \n\t\t    reversibility BIT NOT NULL, \n\t\t    equation TEXT NOT NULL, \n\t\t    coeff_params TEXT NOT NULL,\n\t\t    v1 TEXT NOT NULL,\n\t\t    v2 TEXT NOT NULL,\n\t\t    createdAt DATETIME NOT NULL)')
        coeff_params, reaction_type, reversibility, equation, v1, v2 = (
         kwargs['coeff_params'], kwargs['reaction_type'],
         kwargs['reversibility'], kwargs['equation'], kwargs['v1'], kwargs['v2'])
        vals_to_insert = (
         reaction_set_id, reaction_type, reversibility, equation,
         str(coeff_params), v1, v2, timestamp)
        cursor.execute('INSERT INTO reaction (reaction_set_id, type, \n\t\t\t\t\t   reversibility, equation, coeff_params, v1, v2, createdAt) \n\t\t\t\t\t   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', vals_to_insert)
        self.db.commit()


class HistoryReader:

    def __init__(self):
        self.host = 'cs207reactions.cuj7kddh2nbn.us-east-1.rds.amazonaws.com'
        self.port = 3306
        self.dbname = 'cs207reactions'
        self.user = 'rafettob'
        self.password = 'cs207g72017'
        self.db = pymysql.connect((self.host), user=(self.user), port=(self.port), passwd=(self.password), db=(self.dbname))

    def getCursor(self):
        if not self.db.open:
            self.db = pymysql.connect((self.host), user=(self.user), port=(self.port), passwd=(self.password), db=(self.dbname))
        return self.db.cursor()

    def buildQueriesFromDict(self, dictionary):
        query = ''
        constraints = []
        species = dictionary['species']
        if species != None:
            if type(species) is not list:
                species = [
                 species]
            for specie in list(species):
                constraints.append("species LIKE '%{}%'".format(specie))

        temp = dictionary['temp']
        if temp is not None:
            constraints.append('T {} {}'.format(temp['cmp'], temp['T']))
        reversible = dictionary['type']
        if reversible is not None:
            if reversible == 'reversible' or reversible == 'non_reversible':
                query_set = 'SELECT DISTINCT reaction_set_id FROM reaction ' + 'WHERE reversibility = {}'.format(reversible == 'reversible')
                constraints.append('A.reaction_set_id IN ({})'.format(query_set))
        for i, constraint in enumerate(constraints):
            if i == 0:
                query += ' WHERE ' + constraint
            else:
                query += ' AND ' + constraint

        query_sets = 'SELECT * FROM reaction_set A ' + query
        query_reactions = 'SELECT B.* FROM reaction_set A LEFT JOIN reaction B ON A.reaction_set_id = B.reaction_set_id' + query
        return (
         query_sets, query_reactions)

    def queryDatabase(self, dictionary):
        query1, query2 = self.buildQueriesFromDict(dictionary)
        cursor = self.getCursor()
        cursor.execute(query1)
        A = cursor.fetchall()
        cursor.execute(query2)
        B = cursor.fetchall()
        return (
         A, B)


def testDatabaseQuery():
    hr = HistoryReader()
    queryDict = {'species':None,  'temp':None,  'type':None}
    queryDict['type'] = 'non_reversible'
    result1, result2 = hr.queryDatabase(queryDict)
    print(result1)


if __name__ == '__main__':
    testDatabaseQuery()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/pyniall_sqlite.py
# Compiled at: 2011-04-22 06:35:42
""" a simple markov-chain ki implementation with sqlite backend """
import random, sqlite, os

class pyNiall:

    def __init__(self, dbname):
        if not os.path.exists(dbname):
            init_db(dbname)
        self.db = sqlite.connect(dbname)
        self.cur = self.db.cursor()

    def _addRelation(self, word1, word2):
        """
            adds a relation between word1 and word2

            add a relation, that word1 can be followed by word2

            @param word1: the first word
            @type word1: string
            @param word2: the second word
            @type word2: string
        """
        self.cur.execute('SELECT id FROM words WHERE word=%s', [word1])
        index1 = self.cur.fetchall()[0][0]
        self.cur.execute('SELECT id FROM words WHERE word=%s', [word2])
        result = self.cur.fetchall()
        if len(result):
            index2 = result[0][0]
        else:
            self.cur.execute('INSERT INTO words VALUES (null, %s)', [word2])
            index2 = self.cur.lastrowid
        self.cur.execute('SELECT ranking FROM relations WHERE word1_id=%s AND word2_id=%s', (
         index1, index2))
        result = self.cur.fetchall()
        if not len(result):
            self.cur.execute('INSERT INTO relations VALUES (%s, %s, 1)', (
             index1, index2))
        else:
            ranking = result[0][0]
            self.cur.execute('UPDATE relations SET ranking=%s WHERE word1_id=%s AND word2_id=%s', (
             ranking + 1, index1, index2))

    def _addEndRelation(self, word):
        """
            adds a relation, that a sentence can end with word

            @param word: the word
            @type word: string
        """
        self.cur.execute('SELECT id FROM words WHERE word=%s', [word])
        index = self.cur.fetchall()[0][0]
        self.cur.execute('SELECT ranking FROM relations WHERE word1_id=%s AND word2_id=-1', [
         index])
        result = self.cur.fetchall()
        if not len(result):
            self.cur.execute('INSERT INTO relations VALUES (%s, -1, 1)', [
             index])
        else:
            self.cur.execute('UPDATE relations SET ranking=%s WHERE word1_id=%s and word2_id=-1', (
             result[0][0], index))

    def _rankWord(self, word):
        """
            rank a word by length and probability

            @param word: the word
            @type word: string
            @rtype: float
        """
        rank = 0
        length = len(word)
        return self._getWordRank(word) + length * 0.7

    def _getWordRank(self, word):
        """
            rank a word by propabiltity of occurance

            @param word: the word
            @type word: string
            @rtype: float
        """
        self.cur.execute('SELECT id FROM words WHERE word=%s', word)
        id = self.cur.fetchall()
        if not id or not id[0]:
            return 1
        id = id[0][0]
        self.cur.execute('SELECT ranking FROM relations WHERE word2_id=%s', id)
        result = self.cur.fetchall()
        rank = 0
        for row in result:
            rank += row[0]

        return rank

    def _createRandomSentence(self, index, sentence, forward=True):
        """
            recursive function to create a random sentence

            @param index: database-index of the last/first word
            @type index: int
            @param sentence: the sentence so far
            @type sentence: string
            @param forward: append or prepend? forward=True appends
            to the sentence
            @type forward: bool
        """
        candidates = []
        if forward:
            self.cur.execute('SELECT word2_id, ranking FROM relations WHERE word1_id=%s', [
             index])
        else:
            self.cur.execute('SELECT word1_id, ranking FROM relations WHERE word2_id=%s', [
             index])
        result = self.cur.fetchall()
        for row in result:
            candidates += [row[0]] * row[1]

        newindex = random.choice(candidates)
        if newindex == 0:
            return sentence.strip()
        else:
            if newindex == -1:
                self.cur.execute('SELECT word FROM words WHERE id=%s', index)
                word = self.cur.fetchall()[0][0]
                return (sentence + ' ' + word).strip()
            if forward:
                if index == 0:
                    return self._createRandomSentence(newindex, '')
                self.cur.execute('SELECT word FROM words WHERE id=%s', index)
                word = self.cur.fetchall()[0][0]
                return self._createRandomSentence(newindex, sentence + ' ' + word)
            if index == -1:
                return self._createRandomSentence(newindex, '', False)
            self.cur.execute('SELECT word FROM words WHERE id=%s', newindex)
            word = self.cur.fetchall()[0][0]
            return self._createRandomSentence(newindex, word + ' ' + sentence, False).strip()

    def _createReply(self, msg):
        """
            reply to a message

            use msg to create an appropriate reply.
            first the function tries to identify the most important word.
            then it grows the answer forward and backwards around the word

            @param msg: the msg to reply to
            @type msg: string
        """
        words = msg.strip().split(' ')
        bestword = None
        bestwordrank = 0
        for word in words:
            rank = self._getWordRank(word)
            if not rank > 1:
                continue
            rank = self._rankWord(word)
            if rank > bestwordrank:
                bestwordrank = rank
                bestword = word

        if bestword:
            self.cur.execute('SELECT id FROM words WHERE word=%s', [
             bestword])
            index = self.cur.fetchall()[0][0]
            return self._createRandomSentence(index, '', False) + ' ' + self._createRandomSentence(index, '')
        else:
            return self._createRandomSentence(0, '')
            return

    def learn(self, msg):
        """
            learn the words from msg

            learns the new words from msg,
            and add the new relations between the words.

            @param msg: the message
            @type msg: string
        """
        words = msg.split(' ')
        oldword = '>'
        for word in words:
            word = word.strip()
            if len(word):
                self._addRelation(oldword, word)
                oldword = word

        if oldword != '>':
            self._addEndRelation(oldword)

    def reply(self, msg):
        """
            learn msg and find a reply to it

            @param msg: the message
            @type msg: string
        """
        self.learn(msg)
        return self._createReply(msg).strip()

    def cleanup(self):
        """
            cleanup method to commit all unwritten entries to the database
        """
        self.db.commit()
        self.db.close()


def init_db(name):
    """
        creates a new DB for use with this lib

        @param name: the (file)name of the DB
        @type name: string
    """
    db = sqlite.connect(name)
    cur = db.cursor()
    cur.execute('CREATE TABLE words (id INTEGER PRIMARY KEY, word VARCHAR(255))')
    cur.execute('CREATE TABLE relations (word1_id INTEGER, word2_id INTEGER, ranking INTEGER)')
    cur.execute('INSERT INTO words VALUES (0, ">")')
    cur.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
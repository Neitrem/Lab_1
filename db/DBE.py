import sqlite3


# requests - db with requests and answers [request | answer]
# synonyms - db with core words and their synonyms [core_word | synonym]
# service_words - db with service words [service_word]

class DBExecutor():
    """Deal with local sqlite db."""

    __connection =  None
    __cursor = None

    def __init__(self, file_name: str):
        # Connent to db
        self.__connection = sqlite3.connect(file_name)
        self.__cursor = self.__connection.cursor()

        self.__create_tables()

    def __create_tables(self):
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY,
        request TEXT NOT NULL,
        answer TEXT NOT NULL
        )
        ''')

        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS synonyms (
        id INTEGER PRIMARY KEY,
        core_word TEXT NOT NULL,
        synonym TEXT NOT NULL
        )
        ''')

        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_words (
        id INTEGER PRIMARY KEY,
        servise_word TEXT NOT NULL
        )
        ''')

        self.__connection.commit()

    def getRequests(self):
        self.__cursor.execute('SELECT * FROM requests')
        req = self.__cursor.fetchall()

        return req

    def insertRequest(self, new_request, new_answer):
        self.__cursor.execute('INSERT INTO requests (request, answer) VALUES (?, ?)', (new_request, new_answer))

        self.__connection.commit()

    def getSynonyms(self):
        self.__cursor.execute('SELECT * FROM synonyms')
        syn = self.__cursor.fetchall()

        return syn
    
    def insertSynonym(self, core_word, syn):
        self.__cursor.execute('INSERT INTO synonyms (core_word, synonym) VALUES (?, ?)', (core_word, syn))
         
        self.__connection.commit()

    def updateSynonym(self, core_word, syn):
        self.__cursor.execute('UPDATE synonyms SET synonym = ? WHERE core_word = ?', (syn, core_word))

        self.__connection.commit()
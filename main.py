
from db.DBE import DBExecutor
from SearchExecutor import SearchExecutor
# import db.fullfilDB # Uncomment to load data to db


ex = DBExecutor("db.db")
searchEx = SearchExecutor(ex)
print(ex.getSynonyms())

answ = searchEx.ProcessRequest("Как сейчас доехать в библиотеку")

print(answ[1])

print(ex.getSynonyms())

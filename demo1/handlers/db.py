from pymongo import MongoClient
dbIP = 'localhost';
class DB:
    def connectDB(self, dbname, dbip, port):
        self._conn = MongoClient(dbip, port)
        self._db = self._conn[dbname]
        collectionname = 'resultinfo'
        self._collection = self._db[collectionname];


import unittest
from parser import Parser
from logger import TestLogger as p
from reddit import Reddit
from pymongo import MongoClient
from db import Mongo
from config import Config

   
class TestMongo(unittest.TestCase):
    def test_connect(self):
        # call with none
        mongo = Mongo()
        assert(mongo.db.name == Config().config['DB']['prod'] )

        ## call with test
        mongo = Mongo(env="Test")
        assert(mongo.db.name == Config().config['DB']['test'] )

    def test_put_ids(self): 
        # set up the scenaior
        #Mongo().put_ids(ids)
        pass

    def test_put_ids_same(self):
        mongo = Mongo(env="Test")
        mongo.db.ids.insert_one({"reddit_id":"aisb0hc"})
        ids = ["aisb0hc"]
        mongo.put_ids(ids)
        assert(mongo.get_ids()==ids)
        ids = ["aisb0hc","jshshfdif"]
        mongo.put_ids(ids)
        result = mongo.get_ids()
        assert(result==ids)
        mongo.db.ids.delete_one({"reddit_id":"aisb0hc"})
        mongo.db.ids.delete_one({"reddit_id":"jshshfdif"})
        assert(mongo.get_ids()==[])

    def test_get_ids(self):
        for a in Mongo(env="Test").get_ids():
            print (a)
    


if __name__ == '__main__':
    unittest.main()


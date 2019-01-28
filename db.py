from pymongo import MongoClient
from pymongo import ASCENDING
from parser import Parser
from logger import TestLogger as p
from reddit import Reddit

class Mongo():

    def __init__(self, env=None):
        client = MongoClient('localhost', 27017)
        if env:
            self.db = client.test
            self.ids = self.db.ids
        else:
            self.db = client.reddit
            self.ids = self.db.ids
        
        
    
    def put_ids(self, new_ids):
        ## get all the ids and put them in a set
        current_ids = self.get_ids()
        ids = Mongo.diff(new_ids,current_ids)
        for id in ids:
            try:
                self.ids.insert_one({"reddit_id":id})
            except pymongo.errors.DuplicateKeyError:
                "Duplicate rejected" 
    
    def get_ids(self):
        '''
        returns [strs] ids
        '''
        return [record['reddit_id'] for record in self.ids.find()]

    @staticmethod
    def diff(a, b):
        return set(a).difference(set(b))
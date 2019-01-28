from pymongo import MongoClient
from pymongo import ASCENDING
from parser import Parser
from logger import TestLogger as p
from reddit import Reddit

class Mongo():

    def __init__(self, env):
        client = MongoClient('localhost', 27017)
        if env:
            self.db = client.test
            self.ids = self.db.ids
        else:
            self.db = client.reddit
            self.ids = self.db.ids
        
        ## creates a unique index on the reddit_id
        ## to stop duplicates at the db level
        result = self.db.profiles.create_index([('reddit_id', ASCENDING)],unique=True)
    
    def put_ids(self, new_ids):
        ## get all the ids and put them in a set
        current_ids = self.get_ids()
        ids = Mongo.diff(new_ids,current_ids)
        for id in ids:
            self.ids.insert_one({"reddit_id":id})
    
    def get_ids(self):
        '''
        returns [strs] ids
        '''
        return [record['reddit_id'] for record in self.ids.find()]

    @staticmethod
    def diff(a, b):
        return set(a).difference(set(b))
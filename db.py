from pymongo import MongoClient
from parser import Parser
from logger import TestLogger as p
from reddit import Reddit

class Mongo():

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.reddit
        self.ids = self.db.ids
    
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
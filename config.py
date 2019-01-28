import json

class Config():

    def __init__(self):
        with open('config/environment.json', 'r') as f:
            self.config = json.load(f)
        
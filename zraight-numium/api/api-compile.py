import json
import logging
import os
import random
import time

logging.basicConfig(level=logging.INFO)

class API:
    def __init__(self):
        self.rest = {}
        self.message = {}
        self.response = {}
        self.extension_linker = {}
    
    def load_rest(self, filepath):
        with open(filepath, 'r') as f:
            self.rest = json.load(f)
    
    def load_message(self, filepath):
        with open(filepath, 'r') as f:
            self.message = json.load(f)

    def load_response(self, filepath):
        with open(filepath, 'r') as f:
            self.response = json.load(f)

    def load_extension_linker(self, filepath):
        with open(filepath, 'r') as f:
            self.extension_linker = json.load(f)
            
    def write_api(self, type_api: str, data: dict):
        if type_api == 'rest':
            with open(f'api/{type_api}.json', 'w') as f:
                json.dump(data, f, indent=4)
        elif type_api == 'message':
            with open(f'api/{type_api}.json', 'w') as f:
                json.dump(data, f, indent=4)
        elif type_api == 'response':
            with open(f'api/{type_api}.json', 'w') as f:
                json.dump(data, f, indent=4)
        elif type_api == 'extension_linker':
            with open(f'api/{type_api}.json', 'w') as f:
                json.dump(data, f, indent=4)
        else:
            logging.error(f"Unknown API type: {type_api}")


    def back(self, type_api):
        if type_api == 'rest':
            return self.rest
        elif type_api == 'message':
            return self.message
        elif type_api == 'response':
            return self.response
        elif type_api == 'extension_linker':
            return self.extension_linker
        else:
            logging.error(f"Unknown API type: {type_api}")
            return None
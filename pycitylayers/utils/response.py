import json

class Response:
    def __init__(self):
        pass
    
    def from_requests(self, res):
        self._res_text = res.text
        
    def to_json(self):
        json_obj = json.loads(self._res_text)
        self._res_json = json_obj
        return json_obj
    
    
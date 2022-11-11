import json

from pydantic import BaseModel


class BasicModel(BaseModel):
    
    def to_json(self):
        return json.loads(json.dumps(self,default=lambda x :  x.__str__() if type(x).__name__=="datetime" else x.__dict__))

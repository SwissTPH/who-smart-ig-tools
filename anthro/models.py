
import json
from typing import List, Union
from pydantic import BaseModel

class anthroRecordModel(BaseModel):
    l:Union[float, int]
    s:Union[float, int]
    m:Union[float, int]
    y:Union[float, int]
    def print(self):
        return "{{y:{0},l:{1},s:{2},m:{3}}}".format(
            force_int(self.y),
            force_int(self.l),
            force_int(self.s),
            force_int(self.m)
        )
    
def force_int(y):
    return int(y) if y == int(y) else y

class anthroModel(BaseModel):
    data : List[anthroRecordModel]
    name : str
    y_name = str
    def print_data(self):
        ret = '{\n'
        for row in self.data:
            ret += "\t" + row.print() + ",\n"
        return ret[:-2] + '\n}'
    

    
    
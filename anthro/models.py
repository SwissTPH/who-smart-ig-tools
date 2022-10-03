
import json
from typing import List, Union, Optional
from pydantic import BaseModel

class anthroRecordModel(BaseModel):
    l:Union[float, int]
    s:Union[float, int]
    m:Union[float, int]
    y:Union[float, int]
    def print(self):
        return "{{y:{0},l:{1},s:{2},m:{3}}}".format(
            (self.y),
            (self.l),
            (self.s),
            (self.m)
        )
    


class anthroModel(BaseModel):
    data_female : List[anthroRecordModel]
    data_male : List[anthroRecordModel]
    clean_name : Optional[str]
    name : str
    y_name : str

    def print_data(self):
        ret = 'define {0}For{1}Female:\n{{\n'.format(self.clean_name,self.y_name.capitalize())
        for row in self.data_female:
            ret += "\t" + row.print() + ",\n"
        ret =ret[:-2] + '\n}\n\n'
        ret += 'define {0}For{1}Male:\n{{\n'.format(self.clean_name,self.y_name.capitalize())
        for row in self.data_male:
            ret += "\t" + row.print() + ",\n"
        ret =ret[:-2] + '\n}\n\n'
        return ret
    

    
    
from dataclasses import dataclass

@dataclass
class Employee():
    name : str
    code : str
    unit : str = ''
    
# Employee(name='ali', code='8888888', unit='')
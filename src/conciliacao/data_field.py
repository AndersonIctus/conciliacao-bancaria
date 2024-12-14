from dataclasses import dataclass

@dataclass
class DataField:
    column: str
    value: str | float
    
    def __init__(self, column: str, value: str | float):
        self.column = column
        self.value = value

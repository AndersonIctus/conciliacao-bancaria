from typing import List, Dict, Optional
from dataclasses import dataclass

from src.conciliacao.util.transformation_util import TransformacaoUtil
from src.models.field import Field
from src.models.template import Template

@dataclass
class DataField:
    column: str
    value: str
    
@dataclass
class DataLine:
    rawData: Dict
    hashValue: str
    fields: List[DataField]
    
    def getFields(self, data: Dict, fields: List[Field]) -> List[DataField]:
        print('fields')
        formFields: List[DataField] = []
        for field in fields:
            coluna = field.coluna
            header = field.header
            tipo = field.tipo
            
            value = data[header] if header else ""
            
            # Aplicar transformações, se houver
            if field.transform:
                value = TransformacaoUtil.applyTransformacao(value, field.transform)
            
        return formFields
            
    
    # Construtor personalizado para receber dados diretamente
    def __init__(self, data: Dict, template: Template):
        self.rawData = data
        self.fields = self.getFields(data, template.fields)
    
    
from typing import List, Dict
from dataclasses import dataclass

from src.conciliacao.data_field import DataField
from src.conciliacao.util.transformation_util import TransformacaoUtil
from src.models.field import Field
from src.models.template import Template
    
@dataclass
class DataLine:
    # rawData: Dict
    fields: List[DataField]
    
    def getFields(self, data: Dict, fields: List[Field]) -> List[DataField]:
        print('fields')
        formFields: List[DataField] = []
        for field in fields:
            dataField = TransformacaoUtil.to_data_field(data, field)
            formFields.append(dataField)
        return formFields
    
    # Construtor personalizado para receber dados diretamente
    def __init__(self, data: Dict, template: Template):
        # self.rawData = data
        self.fields = self.getFields(data, template.fields)
        print(self.fields)

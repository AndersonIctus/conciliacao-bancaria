from typing import List, Dict
from dataclasses import dataclass

from src.conciliacao.data_field import DataField
from src.conciliacao.util.transformation_util import TransformacaoUtil
from src.models.field import Field
from src.models.template import Template
    
@dataclass
class DataLine:
    fields: List[DataField]
    
    def getFields(self, data: Dict, fields: List[Field]) -> List[DataField]:
        formFields: List[DataField] = []
        for field in fields:
            dataField = TransformacaoUtil.to_data_field(data, field)
            formFields.append(dataField)
        return formFields
    
    # Construtor personalizado para receber dados diretamente
    def __init__(self, data: Dict, template: Template):
        self.fields = self.getFields(data, template.fields)

    def get_field_by_column(self, column: str) -> DataField | None:
        """
        Retorna o campo cujo nome da coluna seja igual ao fornecido, ou None se não for encontrado.
        """
        for field in self.fields:
            if field.column == column:
                return field
        return None
    
    def __eq__(self, other):
        if not isinstance(other, DataLine):
            return False
        
        # Busca pelo campo "Id" em ambos os objetos
        self_id = self.get_field_by_column("Id")
        other_id = other.get_field_by_column("Id")

        # Comparação: ambos devem ter o campo "Id" e os valores devem ser iguais
        if self_id and other_id:
            return self_id.value == other_id.value
        
        # Retorna False se um dos dois não tiver o campo "Id"
        return False

    def __hash__(self):
        """
        Gera o hash baseado no valor do campo "Id", se existir.
        """
        id_field = self.get_field_by_column("Id")
        return hash(id_field.value) if id_field else super().__hash__()

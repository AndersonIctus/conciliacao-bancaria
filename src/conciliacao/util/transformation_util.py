from dataclasses import dataclass
from datetime import datetime

import hashlib
from typing import List, Dict

from src.conciliacao.data_field import DataField
from src.models.transformacao import Transformacao
from src.models.field import Field

@dataclass
class TransformacaoUtil:
    
    @staticmethod
    def to_data_field(data: Dict, field: Field) -> DataField:
        header = field.header
        value = data[header] if header else ""
        util = TransformacaoUtil()
        
        # Aplicar transformações, se houver
        if field.tipo == 'static':
            value = field.value
        elif field.tipo == 'hash':
            value = util.transform_hash(data, field)
        elif field.tipo == 'decimal':
            value = util.transform_decimal(value)
        elif field.tipo == 'number':
            value = float(value)
        elif field.transform:
            value = util.apply_transformation(value, field)
        
        return DataField(field.coluna, value)
    
    def transform_hash(self, data: Dict, field: Field) -> str:
        textHash = ''
        for header in field.hashHeaders:
            textHash += data[header]
        return hashlib.sha256(textHash.encode()).hexdigest()
    
    def transform_decimal(self, value: str) -> str:
         # Remove o prefixo "R$" e quaisquer espaços
        valor = value.replace("R$", "").strip()
        # Remove o sinal de negativo, se houver, e substitui a vírgula por ponto
        valor = valor.replace("-", "").replace(".", "").replace(",", ".")
        # Converte para float e retorna
        return float(valor)
    
    def transform_date(self, value: str, tipo: str, transformacao: List[Transformacao]):
        encode_entrada = transformacao[0].entrada
        encode_saida = transformacao[0].saida
        
        # Mapear o formato customizado para os padrões do Python
        entrada_format = encode_entrada.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y").replace("hh", "%H").replace("mm", "%M").replace("ss", "%S")
        saida_format = encode_saida.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y").replace("hh", "%H").replace("mm", "%M").replace("ss", "%S")
        
        # Converter a string para o formato de saída
        try:
            data = datetime.strptime(value, entrada_format)
            if tipo == "date":
                return data.strftime(saida_format)
            elif tipo == "time":
                return data.strftime(saida_format)
            else:
                raise ValueError(f"Tipo desconhecido: {tipo}")
        except ValueError as e:
            raise ValueError(f"Erro ao transformar '{value}': {e}") 
        
    def transform_choose(self, value: str, transformacao: List[Transformacao]):
        for transf in transformacao:
            if value == transf.entrada:
                return transf.saida
        raise ValueError(f"Transformação 'choose' não encontrado para o valor '{value}'")

    def apply_transformation(self, value: str, field: Field) -> str:
        tipo = field.tipo
        
        if tipo == 'date' or tipo == 'time':
            return self.transform_date(value, field.tipo, field.transform)
        elif tipo == 'choose':
            return self.transform_choose(value, field.transform)
        else:
            raise ValueError(f"Tipo desconhecido: {tipo}")
    
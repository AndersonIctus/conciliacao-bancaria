from dataclasses import dataclass
from typing import List, Dict, Optional

from src.models.field import Field
from src.models.transformacao import Transformacao

@dataclass
class Template:
    extensao: str
    banco: str
    headers: List[str]
    fields: List[Field]
    
    # Construtor personalizado para receber dados diretamente
    def __init__(self, data: Dict):
        # Atribuindo valores diretamente do dicionário 'data'
        self.extensao = data["extensao"]
        self.banco = data["banco"]
        self.headers = data["headers"]
        
        # Inicializando a lista de campos (fields)
        self.fields = [
            Field(
                coluna=f["coluna"],
                tipo=f["tipo"],
                header=f.get("header"),
                hashHeaders=f.get("hashHeaders"),
                transform=[Transformacao(t["entrada"], t["saida"]) for t in f.get("transform", [])],
                value=f.get("value")
            ) for f in data["fields"]
        ]

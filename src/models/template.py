from dataclasses import dataclass
from typing import List, Dict

from src.models.field import Field
from src.models.transformacao import Transformacao

@dataclass
class Template:
    extensao: str
    banco: str
    outputPath: str
    headers: List[str]
    fields: List[Field]
    
    # Construtor personalizado para receber dados diretamente
    def __init__(self, data: Dict):
        # Atribuindo valores diretamente do dicionário 'data'
        self.extensao = data["extensao"]
        self.banco = data["banco"]
        self.outputPath = data["outputPath"]
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

    # Método clone
    def clone(self) -> "Template":
        """
        Cria e retorna uma cópia da instância atual de Template.
        """
        return Template({
            "extensao": self.extensao,
            "banco": self.banco,
            "outputPath": self.outputPath,
            "headers": self.headers.copy(),  # Faz uma cópia para evitar mutação acidental
            "fields": [
                {
                    "coluna": field.coluna,
                    "tipo": field.tipo,
                    "header": field.header,
                    "hashHeaders": field.hashHeaders,
                    "transform": [
                        {"entrada": t.entrada, "saida": t.saida} for t in field.transform
                    ],
                    "value": field.value
                } for field in self.fields
            ]
        })

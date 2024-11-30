from dataclasses import dataclass

from typing import List, Dict, Optional

from src.models.transformacao import Transformacao

@dataclass
class TransformacaoUtil:
    @staticmethod
    def applyTransformacao(value: str, transformation: List[Transformacao]) -> str:
        print('')
        return ''

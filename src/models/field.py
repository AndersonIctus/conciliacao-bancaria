from dataclasses import dataclass
from typing import List, Optional

from src.models.transformacao import Transformacao

@dataclass
class Field:
    coluna: str
    tipo: str
    header: Optional[str] = None
    hashHeaders: Optional[List[str]] = None
    transform: Optional[List[Transformacao]] = None
    value: Optional[str] = None

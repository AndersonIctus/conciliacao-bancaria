import csv
from typing import List, Dict, Optional

from src.models.template import Template
from src.conciliacao.data_line import DataLine

output_path = 'data/output/'

def toConciliationFromTemplate(input_bank_file: str, template: Template) -> List[DataLine]:
    data_lines: List[DataLine] = []
    
    # Abrir e ler o arquivo CSV
    with open(input_bank_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Ler o CSV como dicionário (coluna -> valor)
        
        # Iterar sobre as linhas do arquivo CSV
        for row in reader:
            dataLine = DataLine(row, template)
            data_lines.append(dataLine)
    
    ## Retornando linhas
    return data_lines


def conciliar_arquivo(input_bank_file, template: Template):
    print(f'Conciliando arquivo "{input_bank_file}"')
    # 1 - Transforma o arquivo passado para a forma conciliada considerando o template passado
    input_conciliados = toConciliationFromTemplate(input_bank_file, template)
    
    # 2 - Carrega os arquivos já conciliados em uma lista
    atual_conciliados = ''
    
    # 3 - Compara as entradas sobrando somente os dados que serão conciliados
    dados_conciliados = '' 

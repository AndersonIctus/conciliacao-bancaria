import os
import csv
from typing import List

from dataclasses import dataclass

from src.conciliacao.data_field import DataField
from src.models.template import Template
from src.conciliacao.data_line import DataLine

@dataclass
class Conciliacao:
    output_path = 'data/output/'
    
    def load_actual_data_conciliation(self, template: Template) -> List[DataLine]:
        print('Carregando dados já conciliados')
        # Construindo o caminho do arquivo
        # TODO: DEVE PEGAR MAIS DE UM ARQUIVO DE CONCILIAÇÃO, pois pode ter conciliação de vários meses!
        data_conciliacao = '2024'
        file_path = os.path.join(self.output_path, template.outputPath, f"Conciliados.{data_conciliacao}.CON")
        
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Arquivo {file_path} não encontrado.")
            return []

        conciliados = []
        # Abrindo o arquivo CSV para leitura
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")  # Supondo que o separador seja `;`

            # Lendo cada linha e criando DataLine
            for row in reader:
                data_line = DataLine(fields=[
                    DataField(column=field.coluna, value=row.get(field.coluna))
                    for field in template.fields if field.coluna in row
                ])
                conciliados.append(data_line)

        print(f"{len(conciliados)} registros carregados do arquivo {file_path}.")
        return conciliados
    
    def save_actual_data_conciliation(self, template: Template, data_conciliacao: str, data_lines: List[DataLine]):
        print('Salvando dados conciliados')

        # Construindo o caminho do arquivo
        file_path = os.path.join(self.output_path, template.outputPath, f"Conciliados.{data_conciliacao}.CON")
        
        # Certificando-se de que o diretório existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Obter cabeçalhos a partir dos campos do template
        headers = [field.coluna for field in template.fields]

        # Escrever o arquivo CSV
        with open(file_path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")

            # Escrever cabeçalho
            writer.writeheader()

            # Escrever linhas de dados
            for data_line in data_lines:
                # Criar um dicionário para cada linha, usando os valores de `DataField`
                row = {field.column: field.value for field in data_line.fields}
                writer.writerow(row)

        print(f"Arquivo salvo em {file_path}.")

    def to_conciliation_from_template(self, input_bank_file: str, template: Template) -> List[DataLine]:
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

    def conciliar_dados(self, input_bank_file, template: Template) -> List[DataLine]:
        print(f'Conciliando arquivo "{input_bank_file}"')
        # 1 - Carrega os arquivos já conciliados em uma lista
        atual_conciliados = self.load_actual_data_conciliation(template)
        
        # 2 - Transforma o arquivo passado para a forma conciliada considerando o template passado
        input_conciliados = self.to_conciliation_from_template(input_bank_file, template)
        
        
        # 3 - Compara as entradas sobrando somente os dados que serão conciliados
        dados_conciliados = '' 
        
        return []

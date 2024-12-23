from datetime import datetime
import os
import csv
from typing import List

from dataclasses import dataclass
from collections import defaultdict

from src.conciliacao.util.data_helper import DataHelper
from src.models.field import Field
from src.models.template import Template
from src.conciliacao.data_line import DataLine

@dataclass
class Conciliacao:
    output_path = 'data/output/'
    
    def load_actual_data_conciliation(self, template: Template) -> List[DataLine]:
        # Caminho da pasta onde estão os arquivos .CON
        folder_path = os.path.join(self.output_path, template.outputPath)

        # Verifica se a pasta existe
        if not os.path.exists(folder_path):
            print(f"Pasta {folder_path} não encontrada. Criando a pasta...")
            os.makedirs(folder_path)  # Cria a pasta e subpastas, se necessário

        # Filtrar arquivos com extensão .CON
        con_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not con_files:
            print(f"Nenhum arquivo .csv encontrado em {folder_path}.")
            return []

        conciliados: List[DataLine] = []
        
        # Processa cada arquivo de saída
        template_padrao = template.clone()
        template_padrao.fields = [Field(coluna=f.coluna,
                tipo='number' if f.tipo == 'decimal' else 'string',
                header=f.coluna,
                value=f.value) 
            for f in template.fields]
        template_padrao.headers = [h.coluna for h in template.fields]
        
        for file_name in con_files:
            file_path = os.path.join(folder_path, file_name)
            print(f"== >>>> Lendo o arquivo {file_path}...")
            
            try:
                # Abre o arquivo e lê os dados
                with open(file_path, mode="r", encoding="utf-8") as file:
                    reader = csv.DictReader(file, delimiter=";")  # Supondo separador `;`
                    for row in reader:
                        conciliados.append(DataLine(row, template_padrao))
                print(f"{file_name}: {len(conciliados)} registros carregados.")
                
            except Exception as e:
                print(f"Erro ao processar o arquivo {file_name}: {e}")

        print(f"== >>>> Total de {len(conciliados)} registros carregados de todos os arquivos .csv.")
        return conciliados
    
    def map_dados_conciliados(self, data_lines: List[DataLine]):
        # Mapa para armazenar os dados, usando defaultdict para inicializar automaticamente listas
        mapa_conciliados = defaultdict(list)

        for data_line in data_lines:
            # Usa o método get_data_extensao para gerar a chave
            date_reference = datetime.strptime(data_line.get_field_by_column('Data').value, '%d/%m/%Y')
            chave = DataHelper.get_data_extensao(date_reference)

            # Adiciona o DataLine à lista correspondente à chave
            mapa_conciliados[chave].append(data_line)

        # Converte o defaultdict de volta para um dict normal se necessário
        return dict(mapa_conciliados)
    
    def save_actual_data_conciliation(self, data_lines: List[DataLine], template: Template):
        print('== **** Salvando dados conciliados')
        # Obter cabeçalhos a partir dos campos do template
        headers = [field.coluna for field in template.fields]
        mp_dados_conciliados = self.map_dados_conciliados(data_lines)
        
        # Caminho da pasta onde estão os arquivos .CON
        folder_path = os.path.join(self.output_path, template.outputPath)
         # Verifica se a pasta existe
        if not os.path.exists(folder_path):
            print(f"Pasta {folder_path} não encontrada. Criando a pasta...")
            os.makedirs(folder_path)  # Cria a pasta e subpastas, se necessário
        
        # Iterando sobre o mapa e gravando em arquivos
        for chave, dados in mp_dados_conciliados.items():
            # Nome do arquivo baseado na chave (data)
            nome_arquivo = f"Conciliados.{chave}.csv"
            file_path = os.path.join(folder_path, nome_arquivo)
            
            # Abrindo o arquivo para gravação
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
                
                writer.writeheader()
                # Escrevendo os dados no arquivo
                for data_line in dados:
                    # Criar um dicionário para cada linha, usando os valores de `DataField`
                    row = {field.column: field.value for field in data_line.fields}
                    writer.writerow(row)

            print(f"== >>>> Arquivo {file_path} atualizado com {len(dados)} registros.")

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

    def conciliar_listas(self, atual: List[DataLine], novos: List[DataLine]) -> List[DataLine]:
        """
        Compara as listas `atual` e `novos` e retorna os elementos de `novos` que não estão em `atual`.

        :param atual: Lista de DataLine já existentes.
        :param novos: Lista de novos DataLine.
        :return: Lista de DataLine exclusivos em `novos`.
        """
        print('==========  Conciliando dados  ==========')

        # Converte a lista `atual` para um conjunto de identificadores únicos
        atual_set = set(atual) 
        
        # Filtra os elementos de `novos` que não estão em `atual_set`
        conciliados = [novo for novo in novos if novo not in atual_set]

        print(f"== >>>>> {len(conciliados)} registros novos encontrados.")
        return conciliados

    def resume_data(self, dados: List[DataLine]):
        """
        Faz um resumo dos dados listados, separando créditos, débitos e o saldo final.

        :param dados: Lista de objetos DataLine a ser resumida.
        :return: Um dicionário contendo total de créditos, débitos e saldo final.
        """
        print("==================  Resumo dos dados  ==================")

        total_credito = 0.0
        total_debito = 0.0

        # Itera pelos dados para calcular os totais
        for data in dados:
            tipo_field = data.get_field_by_column("Tipo")
            valor_field = data.get_field_by_column("Valor")

            if not tipo_field or not valor_field:
                print("Dados incompletos em um dos registros. Ignorando...")
                continue

            tipo = tipo_field.value
            valor = float(valor_field.value)

            if tipo == "CREDITO":
                total_credito += valor
            elif tipo == "DEBITO":
                total_debito += valor

        # Calcula o saldo final
        saldo_final = total_credito - total_debito

        # Retorna o resumo
        print(f"== Total Crédito: {total_credito:.2f}")
        print(f"==  Total Débito: {total_debito:.2f}")
        print(f"==         Saldo: {saldo_final:.2f}")
        print("========================================================")
    
    def conciliar_dados(self, input_bank_file, template: Template):
        print(f'== Conciliando arquivo "{input_bank_file}"')
        
        # 1 - Carrega os arquivos já conciliados em uma lista
        atual_conciliados = self.load_actual_data_conciliation(template)
        
        # 2 - Transforma o arquivo passado para a forma conciliada considerando o template passado
        input_conciliados = self.to_conciliation_from_template(input_bank_file, template)
        
        # 3 - Compara as entradas sobrando somente os dados que serão conciliados
        if len(atual_conciliados) == 0:
            dados_conciliados = input_conciliados
        else:
            dados_conciliados = self.conciliar_listas(atual_conciliados, input_conciliados)
            
        # 4 - Gravar os dados após conciliação
        if len(dados_conciliados) > 0:
            print('======= RESUMO CONCILIADOS')
            self.resume_data(dados_conciliados)
            dados_conciliados = atual_conciliados + dados_conciliados
            dados_conciliados.sort(key=lambda x: (datetime.strptime(x.get_field_by_column('Data').value, "%d/%m/%Y"), x.get_field_by_column('Hora').value))
            self.save_actual_data_conciliation(dados_conciliados, template)
            
            print('======= RESUMO FINAL')
            self.resume_data(dados_conciliados)
        else:
            print('Nenhum dado para conciliar ...')

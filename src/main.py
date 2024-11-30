import json
import sys
import os

from src.models.template import Template

sys.path.append('./src')

# Função para extrair o nome do banco do nome do arquivo
def extrair_nome_banco(nome_arquivo: str) -> str:
    # Remover a extensão do arquivo (se necessário)
    nome_base = os.path.splitext(nome_arquivo)[0]
    
    # Dividir o nome do arquivo pelo ponto (.)
    partes = nome_base.split('.')
    
    # Verificar se o nome do banco está presente (segunda parte)
    if len(partes) >= 2:
        return partes[1]  # A segunda parte é o nome do banco
    else:
        raise ValueError("Formato do nome do arquivo inválido. Esperado: <descricao_arquivo>.<nome_banco_arquivo>.<extensao>")


def main(input_bank_file):
    print("======= INICIANDO CONCILIAÇÃO")
    print(f"Arquivo: {input_bank_file}")
    
    nome_banco = extrair_nome_banco(input_bank_file)
    
    ## Carrega templates
    with open('templates.json', 'r', encoding='utf-8') as file:
        templates = json.load(file)
        
        # Encontra o template com a extensão correspondente ao nome do banco
        template = next((t for t in templates if t["extensao"].lower() == nome_banco.lower()), None)
        
        if template:
            template_obj = Template(template)  # Cria o objeto Template a partir do template encontrado
            print("Template carregado:")
            print(template_obj)
        else:
            raise ValueError(f"Nenhum template encontrado para o banco {nome_banco}.")
    
    ## 

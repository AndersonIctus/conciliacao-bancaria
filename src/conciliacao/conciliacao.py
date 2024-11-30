from src.models.template import Template

output_path = 'data/output/'

def conciliar_arquivo(input_bank_file, template: Template):
    print(f'Conciliando arquivo "{input_bank_file}"')
    # 1 - Transforma o arquivo passado para a forma conciliada considerando o template passado
    input_conciliados = ''
    
    # 2 - Carrega os arquivos já conciliados em uma lista
    atual_conciliados = ''
    
    # 3 - Compara as entradas sobrando somente os dados que serão conciliados
    dados_conciliados = '' 
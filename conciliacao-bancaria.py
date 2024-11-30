import argparse

import sys
from src.main import main

sys.path.append('./src')

if __name__ == "__main__":
    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Conciliação Bancária")
    parser.add_argument(
        "--bank-file",
        required=True,
        help="Caminho do arquivo de extrato bancário (ex.: bank_statement.csv).",
    )
    # parser.add_argument(
    #     "--system-file",
    #     required=True,
    #     help="Caminho do arquivo de relatório do sistema (ex.: system_report.xlsx).",
    # )
    # parser.add_argument(
    #     "--output",
    #     required=True,
    #     help="Caminho do arquivo de saída para o relatório (ex.: reconciliation_report.xlsx).",
    # )
    args = parser.parse_args()

    # Chamada da função principal com os argumentos fornecidos
    main(args.bank_file)

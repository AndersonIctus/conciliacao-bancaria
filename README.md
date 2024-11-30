## Conciliação Bancária em Python
Projeto em python para poder criar uma forma fácil de criar conciliação bancária para vários bancos
1. Precisa ser um arquivo .csv
   - Isso é feito para que seja fácil controlar os templates gerados após o processamento

2. Deve haver um arquivo de template indicando qual campo do csv corresponde a estrutura de dados que será gerada
   - Veja o arquivo de template exemplo que é um json que descreve a entrada e saída

3. Cada arquivo bancário deve ter o seguinte padrao de nomenclatura

   `descricao_arquivo.nome_banco.csv`

### Dependências
```
python >= 3.0
makefile
pandas
openpyxl
xlrd
pdfkit
python-dotenv
pyinstaller
```

### Instalar as dependências
* Acione um ambiente virtual
```
$ python -m venv venv
```

* Ative o ambiente
```
$ venv\Scripts\activate
```

* Instale o pacote de dependencias
```
$ pip install -r requirements.txt
```

### Instalação do MakeFile
* Execute o seguinte código no powershell para instalar o chocolatey
```
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

* Instale o make
```
$ choco install make
```

* Reinicie o terminal para as configurações serem aplicadas
* Use `make --version` para verificar a versão

### Rodando o projeto
* Pode-se usar o make file para rodar o sistema usando
```
$ make run
```

* Mas pode-se chamar diretamente o arquivo usando a chamada 
```
$ python -m src
```

### Gerando executavel
* Use `make deploy` para gerar na pasta dist um executável do projeto que pode ser utilizado em qualquer ambiente.
* É criado o arquivo /dist/conciliacao-bancaria.exe

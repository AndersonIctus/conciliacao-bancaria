# Defina as variáveis com valores padrão
BANK_FILE ?= data/input/bank-default.cora.csv

deploy:
	pyinstaller --onefile conciliacao-bancaria.py
	cp templates.json dist
	cp conciliar_arquivo.bat dist

run: 
	python conciliacao-bancaria.py --bank-file $(BANK_FILE)

debug:
	python -m pdb conciliacao-bancaria.py --bank-file $(BANK_FILE)

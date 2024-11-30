deploy:
	pyinstaller --onefile src/main.py

run: 
	python src/main.py

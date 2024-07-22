all:
	python test.py

server:
	flask --app debug run

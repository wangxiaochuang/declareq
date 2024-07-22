all:
	python test.py

server:
	flask --app server run

all:
	pytest

server:
	flask --app debug run

upload:
	python setup.py sdist upload

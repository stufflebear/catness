all:
	make style

clean:
	find . -type f -name "*.py[co]" -exec rm -v {} \;

style:
	pep8 --ignore=E501,E226 --repeat --show-source .
	importchecker webapp

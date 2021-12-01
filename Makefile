PIP=pip3.9
PYTHON=python3.9

clean:
	@rm -f dist/*

build: clean
	@${PYTHON} setup.py bdist_wheel

upload: build
	@${PYTHON} -m twine upload dist/*

upgrade:
	@${PIP} install --quiet --upgrade DuckDuckGoImages
	@${PIP} install --quiet --upgrade DuckDuckGoImages
	@${PIP} show DuckDuckGoImages
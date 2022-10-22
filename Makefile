include ./Makefile.in.mk


.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
	$(RUN) isort "$(DIR_SRC)"
	$(RUN) black "$(DIR_SRC)"


.PHONY: parse1
parse1:
	$(call log, parsing oriencoop.cl)
	$(PYTHON) src/script1.py


.PHONY: parse2
parse2:
	$(call log, parsing https://www.som1.ru/shops)
	$(PYTHON) src/script2.py


.PHONY: parse3
parse3:
	$(call log, parsing https://naturasiberica.ru)
	$(PYTHON) src/script3.py


.PHONY: parse-all
parse-all: parse1 parse2 parse3
	$(call log, parsing all sites)


.PHONY: parse1-csv
parse1-csv:
	$(call log, parsing oriencoop.cl)
	$(PYTHON) src/script1.py -o csv


.PHONY: parse2-csv
parse2-csv:
	$(call log, parsing https://www.som1.ru/shops)
	$(PYTHON) src/script2.py -o csv


.PHONY: parse3-csv
parse3-csv:
	$(call log, parsing https://naturasiberica.ru)
	$(PYTHON) src/script3.py -o csv


.PHONY: parse-all-csv
parse-all-csv: parse1-csv parse2-csv parse3-csv
	$(call log, parsing all sites)


.PHONY: venv
venv:
	$(call log, installing packages)
	$(PIPENV_INSTALL)


.PHONY: venv-dev
venv-dev:
	$(call log, installing development packages)
	$(PIPENV_INSTALL) --dev



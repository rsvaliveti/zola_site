#
# file: Makefile
# description:
#  contains targets to generate the zola site
#
.PHONY build:
build:
	zola build

.PHONY serve:
serve:
	zola serve

.PHONY bib:
bib:
	python3 scripts/split-bibtex.py

.PHONY bib2:
bib2:
	rye run python3 scripts/import-bibtex.py



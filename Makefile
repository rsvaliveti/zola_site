#
# file: Makefile
# description:
#  contains targets to generate the zola site
#  uses the PDM package/dependency manager
#

.PHONY main:
main:	help

.PHONY env:
env:	## Populate submodules, created env required for python scripts
	git submodule init
	git submodule update
	pdm update

.PHONY build:
build:	## Build the zola site
	zola build

.PHONY serve:
serve:	## Start a webserver, and serve the zola site
	zola serve

.PHONY bib:
bib:	## Process bibliography - style 1
	python3 scripts/split-bibtex.py

.PHONY bib2:
bib2:	## Process bibliography - style 2
	pdm run python3 scripts/import-bibtex.py

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



VENV    ?= .venv
PIP     ?= $(VENV)/bin/pip
PYTHON  ?= $(VENV)/bin/python

PY_VERSION   ?= python3
VENV_COMMAND ?= virtualenv --python=$(PY_VERSION)

all: update-venv

update-venv:
ifeq ($(wildcard $(PIP)),)
	$(VENV_COMMAND) $(VENV)
endif
	$(PIP) install -U -r ./requirements.txt
	$(PIP) uninstall markov -q -y ||: 
	$(VENV)/bin/python setup.py install

clean:
	rm -rf $(VENV)

tests:
	tox

.PHONY: update-venv clean tests

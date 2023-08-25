ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

# Manually define main variables

ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = app

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(APPLICATION_NAME)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(APPLICATION_NAME)
	poetry run python3 -m black $(APPLICATION_NAME)

run:  ##@Application Run application server
	uvicorn app.__main__:app --host 0.0.0.0 --port ${APP_PORT} --reload

docker-clean:  ##@Code Clean directory from garbage files
	docker system prune -f

%::
	echo $(MESSAGE)

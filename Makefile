
EXT_NAME:=com.github.brpaz.ulauncher-trello
EXT_DIR:=$(shell pwd)

lint:
	@find . -iname "*.py" | xargs pylint

format:
	@autopep8 --in-place --recursive --aggressive .

link:
	@ln -s ${EXT_DIR} ~/.cache/ulauncher_cache/extensions/${EXT_NAME}

unlink:
	@rm -r ~/.cache/ulauncher_cache/extensions/${EXT_NAME}

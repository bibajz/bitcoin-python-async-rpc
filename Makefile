RM := rm -rf

DIRS_TO_RM = .mypy_cache .pytest_cache .coverage .eggs build dist */*.egg-info
DIRS_TO_CLEAN = src tests

all: clean

.PHONY: clean
clean:
	@echo Cleaning crew has arrived!
	$(RM) $(DIRS_TO_RM)
	find $(DIRS_TO_CLEAN) -name '*.pyc' -type f -exec $(RM) '{}' +
	find $(DIRS_TO_CLEAN) -name '*.so' -type f -exec $(RM) '{}' +
	find $(DIRS_TO_CLEAN) -name '*.c' -type f -exec $(RM) '{}' +

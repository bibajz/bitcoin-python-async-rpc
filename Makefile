RM := rm -rf

all: clean

.PHONY: clean
clean:
	@echo Cleaning crew has arrived!
	$(RM) .mypy_cache .coverage .eggs build dist */*.egg-info
	$(RM) *.py[co] */*.py[co] */*/*.py[co]
	$(RM) *.so */*.so */*/*.so */*/*/*.so
	$(RM) *.c */*.c */*/*.c */*/*/*.c